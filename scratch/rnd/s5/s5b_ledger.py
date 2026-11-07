#!/usr/bin/env python3
"""S5-B v2: audit ledger provenance per kartu (S1..S4).

Struktur: jumlah baris, jumlah kolom, duplikat ID, urutan, status, berkas rujukan.
Provenance: tiap angka di kolom Angka dicari di subtree JSON yang dirujuk.
Resolver mendukung: a.b.c, list[n], [*], [model=NAMA], dan pencarian subtree.
Rujukan berkas kode (.py) diperiksa dengan mencari literal angkanya di berkas.

Keluaran: scratch/rnd/s5/s5_ledger.json
"""
import hashlib
import json
import os
import re
import time
from collections import Counter

import sys

BASE = "/mnt/d/Capstone 1(v2)"
LEDGER = sys.argv[1] if len(sys.argv) > 1 else f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
OUT = sys.argv[2] if len(sys.argv) > 2 else f"{BASE}/scratch/rnd/s5/s5_ledger.json"
KARTU = ["S1", "S2", "S3", "S4"]


def tafsir(tok):
    """Semua tafsir numerik yang wajar untuk satu token angka Indonesia/Inggris."""
    t = tok.strip().replace("\u00a0", "")
    t = re.sub(r"^(kurang dari|lebih dari|sekitar|maks\.?|min\.?)\s*", "", t, flags=re.I)
    t = t.strip().rstrip("%")
    if not re.fullmatch(r"-?\d[\d.,]*", t):
        return []
    neg = t.startswith("-")
    t = t.lstrip("-")
    kandidat = set()
    for s in {t, t.replace(".", ""), t.replace(",", "")}:
        try:
            kandidat.add(float(s))
        except ValueError:
            pass
    if "," in t:
        kandidat.add(float(t.replace(".", "").replace(",", ".")))
    if "." in t:
        kandidat.add(float(t.replace(",", "")))
    kandidat = {v for v in kandidat if v == v}
    if neg:
        kandidat = {-v for v in kandidat}
    return sorted(kandidat)


def token_angka(sel):
    """Ambil semua token angka dari sel Angka (menangani rentang dan fraksi)."""
    if re.fullmatch(r"[0-9a-f]{16,}", sel.strip()):
        return []  # hash, bukan angka terukur
    toks = re.findall(r"-?\d[\d.,]*", sel)
    return [x.strip(".,") for x in toks if re.search(r"\d", x)]


DIR_CARI = ["scratch/rnd/s1", "scratch/rnd/s2", "scratch/rnd/s3", "scratch/rnd/s4",
            "scratch/rnd/r8", "scratch/v9_i1", "scratch/v9_d1", "scratch/rnd/e3",
            "scratch/rnd/e4", "scratch/rnd/pm", "docs", "code", "data", "data/volve", ""]

# Kartu yang barisnya menyebut kunci JSON tanpa nama berkas: nilai dicari di
# seluruh artefak kartu, supaya baris tetap diuji dan tidak hanya dilaporkan "tak diuji".
SET_ARTEFAK = {
    "S2": ["scratch/rnd/s2/s2_records_vib.json", "scratch/rnd/s2/s2_records_ssi.json",
           "scratch/rnd/s2/s2_ringkas.json", "scratch/rnd/s2/s2_meta.json"],
}
INDEKS_SET = {}


def siapkan_index():
    """Indeks nilai seluruh artefak kartu; dipanggil setelah kumpulan_angka didefinisikan."""
    hasil = {}
    for _k, _daftar in SET_ARTEFAK.items():
        _agg = {}
        for _a in _daftar:
            _p = f"{BASE}/{_a}"
            if not os.path.isfile(_p) or os.path.getsize(_p) == 0:
                continue
            try:
                _o = json.load(open(_p, encoding="utf-8"))
            except Exception:
                continue
            for _v in kumpulan_angka(_o):
                _agg.setdefault(_v, os.path.basename(_a))
        hasil[_k] = _agg
    return hasil


def kumpulan_angka(obj, kedalaman=0):
    """Semua daun numerik di dalam obj (rekursif)."""
    out = set()
    if kedalaman > 40:
        return out
    if isinstance(obj, bool):
        return out
    if isinstance(obj, (int, float)):
        out.add(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            out |= kumpulan_angka(v, kedalaman + 1)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            out |= kumpulan_angka(v, kedalaman + 1)
    return out


def cocok(nilai, kumpulan, desimal=0):
    tol = max(0.5 * 10 ** (-desimal), 1e-9) if desimal else 1e-6
    for v in kumpulan:
        if abs(v - nilai) <= tol:
            return v
        # angka ditulis ribuan tanpa pemisah: 32256 lawan 32,256
        if v != 0 and abs(abs(v) * 1000 - abs(nilai)) <= tol * 1000:
            return v
        if nilai != 0 and abs(abs(nilai) * 1000 - abs(v)) <= tol * 1000:
            return v
    return None


def belah_path(path):
    """a.b[0].c / records[model=X].far / per_well[*].x -> daftar langkah."""
    langkah = []
    for bagian in path.split("."):
        m = re.fullmatch(r"([^\[\]]*)((\[[^\]]*\])*)", bagian)
        if not m:
            return None
        kunci, sisa = m.group(1), m.group(2)
        if kunci:
            langkah.append(("kunci", kunci))
        for sel in re.findall(r"\[([^\]]*)\]", sisa):
            if sel == "*":
                langkah.append(("semua", None))
            elif "=" in sel:
                k, v = sel.split("=", 1)
                langkah.append(("predikat", (k.strip(), v.strip())))
            elif re.fullmatch(r"-?\d+", sel):
                langkah.append(("indeks", int(sel)))
            else:
                return None
    return langkah


def resolve(obj, langkah):
    kandidat = [obj]
    for jenis, arg in langkah:
        baru = []
        for cur in kandidat:
            if jenis == "kunci":
                if isinstance(cur, dict) and arg in cur:
                    baru.append(cur[arg])
            elif jenis == "indeks":
                if isinstance(cur, list) and -len(cur) <= arg < len(cur):
                    baru.append(cur[arg])
            elif jenis == "semua":
                if isinstance(cur, list):
                    baru.extend(cur)
                elif isinstance(cur, dict):
                    baru.extend(cur.values())
            elif jenis == "predikat":
                k, v = arg
                if isinstance(cur, list):
                    for it in cur:
                        if isinstance(it, dict) and str(it.get(k)) == v:
                            baru.append(it)
        kandidat = baru
        if not kandidat:
            return []
    return kandidat


def cari_berkas(tok):
    nama = os.path.basename(tok)
    for d in DIR_CARI:
        for kandidat in (os.path.join(BASE, d, tok) if d and tok.startswith(d.split("/")[0]) else None,
                         os.path.join(BASE, d, nama), os.path.join(BASE, tok)):
            if kandidat and os.path.isfile(kandidat):
                return kandidat
    return None


baris = open(LEDGER, encoding="utf-8").read().splitlines()
blok = {}
for i, ln in enumerate(baris):
    if ln.startswith("## "):
        for k in KARTU:
            if re.search(rf"\b{k}\b", ln):
                blok.setdefault(k, []).append(ln.strip())

hasil = dict(kartu="t_b5b16adc", langkah="S5-B audit ledger",
             tanggal=time.strftime("%Y-%m-%d %H:%M:%S"), ledger=LEDGER,
             sha256_ledger=hashlib.sha256(open(LEDGER, "rb").read()).hexdigest(),
             per_kartu={}, total=0)
INDEKS_SET.update(siapkan_index())

for k in KARTU:
    pola = re.compile(rf"^\| {k}-(\d+) \|")
    rows = [dict(lineno=i + 1, sel=[c.strip() for c in ln.strip().strip("|").split("|")])
            for i, ln in enumerate(baris) if pola.match(ln)]
    d = dict(header_blok=blok.get(k, []), n_baris=len(rows), n_kolom={},
             kolom_tidak_konsisten=[], id_duplikat=[], id_tidak_berurut=[], status={},
             berkas_hilang=[], baris=[])
    ids = []
    for r in rows:
        sel = r["sel"]
        d["n_kolom"][str(len(sel))] = d["n_kolom"].get(str(len(sel)), 0) + 1
        ids.append(int(pola.match(baris[r["lineno"] - 1]).group(1)))
        d["status"][sel[-1]] = d["status"].get(sel[-1], 0) + 1
        # cari sel rujukan: sel yang memuat .json/.jsonl/.py/.log/.parquet
        ruj = next((s for s in sel[3:-1] if re.search(r"\.(jsonl?|py|log|parquet|csv)\b", s)), "")
        angka_sel = sel[1]
        info = dict(id=f"{k}-{ids[-1]:03d}", angka=angka_sel, satuan=sel[2],
                    kelas=sel[3] if len(sel) > 6 else "", rujukan=ruj[:200],
                    status=sel[-1], hasil="TIDAK_DICOBA", n_token=0, cocok=0)
        tokens = token_angka(angka_sel)
        info["n_token"] = len(tokens)
        m = re.search(r"([\w./-]+\.(?:jsonl?|py|log|parquet|csv))", ruj)
        if not m:
            info["hasil"] = "TANPA_BERKAS"
        else:
            p = cari_berkas(m.group(1))
            info["berkas"] = p
            if p is None:
                info["hasil"] = "BERKAS_TIDAK_ADA"
                d["berkas_hilang"].append(info["id"])
            elif "getsize" in ruj:
                # rujukan ukuran berkas: nilai harus sama dengan ukuran berkas nyata
                mp = re.search(r"(data/[\w./-]+\.(?:parquet|csv|json|gz))", ruj)
                if not mp or not os.path.isfile(os.path.join(BASE, mp.group(1))):
                    info["hasil"] = "TANPA_BERKAS"
                    info["catatan"] = "rujukan getsize tanpa nama berkas yang bisa ditunjuk"
                else:
                    ukuran = os.path.getsize(os.path.join(BASE, mp.group(1)))
                    info["nilai_berkas"] = ukuran
                    info["cocok"] = sum(1 for t in tokens if any(abs(v - ukuran) <= 1e-6 for v in tafsir(t)))
                    info["hasil"] = "COCOK_UKURAN" if info["cocok"] == len(tokens) else "BEDA_UKURAN"
            elif p.endswith((".py", ".log", ".csv", ".parquet")):
                # rujukan kode/log: cari literal angka di teks berkas
                teks = open(p, encoding="utf-8", errors="replace").read()
                if not tokens:
                    info["hasil"] = "NON_NUMERIK"
                else:
                    dapat = sum(1 for t in tokens if t in teks or t.replace(",", ".") in teks)
                    info["cocok"] = dapat
                    info["hasil"] = "COCOK_TEKS" if dapat == len(tokens) else "BEDA_TEKS"
            else:
                sisa = ruj[m.end():].lstrip(" :,;")
                pm = re.match(r"([\w.\[\]=-]+)", sisa)
                if not pm:
                    info["hasil"] = "TANPA_PATH"
                else:
                    path = pm.group(1).rstrip(".")
                    info["path"] = path
                    try:
                        obj = json.load(open(p, encoding="utf-8"))
                    except Exception as e:
                        info["hasil"] = f"JSON_GAGAL:{type(e).__name__}"
                        obj = None
                    if obj is not None:
                        if not tokens:
                            info["hasil"] = "NON_NUMERIK"
                        else:
                            langkah = belah_path(path)
                            node = resolve(obj, langkah) if langkah else []
                            kump = set()
                            for nd in node:
                                kump |= kumpulan_angka(nd)
                            if node and kump:
                                cakupan = "PATH"
                            else:
                                kump = kumpulan_angka(obj)
                                cakupan = "BERKAS" if not node else "PATH_TANPA_ANGKA"
                            cocok_n, hilang = 0, []
                            for t in tokens:
                                des = len(t.split(",")[-1]) if "," in t else 0
                                if any(cocok(v, kump, des) is not None for v in tafsir(t)):
                                    cocok_n += 1
                                else:
                                    hilang.append(t)
                            info.update(cocok=cocok_n, cakupan=cakupan,
                                        n_token=len(tokens))
                            if cocok_n == len(tokens):
                                info["hasil"] = f"COCOK_{cakupan}"
                            elif cocok_n and len(tokens) > 1:
                                # sel memuat beberapa fakta; sebagian tidak dirujuk path
                                info["hasil"] = f"SEBAGIAN_{cakupan}"
                                info["hilang"] = hilang[:5]
                            else:
                                info["hasil"] = f"BEDA_{cakupan}"
                                info["hilang"] = hilang[:5]
        if len(sel) != 7:
            d["kolom_tidak_konsisten"].append(dict(id=info["id"], kolom=len(sel), baris=r["lineno"]))
        # baris yang hanya menyebut nama kunci: uji nilainya terhadap indeks artefak kartu
        if info["hasil"] in ("TANPA_BERKAS", "TANPA_PATH") and k in INDEKS_SET and tokens:
            agg = INDEKS_SET[k]
            dapat, hilang = 0, []
            for t in tokens:
                des = len(t.split(",")[-1]) if "," in t else 0
                if any(cocok(v, agg, des) is not None for v in tafsir(t)):
                    dapat += 1
                else:
                    hilang.append(t)
            info["cocok"] = dapat
            if dapat == len(tokens):
                info["hasil"] = "COCOK_SET"
            elif dapat:
                info["hasil"] = "SEBAGIAN_SET"
                info["hilang"] = hilang[:5]
            else:
                info["hasil"] = "BEDA_SET"
                info["hilang"] = hilang[:5]
        d["baris"].append(info)
    cnt = Counter(ids)
    d["id_duplikat"] = [f"{k}-{i:03d}" for i, c in cnt.items() if c > 1]
    d["id_tidak_berurut"] = [f"{k}-{ids[j]:03d}" for j in range(1, len(ids)) if ids[j] != ids[j - 1] + 1]
    d["id_rentang"] = [f"{k}-{ids[0]:03d}", f"{k}-{ids[-1]:03d}"] if ids else []
    hasil["per_kartu"][k] = d
    hasil["total"] += len(rows)

rekap = {}
for k, d in hasil["per_kartu"].items():
    h = Counter(b["hasil"] for b in d["baris"])
    rekap[k] = dict(n=d["n_baris"], kolom=d["n_kolom"], status=d["status"],
                    duplikat=len(d["id_duplikat"]), tidak_berurut=len(d["id_tidak_berurut"]),
                    berkas_hilang=len(d["berkas_hilang"]),
                    hasil=dict(h),
                    baris_beda=[dict(id=b["id"], angka=b["angka"], hilang=b.get("hilang"),
                                     path=b.get("path"), cakupan=b.get("cakupan"))
                                for b in d["baris"] if b["hasil"].startswith("BEDA")],
                    baris_tak_uji=[dict(id=b["id"], angka=b["angka"], hasil=b["hasil"])
                                   for b in d["baris"]
                                   if b["hasil"] in ("TANPA_BERKAS", "BERKAS_TIDAK_ADA", "TANPA_PATH",
                                                     "NON_NUMERIK") or b["hasil"].startswith("JSON_GAGAL")])
hasil["rekap"] = rekap
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(hasil, f, indent=1, ensure_ascii=False)

print("total baris:", hasil["total"], "sha ledger:", hasil["sha256_ledger"][:16])
for k, r in rekap.items():
    print(f"\n[{k}] n={r['n']} kolom={r['kolom']} duplikat={r['duplikat']} "
          f"tak_berurut={r['tidak_berurut']} berkas_hilang={r['berkas_hilang']}")
    print("  hasil:", dict(r["hasil"]))
    print("  status:", dict(r["status"]))
    print("  header blok:", [h[:80] for h in hasil["per_kartu"][k]["header_blok"]])
    if r["baris_beda"]:
        print("  BEDA:", json.dumps(r["baris_beda"][:10], ensure_ascii=False)[:1200])
    if r["baris_tak_uji"]:
        print("  TAK_UJI:", json.dumps(r["baris_tak_uji"][:12], ensure_ascii=False)[:1200])
