#!/usr/bin/env python3
"""Generator blok ledger S2 (7 kolom, idempoten) dari artefak JSON.

Setiap baris memakai resolver jalur JSON, sehingga angka yang tidak ada di JSON
akan melempar KeyError dan generator berhenti. Blok lama dengan judul sama
dibuang lebih dulu supaya menjalankan ulang tidak menggandakan baris.
"""
from __future__ import annotations

import re

import s2_common as C

LEDGER = f"{C.BASE}/docs/RND_PROVENANCE_LEDGER.md"
JUDUL = "## Bagian S2: hybrid vib dan ssi (kartu `t_f52e1ecb`)"


def bangun():
    rec, ring, meta = C.muat()
    L = C.Ledger()

    # meta eksekusi
    L.angka_dari(meta, "durasi_detik", "detik", "RUN-KITA", "bagian 9", digit=1)
    L.angka_dari(meta, "panggil_harness_sinyal", "panggilan", "RUN-KITA", "bagian 9", bulat=True)
    L.angka_dari(meta, "min_pos_uji", "positif", "KONVENSI",
                 "bagian 1", bulat=True)
    L.angka_dari(meta, "far_maks", "alarm palsu per 24 jam kalender", "KONVENSI",
                 "bagian 1", digit=1)
    L.angka_dari(meta, "alpha_budget", "fraksi sampel", "KONVENSI", "bagian 1", digit=6)

    for kelas, kode in (("vib", "vib"), ("ssi", "ssi")):
        d = ring[kelas]
        p = kelas
        L.angka_dari(ring, f"{p}.n_baris", "baris", "RUN-KITA", "bagian 2", bulat=True)
        L.angka_dari(ring, f"{p}.n_well", "well", "RUN-KITA", "bagian 2", bulat=True)
        L.angka_dari(ring, f"{p}.n_fitur", "fitur", "RUN-KITA", "bagian 2", bulat=True)
        L.angka_dari(ring, f"{p}.n_fold_total", "fold", "RUN-KITA", "bagian 2", bulat=True)
        L.angka_dari(ring, f"{p}.n_fold_dapat_diuji", "fold", "RUN-KITA", "bagian 2", bulat=True)
        L.angka_dari(ring, f"{p}.n_fold_tidak_dapat_diuji", "fold", "RUN-KITA", "bagian 2", bulat=True)
        L.angka_dari(ring, f"{p}.n_pos_total_dapat_diuji", "baris positif", "RUN-KITA",
                     "bagian 2", bulat=True)

        # per fold
        for i, w in enumerate(d["wells"]):
            pw = f"{p}.wells.{i}"
            L.angka_dari(ring, f"{pw}.n", "baris", "RUN-KITA", "bagian 2", bulat=True)
            L.angka_dari(ring, f"{pw}.n_pos", "baris positif", "RUN-KITA", "bagian 2", bulat=True)
            L.angka_dari(ring, f"{pw}.menit_kalender", "menit kalender", "RUN-KITA",
                         "bagian 2", bulat=True)
            L.angka_dari(ring, f"{pw}.auc_kanal", "AUC", "RUN-KITA", "bagian 2")
            L.angka_dari(ring, f"{pw}.h_cusum", "ambang CUSUM", "RUN-KITA", "bagian 2", digit=1)
            L.angka_dari(ring, f"{pw}.auprc_ml", "AUPRC", "RUN-KITA", "bagian 2")
            L.angka_dari(ring, f"{pw}.auc_ml", "AUC", "RUN-KITA", "bagian 2")

        # agregat per model
        for m in C.MODEL_SEMUA:
            am = f"{p}.agregat.{m}"
            L.angka_dari(ring, f"{am}.recall_median", "fraksi", "RUN-KITA", "bagian 4")
            L.angka_dari(ring, f"{am}.precision_median", "fraksi", "RUN-KITA", "bagian 4")
            L.angka_dari(ring, f"{am}.far24_kalender_median", "alarm palsu per 24 jam kalender",
                         "RUN-KITA", "bagian 4")
            L.angka_dari(ring, f"{am}.far24_baris_median", "alarm palsu per 24 jam baris",
                         "RUN-KITA", "bagian 4")
            L.angka_dari(ring, f"{am}.fp_total", "baris", "RUN-KITA", "bagian 4", bulat=True)
            L.angka_dari(ring, f"{am}.fold_lolos_far_recall", "fold", "RUN-KITA",
                         "bagian 4", bulat=True)
            L.angka_dari(ring, f"{am}.cakupan_median", "fraksi", "RUN-KITA", "bagian 4")

        # kurva sensitivitas anggaran
        for b in C.BUDGET:
            for m in (f"ML_kalender_b{b}", f"stat_cusum_b{b}"):
                am = f"{p}.sensitivitas.{m}"
                L.angka_dari(ring, f"{am}.recall_median", "fraksi", "RUN-KITA", "bagian 4.3")
                L.angka_dari(ring, f"{am}.precision_median", "fraksi", "RUN-KITA", "bagian 4.3")
                L.angka_dari(ring, f"{am}.far24_kalender_median",
                             "alarm palsu per 24 jam kalender", "RUN-KITA", "bagian 4.3")

        # perbandingan hybrid lawan single
        bd = f"{p}.banding_hybrid_lawan_single"
        L.angka_dari(ring, f"{bd}.delta_recall_median", "selisih fraksi", "DERIVASI", "bagian 5")
        L.angka_dari(ring, f"{bd}.delta_precision_median", "selisih fraksi", "DERIVASI", "bagian 5")
        L.angka_dari(ring, f"{bd}.rasio_far_median", "rasio", "DERIVASI", "bagian 5")
        L.angka_dari(ring, f"{bd}.delta_fold_lolos", "fold", "DERIVASI", "bagian 5", bulat=True)

        # lapisan C: separuh waktu
        for m in C.MODEL_SEMUA:
            sp = f"{p}.lapisan_c_separuh.{m}"
            L.angka_dari(ring, f"{sp}.recall_awal_median", "fraksi", "RUN-KITA", "bagian 6.1")
            L.angka_dari(ring, f"{sp}.recall_akhir_median", "fraksi", "RUN-KITA", "bagian 6.1")
            L.angka_dari(ring, f"{sp}.n_fold_menurun", "fold", "RUN-KITA", "bagian 6.1", bulat=True)

        # lapisan C: variasi seed
        for i, sv in enumerate(d["variasi_seed_ml"]):
            ps = f"{p}.variasi_seed_ml.{i}"
            L.angka_dari(ring, f"{ps}.delta_fp", "baris", "RUN-KITA", "bagian 6.2", bulat=True)
            L.angka_dari(ring, f"{ps}.delta_tp", "baris", "RUN-KITA", "bagian 6.2", bulat=True)
            L.angka_dari(ring, f"{ps}.delta_recall", "selisih fraksi", "RUN-KITA", "bagian 6.2")

    # justifikasi ambang positif (Wilson)
    for i, j in enumerate(ring["justifikasi_ambang_positif"]):
        if j["n_pos"] in (3, 12, 30, 31):
            L.angka_dari(ring, f"justifikasi_ambang_positif.{i}.lebar_penuh", "lebar selang",
                         "DERIVASI", "bagian 2.3")
            L.angka_dari(ring, f"justifikasi_ambang_positif.{i}.wilson_recall_0.hi",
                         "batas atas selang saat recall 0", "DERIVASI", "bagian 2.3")
            L.angka_dari(ring, f"justifikasi_ambang_positif.{i}.wilson_recall_penuh.lo",
                         "batas bawah selang saat recall 1", "DERIVASI", "bagian 2.3")

    # konstanta dan ambang kebijakan yang dikutip dokumen
    L.tambah("32,17405", "ft/s2", "STANDAR", "API RP 7G (nilai 1 g)", "bagian 2.4")
    L.tambah("0,50", "fraksi recall minimum gate", "KONVENSI",
             "`docs/RND_EVALUATION_POLICY.md` bagian gate A", "bagian 4")
    L.tambah("0,50", "fraksi cakupan minimum gate", "KONVENSI",
             "`code/rnd_hybrid_harness.py` ambang cakupan", "bagian 6.3")
    L.tambah(C.fd(1 - meta["alpha_budget"], 6), "kuantil conformal", "DERIVASI",
             "`1 - alpha_budget` pada `s2_meta.json`", "bagian 3")

    # angka turunan yang dikutip narasi
    p_gate = ring["ssi"]["sensitivitas"]["ML_kalender_b24"]["precision_median"]
    L.tambah(C.fd((1 - p_gate) / p_gate, 1), "alarm palsu per alarm benar", "DERIVASI",
             "`(1-p)/p` dengan p = `ssi.sensitivitas.ML_kalender_b24.precision_median`", "bagian 4.3")
    L.tambah(C.fd(ring["vib"]["agregat"]["persistence"]["far24_kalender_median"] / meta["far_maks"], 2),
             "rasio FAR terhadap gate", "DERIVASI",
             "`vib.agregat.persistence.far24_kalender_median / meta.far_maks`", "bagian 4.1")
    for kelas in ("vib", "ssi"):
        L.angka_dari(ring, f"{kelas}.agregat.persistence.lead_median",
                     "menit terhadap onset label", "RUN-KITA", "bagian 7", digit=2)
        L.angka_dari(ring, f"{kelas}.agregat.persistence.n_onset", "jendela onset", "RUN-KITA",
                     "bagian 2.1", bulat=True)
    L.tambah("10", "menit penahanan alarm", "KONVENSI",
             "`W_JENDELA` pada `code/rnd_hybrid_harness.py`", "bagian 2.1")
    L.tambah("60", "menit horizon peringatan", "KONVENSI",
             "`LEAD_HORIZON` pada `code/rnd_hybrid_harness.py`", "bagian 2.1")
    return L


def tulis(L):
    blok = "\n".join([
        JUDUL, "",
        "Kartu: `t_f52e1ecb` · Board: `rnd-algo-2026` · Tanggal: 2026-10-28 (WIB)",
        f"Workspace: `{C.BASE}` · Dokumen pendamping: `docs/RND_S2_HYBRID_VIB_SSI.md`",
        "",
        "Sumber angka: `scratch/rnd/s2/s2_records_vib.json`, `s2_records_ssi.json`, "
        "`s2_ringkas.json`, `s2_meta.json`. Generator: `scratch/rnd/s2/s2c_ledger.py` "
        f"(idempoten, {len(L.baris)} baris).",
        "",
        "Riset pendahuluan: verification-mandatory (setiap baris memakai resolver jalur JSON, "
        "sehingga angka yang tidak ada di artefak melempar KeyError dan generator berhenti; "
        "blok lama dibuang sebelum menulis supaya idempoten).",
        "",
        L.markdown(),
        "",
    ])
    teks = open(LEDGER, encoding="utf-8").read()
    if JUDUL in teks:
        teks = re.sub(re.escape(JUDUL) + r".*?(?=\n## |\Z)", "", teks, flags=re.S)
    # buang sisa baris S2 dari percobaan sebelumnya yang tidak berjudul dan memakai
    # 8 kolom (salah format) serta merujuk artefak yang sudah dibatalkan
    teks = "\n".join(l for l in teks.split("\n") if not l.startswith("| S2-"))
    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write(teks.rstrip("\n") + "\n\n" + blok)
    return len(L.baris)


def main():
    L = bangun()
    n = tulis(L)
    print(f"ledger S2: {n} baris ditulis ke {LEDGER}")
    print("kode pertama:", L.baris[0]["kode"], "terakhir:", L.baris[-1]["kode"])


if __name__ == "__main__":
    main()
