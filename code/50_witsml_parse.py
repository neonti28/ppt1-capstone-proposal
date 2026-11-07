#!/usr/bin/env python3
"""T9 — Parse WITSML 1.4 time-based (indexType "date time") -> CSV per wellbore.

Sumber : data/volve/witsml_raw/<folder>/**/log/**/<chunk>.xml
Output : data/volve/witsml_parsed/<nama>.csv      (timestamp ISO-8601 UTC + kanal mnemonic)
         data/volve/witsml_parsed/<nama>.qc.json  (kualitas; semua angka dari eksekusi)

Desain (diverifikasi pada 1 chunk sebelum dipakai luas):
  * root <logs> namespace http://www.witsml.org/schemas/1series
  * hanya indexType == "date time"; "measured depth" dilewat + dicatat
  * <logData><mnemonicList>..</mnemonicList><unitList>..</unitList><data>..</data>
  * timestamp = kolom indexCurve (TIME / Time), nilai ISO-8601 UTC ('Z')
  * chunk berurutan waktu dan OVERLAP 1 baris di boundary -> duplikat timestamp
  * grup log (per layanan/pass) bisa tumpang tindih -> di-clustering per rentang waktu
    lalu digabung (groupby timestamp, first non-null) agar puncak memori terbatas
  * nilai numerik float32 (resolusi ~5e-4 m pada 4000 m) -> dicatat di laporan
"""
import argparse
import gc
import io
import json
import os
import re
import sys
import time
import traceback

import numpy as np
import pandas as pd

RAW = "/mnt/d/Capstone 1/data/volve/witsml_raw"
OUT = "/mnt/d/Capstone 1/data/volve/witsml_parsed"

RE_INDEX_TYPE = re.compile(r"<indexType>(.*?)</indexType>")
RE_NAME_WELL = re.compile(r"<nameWell>(.*?)</nameWell>")
RE_NAME_WB = re.compile(r"<nameWellbore>(.*?)</nameWellbore>")
RE_INDEX_CURVE = re.compile(r"<indexCurve>(.*?)</indexCurve>")
RE_MNEMONIC_LIST = re.compile(r"<mnemonicList>(.*?)</mnemonicList>", re.S)
RE_DATA = re.compile(r"<data>(.*?)</data>", re.S)
RE_CURVE_INFO = re.compile(r"<logCurveInfo\b[^>]*>(.*?)</logCurveInfo>", re.S)
RE_CI_MNEMONIC = re.compile(r"<mnemonic>(.*?)</mnemonic>")
RE_CI_UNIT = re.compile(r"<unit>(.*?)</unit>")
RE_CI_DESC = re.compile(r"<curveDescription>(.*?)</curveDescription>")
RE_CI_SRC = re.compile(r"<dataSource>(.*?)</dataSource>")
RE_CI_TYPE = re.compile(r"<typeLogData>(.*?)</typeLogData>")

HEAD_BYTES = 400000


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def iso_z(ts):
    """Timestamp pandas -> string ISO-8601 UTC dgn milidetik ('Z')."""
    try:
        if pd.isna(ts):
            return None
    except (TypeError, ValueError):
        return str(ts)
    return ts.strftime("%Y-%m-%dT%H:%M:%S.%f")[:23] + "Z"


def read_text(path, head_only=False):
    """Baca teks. head_only: berhenti setelah </mnemonicList> bila sudah ketemu."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        if not head_only:
            return fh.read()
        txt = fh.read(HEAD_BYTES)
        if "</mnemonicList>" not in txt:
            txt += fh.read()
        return txt


def scan_files(folder_root):
    """Pisahkan chunk time-based vs depth-based vs rusak (depth dicatat namanya)."""
    time_files, depth_files, bad = [], [], []
    for r, _dirs, fs in os.walk(folder_root):
        if os.sep + "log" + os.sep not in (r + os.sep):
            continue
        for f in sorted(fs):
            if not f.endswith(".xml"):
                continue
            p = os.path.join(r, f)
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as fh:
                    head = fh.read(8192)
            except Exception as e:
                bad.append([os.path.relpath(p, folder_root), f"read:{type(e).__name__}:{e}"])
                continue
            m = RE_INDEX_TYPE.search(head)
            it = m.group(1).strip() if m else "NONE"
            if it == "date time":
                time_files.append(p)
            elif it == "measured depth":
                nm = re.search(r"<name>(.*?)</name>", head)
                depth_files.append([os.path.relpath(p, folder_root),
                                    nm.group(1) if nm else "?"])
            else:
                bad.append([os.path.relpath(p, folder_root), f"indexType={it!r}"])
    time_files.sort()
    depth_files.sort()
    return time_files, depth_files, bad


def pass0_union(time_files, folder_root):
    """Header-only: union kolom (urut kemunculan), unit/deskripsi/dataSource, indexCurve.

    Mnemonic yang dipakai sebagai index timestamp di chunk mana pun TIDAK masuk channel
    (nilainya sudah ada di kolom `timestamp`) -> dicatat di qc["ts_columns_excluded"].
    """
    per_file = []
    units, desc, dsrc, ctype = {}, {}, {}, {}
    header_fail = []
    for p in time_files:
        rel = os.path.relpath(p, folder_root)
        try:
            txt = read_text(p, head_only=True)
        except Exception as e:
            header_fail.append([rel, f"{type(e).__name__}:{e}"])
            continue
        m = RE_MNEMONIC_LIST.search(txt)
        if not m:
            header_fail.append([rel, "no <mnemonicList>"])
            continue
        names = [x.strip() for x in m.group(1).split(",")]
        cut = txt.find("<logData>")
        head = txt[:cut] if cut > 0 else txt
        mic = RE_INDEX_CURVE.search(head)
        ic = mic.group(1).strip() if mic else None
        ts_col = ic if (ic and ic in names) else names[0]
        per_file.append((rel, names, ts_col))
        for ci in RE_CURVE_INFO.findall(head):
            mm = RE_CI_MNEMONIC.search(ci)
            if not mm:
                continue
            mn = mm.group(1).strip()
            u = RE_CI_UNIT.search(ci)
            uu = u.group(1).strip() if u else ""
            if mn not in units:
                d = RE_CI_DESC.search(ci)
                s = RE_CI_SRC.search(ci)
                t = RE_CI_TYPE.search(ci)
                units[mn] = uu
                desc[mn] = d.group(1).strip() if d else ""
                dsrc[mn] = s.group(1).strip() if s else ""
                ctype[mn] = t.group(1).strip() if t else ""
            elif uu and uu != units[mn]:
                units[mn] = units[mn] + "|" + uu

    ts_cols = sorted({t for _r, _n, t in per_file})
    union, seen = [], set()
    for _rel, names, ts_col in per_file:
        for nm in names:
            if nm == ts_col or nm in ts_cols:
                continue
            if nm not in seen:
                seen.add(nm)
                union.append(nm)
    return union, units, desc, dsrc, ctype, ts_cols, header_fail


def read_tail(path, n=400000):
    """Baca N byte terakhir file (untuk baris <data> terakhir yang utuh)."""
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - n))
        data = f.read()
    return data.decode("utf-8", "replace")


def group_range(gdir, files, folder_root, frange=None):
    """Rentang waktu grup: baris data pertama chunk pertama & terakhir chunk terakhir.

    Posisi kolom timestamp diambil dari <indexCurve>/urutan <mnemonicList> chunk itu,
    bukan asumsi kolom pertama. Ekor file dibaca terpisah (seek) supaya benar-benar
    baris TERAKHIR -- membaca hanya 400KB pertama membuat rentang terlalu pendek dan
    menyebabkan cluster tidak digabung (timestamp duplikat antar cluster).

    `frange` (opsional) = cache {path: (lo, hi)} hasil compute_file_ranges() ->
    agregat dilakukan tanpa membaca ulang chunk.
    """
    if frange is not None:
        lo = hi = None
        for p in files:
            a, b = frange.get(p, (None, None))
            for v in (a, b):
                if not v:
                    continue
                if lo is None or v < lo:
                    lo = v
                if hi is None or v > hi:
                    hi = v
        return lo, hi

    def header_of(p):
        txt = read_text(p, head_only=True)
        m = RE_MNEMONIC_LIST.search(txt)
        if not m:
            return None, None, None
        names = [x.strip() for x in m.group(1).split(",")]
        cut = txt.find("<logData>")
        head = txt[:cut] if cut > 0 else txt
        mic = RE_INDEX_CURVE.search(head)
        ic = mic.group(1).strip() if mic else None
        ts_col = ic if (ic and ic in names) else names[0]
        return names, ts_col, txt

    def pos_of(names, ts_col):
        return names.index(ts_col) if ts_col in names else 0

    def ts_of_first(txt, names, ts_col):
        a = txt.find("<data>")
        if a < 0:
            return None
        row = txt[a + 6:txt.find("</data>", a)]
        f = row.split(",")
        pos = pos_of(names, ts_col)
        return f[pos].strip() if pos < len(f) else None

    def ts_of_last(p, names, ts_col):
        tail = read_tail(p)
        b = tail.rfind("</data>")
        if b < 0:
            return None
        a = tail.rfind("<data>", 0, b)
        if a < 0:
            return None
        row = tail[a + 6:b]
        f = row.split(",")
        pos = pos_of(names, ts_col)
        return f[pos].strip() if pos < len(f) else None

    lo = hi = None
    try:
        for p in files:
            names, ts_col, txt = header_of(p)
            if names is None:
                continue
            a = ts_of_first(txt, names, ts_col)
            b = ts_of_last(p, names, ts_col)
            for v in (a, b):
                if not v:
                    continue
                if lo is None or v < lo:
                    lo = v
                if hi is None or v > hi:
                    hi = v
    except Exception:
        return None, None
    return lo, hi


CAP_GB = 0.55   # batas est. memori float32 per batch (cgroup worker = 4,06 GB;
                # puncak nyata ~2-3x est karena concat + kolom object)
FRANGE = {}     # cache rentang per chunk (diisi parse_well, dipakai split_batches)


def _h_of(p):
    txt = read_text(p, head_only=True)
    m = RE_MNEMONIC_LIST.search(txt)
    if not m:
        return None, None, None
    names = [x.strip() for x in m.group(1).split(",")]
    cut = txt.find("<logData>")
    head = txt[:cut] if cut > 0 else txt
    mic = RE_INDEX_CURVE.search(head)
    ic = mic.group(1).strip() if mic else None
    ts_col = ic if (ic and ic in names) else names[0]
    return names, ts_col, txt


def _t_first(txt, names, ts_col):
    a = txt.find("<data>")
    if a < 0:
        return None
    row = txt[a + 6:txt.find("</data>", a)]
    f = row.split(",")
    pos = names.index(ts_col) if ts_col in names else 0
    return f[pos].strip() if pos < len(f) else None


def _t_last(p, names, ts_col):
    tail = read_tail(p)
    b = tail.rfind("</data>")
    if b < 0:
        return None
    a = tail.rfind("<data>", 0, b)
    if a < 0:
        return None
    row = tail[a + 6:b]
    f = row.split(",")
    pos = names.index(ts_col) if ts_col in names else 0
    return f[pos].strip() if pos < len(f) else None


def compute_file_ranges(files):
    """Rentang waktu PER CHUNK (baris <data> pertama & terakhir). 2 read/file."""
    out = {}
    for p in files:
        try:
            names, ts_col, txt = _h_of(p)
            if names is None:
                out[p] = (None, None)
                continue
            out[p] = (_t_first(txt, names, ts_col), _t_last(p, names, ts_col))
        except Exception:
            out[p] = (None, None)
    return out


def split_batches(cluster, cap_gb, n_cols, unit_rows=10000):
    """Pecah cluster menjadi batch ber-batas memori TANPA mengubah hasil akhir.

    Aturan aman (duplikat timestamp lintas batch tidak mungkin terjadi):
      * split hanya di titik TIME-DISJOINT (gap antar file) -> aman selalu;
      * cluster 1 grup (stream berurutan per waktu) boleh di-force-split ->
        caller membuang baris dengan timestamp <= prev_tmax (dedup tetap benar);
      * cluster multi-grup yang tumpang-tindihnya MENERUS melewati cap TIDAK
        dipecah (menggabung dua stream overlapping = kehilangan channel) ->
        diproses utuh + peringatan, benar > hemat.
    Return: (list cluster-like [{"gdir","files"}], n_force_split).
    """
    unit = unit_rows * (n_cols + 1) * 4 / 1e9
    items, norange = [], []
    for g in cluster:
        for p in g["files"]:
            lo, hi = FRANGE.get(p, (None, None))
            if lo and hi:
                items.append([lo, hi, g["gdir"], p])
            else:
                norange.append((g["gdir"], p))
    items.sort(key=lambda x: x[0])

    single = len(cluster) == 1
    batches, cur, cur_hi, est, forced = [], [], None, 0.0, 0

    def flush():
        nonlocal cur, cur_hi, est
        if cur:
            batches.append(cur)
            cur, cur_hi, est = [], None, 0.0

    for lo, hi, gdir, p in items:
        over = est + unit > cap_gb
        overlap = bool(cur) and cur_hi is not None and lo <= cur_hi
        if cur and over:
            if not overlap:
                flush()                 # gap -> time-disjoint, aman
            elif single:
                flush()                 # stream berurutan -> aman (drop <= prev_tmax)
                forced += 1
            # multi-grup + overlap -> TIDAK dipecah (dicatat via forced==0 & est>cap)
        cur.append((gdir, p))
        est += unit
        cur_hi = hi if cur_hi is None else max(cur_hi, hi)
    flush()

    if not batches:
        batches = [[]]
    if norange:
        batches[0] = norange + batches[0]

    out = []
    for b in batches:
        gd = {}
        for gdir, p in b:
            gd.setdefault(gdir, []).append(p)
        out.append([{"gdir": k, "files": v} for k, v in gd.items()])
    return out, forced


def parse_chunk(path, union):
    """Satu chunk -> DataFrame (timestamp datetime64 + channel sesuai union)."""
    txt = read_text(path, head_only=False)
    m = RE_MNEMONIC_LIST.search(txt)
    if not m:
        raise ValueError("no <mnemonicList>")
    names = [x.strip() for x in m.group(1).split(",")]
    cut = txt.find("<logData>")
    head = txt[:cut] if cut > 0 else txt[:60000]
    mic = RE_INDEX_CURVE.search(head)
    ic = mic.group(1).strip() if mic else None
    ts_col = ic if (ic and ic in names) else names[0]

    rows = RE_DATA.findall(txt)
    if not rows:
        raise ValueError("no <data> rows")
    n = len(names)
    good, bad_rows, bad_ex = [], 0, []
    for r in rows:
        if r.count(",") == n - 1:
            good.append(r)
        else:
            bad_rows += 1
            if len(bad_ex) < 3:
                bad_ex.append(r[:200])
    if not good:
        raise ValueError(f"semua {len(rows)} baris field-count mismatch (expect {n})")

    df = pd.read_csv(io.StringIO("\n".join(good)), names=names, header=None,
                     na_values=[""], keep_default_na=True, low_memory=False)

    ts = pd.to_datetime(df[ts_col], errors="coerce", utc=True)
    keep = [c for c in union if c in df.columns and c != ts_col]
    missing_in_union = [c for c in df.columns if c != ts_col and c not in union]
    sub = df[keep].copy()
    numc = [c for c in keep if sub[c].dtype != object]
    if numc:
        sub[numc] = sub[numc].apply(pd.to_numeric, errors="coerce").astype(np.float32)
    sub.insert(0, "timestamp", ts)

    meta = {"n_rows": len(df), "n_nat": int(ts.isna().sum()), "bad_fieldcount": bad_rows,
            "bad_examples": bad_ex, "ts_col": ts_col, "missing_in_union": missing_in_union}
    return sub, meta


def process_cluster(cluster, union):
    """Cluster = grup-grup log yang tumpang tindih waktu. Frame -> sort -> dedupe."""
    frames, files_n, rows_raw, nat, badfc, bad_ex = [], 0, 0, 0, 0, []
    fails = []
    for g in cluster:
        for p in g["files"]:
            try:
                df, meta = parse_chunk(p, set(union) | {"timestamp"})
            except Exception as e:
                fails.append([os.path.relpath(p, RAW), f"{type(e).__name__}: {e}"])
                continue
            frames.append(df)
            files_n += 1
            rows_raw += meta["n_rows"]
            nat += meta["n_nat"]
            badfc += meta["bad_fieldcount"]
            for ex in meta["bad_examples"]:
                if len(bad_ex) < 5:
                    bad_ex.append(ex)
            for c in meta["missing_in_union"]:
                fails.append([os.path.relpath(p, RAW), f"kolom di luar union: {c}"])
    if not frames:
        return None

    df = pd.concat(frames, ignore_index=True, join="outer") if len(frames) > 1 else frames[0]
    del frames
    df = df[df["timestamp"].notna()]
    df = df.sort_values("timestamp", kind="mergesort").reset_index(drop=True)

    n_before = len(df)
    dup = int(df["timestamp"].duplicated().sum())
    if dup:
        df = df.groupby("timestamp", sort=True).first().reset_index()
    n_after = len(df)

    df = df.reindex(columns=["timestamp"] + union)
    return {"df": df, "n_files": files_n, "rows_raw": rows_raw, "n_nat": nat,
            "bad_fieldcount": badfc, "bad_examples": bad_ex, "failures": fails,
            "n_before_dedup": n_before, "n_dup_removed": dup, "n_after_dedup": n_after}


def verify_csv_ts(path, chunksize=500000):
    """Verifikasi back-to-back atas CSV yang tertulis: kolom `timestamp` harus
    naik KETAT (setiap baris > seluruh timestamp sebelumnya) dan tanpa NAT.
    Dilakukan sebagai pemeriksaan nyata terhadap file hasil, bukan klaim konstruksi.
    """
    n_rows = n_bad = n_nat = 0
    rmax = None
    for ch in pd.read_csv(path, usecols=["timestamp"], chunksize=chunksize):
        ts = pd.to_datetime(ch["timestamp"], format="%Y-%m-%dT%H:%M:%S.%fZ",
                            utc=True, errors="coerce")
        if ts.dt.tz is not None:            # tz-aware -> object dtype saat to_numpy()
            ts = ts.dt.tz_convert("UTC").dt.tz_localize(None)
        a = ts.to_numpy()
        n_rows += len(a)
        nat = np.isnat(a)
        n_nat += int(nat.sum())
        av = a[~nat]
        if not len(av):
            continue
        if rmax is not None:
            n_bad += int((av <= rmax).sum())          # lintas chunk
        if len(av) > 1:                               # dalam chunk
            n_bad += int((av[1:] <= np.maximum.accumulate(av[:-1])).sum())
        rmax = av.max() if rmax is None else max(rmax, av.max())
    return {"n_rows": n_rows, "n_nat_timestamp": n_nat,
            "n_ts_not_strictly_increasing": n_bad,
            "ok": bool(n_nat == 0 and n_bad == 0)}


def parse_well(folder, out_name, limit_chunks=None):
    t0 = time.time()
    folder_root = os.path.join(RAW, folder)
    os.makedirs(OUT, exist_ok=True)
    qc = {"folder": folder, "out_csv": None, "errors": []}

    if not os.path.isdir(folder_root):
        qc["errors"].append("folder tidak ada")
        return qc

    time_files, depth_files, bad = scan_files(folder_root)
    qc["n_time_files"] = len(time_files)
    qc["n_depth_files"] = len(depth_files)
    qc["depth_logs_skipped"] = depth_files
    qc["files_bad_indexType"] = bad
    if limit_chunks:
        time_files = time_files[:limit_chunks]
    if not time_files:
        qc["errors"].append("tidak ada time-based log chunk")
        log(f"{out_name}: TIDAK ADA time chunk")
        return qc

    # identitas wellbore dari chunk pertama
    try:
        h = read_text(time_files[0], head_only=True)
        a = RE_NAME_WB.search(h)
        b = RE_NAME_WELL.search(h)
        qc["name_wellbore"] = a.group(1) if a else None
        qc["name_well"] = b.group(1) if b else None
    except Exception as e:
        qc["name_wellbore"] = None
        qc["errors"].append(f"identitas wellbore gagal: {e}")

    log(f"{out_name}: pass0 union (n_file={len(time_files)})")
    union, units, desc, dsrc, ctype, ts_cols, hfail = pass0_union(time_files, folder_root)
    qc["pass0_failures"] = hfail
    qc["ts_columns_excluded"] = ts_cols
    qc["n_channels"] = len(union)
    qc["channels"] = union
    qc["units"] = units
    qc["descriptions"] = desc
    qc["datasources"] = dsrc
    qc["typeLogData"] = ctype

    # kelompokkan per direktori log
    groups = {}
    for p in time_files:
        groups.setdefault(os.path.dirname(p), []).append(p)
    qc["n_groups"] = len(groups)

    # rentang waktu per chunk (sekali baca) -> agregat per grup (clustering) +
    # dipakai lagi split_batches (hemat-memori) tanpa baca ulang
    FRANGE.clear()
    FRANGE.update(compute_file_ranges(time_files))
    granges = []
    for gdir, files in sorted(groups.items()):
        lo, hi = group_range(gdir, files, folder_root, FRANGE)
        granges.append({"gdir": os.path.relpath(gdir, folder_root), "files": files,
                        "lo": lo, "hi": hi})
    unrange = [g for g in granges if not g["lo"] or not g["hi"]]
    granges = [g for g in granges if g["lo"] and g["hi"]]
    qc["groups_without_range"] = [{"gdir": g["gdir"], "n_files": len(g["files"])}
                                  for g in unrange]

    # clustering: rentang tumpang tindih (inklusif) -> satu cluster
    granges.sort(key=lambda g: g["lo"])
    clusters, cur, cur_max = [], [], None
    for g in granges:
        if cur and g["lo"] <= cur_max:
            cur.append(g)
            cur_max = max(cur_max, g["hi"])
        else:
            if cur:
                clusters.append(cur)
            cur, cur_max = [g], g["hi"]
    if cur:
        clusters.append(cur)
    # grup tanpa rentang terdeteksi TIDAK dibuang: dijadikan cluster terakhir
    if unrange:
        clusters.append(unrange)
    qc["n_clusters"] = len(clusters)
    qc["cluster_plan"] = [{"t_min": c[0]["lo"],
                           "t_max": max((x["hi"] for x in c if x["hi"]), default=None),
                           "n_groups": len(c),
                           "n_files": sum(len(x["files"]) for x in c),
                           "groups": [x["gdir"] for x in c]} for c in clusters]

    out_path = os.path.join(OUT, f"{out_name}.csv")
    fill = {c: 0 for c in union}
    vmin, vmax = {}, {}
    year_hist = {}
    per_cluster = []
    total_written = 0
    all_failures = []
    total_badfc = 0
    total_bad_ex = []
    prev_tmax = None
    global_dup_boundary = 0
    n_overlap_removed = 0
    n_batch_split = 0
    n_over_cap = 0
    header_written = False

    for ci, cluster in enumerate(clusters, 1):
        n_files_c = sum(len(x["files"]) for x in cluster)
        est_gb = n_files_c * 10000 * (len(union) + 1) * 4 / 1e9
        log(f"{out_name}: cluster {ci}/{len(clusters)} "
            f"({len(cluster)} grup, {n_files_c} file, "
            f"{cluster[0]['lo']} → {max((x['hi'] for x in cluster if x['hi']), default=None)}, "
            f"est memori {est_gb:.2f} GB)")
        batches = [cluster]
        if est_gb > CAP_GB:
            batches, nforced = split_batches(cluster, CAP_GB, len(union))
            if len(batches) > 1:
                n_batch_split += len(batches) - 1
                log(f"{out_name}: cluster {ci} dipecah -> {len(batches)} batch "
                    f"(cap {CAP_GB} GB; force-split aman per-stream={nforced})")
        for bi, cluster_b in enumerate(batches, 1):
            nb = sum(len(x["files"]) for x in cluster_b)
            est_b = nb * 10000 * (len(union) + 1) * 4 / 1e9
            if len(batches) > 1:
                log(f"{out_name}:   batch {bi}/{len(batches)}: {nb} file, "
                    f"{len(cluster_b)} grup, est {est_b:.2f} GB")
            if est_b > CAP_GB:
                n_over_cap += 1
                log(f"{out_name}: PERINGATAN batch {bi}/{len(batches)} melebihi cap "
                    f"({est_b:.2f} GB, multi-grup tumpang-tindih -> TIDAK dipecah: "
                    f"benar > hemat)")
            res = process_cluster(cluster_b, union)
            if res is None:
                continue
            df = res["df"]
            # batas antar batch/cluster harus tegas (tidak boleh timestamp sama):
            # overlap 1 baris antar chunk berurutan dibuang, bukan ditulis dobel
            n_ov = 0
            cmin, cmax = df["timestamp"].iloc[0], df["timestamp"].iloc[-1]
            if prev_tmax is not None and cmin <= prev_tmax:
                mask = df["timestamp"] <= prev_tmax
                n_ov = int(mask.sum())
                global_dup_boundary += n_ov
                n_overlap_removed += n_ov
                df = df[~mask]
                if df.empty:
                    del res
                    gc.collect()
                    continue
                df = df.reset_index(drop=True)
                cmin, cmax = df["timestamp"].iloc[0], df["timestamp"].iloc[-1]
            prev_tmax = cmax

            # statistik kolom (dihitung sebelum format timestamp)
            ts_str = (df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S.%f").str.slice(0, 23) + "Z")
            yrs = df["timestamp"].dt.year.value_counts()
            for y, n in yrs.items():
                year_hist[int(y)] = year_hist.get(int(y), 0) + int(n)
            nn = df[union].notna().sum()
            for c in union:
                fill[c] += int(nn[c])
            for c in union:
                s = df[c]
                if s.dtype != object and int(nn[c]):
                    mn = float(np.nanmin(s.values))
                    mx = float(np.nanmax(s.values))
                    vmin[c] = mn if c not in vmin else min(vmin[c], mn)
                    vmax[c] = mx if c not in vmax else max(vmax[c], mx)
            df["timestamp"] = ts_str

            df.to_csv(out_path, index=False, mode="w" if not header_written else "a",
                      header=not header_written)
            header_written = True
            total_written += len(df)
            per_cluster.append({"i": ci, "batch": bi, "n_batches": len(batches),
                                "t_min": iso_z(cmin), "t_max": iso_z(cmax),
                                "n_groups": len(cluster_b),
                                "n_files": res["n_files"], "rows_raw": res["rows_raw"],
                                "rows_written": len(df),
                                "n_nat_dropped": res["n_nat"],
                                "n_dup_removed": res["n_dup_removed"],
                                "n_boundary_overlap_removed": n_ov,
                                "n_bad_fieldcount": res["bad_fieldcount"],
                                "groups": [g["gdir"] for g in cluster_b]})
            total_badfc += res["bad_fieldcount"]
            total_bad_ex.extend(res["bad_examples"])
            all_failures.extend(res["failures"])
            del df, res
            gc.collect()
            log(f"{out_name}: cluster {ci} batch {bi}/{len(batches)} selesai -> "
                f"{total_written} baris total, {round((time.time()-t0))}s")
            if len(all_failures) > 200:
                all_failures = all_failures[:200]

    qc["clusters"] = per_cluster
    qc["n_parse_failures"] = len(all_failures)
    qc["parse_failures"] = all_failures[:50]
    qc["n_rows_bad_fieldcount"] = total_badfc
    qc["bad_fieldcount_examples"] = total_bad_ex[:5]
    qc["boundary_duplicate_ts"] = int(global_dup_boundary)
    qc["n_boundary_overlap_removed"] = int(n_overlap_removed)
    qc["n_batches_split"] = int(n_batch_split)
    qc["n_batches_over_cap"] = int(n_over_cap)
    qc["memory_cap_gb_per_batch"] = CAP_GB
    qc["groups_without_range"] = qc["groups_without_range"]

    if not per_cluster:
        qc["errors"].append("tidak ada cluster berhasil")
        return qc

    qc["out_csv"] = out_path
    qc["n_rows_final"] = total_written
    qc["n_columns_excl_timestamp"] = len(union)
    qc["t_min_utc"] = per_cluster[0]["t_min"]
    qc["t_max_utc"] = per_cluster[-1]["t_max"]
    # verifikasi nyata atas file CSV hasil parse (bukan klaim dari alur program)
    try:
        v = verify_csv_ts(out_path)
        v["n_rows_match"] = (v["n_rows"] == total_written)
        qc["verify_timestamp"] = v
        qc["timestamp_sorted_unique"] = bool(v["ok"] and v["n_rows_match"])
    except Exception as e:
        qc["verify_timestamp"] = {"error": f"{type(e).__name__}: {e}"}
        qc["timestamp_sorted_unique"] = False
    qc["fill_counts"] = fill
    qc["fill_rate"] = {c: round(fill[c] / total_written, 6) if total_written else 0.0
                       for c in union}
    qc["n_channels_ge_50pct"] = sum(1 for c in union
                                    if total_written and fill[c] / total_written >= 0.5)
    qc["n_channels_lt_50pct"] = sum(1 for c in union
                                    if total_written and fill[c] / total_written < 0.5)
    qc["col_min"] = vmin
    qc["col_max"] = vmax
    qc["year_histogram"] = dict(sorted(year_hist.items()))
    qc["n_rows_outside_2007_2017"] = sum(v for y, v in year_hist.items()
                                         if y < 2007 or y > 2017)
    qc["float32_numeric"] = True
    qc["csv_bytes"] = os.path.getsize(out_path)
    qc["runtime_s"] = round(time.time() - t0, 1)

    qc_path = os.path.join(OUT, f"{out_name}.qc.json")
    with open(qc_path, "w") as f:
        json.dump(qc, f, indent=1)

    log(f"{out_name}: SELESAI {total_written} baris x {len(union)+1} kolom, "
        f"{qc['t_min_utc']} → {qc['t_max_utc']}, {qc['csv_bytes']/1e6:.1f} MB, "
        f"{qc['runtime_s']}s -> {out_path}")
    return qc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, help="JSON {out_name: folder}")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()

    with open(args.map) as f:
        mapping = json.load(f)
    os.makedirs(OUT, exist_ok=True)

    results = {}
    for name, folder in mapping.items():
        if args.only and name not in args.only:
            continue
        log(f"=== {name} <- {folder} ===")
        try:
            results[name] = parse_well(folder, name, limit_chunks=args.limit)
        except Exception as e:
            log(f"{name}: EXCEPTION {type(e).__name__}: {e}")
            traceback.print_exc()
            results[name] = {"folder": folder, "errors": [f"{type(e).__name__}: {e}"]}

    summary = os.path.join(OUT, "_parse_summary.json")
    old = {}
    if os.path.exists(summary):
        try:
            old = json.load(open(summary))
        except Exception:
            old = {}
    old.update(results)
    with open(summary, "w") as f:
        json.dump(old, f, indent=1)
    ok = sum(1 for v in results.values() if v.get("out_csv"))
    log(f"DONE {ok}/{len(results)} wellbore -> {summary}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
