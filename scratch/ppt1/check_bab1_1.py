"""Uji penerimaan (acceptance) docs/PPT1_BAB1_1.md.

Yang diuji, bukan diasumsikan:
1. Enam sub-bagian ada, termasuk empat sub-bagian wajib pedoman (objek studi,
   stakeholder, alur operasi, uraian masalah) plus rich picture dan trade-off.
2. Rich picture: jumlah simpul N*, relasi R*, loop L*, gangguan G*.
3. Setiap baris yang memuat ANGKA UKUR punya tanda jejak [L:..] / [H:..] / [S:..].
4. Tidak ada em-dash sebagai penghubung klausa.
5. Setiap tanda [L:ID] benar-benar ada di docs/PPT1_LEDGER_ANGKA.md.
6. Setiap tanda [H:kunci] benar-benar ada di scratch/ppt1/bab1_1_angka.json.
7. Angka kunci wajib muncul apa adanya.

Catatan metodologis untuk uji nomor 3: yang dibuang dari baris sebelum diuji
adalah PENANDA STRUKTURAL, bukan angka ukur. Penanda yang dibuang: blok kode
berpagar, teks dalam backtick (nama berkas, perintah, nama kolom), ID simpul
dan relasi (N1, R2, L3, G4, S5, T6, P0, D1), nomor sub-bab (1.1.3), rujukan
seksi (§3.2.1), rujukan halaman (h.38), nomor tahap, kategori 6M, versi
lisensi, serta penomoran daftar. Angka hasil ukur tidak pernah dibuang, jadi
kalau ada angka ukur tanpa tanda jejak, uji ini tetap gagal.

Jalankan: python3 scratch/ppt1/check_bab1_1.py
"""
import json
import re

BASE = "/mnt/d/Capstone 1(v2)"
DOC = BASE + "/docs/PPT1_BAB1_1.md"
LEDGER = BASE + "/docs/PPT1_LEDGER_ANGKA.md"
ANGKA = BASE + "/scratch/ppt1/bab1_1_angka.json"

text = open(DOC, encoding="utf-8").read()
lines = text.splitlines()
ledger = open(LEDGER, encoding="utf-8").read()
angka = json.load(open(ANGKA, encoding="utf-8"))

report = {"ok": True, "gagal": []}


def cek(nama, lolos, detail=""):
    report[nama] = {"lolos": bool(lolos), "detail": detail}
    if not lolos:
        report["ok"] = False
        report["gagal"].append(nama)


# ---------------------------------------------------------------- 1. sub-bagian
wajib = {
    "objek_studi": r"^### 1\.1\.1 Deskripsi Objek Studi",
    "stakeholder": r"^### 1\.1\.2 Stakeholder",
    "alur_operasi": r"^### 1\.1\.3 Alur Operasi",
    "rich_picture": r"^### 1\.1\.4 Rich Picture",
    "trade_off": r"^### 1\.1\.5 Trade-off",
    "uraian_masalah": r"^### 1\.1\.6 Uraian Singkat Permasalahan",
}
ada = {k: bool(re.search(v, text, re.M)) for k, v in wajib.items()}
cek("empat_sub_bagian_plus_pendukung", all(ada.values()), ada)


# ---------------------------------------------------------------- 2. elemen rich picture
def hitung_id(prefix):
    return sorted(set(re.findall(r"^\| (%s\d+) \|" % prefix, text, re.M)), key=lambda s: int(s[1:]))


nodes, rels, loops, gang = hitung_id("N"), hitung_id("R"), hitung_id("L"), hitung_id("G")
cek("simpul_min_10", len(nodes) >= 10, {"jumlah": len(nodes)})
cek("relasi_min_8", len(rels) >= 8, {"jumlah": len(rels)})
cek("loop_min_3", len(loops) >= 3, {"jumlah": len(loops)})
cek("gangguan_min_4", len(gang) >= 4, {"jumlah": len(gang)})

# ---------------------------------------------------------------- 3. angka wajib bertanda
TAG = re.compile(r"\[(L|H|S):")
NUM = re.compile(r"\d")

STRIP = [
    (re.compile(r"```.*?```", re.S), " "),          # blok kode berpagar
    (re.compile(r"`[^`]*`"), " "),                  # nama berkas, perintah, nama kolom
    (re.compile(r"\*\*[^*]*\*\*"), lambda m: m.group(0)),  # biarkan tebal, hanya penanda
    (re.compile(r"\[[LH]:(?:[A-D]\d{2}|[a-zA-Z0-9_.]+)\]"), " "),  # tanda jejak itu sendiri
    (re.compile(r"\[S:[^\]]*\]"), " "),
    (re.compile(r"\b[SNRLGTPBD]\d+\b"), " "),       # ID simpul/relasi/loop/gangguan/stakeholder/tahap/kartu/engine
    (re.compile(r"\bWP\d+\b"), " "),
    (re.compile(r"\bK-[ivx]+\b"), " "),
    (re.compile(r"\b1\.1(?:\.\d+)?\b"), " "),        # nomor sub-bab
    (re.compile(r"\b\d\.\d(?:\.\d+)?[a-z]?\b"), " "),  # nomor sub-bab/klausa pedoman (1.3, 2.8c)
    (re.compile(r"§\s*\d+(?:\.\d+)*"), " "),
    (re.compile(r"\bh\.\d+(?:-\d+)?"), " "),         # rujukan halaman
    (re.compile(r"\bl\.\d+(?:-\d+)?"), " "),         # rujukan baris (l.31-32)
    (re.compile(r"\b(?:19|20)\d{2}\b"), " "),        # tahun pada tanggal administratif
    (re.compile(r"CC BY-NC-SA \d\.\d"), " "),
    (re.compile(r"\b\dM\b"), " "),                   # kategori 6M, 4M
    (re.compile(r"^\s*\d+\.\s"), " "),              # penomoran daftar
    (re.compile(r"\(\d\)"), " "),                    # penanda urutan dalam kalimat
]

bocor = []
in_fence = False
in_meta = True  # tabel identitas di kepala dokumen: tanggal, mitra, acuan (administratif)
for i, ln in enumerate(lines, 1):
    if ln.strip().startswith("```"):
        in_fence = not in_fence
        continue
    if in_fence:
        continue
    s = ln.strip()
    if in_meta:
        if s.startswith("**Riset pendahuluan:"):
            in_meta = False
        else:
            continue
    if not s or s.startswith("#") or s.startswith("|---"):
        continue
    if TAG.search(s):
        continue
    sisa = s
    for pola, ganti in STRIP:
        sisa = pola.sub(ganti, sisa)
    if NUM.search(sisa):
        bocor.append({"baris": i, "sisa": sisa[:400]})
cek("semua_baris_berangka_bertanda", not bocor, {"jumlah_bocor": len(bocor), "contoh": bocor[:12]})

# ---------------------------------------------------------------- 4. em-dash
cek("tanpa_em_dash", text.count("\u2014") == 0, {"jumlah": text.count("\u2014")})

# ---------------------------------------------------------------- 5. rujukan ledger
ids = sorted(set(re.findall(r"\[L:([A-D]\d{2})\]", text)))
hilang = [i for i in ids if ("| %s |" % i) not in ledger]
cek("rujukan_ledger_valid", not hilang, {"jumlah_id": len(ids), "tidak_ada_di_ledger": hilang})

# ---------------------------------------------------------------- 6. rujukan JSON bukti
hkeys = sorted(set(re.findall(r"\[H:([a-zA-Z0-9_.]+)\]", text)))


def resolve(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return False
    return True


h_hilang = [k for k in hkeys if not resolve(angka, k)]
cek("rujukan_h_valid", not h_hilang, {"jumlah_kunci": len(hkeys), "tidak_ada_di_json": h_hilang})

# ---------------------------------------------------------------- 7. angka kunci
kunci = ["884", "73.500", "1.225", "292.954", "27", "55", "0 dari 7",
         "4,5 sampai 8,5", "62,34", "56,1", "5,7", "64,6", "20,6", "37 lipatan"]
tidak_muncul = [k for k in kunci if k not in text]
cek("angka_kunci_muncul", not tidak_muncul, {"tidak_muncul": tidak_muncul})

report["statistik"] = {
    "baris_dokumen": len(lines),
    "karakter": len(text),
    "simpul": len(nodes),
    "relasi": len(rels),
    "loop": len(loops),
    "gangguan": len(gang),
    "tag_L": len(re.findall(r"\[L:", text)),
    "tag_H": len(re.findall(r"\[H:", text)),
    "tag_S": len(re.findall(r"\[S:", text)),
    "id_ledger_unik": len(ids),
    "kunci_json_unik": len(hkeys),
}
print(json.dumps(report, indent=1, ensure_ascii=False))
print("\nHASIL:", "LULUS" if report["ok"] else "GAGAL")
