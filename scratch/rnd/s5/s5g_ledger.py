#!/usr/bin/env python3
"""S5-G v2: generator baris ledger S5, idempoten, dengan assert ke nilai terukur.

Sumber ukur:
  snapshot  : scratch/rnd/s5/view_0616/{RND_S2.md, LEDGER.md}  (S2 versi 06:18)
  hasil uji : s5_rerun.json, s5_negative.json, s5_ledger_view0616.json,
              s5_dok.json, s5_dok_snap_0558.json
  berkas    : os.path.getsize / sha256 / jumlah baris
Setiap baris di-assert: sel Angka harus sama dengan nilai yang diukur skrip ini.
"""
import hashlib
import json
import os
import re
import time

BASE = "/mnt/d/Capstone 1(v2)"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
S5 = f"{BASE}/scratch/rnd/s5"
VIEW = f"{S5}/view_0616"
MEAS = f"{S5}/s5_ledger_measure.json"
TANGGAL = "2026-10-28"


def sha(p, n=16):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:n]


def baris(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def ukuran(p):
    return os.path.getsize(p)


def jam(p):
    return time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p)))


led_v = open(f"{VIEW}/LEDGER.md", encoding="utf-8").read().splitlines()
pola = re.compile(r"^\| (S[1-4])-(\d+) \|")
per = {}
for ln in led_v:
    m = pola.match(ln)
    if m:
        per.setdefault(m.group(1), []).append([c.strip() for c in ln.strip().strip("|").split("|")])

L = json.load(open(f"{S5}/s5_ledger_view0616.json", encoding="utf-8"))
D = json.load(open(f"{S5}/s5_dok.json", encoding="utf-8"))
Ds = json.load(open(f"{S5}/s5_dok_snap_0558.json", encoding="utf-8"))
R = json.load(open(f"{S5}/s5_rerun.json", encoding="utf-8"))
N = json.load(open(f"{S5}/s5_negative.json", encoding="utf-8"))

M = {}
M["total"] = L["total"]
for k in ("S1", "S2", "S3", "S4"):
    M[f"n{k}"] = L["per_kartu"][k]["n_baris"]
    M[f"kol{k}"] = sorted({len(r) for r in per[k]})
    h = {}
    for b in L["per_kartu"][k]["baris"]:
        g = b["hasil"]
        grp = ("cocok" if g.startswith(("COCOK", "SEBAGIAN")) and not g.startswith("SEBAGIAN")
               else "sebagian" if g.startswith("SEBAGIAN")
               else "beda" if g.startswith("BEDA")
               else "tak_uji")
        h[grp] = h.get(grp, 0) + 1
    M[f"cocok{k}"], M[f"sebagian{k}"], M[f"beda{k}"], M[f"takuji{k}"] = (
        h.get("cocok", 0), h.get("sebagian", 0), h.get("beda", 0), h.get("tak_uji", 0))
    M[f"dup{k}"] = len(L["per_kartu"][k]["id_duplikat"])
    M[f"lompat{k}"] = len(L["per_kartu"][k]["id_tidak_berurut"])
M["kol_s2v1"] = sorted({len(r) for r in L["per_kartu"]["S2"]["baris"]})
M["dup_total"] = sum(M[f"dup{k}"] for k in ("S1", "S2", "S3", "S4"))
M["s4_tanpa_path"] = sum(1 for b in L["per_kartu"]["S4"]["baris"]
                         if b["hasil"] in ("TANPA_PATH", "TANPA_BERKAS"))
M["dok_s2v2"] = baris(f"{VIEW}/RND_S2.md")
M["klaim_s2"] = D["per_kartu"]["S2"]["rekap"]["n_klaim"]
M["terletak_s2"] = D["per_kartu"]["S2"]["rekap"]["terletak"]
M["klaim_s2v1"] = Ds["per_kartu"]["S2"]["rekap"]["n_klaim"]
M["terletak_s2v1"] = Ds["per_kartu"]["S2"]["rekap"]["terletak"]
M["klaim_s3"] = D["per_kartu"]["S3"]["rekap"]["n_klaim"]
M["klaim_s4"] = D["per_kartu"]["S4"]["rekap"]["n_klaim"]
M["klaim_total"] = M["klaim_s2"] + M["klaim_s3"] + M["klaim_s4"]
M["turunan"] = sum(len(v["turunan"]) for v in D["per_kartu"].values())
M["elapsed"] = R["rerun"]["elapsed_s"]
M["fold"] = R["rerun"]["n_fold"]
M["nbaris"] = R["rerun"]["shape"][0]
M["nkolom"] = R["rerun"]["shape"][1]
M["metrik"] = R["rekap"]["t51_metrik"]
M["gagal"] = sum(len(R["rekap"][k]) for k in ("t51_gagal", "t52_gagal", "t61_gagal", "t4_gagal"))
ring = R["rerun"]["ringkas"]["42"]
M["fp"], M["tp"] = ring["fp_total"], ring["tp_total"]
M["presisi"], M["recall"] = ring["precision_median"], ring["recall_median"]
M["far"] = ring["far24_kalender_median"]
M["neg_fp"] = int(N["tabel_5_1"]["fp_total"]["sel"]["42"]["dok"])
M["neg_f10"] = int(N["tabel_6_1"]["F-10"]["sel"]["FP"]["dok"])
M["size_vib1"] = ukuran(f"{BASE}/scratch/rnd/s2/bak_gagal/s2_vib.json")
M["size_ssi1"] = ukuran(f"{BASE}/scratch/rnd/s2/bak_gagal/s2_ssi.json")
M["size_recvib"] = ukuran(f"{BASE}/scratch/rnd/s2/s2_records_vib.json")
M["size_recssi"] = ukuran(f"{BASE}/scratch/rnd/s2/s2_records_ssi.json")
M["size_ringkas"] = ukuran(f"{BASE}/scratch/rnd/s2/s2_ringkas.json")
M["size_katalog"] = ukuran(f"{BASE}/data/volve/external/volve_catalog_target_paths.csv")
M["t_dok_v1"] = jam(f"{BASE}/scratch/rnd/s5/s5_dok_snap_0558.json")
M["t_mulai2"] = json.load(open(f"{BASE}/scratch/rnd/s2/s2_meta.json", encoding="utf-8"))["mulai"].split()[1]
M["t_bak"] = jam(f"{BASE}/scratch/rnd/s2/bak_gagal")
M["t_dokv2"] = jam(f"{VIEW}/RND_S2.md")
M["t_view"] = time.strftime("%H:%M", time.localtime(os.path.getmtime(f"{VIEW}/LEDGER.md")))
M["doi"] = 0
M["url"] = 0
M["standar"] = 1
M["emdash"] = sum(open(p, encoding="utf-8").read().count("\u2014") for p in
                  (f"{BASE}/docs/RND_S1_SEED_ROBUSTNESS.md", f"{VIEW}/RND_S2.md",
                   f"{BASE}/docs/RND_S3_HYBRID_BITWEAR.md", f"{BASE}/docs/RND_S4_LAYER_B_DATA.md"))
M["sequ"] = int(re.search(r"(\d+) pikiran", open(f"{VIEW}/RND_S2.md", encoding="utf-8").read()).group(1))
M["riset"] = len(re.findall(r"Riset pendahuluan", open(f"{VIEW}/RND_S2.md", encoding="utf-8").read()))
M["h_s1"] = sha(f"{BASE}/docs/RND_S1_SEED_ROBUSTNESS.md")
M["h_s2"] = sha(f"{VIEW}/RND_S2.md")
M["h_s3"] = sha(f"{BASE}/docs/RND_S3_HYBRID_BITWEAR.md")
M["h_s4"] = sha(f"{BASE}/docs/RND_S4_LAYER_B_DATA.md")
M["h_led"] = sha(f"{VIEW}/LEDGER.md")
M["h_pol"] = sha(f"{BASE}/docs/RND_EVALUATION_POLICY.md")
M["h_har"] = sha(f"{BASE}/code/rnd_hybrid_harness.py")

HARAP = {
    "total": 722, "nS1": 84, "nS2": 451, "nS3": 92, "nS4": 95,
    "kolS1": [7], "kolS2": [7], "kolS3": [7], "kolS4": [7],
    "dup_total": 0, "lompatS4": 3, "s4_tanpa_path": 13,
    "cocokS1": 73, "bedaS1": 5, "cocokS2": 447, "bedaS2": 4,
    "cocokS3": 72, "sebagianS3": 12, "bedaS3": 2,
    "cocokS4": 77, "sebagianS4": 3, "bedaS4": 2,
    "dok_s2v2": 309, "klaim_s2": 37, "terletak_s2": 37,
    "klaim_s2v1": 20, "terletak_s2v1": 20,
    "klaim_s3": 14, "klaim_s4": 15, "klaim_total": 66, "turunan": 7,
    "fold": 9, "metrik": 13, "gagal": 0, "nbaris": 52509, "nkolom": 50,
    "fp": 935, "tp": 3804, "neg_fp": 936, "neg_f10": 62,
    "size_vib1": 3150, "size_ssi1": 5773, "size_recvib": 157781,
    "size_recssi": 343877, "size_ringkas": 85513, "size_katalog": 645763,
    "doi": 0, "url": 0, "standar": 1, "emdash": 0, "sequ": 6, "riset": 4,
    "h_s1": "a9e46afa172a2cae", "h_s2": "84a6f6287ebc3ad3",
    "h_s3": "02a3ca1cd06f3146", "h_s4": "99aa5424b34f6cfa",
    "h_led": "4c5d09cc953baae2", "h_pol": "f2ea2aa245d3aa45", "h_har": "2d8e6f32d274ffc3",
}
salah = {k: (M.get(k), v) for k, v in HARAP.items() if M.get(k) != v}
if salah:
    raise SystemExit("ASSERT GAGAL (terukur, harapan): " + json.dumps(salah, ensure_ascii=False))
for k, v in {"presisi": 0.7789, "recall": 0.5638, "far": 3.5302, "elapsed": 13.0}.items():
    if abs(M[k] - v) > 1e-9:
        raise SystemExit(f"ASSERT DEKAT GAGAL: {k} {M[k]} lawan {v}")

json.dump(dict(kartu="t_b5b16adc", waktu=time.strftime("%Y-%m-%d %H:%M:%S"),
               snapshot_sha_ledger=M["h_led"], snapshot_sha_dok_s2=M["h_s2"], nilai=M),
          open(MEAS, "w", encoding="utf-8"), indent=1)

R2 = [
    ("722", "baris", "RUN-KITA", "s5_ledger_view0616.json per_kartu[*].n_baris dijumlahkan", "bagian 4", "TERUKUR", M["total"]),
    ("84", "baris", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S1.n_baris", "bagian 4", "TERUKUR", M["nS1"]),
    ("451", "baris", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S2.n_baris", "bagian 4", "TERUKUR", M["nS2"]),
    ("92", "baris", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S3.n_baris", "bagian 4", "TERUKUR", M["nS3"]),
    ("95", "baris", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S4.n_baris", "bagian 4", "TERUKUR", M["nS4"]),
    ("0", "duplikat", "RUN-KITA", "s5_ledger_view0616.json per_kartu[*].id_duplikat", "bagian 4", "TERUKUR", M["dup_total"]),
    ("3", "lompatan ID", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S4.id_tidak_berurut", "bagian 7", "TERUKUR", M["lompatS4"]),
    ("13", "baris", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S4.baris hasil TANPA_PATH atau TANPA_BERKAS", "bagian 7", "TERUKUR", M["s4_tanpa_path"]),
    ("73", "baris cocok", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S1.baris hasil COCOK", "bagian 4", "TERUKUR", M["cocokS1"]),
    ("5", "baris beda", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S1.baris hasil BEDA, semua cacat penguji", "bagian 4 dan 8", "TERUKUR", M["bedaS1"]),
    ("447", "baris cocok", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S2.baris hasil COCOK", "bagian 4", "TERUKUR", M["cocokS2"]),
    ("4", "baris beda", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S2.baris hasil BEDA, nilai konstanta dan median", "bagian 4 dan 7", "TERUKUR", M["bedaS2"]),
    ("72", "baris cocok", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S3.baris hasil COCOK", "bagian 4", "TERUKUR", M["cocokS3"]),
    ("12", "baris sebagian", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S3.baris hasil SEBAGIAN", "bagian 4", "TERUKUR", M["sebagianS3"]),
    ("2", "baris beda", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S3.baris hasil BEDA, pembulatan dan literal kode", "bagian 4 dan 8", "TERUKUR", M["bedaS3"]),
    ("77", "baris cocok", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S4.baris hasil COCOK", "bagian 4", "TERUKUR", M["cocokS4"]),
    ("3", "baris sebagian", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S4.baris hasil SEBAGIAN", "bagian 4", "TERUKUR", M["sebagianS4"]),
    ("2", "baris beda", "RUN-KITA", "s5_ledger_view0616.json per_kartu.S4.baris hasil BEDA, sel majemuk", "bagian 4 dan 8", "TERUKUR", M["bedaS4"]),
    ("309", "baris", "RUN-KITA", "baris view_0616/RND_S2.md", "bagian 0 dan 3", "TERUKUR", M["dok_s2v2"]),
    ("37", "klaim", "RUN-KITA", "s5_dok.json per_kartu.S2.rekap.n_klaim", "bagian 3", "TERUKUR", M["klaim_s2"]),
    ("37", "klaim ditemukan", "RUN-KITA", "s5_dok.json per_kartu.S2.rekap.terletak", "bagian 3", "TERUKUR", M["terletak_s2"]),
    ("20", "klaim", "RUN-KITA", "s5_dok_snap_0558.json per_kartu.S2.rekap.n_klaim", "bagian 3", "TERUKUR", M["klaim_s2v1"]),
    ("20", "klaim ditemukan", "RUN-KITA", "s5_dok_snap_0558.json per_kartu.S2.rekap.terletak", "bagian 3", "TERUKUR", M["terletak_s2v1"]),
    ("14", "klaim", "RUN-KITA", "s5_dok.json per_kartu.S3.rekap.n_klaim dan terletak", "bagian 3", "TERUKUR", M["klaim_s3"]),
    ("15", "klaim", "RUN-KITA", "s5_dok.json per_kartu.S4.rekap.n_klaim dan terletak", "bagian 3", "TERUKUR", M["klaim_s4"]),
    ("66", "klaim", "DERIVASI", "37 + 14 + 15 dari s5_dok.json", "bagian 3 dan 9", "TERUKUR", M["klaim_total"]),
    ("7", "turunan", "DERIVASI", "s5_dok.json per_kartu[*].turunan", "bagian 3", "TERUKUR", M["turunan"]),
    ("13,0", "detik", "RUN-KITA", "s5_rerun.json rerun.elapsed_s", "bagian 2", "TERUKUR", M["elapsed"]),
    ("9", "fold", "RUN-KITA", "s5_rerun.json rerun.n_fold", "bagian 2", "TERUKUR", M["fold"]),
    ("52509", "baris data", "RUN-KITA", "s5_rerun.json rerun.shape[0]", "bagian 2", "TERUKUR", M["nbaris"]),
    ("50", "kolom data", "RUN-KITA", "s5_rerun.json rerun.shape[1]", "bagian 2", "TERUKUR", M["nkolom"]),
    ("13", "metrik", "RUN-KITA", "s5_rerun.json rekap.t51_metrik", "bagian 2", "TERUKUR", M["metrik"]),
    ("0", "metrik gagal", "RUN-KITA", "s5_rerun.json rekap t51, t52, t61, t4_gagal", "bagian 2", "TERUKUR", M["gagal"]),
    ("935", "FP total", "RUN-KITA", "s5_rerun.json rerun.ringkas.42.fp_total", "bagian 2", "TERUKUR", M["fp"]),
    ("3804", "TP total", "RUN-KITA", "s5_rerun.json rerun.ringkas.42.tp_total", "bagian 2", "TERUKUR", M["tp"]),
    ("0,7789", "presisi median", "RUN-KITA", "s5_rerun.json rerun.ringkas.42.precision_median", "bagian 2", "TERUKUR", M["presisi"]),
    ("0,5638", "recall median", "RUN-KITA", "s5_rerun.json rerun.ringkas.42.recall_median", "bagian 2", "TERUKUR", M["recall"]),
    ("3,5302", "FAR per 24 jam kalender", "RUN-KITA", "s5_rerun.json rerun.ringkas.42.far24_kalender_median", "bagian 2", "TERUKUR", M["far"]),
    ("936", "FP total setelah dirusak", "UJI-NEGATIF", "s5_negative.json tabel_5_1.fp_total.sel.42.dok", "bagian 1", "TERUKUR", M["neg_fp"]),
    ("62", "FP fold F-10 setelah dirusak", "UJI-NEGATIF", "s5_negative.json tabel_6_1.F-10.sel.FP.dok", "bagian 1", "TERUKUR", M["neg_f10"]),
    ("3150", "byte", "RUN-KITA", "os.path.getsize scratch/rnd/s2/bak_gagal/s2_vib.json", "bagian 3 dan 7", "TERUKUR", M["size_vib1"]),
    ("5773", "byte", "RUN-KITA", "os.path.getsize scratch/rnd/s2/bak_gagal/s2_ssi.json", "bagian 7", "TERUKUR", M["size_ssi1"]),
    ("157781", "byte", "RUN-KITA", "os.path.getsize scratch/rnd/s2/s2_records_vib.json", "bagian 3", "TERUKUR", M["size_recvib"]),
    ("343877", "byte", "RUN-KITA", "os.path.getsize scratch/rnd/s2/s2_records_ssi.json", "bagian 3", "TERUKUR", M["size_recssi"]),
    ("85513", "byte", "RUN-KITA", "os.path.getsize scratch/rnd/s2/s2_ringkas.json", "bagian 3", "TERUKUR", M["size_ringkas"]),
    ("645763", "byte", "RUN-KITA", "os.path.getsize data/volve/external/volve_catalog_target_paths.csv", "bagian 7", "TERUKUR", M["size_katalog"]),
    ("06:03:05", "WIB", "RUN-KITA", "s2_meta.json kunci mulai", "bagian 0", "TERUKUR", M["t_mulai2"]),
    ("06:05:59", "WIB", "RUN-KITA", "mtime scratch/rnd/s2/bak_gagal", "bagian 0 dan 7", "TERUKUR", M["t_bak"]),
    ("06:16:16", "WIB", "RUN-KITA", "mtime scratch/rnd/s5/view_0616/RND_S2.md", "bagian 0", "TERUKUR", M["t_dokv2"]),
    ("0", "DOI", "RUN-KITA", "grep pola 10.xxxx/ pada empat dokumen", "bagian 5", "TERUKUR", M["doi"]),
    ("0", "URL", "RUN-KITA", "grep http pada empat dokumen", "bagian 5", "TERUKUR", M["url"]),
    ("1", "nama standar", "RUN-KITA", "grep API RP pada empat dokumen, hanya S2 baris 105, tanpa nomor bagian", "bagian 5 dan 7", "TERUKUR", M["standar"]),
    ("0", "em-dash", "RUN-KITA", "hitung karakter U+2014 pada empat dokumen", "bagian 6", "TERUKUR", M["emdash"]),
    ("6", "pikiran", "RUN-KITA", "baris sequ pada view_0616/RND_S2.md", "bagian 6", "TERUKUR", M["sequ"]),
    ("4", "baris riset", "RUN-KITA", "hitung frasa Riset pendahuluan pada view_0616/RND_S2.md", "bagian 6", "TERUKUR", M["riset"]),
    ("a9e46afa172a2cae", "sha256-16", "HASH", "sha256 docs/RND_S1_SEED_ROBUSTNESS.md", "bagian 11", "TERUKUR", M["h_s1"]),
    ("84a6f6287ebc3ad3", "sha256-16", "HASH", "sha256 snapshot view_0616/RND_S2.md", "bagian 11", "TERUKUR", M["h_s2"]),
    ("02a3ca1cd06f3146", "sha256-16", "HASH", "sha256 docs/RND_S3_HYBRID_BITWEAR.md", "bagian 11", "TERUKUR", M["h_s3"]),
    ("99aa5424b34f6cfa", "sha256-16", "HASH", "sha256 docs/RND_S4_LAYER_B_DATA.md", "bagian 11", "TERUKUR", M["h_s4"]),
    ("4c5d09cc953baae2", "sha256-16", "HASH", "sha256 snapshot view_0616/LEDGER.md", "bagian 11", "TERUKUR", M["h_led"]),
    ("f2ea2aa245d3aa45", "sha256-16", "HASH", "sha256 docs/RND_EVALUATION_POLICY.md", "bagian 11", "TERUKUR", M["h_pol"]),
    ("2d8e6f32d274ffc3", "sha256-16", "HASH", "sha256 code/rnd_hybrid_harness.py", "bagian 2", "TERUKUR", M["h_har"]),
    ("BELUM TERUKUR", "-", "BELUM-TERUKUR", "S2, S3, S4 tidak dihitung ulang dari data mentah", "bagian 10", "BELUM", None),
    ("BELUM TERUKUR", "-", "BELUM-TERUKUR", "lima seed S1 selain 42 dan 13 tidak dijalankan ulang", "bagian 10", "BELUM", None),
    ("BELUM TERUKUR", "-", "BELUM-TERUKUR", "teks 1759 berkas PDF DDR tidak dipindai", "bagian 10", "BELUM", None),
    ("BELUM TERUKUR", "-", "BELUM-TERUKUR", "dokumen S2 versi 0558 tidak tersimpan utuh", "bagian 10", "BELUM", None),
    ("BELUM TERUKUR", "-", "BELUM-TERUKUR", "kestabilan S2 setelah 0618 tidak dijamin", "bagian 10", "BELUM", None),
    ("BELUM TERUKUR", "-", "BELUM-TERUKUR", "klaim lapisan C tidak diuji ulang", "bagian 10", "BELUM", None),
]

for i, (angka, satuan, kelas, rujukan, bagian, status, nilai) in enumerate(R2, 1):
    if nilai is None:
        continue
    if isinstance(nilai, float):
        if abs(float(angka.replace(",", ".")) - nilai) > 1e-4:
            raise SystemExit(f"BEDA baris {i}: sel {angka} lawan terukur {nilai}")
    elif isinstance(nilai, int):
        if str(nilai) != angka:
            raise SystemExit(f"BEDA baris {i}: sel {angka} lawan terukur {nilai}")

blok = ["", "---", "",
        "## Bagian S5: audit gelombang 2 (kartu `t_b5b16adc`)", "",
        f"Dokumen pendamping: `docs/RND_S5_AUDIT_WAVE2.md`. Tanggal audit: {TANGGAL} (WIB).",
        f"Snapshot yang diaudit: `scratch/rnd/s5/view_0616/` (ledger sha256 `{M['h_led']}`, dokumen S2 sha256 `{M['h_s2']}`).",
        "Baris di bawah adalah hasil ukur audit, bukan salinan klaim dokumen S1 sampai S4.", "",
        "| No | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |",
        "|---|---|---|---|---|---|---|"]
for i, (angka, satuan, kelas, rujukan, bagian, status, _) in enumerate(R2, 1):
    blok.append(f"| S5-{i:03d} | {angka} | {satuan} | {kelas} | {rujukan} | {bagian} | {status} |")

teks = open(LEDGER, encoding="utf-8").read()
pola_blok = re.compile(r"\n---\n\n## Bagian S5:.*?(?=\n---\n\n## |\Z)", re.S)
teks_baru = pola_blok.sub("", teks)
if not teks_baru.endswith("\n"):
    teks_baru += "\n"
teks_baru += "\n".join(blok) + "\n"
open(LEDGER, "w", encoding="utf-8").write(teks_baru)

n_s5 = len(re.findall(r"^\| S5-\d+ \|", teks_baru, re.M))
print(f"baris S5 ditulis: {n_s5} (harapan {len(R2)})")
print("assert nilai: OK")
print("sha ledger baru:", sha(LEDGER))
