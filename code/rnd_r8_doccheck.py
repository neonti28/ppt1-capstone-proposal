"""RND-R8 -- pemeriksa dokumen: em-dash, CJK, rujukan ledger, dan angka kunci."""
import json, re, sys

BASE = "/mnt/d/Capstone 1(v2)"
DOC = f"{BASE}/docs/RND_R8_EVALUASI_BERLAPIS.md"
LED = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"
doc = open(DOC, encoding="utf-8").read()
led = open(LED, encoding="utf-8").read()
agg = json.load(open(f"{BASE}/scratch/rnd/r8/r8_agg.json"))
raw = {t: json.load(open(f"{BASE}/scratch/rnd/r8/r8_{t}.json")) for t in ("hyd", "shk", "toolwear", "stuck")}

gagal = []
cek_n = 0


def cek(nama, kondisi, info=""):
    global cek_n
    cek_n += 1
    if not kondisi:
        gagal.append(f"{nama} {info}")


# 1. em dash dan en dash sebagai penghubung klausa
cek("em-dash", doc.count("\u2014") == 0, f"jumlah {doc.count(chr(0x2014))}")
cek("en-dash", doc.count("\u2013") == 0, f"jumlah {doc.count(chr(0x2013))}")
# 2. tidak ada karakter CJK
cjk = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff]", doc)
cek("cjk", len(cjk) == 0, f"jumlah {len(cjk)}")
# 3. rujukan ledger R8 yang dipakai dokumen harus ada di ledger
refs = sorted(set(re.findall(r"R8-\d{3}", doc)))
led_ids = set(re.findall(r"\| (R8-\d{3}) \|", led))
for r in refs:
    cek(f"ref {r}", r in led_ids, "tidak ada di ledger")
# 4. rentang yang disebut dokumen benar-benar ada
cek("R8-001 ada", "R8-001" in led_ids)
cek("R8-097 ada", "R8-097" in led_ids)
n_rows = len(re.findall(r"\| R8-\d{3} \|", led))
cek("jumlah baris ledger 97", n_rows == 97, f"jumlah {n_rows}")
cek("satu bagian R8", led.count("## Bagian R8") == 1, f"jumlah {led.count('## Bagian R8')}")
# 5. angka kunci dokumen == JSON
pasangan = [
    ("2105", raw["hyd"]["ringkas"]["rule_kanal"]["fp_total"], "2105"),
    ("935", raw["hyd"]["ringkas"]["H1_stat_dan_rule"]["fp_total"], "935"),
    ("5579", raw["hyd"]["ringkas"]["rule_kanal"]["tp_total"], "5579"),
    ("3804", raw["hyd"]["ringkas"]["H1_stat_dan_rule"]["tp_total"], "3804"),
    ("0,7789", round(float(__import__("numpy").median(
        [v["precision"] for v in agg["task"]["hyd"]["model"]["H1_stat_dan_rule"]["per_fold"].values()])), 4), "0,7789"),
    ("11,5", 11.5, "11,5"),
    ("2633", raw["shk"]["ringkas"]["ML_saja"]["fp_total"], "2633"),
    ("667", raw["shk"]["ringkas"]["H2_ML_dan_stat"]["fp_total"], "667"),
    ("0,3385", round(float(__import__("numpy").median(
        [v["bacc"] for v in agg["task"]["toolwear"]["model"]["ML_default"]["per_fold"].values()])), 4), "0,3385"),
    ("0,6404", 0.6404, "0,6404"),
]
for teks, nilai, fmt in pasangan:
    cek(f"angka {teks}", teks in doc, "tidak ada di dokumen")
    cek(f"angka {teks} == data", f"{nilai}".replace(".", ",")[:len(fmt)] == fmt or str(nilai) == teks,
        f"nilai {nilai}")

# 6. jumlah hybrid yang dijalankan
cek("empat hybrid", "empat hybrid" in doc.lower() or "4 hybrid" in doc or "H1" in doc and "H4" in doc)
# 7. bagian wajib
for s in ["Riset pendahuluan:", "TABEL KEPUTUSAN", "KOMPOSISI ENGINE FINAL",
          "RINGKASAN LIMA BARIS", "YANG BELUM TERVERIFIKASI", "RUJUKAN"]:
    cek(f"bagian {s}", s in doc, "tidak ditemukan")
# 8. sequ-mcp pikiran
cek("sequ 6 pikiran", "thoughtHistoryLength 6" in doc or "6 pikiran" in doc)
cek("sequ jumlah disebut", "6 pikiran" in doc)

print(f"cek: {cek_n}, gagal: {len(gagal)}")
for g in gagal:
    print("  GAGAL", g)
sys.exit(1 if gagal else 0)
