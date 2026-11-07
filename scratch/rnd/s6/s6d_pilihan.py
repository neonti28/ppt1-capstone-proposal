"""RND-S6: bangun scratch/rnd/s6/pilihan.json dari s6_verifikasi.json.

Aturan:
1. Semua angka hasil S6 diambil dari s6_verifikasi.json lewat fungsi m(), tidak diketik.
2. Nomor baris ledger dicari dari docs/RND_PROVENANCE_LEDGER.md berdasarkan teks
   rujukan, sehingga tidak ada nomor yang dikarang. Bila tidak ketemu, berhenti.
3. Angka kartu lain masuk kelompok kutipan dengan nomor baris sumbernya.
4. Tier hanya ditulis sebagai usulan dan wajib persetujuan user.
"""
import json
import re

B = "/mnt/d/Capstone 1(v2)"
V = json.load(open(f"{B}/scratch/rnd/s6/s6_verifikasi.json"))
OUT = f"{B}/scratch/rnd/s6/pilihan.json"
LED = f"{B}/docs/RND_PROVENANCE_LEDGER.md"
R, DER = V["ringkas"], V["turunan"]

# --------------------------------------------------------------- indeks ledger
LED_ROWS = []
for line in open(LED):
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) == 7 and re.fullmatch(r"S6-\d{3}", c[0]):
        LED_ROWS.append(dict(id=c[0], angka=c[1], satuan=c[2], kelas=c[3], ref=c[4],
                             dipakai=c[5], status=c[6]))


def ids_for(*subs, batas=4):
    """Cari nomor baris S6 yang rujukannya memuat semua substring (case sensitive)."""
    out = []
    for r in LED_ROWS:
        if all(s in r["ref"] for s in subs):
            out.append(r["id"])
        if len(out) >= batas:
            break
    assert out, ("tidak ada baris ledger untuk", subs)
    return out


def m(kelas, model, key):
    return R[kelas][model][key]


def bagian_A(kelas, model):
    return dict(fp_total=m(kelas, model, "fp_total"), tp_total=m(kelas, model, "tp_total"),
                presisi_median=m(kelas, model, "presisi_median"),
                recall_median=m(kelas, model, "recall_median"),
                recall_min_fold=m(kelas, model, "recall_min"),
                far24_kalender_median=m(kelas, model, "far24_kalender_median"),
                far24_kalender_maks=m(kelas, model, "far24_kalender_maks"),
                fold_far_le6=m(kelas, model, "fold_far_le6"),
                fold_recall_ge05=m(kelas, model, "fold_recall_ge05"),
                fold_gate_A=m(kelas, model, "fold_gate_A"),
                n_fold=m(kelas, model, "n_fold"))


def bagian_B(kelas, model):
    return dict(lead_median_menit=m(kelas, model, "lead_median"),
                n_diperingatkan=m(kelas, model, "n_diperingatkan"),
                n_onset=m(kelas, model, "n_onset"),
                alarm_palsu_per_onset=round(m(kelas, model, "fp_total") / m(kelas, model, "n_onset"), 4),
                lead_persen_dari_henti_median_60menit=round(100.0 * m(kelas, model, "lead_median") / 60.0, 2),
                catatan="nilai uang, jam orang, dan pengurangan inspeksi BELUM TERUKUR (S4: biaya, work order, jadwal tidak ada)")


def bagian_C(kelas, model):
    return dict(cakupan_median=m(kelas, model, "cakupan_median"),
                rasio_far_maks_min=m(kelas, model, "rasio_far_maks_min"),
                fold_paruh_kedua_positif=m(kelas, model, "fold_paruh_dua_positif"),
                fold_recall_positif=m(kelas, model, "fold_recall_positive"),
                n_fold=m(kelas, model, "n_fold"),
                catatan="kestabilan lintas kampanye BELUM TERUKUR karena tanggal kampanye tidak ada per baris")


def kandidat(kelas, tugas, model, asal, batas, bukti, *cari):
    return dict(kelas=kelas, tugas=tugas, kandidat=model, asal=asal,
                lapisan_A=bagian_A(kelas, model), lapisan_B=bagian_B(kelas, model),
                lapisan_C=bagian_C(kelas, model), batas_pakai=batas,
                kekuatan_bukti=bukti, ledger=ids_for(*cari),
                ledger_tambahan=[r["id"] for r in LED_ROWS if r["kelas"] == "KUTIPAN"][:0])


tabel = [
    kandidat("hyd", "K-i peringatan dini", "rule_kanal", "pra-riset (V9 rule_display, L1)",
             "ambang global tidak portabel, FAR menyebar antar well", "TERUKUR, 9 fold x 2 seed",
             "ringkas.hyd.rule_kanal"),
    kandidat("hyd", "K-i peringatan dini", "persistence", "pra-riset (V9 persistence, L0)",
             "konfirmasi status, RF dilarang di kelas ini", "TERUKUR, 9 fold x 2 seed",
             "ringkas.hyd.persistence"),
    kandidat("hyd", "K-i peringatan dini", "H1_stat_dan_rule", "pasca-riset (R8 H1, diadopsi PM A-1)",
             "bukan untuk mode cakupan penuh", "TERUKUR, direproduksi tepat dari R8",
             "ringkas.hyd.H1_stat_dan_rule"),
    kandidat("hyd", "K-i peringatan dini", "H1p_rule_dan_persist",
             "hybrid formula pra-riset V9 D-A3, diuji ulang S6 di 9 fold",
             "butuh riwayat y_prev 10 menit yang lengkap", "TERUKUR, menang di 9 dari 9 fold untuk recall",
             "ringkas.hyd.H1p_rule_dan_persist"),
    kandidat("hyd", "K-i peringatan dini", "H1p3_rule_persist_stat",
             "baru, tiga komponen hasil S6", "CUSUM tetap tersaturasi h=30",
             "TERUKUR, satu-satunya komposisi dengan FAR di bawah 6 pada 9 dari 9 fold",
             "ringkas.hyd.H1p3_rule_persist_stat"),
    kandidat("hyd", "K-i peringatan dini", "H1b_stat_atau_rule", "pasca-riset (pembanding cakupan)",
             "FAR median 14,7156", "TERUKUR, tidak dipilih", "ringkas.hyd.H1b_stat_atau_rule"),
    kandidat("vib", "K-i deteksi kondisi", "persistence", "pra-riset (V9 persistence, L0)",
             "recall tertinggi, FAR 22,0218 per 24 jam", "TERUKUR, 4 fold, cocok S2",
             "ringkas.vib.persistence"),
    kandidat("vib", "K-i deteksi kondisi", "rule_kanal", "pra-riset (V9 rule_display, L1)",
             "presisi 0,4856, FAR 37,3627", "TERUKUR, 4 fold, cocok S2", "ringkas.vib.rule_kanal"),
    kandidat("vib", "K-i deteksi kondisi", "H1_stat_dan_rule", "pasca-riset (S2)",
             "kalah dari persistence pada tiga sumbu", "TERUKUR, 4 fold, cocok S2",
             "ringkas.vib.H1_stat_dan_rule"),
    kandidat("vib", "K-i deteksi kondisi", "H1p_rule_dan_persist",
             "hybrid formula pra-riset V9 D-A3, diuji ulang S6",
             "recall 0,1906, hanya layak peringatan hemat", "TERUKUR, presisi dan FAR terbaik di kelas ini",
             "ringkas.vib.H1p_rule_dan_persist"),
    kandidat("ssi", "K-i deteksi kondisi", "persistence", "pra-riset (V9 persistence)",
             "presisi median 0,0940", "TERUKUR, 9 fold, cocok S2 pada 7 fold uji",
             "ringkas.ssi.persistence"),
    kandidat("ssi", "K-i deteksi kondisi", "rule_kanal", "pra-riset (V9 rule_display)",
             "recall median 0,0000", "TERUKUR, 9 fold", "ringkas.ssi.rule_kanal"),
    kandidat("ssi", "K-i deteksi kondisi", "stat_cusum", "pra-riset dan pasca-riset sama",
             "presisi median 0,0153", "TERUKUR, 9 fold", "ringkas.ssi.stat_cusum"),
    kandidat("ssi", "K-i deteksi kondisi", "H1_stat_dan_rule", "pasca-riset (S2)",
             "gerbang DAN tertutup", "TERUKUR, 9 fold", "ringkas.ssi.H1_stat_dan_rule"),
    kandidat("ssi", "K-i deteksi kondisi", "H1p_rule_dan_persist",
             "hybrid formula pra-riset V9 D-A3, diuji ulang S6",
             "1 TP dari 132 onset, praktis mati", "TERUKUR, hasil menolak",
             "ringkas.ssi.H1p_rule_dan_persist"),
]

kutipan = [
    dict(kelas="shk", tugas="K-i status", kandidat="ML LightGBM single",
         angka=dict(AUPRC=0.0499, prevalensi=0.024311, recall_median=0.0829, fp=2633, tp=192),
         sumber="R8 bagian 5.1", catatan="tidak diuji ulang di S6"),
    dict(kelas="shk", tugas="K-i status", kandidat="H2 ML dan statistik",
         angka=dict(fp=667, tp=46, recall_median=0.0037), sumber="R8 bagian 2",
         catatan="ditolak PM, TP turun 76,04 persen"),
    dict(kelas="stuck", tugas="K-ii onset", kandidat="H4 tiga komponen",
         angka=dict(fp=41, tp=17, presisi_median=0.6404, recall_median=0.001,
                    onset_diperingatkan=13, onset_total=148), sumber="R8 bagian 7",
         catatan="verifikasi manual bertarget, bukan alarm"),
    dict(kelas="tool_wear", tugas="K-i perubahan regime", kandidat="op_far_calibrated",
         angka=dict(fp_r01="1-3 per alat", tlead_detik="20-36", presisi_run=0.5672,
                    peluang_kebetulan=0.5678), sumber="R8 dan PM-101",
         catatan="presisi run praktis sama dengan peluang kebetulan"),
    dict(kelas="bit_wear", tugas="K-1 status", kandidat="persistence",
         angka=dict(auprc="0,119-0,984", far_waktu="tidak sah, grid kedalaman"), sumber="V9 dan PM",
         catatan="tidak ada identitas bit dan run, K-2 belum dijalankan"),
]

pilihan = {
    "hyd": dict(
        tugas="K-i peringatan dini",
        pilihan="H1p_rule_dan_persist sebagai mode peringatan utama, H1p3_rule_persist_stat sebagai titik operasi tenang, rule kanal tetap untuk cakupan penuh",
        alasan=dict(
            recall_median_H1p=m("hyd", "H1p_rule_dan_persist", "recall_median"),
            recall_min_fold_H1p=m("hyd", "H1p_rule_dan_persist", "recall_min"),
            fold_recall_ge05_H1p=m("hyd", "H1p_rule_dan_persist", "fold_recall_ge05"),
            presisi_median_H1p=m("hyd", "H1p_rule_dan_persist", "presisi_median"),
            fold_far_le6_H1p=m("hyd", "H1p_rule_dan_persist", "fold_far_le6"),
            fold_far_le6_H1p3=m("hyd", "H1p3_rule_persist_stat", "fold_far_le6"),
            recall_median_H1p3=m("hyd", "H1p3_rule_persist_stat", "recall_median"),
            presisi_median_H1p3=m("hyd", "H1p3_rule_persist_stat", "presisi_median"),
            delta_tp_H1p_lawan_H1=DER["delta_tp_H1p_lawan_H1"],
            delta_tp_persen=DER["delta_tp_H1p_persen"],
            delta_fp_H1p_lawan_H1=DER["delta_fp_H1p_lawan_H1"],
            delta_far_H1p_lawan_H1=DER["delta_far_H1p_lawan_H1"]),
        yang_dikorbankan="lead median H1p 8,0 menit lawan H1 11,5 menit, dan FAR median H1p 4,0984 lawan 3,5302",
        catatan="H1 tidak lagi pilihan pertama, tetapi tetap dicatat sebagai titik operasi pembanding"),
    "vib": dict(
        tugas="K-i deteksi kondisi",
        pilihan="rule kanal tetap status, H1p sebagai peringatan hemat, persistence tetap pembanding cakupan",
        alasan=dict(
            presisi_H1p=m("vib", "H1p_rule_dan_persist", "presisi_median"),
            far_median_H1p=m("vib", "H1p_rule_dan_persist", "far24_kalender_median"),
            fp_H1p=m("vib", "H1p_rule_dan_persist", "fp_total"),
            fp_rule=m("vib", "rule_kanal", "fp_total"),
            fp_persistence=m("vib", "persistence", "fp_total"),
            recall_H1p=m("vib", "H1p_rule_dan_persist", "recall_median"),
            recall_persistence=m("vib", "persistence", "recall_median")),
        yang_dikorbankan="recall 0,1906 lawan persistence 0,7405, jadi H1p bukan pengganti cakupan",
        catatan="ini perbaikan beban alarm, bukan perbaikan deteksi"),
    "ssi": dict(
        tugas="K-i deteksi kondisi",
        pilihan="persistence dan ML tetap untuk pemantauan tren, hybrid rule dan persistence ditolak",
        alasan=dict(tp_H1p=m("ssi", "H1p_rule_dan_persist", "tp_total"),
                    fp_H1p=m("ssi", "H1p_rule_dan_persist", "fp_total"),
                    n_onset=m("ssi", "H1p_rule_dan_persist", "n_onset"),
                    tp_H1=m("ssi", "H1_stat_dan_rule", "tp_total"),
                    fp_persistence=m("ssi", "persistence", "fp_total"),
                    presisi_persistence=m("ssi", "persistence", "presisi_median")),
        yang_dikorbankan="tidak ada, karena kandidat yang diuji gagal",
        catatan="hasil negatif, bukan penundaan"),
    "shk": dict(tugas="K-i status", pilihan="tidak berubah dari PM: ML single untuk tren, rule untuk peringatan",
                alasan={}, yang_dikorbankan="-",
                catatan="H1p belum diuji di kelas ini, jadi tidak boleh diklaim menang atau kalah"),
    "stuck": dict(tugas="K-i dan K-ii", pilihan="tidak berubah dari PM: rule status untuk K-i, triase manual untuk K-ii",
                  alasan={}, yang_dikorbankan="-",
                  catatan="H1p untuk K-ii belum diuji dan onset punya definisi berbeda"),
    "tool_wear": dict(tugas="K-i perubahan regime",
                      pilihan="tidak berubah dari PM: op_far_calibrated untuk peringatan alat dikenal",
                      alasan={}, yang_dikorbankan="-",
                      catatan="H1p belum diuji, data toolwear_windows.csv tersedia"),
    "bit_wear": dict(tugas="K-1 status", pilihan="tidak berubah dari PM: persistence sebagai ranking",
                     alasan={}, yang_dikorbankan="-",
                     catatan="FAR waktu tidak sah karena baris berupa grid kedalaman"),
}

usulan_tier = [
    dict(engine="hyd K-i peringatan dini", tier_sekarang="PERINGATAN-BERPENGAWAS",
         usulan="tier tetap, engine H1 diganti H1p",
         alasan="recall median 0,6519 dan presisi 0,8243 pada FP 927 lawan 935",
         syarat="persetujuan user, bukti lintas seed sudah ada dua seed dengan nol selisih",
         status="USULAN, bukan keputusan"),
    dict(engine="hyd K-i titik operasi tenang", tier_sekarang="PERINGATAN-BERPENGAWAS",
         usulan="titik operasi kedua H1p3, bukan tier baru",
         alasan="FAR di bawah 6 pada 9 dari 9 fold, recall median 0,5296",
         syarat="persetujuan user, dan penerimaan bahwa empat fold di bawah recall 0,5",
         status="USULAN, bukan keputusan"),
    dict(engine="vib", tier_sekarang="rule_display PERINGATAN-BERPENGAWAS, rf TREN",
         usulan="tier tetap, tambah H1p sebagai peringatan hemat bertier TREN",
         alasan="presisi 0,8615 dan FAR median 1,4934, tetapi recall 0,1906",
         syarat="persetujuan user, kalibrasi per well belum ada",
         status="USULAN, bukan keputusan"),
    dict(engine="ssi", tier_sekarang="hybrid rule dan persistence PERINGATAN-BERPENGAWAS",
         usulan="tier tetap, hybrid rule dan persistence dihapus dari kandidat aktif",
         alasan="H1p ssi hanya 1 TP dari 132 onset",
         syarat="persetujuan user untuk mengubah registry",
         status="USULAN, bukan keputusan"),
    dict(engine="semua kelas", tier_sekarang="ALARM-OTOMATIS 0 slot", usulan="tetap 0 slot",
         alasan="syarat EVAL_C bagian 4 belum dipenuhi kelas mana pun", syarat="-",
         status="TIDAK ADA USULAN KENAIKAN"),
]

kandidat_baru = [
    dict(nama="H1p_rule_dan_persist", status="SUDAH DIJALANKAN pada hyd, vib, ssi",
         hasil="hyd menang, vib hemat alarm, ssi gagal",
         biaya_uji="nol tambahan, termasuk dalam 170,4 detik untuk 3 kelas x 2 seed",
         syarat_data="kolom y_prev_<kelas> dan riwayat 10 menit"),
    dict(nama="H1p3_rule_persist_stat", status="SUDAH DIJALANKAN pada hyd",
         hasil="satu-satunya komposisi dengan 9 dari 9 fold FAR di bawah 6",
         biaya_uji="nol tambahan, termasuk 170,4 detik",
         syarat_data="ketiga sinyal tersedia, CUSUM tetap tersaturasi"),
    dict(nama="H1p dan H1p3 pada shk, stuck K-i, bit_wear, tool_wear",
         status="BELUM DIJALANKAN, diusulkan gelombang 3", hasil="belum ada, dilarang diklaim",
         biaya_uji="ESTIMASI 80 sampai 300 detik per kelas per seed, diukur dari 170,4 detik untuk 3 kelas x 2 seed",
         syarat_data="shk.csv.gz dan lowo_shk.json, stuck_k1.csv.gz dan lowo_stuck_k1.json, USROP_labeled.csv, toolwear_windows.csv, semuanya ada"),
]

tidak_boleh = [
    "H1p menang di semua kelas. Yang terukur: menang di hyd, menghemat alarm di vib, gagal di ssi.",
    "Alarm otomatis siap untuk kelas mana pun.",
    "Nilai rupiah atau jam henti yang dihemat.",
    "Pengurangan pemeriksaan fisik per shift.",
    "Kestabilan lintas kampanye pengeboran.",
    "H1p3 sudah divalidasi di kelas selain hyd.",
    "Kelas vib punya engine dengan FAR di bawah 6 pada semua fold. Yang terukur 3 dari 4 fold.",
    "Angka ssi S6 sama penyebutnya dengan S2, karena S6 memakai 9 fold dan S2 memakai 7 fold yang dapat diuji.",
    "H1p3 menggantikan H1 pada semua sumbu. H1p3 menurunkan TP 247 dan recall median 0,0342.",
]

belum_terukur = [
    dict(apa="lapisan B dalam rupiah, jam henti terhindar, jam orang",
         sebab="biaya, work order, dan jadwal inspeksi tidak ada di repo", bukti="S4-N1, S4-N2, S4-N3"),
    dict(apa="rasio alarm per inspeksi", sebab="penyebut jadwal inspeksi tidak ada",
         bukti="0 dari 23.447 record berkode inspect"),
    dict(apa="kestabilan lintas kampanye", sebab="tanggal kampanye tidak ada per baris", bukti="R8-097"),
    dict(apa="kalibrasi ambang per well prospektif", sebab="belum pernah dijalankan", bukti="PM-119"),
    dict(apa="H1p dan H1p3 pada shk, stuck, bit_wear, tool_wear", sebab="belum dijalankan",
         bukti="tidak ada artefak"),
    dict(apa="pengaruh well kalibrasi tunggal", sebab="belum diuji kalibrasi bergilir",
         bukti="S1 bagian 6.4"),
]

roadmap3 = [
    dict(pekerjaan="uji H1p dan H1p3 pada shk K-i",
         data="scratch/v9_d1/datasets/shk.csv.gz dan scratch/v9_d1/lowo_shk.json",
         biaya="ESTIMASI 80 sampai 200 detik per seed",
         gate="FAR dan recall dilaporkan berpasangan pada titik operasi yang sama"),
    dict(pekerjaan="uji H1p pada stuck K-i status",
         data="scratch/v9_d1/datasets/stuck_k1.csv.gz dan lowo_stuck_k1.json",
         biaya="ESTIMASI 80 sampai 200 detik per seed",
         gate="presisi dan cakupan per well, cakupan kini hanya 2 well"),
    dict(pekerjaan="uji H1p pada bit_wear K-1 tanpa metrik waktu",
         data="data/USROP_labeled.csv", biaya="ESTIMASI 120 sampai 300 detik per seed",
         gate="tanpa FAR per 24 jam karena baris berupa grid kedalaman"),
    dict(pekerjaan="uji H1p pada tool_wear K-i",
         data="scratch/v6_e1/toolwear_windows.csv", biaya="ESTIMASI 60 sampai 120 detik per seed",
         gate="leave-one-tool-out empat alat, lapisan B tetap belum terukur"),
    dict(pekerjaan="kalibrasi grid CUSUM diperluas untuk vib dan ssi",
         data="dataset yang sama tanpa data baru", biaya="ESTIMASI 100 sampai 250 detik per kelas",
         gate="hasil dilaporkan sebagai titik operasi, bukan kenaikan tier"),
    dict(pekerjaan="kalibrasi bergilir well kalibrasi",
         data="fold yang sama", biaya="ESTIMASI 9 kali jalannya per kelas",
         gate="menjawab keberatan satu well kalibrasi"),
]

meta = dict(kartu="RND-S6", judul="vonis PM gelombang 2 dan pemilihan komposisi terbaik",
            waktu=V["waktu"], harness=f"{B}/code/rnd_hybrid_harness.py", seed=[42, 13],
            alpha_budget=DER["meta"]["alpha_budget"], far_maks=6.0, recall_min=0.5,
            sumber_angka="scratch/rnd/s6/s6_kandidat.json lewat s6_verifikasi.json",
            pemeriksaan_terbit=dict(jumlah=V["jumlah_cek"], lulus=V["jumlah_cek_lulus"]),
            kebijakan="docs/RND_EVALUATION_POLICY.md", baris_ledger_s6=len(LED_ROWS))

json.dump(dict(meta=meta, tabel_perbandingan=tabel, kutipan_kartu_lain=kutipan,
               pilihan_per_kelas=pilihan, usulan_tier=usulan_tier,
               kandidat_baru=kandidat_baru, tidak_boleh_diklaim=tidak_boleh,
               belum_terukur=belum_terukur, roadmap_gelombang_3=roadmap3),
          open(OUT, "w"), indent=1)
print("tulis", OUT, "baris tabel", len(tabel), "kutipan", len(kutipan), "ledger S6", len(LED_ROWS))
for t in tabel:
    print(t["kelas"], t["kandidat"], t["ledger"])
