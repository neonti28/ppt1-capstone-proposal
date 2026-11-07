#!/usr/bin/env python3
"""T9 — Verifier hasil parse WITSML (dijalankan SETELAH parser, bukan bagian dari parser).

Empat pemeriksaan per wellbore, semua dari eksekusi nyata:
  V1  CSV dapat dibaca, jumlah baris == qc.n_rows_final
  V2  kolom timestamp naik KETAT & tanpa NAT (baca ulang CSV, bukan klaim alur program)
  V3  rekonsiliasi angka qc:
        rows_raw - n_nat_dropped - n_dup_removed - n_boundary_overlap_removed
        == rows_written (per cluster, lalu total)
  V4  jumlah baris <data> mentah di folder sumber >= rows_raw (sisa dijelaskan:
        chunk duplikat identik / baris field-count / file gagal parse -> dicatat)

Output: tabel PASS/FAIL di stdout + data/volve/witsml_parsed/_verify.json
Exit 0 hanya jika SEMUA wellbore PASS pada V1-V3 (V4 informatif + selalu dicatat).
"""
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd

RAW = "/mnt/d/Capstone 1/data/volve/witsml_raw"
OUT = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
RE_IT = re.compile(r"<indexType>(.*?)</indexType>")


def log(m=""):
    print(m, flush=True)


def verify_ts(path, chunksize=500000):
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
            n_bad += int((av <= rmax).sum())
        if len(av) > 1:
            n_bad += int((av[1:] <= np.maximum.accumulate(av[:-1])).sum())
        rmax = av.max() if rmax is None else max(rmax, av.max())
    return n_rows, n_bad, n_nat


def raw_data_count(folder_root):
    """Jumlah <data> mentah per kategori indexType + jumlah file."""
    n_time = n_other = rows_time = rows_other = 0
    for r, _d, fs in os.walk(folder_root):
        if os.sep + "log" + os.sep not in (r + os.sep):
            continue
        for fn in sorted(fs):
            if not fn.endswith(".xml"):
                continue
            p = os.path.join(r, fn)
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as fh:
                    txt = fh.read()
            except Exception:
                continue
            m = RE_IT.search(txt)
            it = m.group(1).strip() if m else "NONE"
            n = txt.count("<data>")
            if it == "date time":
                n_time += 1
                rows_time += n
            else:
                n_other += 1
                rows_other += n
    return n_time, rows_time, n_other, rows_other


def main():
    qcs = sorted(glob.glob(os.path.join(OUT, "*.qc.json")))
    results, all_ok = {}, True
    for qp in qcs:
        name = os.path.basename(qp)[:-len(".qc.json")]
        q = json.load(open(qp))
        csv = os.path.join(OUT, f"{name}.csv")
        log("=" * 78)
        log(f"{name}  (folder: {q.get('folder')})")
        res = {"folder": q.get("folder")}

        # V1: CSV ada + baris == qc
        if not os.path.exists(csv):
            log("  V1 FAIL: CSV tidak ada")
            res["V1"] = "FAIL: csv missing"
            all_ok = False
            results[name] = res
            continue
        res["csv_bytes"] = os.path.getsize(csv)

        # V2: timestamp naik ketat
        n_rows, n_bad, n_nat = verify_ts(csv)
        v1 = (n_rows == q.get("n_rows_final"))
        res["V1_rows_match"] = {"csv_rows": n_rows, "qc_rows": q.get("n_rows_final"),
                                "pass": bool(v1)}
        res["V2_timestamp"] = {"n_rows": n_rows, "n_not_strictly_increasing": n_bad,
                               "n_nat": n_nat, "pass": bool(n_bad == 0 and n_nat == 0)}
        log(f"  V1 rows: csv={n_rows} qc={q.get('n_rows_final')} -> {'PASS' if v1 else 'FAIL'}")
        log(f"  V2 ts  : not_increasing={n_bad} nat={n_nat} -> "
            f"{'PASS' if (n_bad == 0 and n_nat == 0) else 'FAIL'}")

        # tulis hasil verifikasi balik ke qc (sumber: verifier ini, bukan klaim parser)
        q["verify_timestamp"] = {"n_rows": n_rows, "n_nat_timestamp": n_nat,
                                 "n_ts_not_strictly_increasing": n_bad,
                                 "n_rows_match": bool(v1),
                                 "ok": bool(n_bad == 0 and n_nat == 0),
                                 "by": "code/52_verify_witsml_parse.py"}
        q["timestamp_sorted_unique"] = bool(v1 and n_bad == 0 and n_nat == 0)

        # V3: rekonsiliasi internal
        per, tot_written, probs = [], 0, []
        for c in q.get("clusters", []):
            exp = (c["rows_raw"] - c.get("n_nat_dropped", 0) - c.get("n_dup_removed", 0)
                   - c.get("n_boundary_overlap_removed", 0))
            okc = (exp == c["rows_written"])
            per.append({"i": c["i"], "batch": c.get("batch"), "expected": exp,
                        "written": c["rows_written"], "pass": bool(okc)})
            if not okc:
                probs.append(f"cluster {c['i']}/batch {c.get('batch')}: {exp} != {c['rows_written']}")
            tot_written += c["rows_written"]
        v3 = (not probs) and (tot_written == q.get("n_rows_final"))
        res["V3_reconcile"] = {"per_cluster": per, "sum_written": tot_written,
                               "qc_n_rows_final": q.get("n_rows_final"),
                               "problems": probs, "pass": bool(v3)}
        log(f"  V3 rekonsiliasi: sum(written)={tot_written} qc={q.get('n_rows_final')} "
            f"-> {'PASS' if v3 else 'FAIL: ' + '; '.join(probs)}")

        # V4: baris <data> mentah
        folder_root = os.path.join(RAW, q.get("folder", ""))
        if os.path.isdir(folder_root):
            nt, rt, no, ro = raw_data_count(folder_root)
            rows_raw = sum(c["rows_raw"] for c in q.get("clusters", []))
            badfc = q.get("n_rows_bad_fieldcount", 0)
            nfail = q.get("n_parse_failures", 0)
            res["V4_raw"] = {"files_time": nt, "data_rows_time": rt,
                             "files_other": no, "data_rows_other": ro,
                             "qc_rows_raw": rows_raw, "qc_bad_fieldcount": badfc,
                             "qc_parse_failures": nfail,
                             "delta_time_vs_rows_raw": rt - rows_raw}
            log(f"  V4 raw  : <data> time={rt} (file {nt}) | rows_raw={rows_raw} | "
                f"delta={rt - rows_raw} | bad_fieldcount={badfc} | failures={nfail}")
        else:
            res["V4_raw"] = {"error": f"folder tidak ada: {folder_root}"}
            log(f"  V4 raw  : folder tidak ada -> {folder_root}")

        with open(qp, "w") as f:          # persist hasil verifikasi ke qc
            json.dump(q, f, indent=1)

        ok = bool(v1 and res["V2_timestamp"]["pass"] and v3)
        res["overall"] = "PASS" if ok else "FAIL"
        all_ok = all_ok and ok
        log(f"  OVERALL: {res['overall']}")
        results[name] = res

    dst = os.path.join(OUT, "_verify.json")
    with open(dst, "w") as f:
        json.dump(results, f, indent=1)
    log("")
    log(f"wrote {dst}")
    n_pass = sum(1 for r in results.values() if r.get("overall") == "PASS")
    log(f"SUMBER: {n_pass}/{len(results)} wellbore PASS (V1-V3)")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
