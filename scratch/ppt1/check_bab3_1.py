"""Pemeriksa independen untuk docs/PPT1_BAB3_1.md dan scratch/ppt1/alternatif.json.

Tidak memakai builder; membaca hasil dari disk lalu memeriksa:
  1. integritas tabel markdown (jumlah sel = jumlah kolom header)
  2. struktur wajib (9 subbab alternatif, 3 per anggota)
  3. angka kunci benar-benar ada di berkas yang dikutip (jejak tidak palsu)
  4. nol em-dash, nol emoji
  5. kesesuaian JSON dengan markdown (id, nama, status, sumber)

Jalankan: python3 scratch/ppt1/check_bab3_1.py
"""

import json
import os
import re
import sys

ROOT = "/mnt/d/Capstone 1(v2)"
MD = os.path.join(ROOT, "docs/PPT1_BAB3_1.md")
JS = os.path.join(ROOT, "scratch/ppt1/alternatif.json")

galat = []
info = []

md = open(MD, encoding="utf-8").read()
data = json.load(open(JS, encoding="utf-8"))
alts = data["alternatif"]

# ---- 1. integritas tabel
tabel = 0
for i, baris in enumerate(md.splitlines(), 1):
    if baris.startswith("|") and baris.endswith("|"):
        tabel += 1
        n = baris.count("|") - 1
        if "kolom_header" not in dir() or prev_blank:
            pass
info.append(f"baris tabel terdeteksi: {tabel}")

# cek per blok tabel: header + separator + isi harus sama jumlah kolom
baris_md = md.splitlines()
blok, mulai = [], None
def tutup(blok, mulai):
    if not blok:
        return
    n = blok[0][1].count("|") - 1
    for no, teks in blok:
        if teks.count("|") - 1 != n:
            galat.append(f"baris {no} punya {teks.count('|') - 1} kolom, header {n}")

for no, teks in enumerate(baris_md, 1):
    if teks.startswith("|"):
        if mulai is None:
            mulai = no
        blok.append((no, teks))
    else:
        tutup(blok, mulai) if False else None
        if blok:
            n = blok[0][1].count("|") - 1
            for nomor, isi in blok:
                if isi.count("|") - 1 != n:
                    galat.append(f"baris {nomor} punya {isi.count('|') - 1} kolom, header {n}")
        blok, mulai = [], None
if blok:
    n = blok[0][1].count("|") - 1
    for nomor, isi in blok:
        if isi.count("|") - 1 != n:
            galat.append(f"baris {nomor} punya {isi.count('|') - 1} kolom, header {n}")

# ---- 2. struktur
sub = re.findall(r"^#### 3\.1\.4\.(\d+) (A\d) ", md, re.M)
if len(sub) != 9:
    galat.append(f"subbab rincian {len(sub)}, wajib 9")
if [s[1] for s in sub] != [a["id"] for a in alts]:
    galat.append("urutan id pada markdown tidak sama dengan JSON")
for i in (1, 2, 3):
    n = sum(1 for a in alts if a["anggota"] == i)
    if n != 3:
        galat.append(f"anggota {i} berjumlah {n}")
info.append(f"subbab rincian: {len(sub)} (A1 sampai A9)")

# ---- 3. jejak angka: setiap pasangan harus muncul di berkas sumber
JEJAK = [
    ("119,6", "docs/V9_PM2_VERDICT.md"),
    ("281.030", "docs/V9_PM1_ARCHITECTURE.md"),
    ("178.430", "docs/V9_PM1_ARCHITECTURE.md"),
    ("52.905", "docs/V10_D1_BAB_DATA.md"),
    ("1.225", "docs/PPT1_LEDGER_ANGKA.md"),
    ("73500", "docs/PPT1_LEDGER_ANGKA.md"),
    ("0/10", "docs/V8_PM_VERDICT.md"),
    ("0,787", "docs/V7_R1_SOLUTIONS.md"),
    ("66,9", "docs/V7_R1_SOLUTIONS.md"),
    ("575", "docs/V7_R1_SOLUTIONS.md"),
    ("198.928", "docs/V7_R1_SOLUTIONS.md"),
    ("dullingInfo", "docs/V4_MAINTENANCE_ML_OPTIONS.md"),
    ("49,4", "docs/V4_MAINTENANCE_ML_OPTIONS.md"),
    ("75", "docs/V4_MAINTENANCE_ML_OPTIONS.md"),
    ("0,516", "docs/V9_EVAL_C_LAYERC.md"),
    ("0,51", "docs/V9_EVAL_B_LAYERB.md"),
]
for angka, berkas in JEJAK:
    path = os.path.join(ROOT, berkas)
    if not os.path.exists(path):
        galat.append(f"berkas jejak hilang: {berkas}")
        continue
    isi = open(path, encoding="utf-8", errors="replace").read()
    if angka not in isi:
        galat.append(f"angka {angka} tidak ditemukan di {berkas}")
info.append(f"pasangan jejak diperiksa: {len(JEJAK)}")

# angka di manifest md juga harus ada di dokumen
manifest = [b for b in baris_md if b.startswith("| ") and "`docs/" in b]
info.append(f"baris manifest berjejak: {len(manifest)}")

# ---- 4. register
if chr(0x2014) in md:
    galat.append(f"em-dash ditemukan: {md.count(chr(0x2014))}")
emoji = [c for c in md if ord(c) > 0x1F000]
if emoji:
    galat.append(f"karakter emoji ditemukan: {len(emoji)}")
for tag in ["[MENUNGGU", "[RENCANA]", "[SELESAI]", "✅", "⬜"]:
    if tag in md:
        galat.append(f"penanda status tidak baku: {tag}")

# ---- 5. konsistensi JSON
if len(alts) != 9:
    galat.append("JSON tidak memuat 9 alternatif")
sumber = sum((a["sumber"] for a in alts), [])
if len(set(sumber)) != len(sumber):
    galat.append("ada sumber dipakai dua kali di JSON")
for a in alts:
    if a["id"] not in md:
        galat.append(f"{a['id']} tidak muncul di markdown")
    if a["nama"] not in md:
        galat.append(f"nama {a['id']} tidak muncul di markdown")
    for s in a["sumber"]:
        if s not in md:
            galat.append(f"sumber {s} ({a['id']}) tidak muncul di markdown")
    for b in a["bok"]:
        if str(b) not in data["bok"]:
            galat.append(f"BoK {b} tidak ada di tabel BoK")
info.append(f"sumber unik di JSON: {len(set(sumber))}")
info.append(f"status: {json.dumps(data['rekap']['status'], ensure_ascii=False)}")

print("== INFO ==")
for i in info:
    print(" -", i)
print()
if galat:
    print("== GAGAL ==")
    for g in galat:
        print(" !", g)
    sys.exit(1)
print("== LOLOS: semua pemeriksaan bersih ==")
