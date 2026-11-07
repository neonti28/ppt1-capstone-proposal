#!/usr/bin/env python3
"""Pemeriksa independen untuk docs/RND_S5_AUDIT_WAVE2.md dan blok ledger S5.

Tidak mengimpor generator. Membaca dokumen dan ledger dari disk, memformat ulang
angkanya sendiri, dan menguji hal yang bisa gagal.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
DOC = BASE / "docs/RND_S5_AUDIT_WAVE2.md"
LED = BASE / "docs/RND_PROVENANCE_LEDGER.md"
GEN = BASE / "scratch/rnd/s5/s5g_dokumen.py"

dok = DOC.read_text(encoding="utf-8")
led = LED.read_text(encoding="utf-8")
gagal = []


def cek(nama, kondisi, detail=""):
    print(("OK   " if kondisi else "GAGAL") + "  " + nama + ("  " + str(detail) if detail else ""))
    if not kondisi:
        gagal.append(nama)


# 1. struktur dokumen
cek("dokumen ada dan tidak kosong", len(dok) > 10000, len(dok))
cek("em-dash nol", dok.count("\u2014") == 0, dok.count("\u2014"))
cek("en-dash nol", dok.count("\u2013") == 0, dok.count("\u2013"))
cek("Riset pendahuluan ada", len(re.findall(r"^Riset pendahuluan:", dok, re.M)) >= 1)
cek("menyebut jumlah pikiran sequ",
    re.search(r"Jumlah pikiran yang dipakai: \d+", dok) is not None)
bag = re.findall(r"^## (\d+)\. ", dok, re.M)
cek("sembilan bagian bernomor", bag == [str(i) for i in range(1, 10)], bag)
cek("bagian 8 memuat daftar belum terverifikasi", "Yang belum terverifikasi pada audit ini" in dok)
cek("ringkasan lima baris", dok.count("\n1. ") >= 1 and "\n5. " in dok)

# 2. ringkasan lima baris tepat 5 butir
i = dok.index("## 9. Ringkasan lima baris")
blok9 = dok[i:].splitlines()
butir = [l for l in blok9 if re.match(r"^\d+\.\s", l)]
cek("ringkasan berisi 5 butir", len(butir) == 5, len(butir))

# 3. daftar belum terverifikasi tepat 8 butir
i8 = dok.index("## 8. Yang belum terverifikasi pada audit ini")
blok8 = []
for l in dok[i8:].splitlines()[1:]:
    if l.startswith("## "):
        break
    blok8.append(l)
butir8 = [l for l in blok8 if re.match(r"^\d+\.\s", l)]
cek("daftar belum terverifikasi 8 butir", len(butir8) == 8, len(butir8))

# 4. ledger S5
blok = []
aktif = False
for l in led.splitlines():
    if l.startswith("## Bagian"):
        aktif = l.startswith("## Bagian S5:")
        continue
    if aktif:
        blok.append(l)
baris_s5 = [l for l in blok if re.match(r"^\| S5-\d{3} \|", l)]
cek("blok ledger S5 ada", len(blok) > 100, len(blok))
cek("semua baris S5 tepat 7 kolom",
    all(len([c for c in l.strip().strip("|").split("|")]) == 7 for l in baris_s5),
    sum(1 for l in baris_s5 if len(l.strip().strip("|").split("|")) != 7))
ids = [re.match(r"^\| (S5-\d{3}) \|", l).group(1) for l in baris_s5]
cek("tidak ada id ganda", len(ids) == len(set(ids)), len(ids) - len(set(ids)))
cek("id berurutan tanpa lubang",
    ids == ["S5-%03d" % i for i in range(1, len(ids) + 1)], len(ids))
cek("tidak ada baris BELUM palsu", all("BELUM" not in l.split("|")[1] for l in baris_s5))

# 5. angka dokumen harus ada di blok S5
def kandidat(tok):
    tok = tok.rstrip(".,")
    out = set()
    try:
        if "," in tok and "." in tok:
            out.add(round(abs(float(tok.replace(".", "").replace(",", "."))), 4))
        elif "," in tok:
            out.add(round(abs(float(tok.replace(",", "."))), 4))
            out.add(round(abs(float(tok.replace(",", ""))), 4))
        elif re.fullmatch(r"\d{1,3}(?:\.\d{3})+", tok):
            out.add(round(abs(float(tok.replace(".", ""))), 4))
            out.add(round(abs(float(tok)), 4))
        else:
            out.add(round(abs(float(tok)), 4))
    except ValueError:
        pass
    return out


def himpunan(teks):
    s = set()
    for tok in re.findall(r"\d[\d.,]*", teks):
        s |= kandidat(tok)
    return s


led_angka = himpunan("\n".join(blok))
tanpa = []
for l in dok.splitlines():
    if not l.strip().startswith("|"):
        continue
    for c in l.strip().strip("|").split("|"):
        c = c.strip().strip("*` ")
        if re.fullmatch(r"-?\d+(?:[.,]\d+)?", c):
            k = kandidat(c)
            if k and not any(any(abs(v - x) <= 0.5 * 10 ** (-2) + 1e-9 for x in led_angka) for v in k):
                tanpa.append(c)
fraksi = 1 - len(tanpa) / max(1, len([1 for l in dok.splitlines() if l.strip().startswith("|")
                                      for c in l.strip().strip("|").split("|")
                                      if re.fullmatch(r"-?\d+(?:[.,]\d+)?", c.strip().strip("*` "))]))
cek("mayoritas angka tabel dokumen ada di ledger S5", fraksi > 0.9, round(fraksi, 4))
print("     contoh angka tanpa padanan:", tanpa[:8])

# 6. pengunci silang ke artefak JSON
rerun = json.loads((BASE / "scratch/rnd/s5/s5_rerun_audit.json").read_text(encoding="utf-8"))
n_sel = len(rerun["banding_dok_51"]) + len(rerun["banding_dok_4_perfold"]) + len(rerun["banding_dok_61"])
cek("dokumen menyebut 143 sel", "143" in dok, n_sel)
cek("semua sel lulus", all(x["lulus"] for x in rerun["banding_dok_51"] + rerun["banding_dok_4_perfold"]
                          + rerun["banding_dok_61"]))
klaim = json.loads((BASE / "scratch/rnd/s5/s5_klaim2.json").read_text(encoding="utf-8"))
cek("dokumen menyebut 51 klaim", "51" in dok and len(klaim) == 51, len(klaim))
cek("semua klaim lulus", all(c["lulus"] for c in klaim))

# 7. cacat S4-013 diuji ulang dari sumber primer
labels = json.loads((BASE / "scratch/rnd/s4/labels_duration.json").read_text(encoding="utf-8"))
cek("sumber.kolom berisi 20", len(labels["sumber"]["kolom"]) == 20, len(labels["sumber"]["kolom"]))
cek("baris ledger S4-013 masih menulis 884 kolom",
    "| S4-013 | 884 record / 884 kolom |" in led)
cek("dokumen audit mencatat cacat S4-013", "S4-013" in dok and "D1" in dok)
s4dok = (BASE / "docs/RND_S4_LAYER_B_DATA.md").read_text(encoding="utf-8")
cek("dokumen S4 mengutip S4-013 untuk 20 kolom", "884 record, 20 kolom (`S4-013`)" in s4dok)

# 8. kartu tidak boleh diubah: empat dokumen gelombang 2 masih ada
for k in ("RND_S1_SEED_ROBUSTNESS.md", "RND_S2_HYBRID_VIB_SSI.md",
          "RND_S3_HYBRID_BITWEAR.md", "RND_S4_LAYER_B_DATA.md"):
    p = BASE / "docs" / k
    cek("dokumen asal utuh " + k, p.exists() and p.stat().st_size > 10000, p.stat().st_size if p.exists() else None)

# 9. idempotensi: jalankan generator dua kali, bandingkan sha256
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


a1, b1 = sha(DOC), sha(LED)
r = subprocess.run([sys.executable, str(GEN)], capture_output=True, text=True)
cek("generator jalan ulang tanpa error", r.returncode == 0, r.stderr[-300:])
a2, b2 = sha(DOC), sha(LED)
cek("dokumen idempoten", a1 == a2, (a1[:12], a2[:12]))
cek("ledger idempoten", b1 == b2, (b1[:12], b2[:12]))

print()
print("RINGKAS: gagal =", len(gagal), gagal if gagal else "")
sys.exit(1 if gagal else 0)
