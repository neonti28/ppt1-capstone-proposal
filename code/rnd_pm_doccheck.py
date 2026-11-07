#!/usr/bin/env python3
"""Pemeriksa dokumen RND_PM_VERDICT.md dan Bagian PM ledger.

Tidak menulis apa pun. Setiap pemeriksaan mencetak PASS/FAIL dan exit code 1
bila ada yang gagal.
"""
import json
import re
import sys
from pathlib import Path

WS = Path("/mnt/d/Capstone 1(v2)")
DOC = WS / "docs/RND_PM_VERDICT.md"
LED = WS / "docs/RND_PROVENANCE_LEDGER.md"

hasil = []


def cek(nama, kondisi, detail=""):
    hasil.append((nama, bool(kondisi), detail))


doc = DOC.read_text(encoding="utf-8")
led = LED.read_text(encoding="utf-8")
lines = doc.splitlines()

# 1. Karakter terlarang
cek("em_dash_0", doc.count("\u2014") == 0, f"em-dash={doc.count(chr(8212))}")
cek("en_dash_0", doc.count("\u2013") == 0, f"en-dash={doc.count(chr(8211))}")
cjk = [c for c in doc if "\u4e00" <= c <= "\u9fff"]
cek("cjk_0", len(cjk) == 0, f"cjk={len(cjk)}")

# 2. Baris riset pendahuluan
empat = ["what-if-oracle", "consciousness-council",
         "scientific-critical-thinking", "verification-mandatory"]
cek("baris_riset_pendahuluan",
    any(l.startswith("Riset pendahuluan: what-if-oracle") for l in lines),
    "baris wajib")
for s in empat:
    cek(f"skill_disebut_{s}", s in doc, "")

# 3. sequ-mcp
m = re.search(r"sequentialthinking,\s*(\d+)\s*pikiran", doc)
cek("sequ_jumlah_pikiran", m is not None and int(m.group(1)) >= 3,
    m.group(0) if m else "tidak ditemukan")

# 4. Struktur bagian
secs = [l for l in lines if l.startswith("## ")]
cek("jumlah_bagian", len(secs) >= 12, f"{len(secs)} bagian")

# 5. Ringkasan lima baris (hanya sampai judul bagian berikutnya)
idx = next(i for i, l in enumerate(lines) if l.startswith("## 11. RINGKASAN"))
sisa = []
for l in lines[idx + 1:]:
    if l.startswith("## "):
        break
    sisa.append(l)
ringkas = [l for l in sisa if re.match(r"^\d\. ", l)]
cek("ringkasan_5_baris", len(ringkas) == 5, f"{len(ringkas)} baris")

# 6. Daftar belum terverifikasi
cek("daftar_belum_terverifikasi",
    any("DAFTAR YANG BELUM TERVERIFIKASI" in l for l in lines), "")

# 7. Bagian PM di ledger
cek("ledger_bagian_pm", "## Bagian PM" in led, "")
pm_rows = [l for l in led.splitlines() if re.match(r"^\| PM-\d{3} \|", l)]
ids = [re.match(r"^\| (PM-\d{3}) \|", l).group(1) for l in pm_rows]
cek("ledger_id_unik", len(ids) == len(set(ids)), f"{len(ids)} baris, {len(set(ids))} unik")
cek("ledger_id_berurutan",
    ids == [f"PM-{i:03d}" for i in range(1, len(ids) + 1)],
    f"pertama {ids[0]}, terakhir {ids[-1]}")

# 8. Tujuh kolom per baris
salah_kolom = []
for l in pm_rows:
    n = len([c for c in l.strip().strip("|").split("|")])
    if n != 7:
        salah_kolom.append((l[:14], n))
cek("ledger_tujuh_kolom", not salah_kolom, str(salah_kolom[:5]))

# 9. Tidak ada sel kosong
kosong = [l[:14] for l in pm_rows
          if any(not c.strip() for c in l.strip().strip("|").split("|"))]
cek("ledger_tanpa_sel_kosong", not kosong, str(kosong[:5]))

# 10. Setiap sitasi PM di dokumen ada di ledger, dan setiap baris tercakup
#     sitasi tunggal maupun rentang "PM-001 sampai PM-056".
sitasi = sorted(set(re.findall(r"PM-\d{3}", doc)))
hilang = [s for s in sitasi if s not in set(ids)]
cek("sitasi_pm_semua_ada", not hilang, f"hilang={hilang}")

tercakup = set(sitasi)
for a, b in re.findall(r"PM-(\d{3}) sampai PM-(\d{3})", doc):
    tercakup |= {f"PM-{i:03d}" for i in range(int(a), int(b) + 1)}
tak = sorted(set(ids) - tercakup)
cek("semua_baris_ledger_dipakai", not tak, f"tak_disitasi={tak}")

# 11. Komposisi kelas ledger lawan klaim dokumen
kelas = {}
for l in pm_rows:
    sel = [c.strip() for c in l.strip().strip("|").split("|")]
    kelas[sel[3]] = kelas.get(sel[3], 0) + 1
ratakan = re.sub(r"\s+", " ", doc)
klaim = re.search(
    r"Komposisi kelas: RUN-KITA (\d+) baris, JURNAL (\d+) baris, DERIVASI (\d+) baris, "
    r"KONVENSI (\d+) baris, BELUM-TERUKUR (\d+) baris", ratakan)
cek("klaim_komposisi_kelas_ada", klaim is not None, "")
if klaim:
    target = dict(zip(["RUN-KITA", "JURNAL", "DERIVASI", "KONVENSI", "BELUM-TERUKUR"],
                      [int(g) for g in klaim.groups()]))
    cek("komposisi_kelas_cocok", target == kelas,
        f"klaim={target} aktual={kelas}")

# 12. Klaim jumlah baris di dokumen
m = re.search(r"Bagian PM, (\d+) baris", doc)
cek("klaim_jumlah_baris",
    m is not None and int(m.group(1)) == len(pm_rows),
    f"klaim={m.group(1) if m else None} aktual={len(pm_rows)}")

# 13. Klaim jumlah baris kutipan
m = re.search(r"([A-Za-z ]+?) baris RUN-KITA berstatus kutipan", doc)
kutipan = [l for l in pm_rows if "TERUKUR (kutipan)" in l]
angka = {"sebelas": 11, "dua belas": 12, "tiga belas": 13, "sepuluh": 10,
         "sembilan": 9, "empat belas": 14}
kunci = " ".join(m.group(1).split()[-2:]).lower() if m else None
cek("klaim_baris_kutipan",
    kunci is not None and angka.get(kunci) == len(kutipan),
    f"klaim={kunci} aktual={len(kutipan)}")

# 14. Setiap angka di tabel tier punya minimal satu sitasi PM
tier = [l for l in lines if l.startswith("| ") and "PERINGATAN-BERPENGAWAS" in l]
tanpa = [l.split("|")[1].strip() for l in tier if not re.search(r"PM-\d{3}|EVAL_C", l)]
cek("tabel_tier_bersitasi", not tanpa, f"tanpa_sitasi={tanpa}")

# 15. DOI di dokumen
doi = re.findall(r"10\.\d{4,9}/[^\s|)]+", doc)
cek("doi_ada", len(doi) >= 8, f"{len(doi)} DOI unik={len(set(doi))}")
terlarang = {"10.1109/TII.2019.2950661", "10.2307/4615733"}
cek("doi_terlarang_tidak_dipakai", not (set(doi) & terlarang),
    str(set(doi) & terlarang))

# 16. Rekomendasi tidak boleh bersandar pada rujukan gagal
cek("tanpa_belum_terverifikasi_sebagai_dasar",
    "Tidak ada rekomendasi di dokumen ini yang bersandar pada rujukan berstatus belum terverifikasi"
    in doc, "")

# 17. Larangan bahasa
cek("tanpa_kata_lebih_baik_tanpa_baseline",
    doc.count("lebih baik") <= 3, f"{doc.count('lebih baik')} kemunculan")

# 18. JSON PM terbaca
pj = json.loads((WS / "scratch/rnd/pm/pm_ledger.json").read_text())
cek("pm_ledger_json_terbaca", isinstance(pj, (dict, list)), str(type(pj)))

gagal = [h for h in hasil if not h[1]]
for nama, ok, detail in hasil:
    print(("PASS " if ok else "FAIL ") + nama + ((" :: " + detail) if detail else ""))
print(f"\nTotal {len(hasil)} pemeriksaan, {len(gagal)} gagal")
sys.exit(1 if gagal else 0)
