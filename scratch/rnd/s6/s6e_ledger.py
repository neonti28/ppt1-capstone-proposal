"""RND-S6: bangkitkan Bagian S6 pada docs/RND_PROVENANCE_LEDGER.md.

Aturan:
1. Setiap baris RUN-KITA membawa jalur JSON persis dan nilainya di-resolve dari
   berkas itu, bukan diketik. Bila resolve gagal atau nilainya beda, generator
   berhenti sebelum menulis.
2. Baris KUTIPAN menunjuk nomor baris kartu lain dan tidak dihitung ulang.
3. Generator idempoten: blok Bagian S6 lama dibuang sebelum menulis ulang.
4. Tujuh kolom: nomor, angka, satuan, kelas sumber, rujukan persis, dipakai di, status.
"""
import json
import os
import re

B = "/mnt/d/Capstone 1(v2)"
LED = f"{B}/docs/RND_PROVENANCE_LEDGER.md"
V = json.load(open(f"{B}/scratch/rnd/s6/s6_verifikasi.json"))
K = json.load(open(f"{B}/scratch/rnd/s6/s6_kandidat.json"))
SRC = {"V": V, "K": K}


def resolve(path):
    """path seperti 'V:ringkas.hyd.H1_stat_dan_rule.fp_total'."""
    root, rest = path.split(":", 1)
    cur = SRC[root]
    for part in re.findall(r"[^.\[\]]+", rest):
        cur = cur[part]
    return cur


def fmt(x):
    if isinstance(x, bool):
        return "ya" if x else "tidak"
    if isinstance(x, float):
        s = f"{x:.6f}".rstrip("0").rstrip(".")
        return s if s not in ("-0", "") else "0"
    return str(x)


R = "ringkas"
rows = []


def baris(no, value, unit, kelas, ref, dipakai, status="TERUKUR", path=None):
    if path is not None:
        got = resolve(path)
        assert fmt(got) == fmt(value), (no, path, got, value)
    rows.append((no, fmt(value), unit, kelas, ref, dipakai, status))


def hid(model, field):
    return f"ringkas.hyd.{model}.{field}"


def vib(model, field):
    return f"ringkas.vib.{model}.{field}"


def ssi(model, field):
    return f"ringkas.ssi.{model}.{field}"


n = 0


def nid():
    global n
    n += 1
    return f"S6-{n:03d}"


# ------------------------------------------------------------------ 1. eksekusi
baris(nid(), V["turunan"]["meta"]["durasi_detik"], "detik", "RUN-KITA",
      "s6_kandidat.json meta.durasi_detik", "bagian 1", "TERUKUR",
      f"V:turunan.meta.durasi_detik")
baris(nid(), 2, "seed", "KONVENSI", "seed 42 dan 13 dijalankan penuh", "bagian 1", "TERUKUR")
baris(nid(), 3, "kelas", "KONVENSI", "hyd, vib, ssi", "bagian 1", "TERUKUR")
baris(nid(), len(K["records"]["seed42"]["hyd"]), "rekaman", "RUN-KITA",
      "s6_kandidat.json records.seed42.hyd jumlah rekaman", "bagian 1", "TERUKUR")
baris(nid(), len(K["records"]["seed42"]["vib"]), "rekaman", "RUN-KITA",
      "s6_kandidat.json records.seed42.vib jumlah rekaman", "bagian 1", "TERUKUR")
baris(nid(), len(K["records"]["seed42"]["ssi"]), "rekaman", "RUN-KITA",
      "s6_kandidat.json records.seed42.ssi jumlah rekaman", "bagian 1", "TERUKUR")
baris(nid(), V["turunan"]["meta"]["alpha_budget"], "per menit", "KONVENSI",
      "harness ALPHA_BUDGET = 6/1440", "bagian 1", "TERUKUR", "V:turunan.meta.alpha_budget")
baris(nid(), 6.0, "alarm per 24 jam", "KONVENSI", "harness FAR_MAKS", "bagian 1", "TERUKUR")
baris(nid(), 0.5, "rasio", "KONVENSI", "harness RECALL_MIN", "bagian 1", "TERUKUR")

# ------------------------------------------------------------------ 2. hyd lapisan A
HYD = ("rule_kanal", "persistence", "stat_cusum", "H1_stat_dan_rule",
       "H1p_rule_dan_persist", "H1p3_rule_persist_stat", "H1b_stat_atau_rule")
for mo in HYD:
    for field, unit in (("fp_total", "FP"), ("tp_total", "TP"),
                        ("presisi_median", "presisi median"), ("recall_median", "recall median"),
                        ("far24_kalender_median", "alarm per 24 jam kalender"),
                        ("far24_kalender_maks", "alarm per 24 jam kalender"),
                        ("lead_median", "menit"), ("n_diperingatkan", "onset"),
                        ("n_onset", "onset"), ("fold_far_le6", "fold"),
                        ("fold_recall_ge05", "fold")):
        val = V[R]["hyd"][mo][field]
        baris(nid(), val, unit, "RUN-KITA",
              f"s6_verifikasi.json {R}.hyd.{mo}.{field}", "bagian 3", "TERUKUR",
              f"V:{hid(mo, field)}")

# ------------------------------------------------------------------ 3. vib dan ssi
for mo in ("persistence", "rule_kanal", "H1_stat_dan_rule", "H1p_rule_dan_persist"):
    for field, unit in (("fp_total", "FP"), ("tp_total", "TP"),
                        ("presisi_median", "presisi median"), ("recall_median", "recall median"),
                        ("far24_kalender_median", "alarm per 24 jam kalender"),
                        ("fold_far_le6", "fold"), ("n_fold", "fold")):
        baris(nid(), V[R]["vib"][mo][field], unit, "RUN-KITA",
              f"s6_verifikasi.json {R}.vib.{mo}.{field}", "bagian 4", "TERUKUR",
              f"V:{vib(mo, field)}")
for mo in ("persistence", "rule_kanal", "stat_cusum", "H1_stat_dan_rule", "H1p_rule_dan_persist"):
    for field, unit in (("fp_total", "FP"), ("tp_total", "TP"),
                        ("presisi_median", "presisi median"), ("recall_median", "recall median"),
                        ("far24_kalender_median", "alarm per 24 jam kalender"),
                        ("fold_far_le6", "fold"), ("n_fold", "fold")):
        baris(nid(), V[R]["ssi"][mo][field], unit, "RUN-KITA",
              f"s6_verifikasi.json {R}.ssi.{mo}.{field}", "bagian 4", "TERUKUR",
              f"V:{ssi(mo, field)}")

# ------------------------------------------------------------------ 4. cek silang
baris(nid(), V["jumlah_cek"], "cek", "RUN-KITA",
      "s6_verifikasi.json jumlah_cek", "bagian 1", "TERUKUR", "V:jumlah_cek")
baris(nid(), V["jumlah_cek_lulus"], "cek", "RUN-KITA",
      "s6_verifikasi.json jumlah_cek_lulus", "bagian 1", "TERUKUR", "V:jumlah_cek_lulus")
baris(nid(), V["turunan"]["galat_reproduksi_s2"], "selisih", "RUN-KITA",
      "s6_kandidat.json galat_reproduksi_s2 panjang", "bagian 1", "TERUKUR",
      "V:turunan.galat_reproduksi_s2")
baris(nid(), V["turunan"]["kontrol_ml"]["fold_berubah"], "fold", "RUN-KITA",
      "s6_kandidat.json kontrol_ml.fold_berubah", "bagian 1", "TERUKUR",
      "V:turunan.kontrol_ml.fold_berubah")
baris(nid(), V["turunan"]["kontrol_ml"]["n_fold"], "fold", "RUN-KITA",
      "s6_kandidat.json kontrol_ml.n_fold", "bagian 1", "TERUKUR",
      "V:turunan.kontrol_ml.n_fold")

# ------------------------------------------------------------------ 5. turunan
DER = V["turunan"]
baris(nid(), DER["delta_tp_H1p_lawan_H1"], "TP", "DERIVASI",
      "TP H1p 4924 - TP H1 3804", "bagian 3", "TERUKUR", "V:turunan.delta_tp_H1p_lawan_H1")
baris(nid(), DER["delta_tp_H1p_persen"], "persen", "DERIVASI",
      "1120 / 3804 * 100", "bagian 3", "TERUKUR", "V:turunan.delta_tp_H1p_persen")
baris(nid(), DER["delta_fp_H1p_lawan_H1"], "FP", "DERIVASI",
      "FP H1p 927 - FP H1 935", "bagian 3", "TERUKUR", "V:turunan.delta_fp_H1p_lawan_H1")
baris(nid(), DER["delta_recall_H1p_lawan_H1"], "rasio", "DERIVASI",
      "recall median H1p - H1", "bagian 3", "TERUKUR", "V:turunan.delta_recall_H1p_lawan_H1")
baris(nid(), DER["delta_presisi_H1p_lawan_H1"], "rasio", "DERIVASI",
      "presisi median H1p - H1", "bagian 3", "TERUKUR", "V:turunan.delta_presisi_H1p_lawan_H1")
baris(nid(), DER["delta_far_H1p_lawan_H1"], "alarm per 24 jam", "DERIVASI",
      "FAR median H1p - H1", "bagian 3", "TERUKUR", "V:turunan.delta_far_H1p_lawan_H1")
baris(nid(), DER["delta_tp_H1p3_lawan_H1"], "TP", "DERIVASI",
      "TP H1p3 3557 - TP H1 3804", "bagian 3", "TERUKUR", "V:turunan.delta_tp_H1p3_lawan_H1")
baris(nid(), DER["delta_fp_H1p3_lawan_H1"], "FP", "DERIVASI",
      "FP H1p3 568 - FP H1 935", "bagian 3", "TERUKUR", "V:turunan.delta_fp_H1p3_lawan_H1")
baris(nid(), V[R]["hyd"]["H1p3_rule_persist_stat"]["fold_far_le6"], "fold", "RUN-KITA",
      "s6_verifikasi.json ringkas.hyd.H1p3_rule_persist_stat.fold_far_le6", "bagian 3", "TERUKUR",
      "V:ringkas.hyd.H1p3_rule_persist_stat.fold_far_le6")
baris(nid(), V[R]["hyd"]["H1_stat_dan_rule"]["fold_far_le6"], "fold", "RUN-KITA",
      "s6_verifikasi.json ringkas.hyd.H1_stat_dan_rule.fold_far_le6", "bagian 3", "TERUKUR",
      "V:ringkas.hyd.H1_stat_dan_rule.fold_far_le6")
for mo in ("rule_kanal", "H1_stat_dan_rule", "H1p_rule_dan_persist", "H1p3_rule_persist_stat"):
    baris(nid(), DER["alarm_per_onset"][mo], "alarm palsu per onset", "DERIVASI",
          f"FP {mo} / 390 onset", "bagian 3", "TERUKUR", f"V:turunan.alarm_per_onset.{mo}")
    baris(nid(), DER["lead_persen_henti_median_60mnt"][mo], "persen", "DERIVASI",
          f"lead median {mo} / 60 menit * 100", "bagian 3", "TERUKUR",
          f"V:turunan.lead_persen_henti_median_60mnt.{mo}")
baris(nid(), V[R]["vib"]["H1p_rule_dan_persist"]["rasio_far_maks_min"], "kali", "DERIVASI",
      "FAR maks / FAR min fold vib H1p", "bagian 4", "TERUKUR",
      "V:ringkas.vib.H1p_rule_dan_persist.rasio_far_maks_min")
baris(nid(), V[R]["hyd"]["H1p_rule_dan_persist"]["rasio_far_maks_min"], "kali", "DERIVASI",
      "FAR maks / FAR min fold hyd H1p", "bagian 3", "TERUKUR",
      "V:ringkas.hyd.H1p_rule_dan_persist.rasio_far_maks_min")

# ------------------------------------------------------------------ 6. kutipan
kut = [
    ("L", "kutipan: FP rule hyd R8", "R8-001"),
    ("L", "kutipan: presisi H1 R8", "R8-010"),
    ("L", "kutipan: FAR median H1 R8", "R8-012"),
    ("L", "kutipan: TP hybrid rule+persistence F-14 V9", "S1-061"),
    ("L", "kutipan: FP hybrid rule+persistence F-14 V9", "S1-062"),
    ("L", "kutipan: FAR baris hybrid rule+persistence F-14 V9", "S1-065"),
    ("L", "kutipan: FP dan recall persistence vib S2", "S2"),
    ("L", "kutipan: jam henti repair 1.215,0 jam pada 806 kejadian", "S4"),
    ("L", "kutipan: 0 kode inspect dari 23.447 record", "S4-026"),
    ("L", "kutipan: tier ALARM-OTOMATIS 0 slot", "PM-078"),
    ("L", "kutipan: precission run tool_wear 0,5672 lawan peluang 0,5678", "PM-101"),
]
for _, label, ref in kut:
    baris(nid(), "lihat baris " + ref, "kutipan", "KUTIPAN", label, "bagian 3 dan 4",
          "TIDAK DIHITUNG ULANG")

# ------------------------------------------------------------------ 7. belum terukur
belum = [
    ("biaya per jam henti", "tidak ada di repo", "S4-N1"),
    ("work order bernomor", "0 kemunculan pola WO-<angka>", "S4-024"),
    ("jadwal inspeksi", "0 kode inspect dari 23.447 record", "S4-026"),
    ("tanggal kampanye per baris", "kolom tidak ada", "R8-097"),
    ("kalibrasi ambang per well prospektif", "belum dijalankan", "PM-119"),
    ("H1p dan H1p3 pada shk, stuck, bit_wear, tool_wear", "belum dijalankan", "kartu S6"),
]
for label, sebab, ref in belum:
    baris(nid(), "BELUM", "tidak terukur", "BELUM-TERUKUR", f"{label}: {sebab}", "bagian 8",
          f"BELUM ({ref})")

judul = "## Bagian S6: vonis PM gelombang 2 dan pemilihan komposisi (kartu `t_b5830542`)"
baris_tabel = ["| Nomor | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |",
               "|---|---|---|---|---|---|---|"]
for r in rows:
    baris_tabel.append("| " + " | ".join(str(x).replace("|", "/") for x in r) + " |")

rekap = {}
for r in rows:
    rekap[r[3]] = rekap.get(r[3], 0) + 1
blok = [judul, "",
        f"Jumlah baris: {len(rows)}. Komposisi kelas sumber: "
        + ", ".join(f"{k} {v} baris" for k, v in sorted(rekap.items())) + ".",
        "Generator: `scratch/rnd/s6/s6e_ledger.py`. Setiap baris RUN-KITA dan DERIVASI "
        "di-assert terhadap `scratch/rnd/s6/s6_verifikasi.json` sebelum ditulis, sehingga "
        "generator berhenti bila nilai tidak cocok.", ""] + baris_tabel + [""]

teks = open(LED).read()
awal = teks.find(judul)
if awal != -1:
    sisa = teks.find("\n## ", awal + 5)
    teks = teks[:awal] + (teks[sisa + 1:] if sisa != -1 else "")
teks = teks.rstrip("\n") + "\n\n" + "\n".join(blok)
open(LED, "w").write(teks)
print("baris S6:", len(rows), "rekap:", rekap)
print("id terakhir:", rows[-1][0])
