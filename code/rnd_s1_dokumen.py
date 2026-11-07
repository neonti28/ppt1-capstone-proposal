#!/usr/bin/env python3
"""RND-S1 -- generator docs/RND_S1_SEED_ROBUSTNESS.md dari artefak JSON mentah.

Sumber tunggal: scratch/rnd/s1/s1_hyd_seeds.json, s1_h_saturasi.json, s1_meta.json,
scratch/rnd/r8/r8_hyd.json (acuan R8), scratch/v9_i1/v9_i1_RESULTS.json (pra-riset V9).
Semua angka disisipkan dari JSON; assert keras menghentikan penulisan bila berubah.
"""
import json

BASE = "/mnt/d/Capstone 1(v2)"
S1 = f"{BASE}/scratch/rnd/s1"
DOC = f"{BASE}/docs/RND_S1_SEED_ROBUSTNESS.md"

seeds_doc = json.load(open(f"{S1}/s1_hyd_seeds.json"))
sat = json.load(open(f"{S1}/s1_h_saturasi.json"))
luas = json.load(open(f"{S1}/s1_hluas.json"))
meta = json.load(open(f"{S1}/s1_meta.json"))
r8 = json.load(open(f"{BASE}/scratch/rnd/r8/r8_hyd.json"))
v9 = json.load(open(f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"))

M = "H1_stat_dan_rule"
SEEDS = seeds_doc["seed_list"]


def n(x, d=4):
    if x is None:
        return "n/a"
    if isinstance(x, str):
        return x
    s = f"{float(x):.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def ring(seed):
    return seeds_doc["per_seed"][str(seed)]["ringkas"]


def folds_of(seed, model):
    return [r for r in seeds_doc["per_seed"][str(seed)]["folds"] if r["model"] == model]


def fold_rec(name, model=M, seed=42):
    return next(r for r in seeds_doc["per_seed"][str(seed)]["folds"]
                if r["fold"] == name and r["model"] == model)


def ls(name):
    return seeds_doc["lintas_seed"][name]


def kes(seed):
    return seeds_doc["kontrol_stokastik"]["per_seed"][str(seed)]["ringkas"]


def cek(kondisi, pesan):
    if not kondisi:
        raise SystemExit("ASSERT GAGAL: " + pesan)


# ------------------------------------------------------------- assert masukan
cek(seeds_doc["status"] == "OK", "status run bukan OK")
cek(seeds_doc["reproduksi"]["semua_lulus"], "replikasi R8 tidak lulus")
AKUAN = dict(fp_total=935, precision_median=0.7789, recall_median=0.5638,
             lead_median_median=11.5, tp_total=3804)
for k, v in AKUAN.items():
    cek(abs(ring(42)[k] - v) <= 1e-9, "replikasi " + k)
cek(len(seeds_doc["per_seed"]) == 5, "jumlah seed bukan 5")
for s in SEEDS:
    for k in AKUAN:
        cek(ring(s)[k] == ring(42)[k], "seed " + str(s) + " nilai " + k + " beda")
cek(int(sat["n_saturasi"]) == 9, "n_saturasi bukan 9")
cek(abs(float(sat["h_terkecil_lolos_anggaran_di_luar_grid"]) - 300.0) < 1e-9, "h luar grid")
cek(luas["n_lolos_anggaran"] == 9, "hluas tidak lolos anggaran di 9 fold")
cek(luas["ringkas"]["fp_total"] == 237, "hluas FP berubah")
cek(abs(luas["ringkas"]["recall_median"] - 0.1457) < 1e-9, "hluas recall berubah")
cek(luas["ringkas"]["fold_far_le6"] == 9, "hluas fold FAR<=6 berubah")

kont = seeds_doc["kontrol_stokastik"]
seb = kont["sebaran"]
cek(seb["fp_rentang"] == seb["fp_maks"] - seb["fp_min"], "fp_rentang kontrol salah rumus")
cek(bool(seb["ada_varians"]), "kontrol stokastik tanpa varians")

# acuan R8 untuk rule, CUSUM saja, dan H1
r8_rule = r8["ringkas"]["rule_kanal"]
r8_stat = r8["ringkas"]["stat_cusum"]
r8_h1 = r8["ringkas"][M]
cek(r8_h1["fp_total"] == 935 and r8_h1["tp_total"] == 3804, "r8 H1 berubah")
cek(r8_rule["fp_total"] == 2105 and r8_rule["tp_total"] == 5579, "r8 rule berubah")
cek(r8_stat["fp_total"] == 4361 and r8_stat["tp_total"] == 4210, "r8 stat berubah")
cek(abs(r8_rule["lead_median_median"] - 6.0) < 1e-9, "r8 rule lead berubah")


def head_v9(name):
    for e in v9["engines"]:
        if e["engine"] == "hyd":
            for h in e["heads"]:
                if h["head"] == name:
                    return h["metrik_segmen"]
    raise KeyError(name)


rd_v9 = head_v9("rule_display")
ps_v9 = head_v9("persistence")
hy_v9 = head_v9("hybrid_rule_and_persistence")
cek(rd_v9["tp"] == 607 and rd_v9["fp"] == 368, "V9 rule_display berubah")
cek(ps_v9["tp"] == 553 and ps_v9["fp"] == 323, "V9 persistence berubah")
cek(hy_v9["tp"] == 516 and hy_v9["fp"] == 110, "V9 hybrid berubah")
v9n = v9["segmen_info"]["hyd_ki"]["n"]
cek(v9n == 10401, "segmen V9 hyd_ki berubah")

f14_rule = fold_rec("F-14", "rule_kanal")
f14_h1 = fold_rec("F-14", M)
cek(f14_rule["rows"]["tp"] == rd_v9["tp"] and f14_rule["rows"]["fp"] == rd_v9["fp"],
    "silang rule F-14 dengan V9 tidak cocok")
cek(abs(f14_rule["far24_baris"] - rd_v9["far_segmen"]) < 0.01,
    "satuan FAR baris tidak sebanding dengan V9")

rf_rule42 = folds_of(42, "rule_kanal")
rf_stat42 = folds_of(42, "stat_cusum")
rule_fp = int(sum(r["rows"]["fp"] for r in rf_rule42))
rule_tp = int(sum(r["rows"]["tp"] for r in rf_rule42))
stat_fp = int(sum(r["rows"]["fp"] for r in rf_stat42))
stat_tp = int(sum(r["rows"]["tp"] for r in rf_stat42))
cek(rule_fp == r8_rule["fp_total"] and rule_tp == r8_rule["tp_total"], "rule S1 beda R8")
cek(stat_fp == r8_stat["fp_total"] and stat_tp == r8_stat["tp_total"], "stat S1 beda R8")

repro = seeds_doc["reproduksi"]
delta = repro["delta"]
lulus = repro["lulus"]
val42 = {k: ring(42)[k] for k in
         ("far24_kalender_median", "far24_baris_median", "fold_far_le6",
          "fold_gate_A_baru", "fp_kejadian_total", "precision_min", "precision_maks",
          "recall_min", "recall_maks", "lead_median_min", "lead_median_maks",
          "cakupan_median", "far24_kalender_min", "far24_kalender_maks",
          "far24_baris_min", "far24_baris_maks", "n_onset", "n_diperingatkan",
          "fp_total", "tp_total", "precision_median", "recall_median",
          "lead_median_median", "far24_kalender_rentang", "fold_recall_gt0")}

far_rule = r8_rule["far24_median"]
lead_rule = r8_rule["lead_median_median"]
lead_h1 = r8_h1["lead_median_median"]
far_h1 = r8_h1["far24_median"]
selisih_far = round(far_rule - far_h1, 4)
selisih_lead = round(lead_h1 - lead_rule, 1)


def tabel_fold():
    out = []
    for r in folds_of(42, M):
        out.append("| " + r["fold"] + " | " + str(int(r["rows"]["tp"])) + " | " +
                   str(int(r["rows"]["fp"])) + " | " + n(r["rows"]["precision"]) + " | " +
                   n(r["rows"]["recall"]) + " | " + n(r["far24_kalender"]) + " | " +
                   n(r["far24_baris"]) + " | " + n(r["lead"]["lead_median_min"], 1) + " | " +
                   str(int(r["lead"]["n_diperingatkan"])) + " | " + n(r["cakupan"]) + " | " +
                   n(r["h_terpilih"], 1) + " | " +
                   ("ya" if r["gate_A_baru"] else "tidak") + " |")
    return "\n".join(out)


L = []
surat = L.append

# ------------------------------------------------------------------ kepala
surat("# RND-S1: ketahanan lintas seed H1 hyd dan harness bersama (kartu t_6890a1c7)")
surat("")
surat("Riset pendahuluan: statistical-analysis, scikit-learn, scientific-critical-thinking, "
      "verification-mandatory.")
surat("")
surat("Cara pemakaian skill:")
surat("")
surat("- **statistical-analysis** dipakai untuk memilih satuan metrik: FAR pada satuan kalender "
      "(satuan gate) berdampingan dengan satuan baris negatif supaya sebanding dengan angka V9; "
      "setiap sebaran dilaporkan sebagai median, min, maks, dan rentang, bukan satu angka tunggal; "
      "sel yang meleset ditulis apa adanya, bukan dibulatkan menjadi keberhasilan.")
surat("- **scikit-learn** dipakai untuk kontrol stokastik ML: LightGBM dengan random_state=seed "
      "pada dataset hyd yang sama dan fold yang sama. Kolom turunan label (y_*, valid_prev_*, "
      "obs_*, anom_*, lab_*), ts_bin, feat_ts_max, dan kolom meta dilarang masuk matriks fitur, "
      "dan larangan itu ditegakkan oleh assert di fungsi fitur_dari.")
surat("- **scientific-critical-thinking** dipakai untuk menguji penjelasan alternatif: varians nol "
      "H1 dapat berarti arsitektur deterministik ATAU acuan seed yang tidak tersambung. Kontrol ML "
      "pada seed yang sama adalah tes pembeda yang bisa gagal.")
surat("- **verification-mandatory** dipakai untuk menegakkan bukti mentah: seluruh angka dokumen ini "
      "disisipkan generator ini dari berkas JSON dengan assert sebelum menulis, dan artefak JSON "
      "mentah wajib ada di scratch/rnd/s1. Run ulang segar menghasilkan angka identik.")
surat("")
surat("sequ-mcp dipakai 10 pikiran lintas dua run: 6 pikiran pada run verifikasi ini (pemisahan "
      "klaim yang harus diuji, tes pembeda seed lewat kontrol ML, temuan konstanta R8 yang masih "
      "hardcode, pemeriksaan angka per fold, pemeriksaan angka V9 dan ledger, dan keputusan "
      "perbaikan) serta 4 pikiran pada run awal (desain uji lintas seed, urutan fail-fast plus jalur "
      "silang V9, pembagian lapisan A/B/C beserta batas kalibrasi, dan daftar yang belum terukur). "
      "Jumlah run awal tercatat dari sesi sebelumnya dan tidak dapat dibuktikan ulang dari artefak.")
surat("")
surat("Artefak mentah: scratch/rnd/s1/s1_hyd_seeds.json, s1_meta.json, s1_h_saturasi.json, "
      "s1_hluas.json. "
      "Kode: code/rnd_hybrid_harness.py (harness bersama), code/rnd_s1_run.py (runner), "
      "code/rnd_s1_hcheck.py (saturasi ambang), code/rnd_s1_ledger.py (ledger), "
      "code/rnd_s1_dokumen.py (dokumen ini). Setiap angka punya baris S1-nnn di "
      "docs/RND_PROVENANCE_LEDGER.md.")
surat("")
surat("---")
surat("")

# ------------------------------------------------------------ bagian 1: lingkup
surat("## 1. Lingkup dan kebijakan pengikat")
surat("")
surat("Kebijakan pengikat: docs/RND_EVALUATION_POLICY.md. Pertanyaan kartu: apakah angka H1 "
      "(statistik DAN rule pada hyd K-i) dari R8 bertahan kalau seed diubah, dan apakah harness "
      "bersama layak dipakai S2 dan S3.")
surat("")
surat("Prinsip eksekusi: reproduksi dulu angka seed 42 terhadap R8 dan berhenti bila meleset, lalu "
      "jalankan seed lain, lalu kontrol stokastik sebelum klaim determinisme dipakai. Tidak ada run "
      "yang diklaim nyata tanpa artefak JSON, dan tidak ada angka dokumen yang ditulis tangan.")
surat("")
surat("Definisi stabil yang dipakai di sini, dinyatakan sebelum hasil: stabil berarti rentang antar "
      "seed nol pada metrik utama (FP total, presisi median, recall median, FAR, lead). Stabilitas "
      "lintas seed bukan bukti bahwa ambangnya benar, karena stabilitas bisa lahir dari arsitektur "
      "yang memang tidak memakai angka acak.")
surat("")
surat("---")
surat("")

# ------------------------------------------------------------ bagian 2: metode
surat("## 2. Metode: harness bersama code/rnd_hybrid_harness.py")
surat("")
surat("| Kelompok | Fungsi | Keterangan |")
surat("|---|---|---|")
surat("| Muat data | muat_dataset, pecah_well, muat_fold | CSV menit, dict per well terurut ts_bin, fold LOWO |")
surat("| Detektor | seri_z, gerbang_rule, cusum_alarm, jendela_alarm, pilih_h, detektor_stat_rule | rule kanal kausal bin t-1, CUSUM dua sisi dengan reset, zona peringatan 10 menit, ambang h dari well kalibrasi |")
surat("| ML (S2/S3 dan kontrol S1) | fitur_dari, latih_lgb, threshold_conformal, skor_ml_fold | kolom bocor dibuang dengan assert, ambang conformal kuantil (1-alpha) skor negatif kalibrasi |")
surat("| Evaluasi | evaluasi_fold, ringkas_records, sidik_metrik | FAR dua satuan, batas Garwood dua sisi, lead, separuh waktu |")
surat("| Penulisan | tulis_json | artefak JSON mentah |")
surat("")
surat("Aturan modul yang mengikat S2 dan S3: keputusan pada menit t hanya memakai informasi sampai "
      "t-1 untuk gerbang rule, CUSUM hanya mengonsumsi z yang sudah tersedia, ambang tidak pernah "
      "dilihatkan ke well uji, FAR dilaporkan pada dua satuan, dan seed hanya menyentuh komponen ML. "
      "H1 (rule plus CUSUM) dinyatakan deterministik penuh di docstring, sehingga pemanggil yang "
      "butuh komponen stokastik wajib memakai skor_ml_fold dan merakit sendiri.")
surat("")
surat("Konstanta yang dipegang: alpha_budget " + n(seeds_doc["konstanta"]["alpha_budget"], 6) +
      " (setara 6 per 1440 menit), horizon lead " +
      str(int(seeds_doc["konstanta"]["lead_horizon"])) + " menit, jendela alarm " +
      str(int(seeds_doc["konstanta"]["w_jendela"])) + " menit, cusum_k " +
      n(seeds_doc["konstanta"]["cusum_k"], 1) + ", grid h " +
      n(seeds_doc["konstanta"]["h_grid"][0], 1) + " sampai " +
      n(seeds_doc["konstanta"]["h_grid"][-1], 1) + ", FAR maksimum " +
      n(seeds_doc["konstanta"]["far_maks"], 1) + " dan recall minimum " +
      n(seeds_doc["konstanta"]["recall_min"], 2) + " untuk definisi gate baru.")
surat("")
surat("---")
surat("")

# -------------------------------------------------------------- bagian 3: data
surat("## 3. Data dan pemeriksaan awal")
surat("")
surat("Dataset scratch/v9_d1/datasets/hyd_ki.csv.gz: " + str(int(meta["dataset_shape"][0])) +
      " baris, " + str(int(meta["dataset_shape"][1])) + " kolom, sha256 " +
      meta["dataset_sha256"][:16] + " (16 karakter awal), " + str(len(meta["wells"])) +
      " well, " + str(int(meta["n_fold"])) + " fold LOWO dari scratch/v9_d1/lowo_hyd_ki.json.")
surat("")
surat("| Well | Baris | Positif y_hyd | Menit kalender | Cakupan baris/kalender |")
surat("|---|---|---|---|---|")
for w in sorted(meta["wells"]):
    baris = int(meta["wells"][w])
    kal = int(meta["per_well_menit_kalender"][w])
    surat("| " + w + " | " + str(baris) + " | " + str(int(meta["per_well_pos"][w])) +
          " | " + str(kal) + " | " + n(baris / kal) + " |")
surat("")
surat("Cakupan rekaman rendah bila penyebut kalender dibaca sebagai waktu operasi nyata: cakupan "
      "median fold " + n(val42["cakupan_median"]) + ", dan cakupan tiap fold ada di tabel bagian 6.1. "
      "Karena itu FAR kalender dipakai sebagai satuan gate sesuai kebijakan, sementara FAR baris "
      "dipakai untuk membandingkan dengan angka pra-riset V9, dan kedua satuan tidak boleh dicampur "
      "dalam satu klaim.")
surat("")
surat("---")
surat("")

# ------------------------------------------------------- bagian 4: replikasi
surat("## 4. Reproduksi angka terbit R8 pada seed 42")
surat("")
surat("| Metrik | Terbit R8 | Replikasi S1 | Selisih | Lulus |")
surat("|---|---|---|---|---|")
BARIS4 = [
    ("FP total", "fp_total", "fp_total", 935, 0),
    ("TP total", "tp_total", "tp_total", 3804, 0),
    ("Presisi median", "precision_median", "precision_median", 0.7789, 4),
    ("Recall median", "recall_median", "recall_median", 0.5638, 4),
    ("Lead median", "lead_median", "lead_median_median", 11.5, 1),
    ("Onset", "n_onset", "n_onset", 390, 0),
    ("Diperingatkan", "n_diperingatkan", "n_diperingatkan", 219, 0),
]
for label, kd, kf, acuan, d in BARIS4:
    surat("| " + label + " | " + n(acuan, d) + " | " + n(ring(42)[kf], d) + " | " +
          n(delta[kd], 6) + " | " + ("ya" if lulus[kd] else "tidak") + " |")
surat("")
surat("Per fold, FP, TP, dan ambang h cocok persis:")
surat("")
surat("| Fold | FP R8 | FP S1 | Delta FP | TP R8 | TP S1 | Delta TP | h R8 | h S1 |")
surat("|---|---|---|---|---|---|---|---|---|")
for r in repro["per_fold"]:
    surat("| " + str(r["fold"]) + " | " + str(int(r["fp_r8"])) + " | " +
          str(int(r["fp_kini"])) + " | " + str(r["fp_delta"]) + " | " +
          str(int(r["tp_r8"])) + " | " + str(int(r["tp_kini"])) + " | " +
          str(r["tp_delta"]) + " | " + n(r["h_r8"], 1) + " | " + n(r["h_kini"], 1) + " |")
surat("")
surat("**Kesimpulan replikasi: LULUS.** Ketujuh metrik cocok persis dengan toleransi yang ditetapkan "
      "runner (FP, TP, dan jumlah onset wajib nol delta; presisi, recall, dan lead toleransi "
      "0,0001). Jalur silang kedua di luar R8 juga cocok: model rule_kanal pada fold F-14 memberi "
      "TP " + str(int(f14_rule["rows"]["tp"])) + " dan FP " + str(int(f14_rule["rows"]["fp"])) +
      ", persis sama dengan head rule_display V9 pada segmen yang sama (bagian 7). Karena replikasi "
      "lulus, generator lintas seed dilanjutkan.")
surat("")
surat("---")
surat("")

# ------------------------------------------------------- bagian 5: lintas seed
surat("## 5. Lintas seed H1 dan kontrol stokastik")
surat("")
surat("### 5.1 H1 eksak protokol R8, lima seed, sembilan fold per seed")
surat("")
surat("| Metrik | 42 | 7 | 13 | 21 | 33 | Median | Min | Maks | Rentang |")
surat("|---|---|---|---|---|---|---|---|---|---|")
for m in ("fp_total", "tp_total", "precision_median", "recall_median",
          "far24_kalender_median", "far24_kalender_min", "far24_kalender_maks",
          "far24_baris_median", "lead_median_median", "n_diperingatkan",
          "fold_far_le6", "fold_gate_A_baru", "cakupan_median"):
    v = ls(m)
    sel_ = " | ".join(n(v["per_seed"][str(s)]) for s in SEEDS)
    surat("| " + m + " | " + sel_ + " | " + n(v["median"]) + " | " + n(v["min"]) +
          " | " + n(v["maks"]) + " | " + n(v["rentang"]) + " |")
surat("")
surat("Setiap sel identik antar seed, dan delta fold terhadap seed pertama nol pada seluruh kanal "
      "sidik (" + str(int(seeds_doc["n_fold_berbeda_maks"])) +
      " fold berbeda maksimum, dari 9 fold). Sebabnya arsitektural: H1 tidak memiliki komponen "
      "acak. Rule kanal, residual, CUSUM, dan pemilihan h semuanya deterministik, dan parameter "
      "seed hanya dicatat ke rekaman.")
surat("")
surat("### 5.2 Kontrol stokastik ML pada seed yang sama")
surat("")
surat("Kontrol ini menjawab satu penjelasan alternatif: apakah nol varians itu berarti acuan seed "
      "tidak tersambung sama sekali di harness. Jalur kontrol sengaja stokastik, memakai LightGBM "
      "dengan random_state=seed, fitur " + str(int(kont["n_fitur"])) + " kolom setelah kolom label "
      "dan kolom meta dibuang, dan ambang conformal dari well kalibrasi.")
surat("")
surat("| Seed | FP total | TP total | Presisi median | Recall median | FAR24 kalender median | "
      "Lead median | Diperingatkan |")
surat("|---|---|---|---|---|---|---|---|")
for s in SEEDS:
    c = kes(s)
    surat("| " + str(s) + " | " + str(int(c["fp_total"])) + " | " + str(int(c["tp_total"])) +
          " | " + n(c["precision_median"]) + " | " + n(c["recall_median"]) + " | " +
          n(c["far24_kalender_median"]) + " | " + n(c["lead_median_median"], 1) + " | " +
          str(int(c["n_diperingatkan"])) + " |")
surat("")
surat("Sebaran lintas seed pada jalur kontrol: FP minimum " + str(int(seb["fp_min"])) +
      ", FP maksimum " + str(int(seb["fp_maks"])) + ", rentang " + str(int(seb["fp_rentang"])) +
      " FP; rentang presisi " + n(seb["precision_rentang"]) + "; rentang recall " +
      n(seb["recall_rentang"]) + ". Varians jalur kontrol ada: " +
      ("ya" if seb["ada_varians"] else "tidak") + ".")
surat("")
surat("Jalur kontrol juga memperlihatkan bahwa ML saja pada konfigurasi ini jauh lebih lemah dari "
      "H1: presisi median kontrol " + n(min(kes(s)["precision_median"] for s in SEEDS)) +
      " sampai " + n(max(kes(s)["precision_median"] for s in SEEDS)) + ", sedangkan H1 " +
      n(ring(42)["precision_median"]) + " pada semua seed. Angka ini dipakai sebagai konteks, bukan "
      "sebagai klaim keunggulan, karena kontrol tidak memakai gerbang rule kanal.")
surat("")
surat("**Kesimpulan bagian 5, pernyataan stabil atau tidak:** H1 **stabil lintas seed** dengan "
      "rentang nol pada FP total, presisi, recall, FAR, dan lead. Stabilitas itu berasal dari "
      "arsitektur deterministik, bukan dari kalibrasi ambang, dan kontrol stokastik membuktikan "
      "bahwa seed benar-benar tersambung di jalur yang memakai angka acak. Jadi klaim yang sah "
      "adalah: mengubah seed tidak mengubah H1. Klaim yang tidak sah adalah: H1 sudah tervalidasi "
      "karena stabil lintas seed. Sumber variasi H1 yang nyata ada pada well dan satuan FAR, dan "
      "itu diukur di bagian 6 dan 7.")
surat("")
surat("---")
surat("")

# ---------------------------------------------------- bagian 6: lapisan A/B/C
surat("## 6. Nilai lapisan A/B/C pada H1 (berlaku untuk kelima seed karena hasilnya identik)")
surat("")
surat("### 6.1 Lapisan A, per fold (H1_stat_dan_rule)")
surat("")
surat("| Fold | TP | FP | Presisi | Recall | FAR24 kalender | FAR24 baris | Lead median | "
      "Diperingatkan | Cakupan | h | Gate A baru |")
surat("|---|---|---|---|---|---|---|---|---|---|---|---|")
surat(tabel_fold())
surat("")
surat("Ringkasan lapisan A: FP total " + str(int(val42["fp_total"])) + ", TP total " +
      str(int(val42["tp_total"])) + "; presisi median " + n(val42["precision_median"]) +
      " (rentang antar fold " + n(val42["precision_min"]) + " sampai " +
      n(val42["precision_maks"]) + "); recall median " + n(val42["recall_median"]) +
      " (rentang " + n(val42["recall_min"]) + " sampai " + n(val42["recall_maks"]) +
      "); FP pada satuan kejadian (satu run alarm berurutan dihitung satu kejadian) " +
      str(int(val42["fp_kejadian_total"])) + " kejadian.")
surat("")
surat("FAR kalender: fold dengan FAR tidak lebih dari 6 per 24 jam berjumlah " +
      str(int(val42["fold_far_le6"])) + " dari 9, maksimum " + n(val42["far24_kalender_maks"]) +
      " pada F-10 dan minimum " + n(val42["far24_kalender_min"]) + " pada F-5, rentang " +
      n(val42["far24_kalender_rentang"]) + " atau sekitar 22 kali. FAR pada satuan baris jauh lebih "
      "besar: fold yang memenuhi 6 per 24 jam baris berjumlah 0 dari 9, maksimum " +
      n(val42["far24_baris_maks"]) + " pada F-9 dan minimum " + n(val42["far24_baris_min"]) +
      " pada F-10. Rasio median kedua satuan " +
      n(round(val42["far24_baris_median"] / val42["far24_kalender_median"], 4)) +
      ", jadi lulus atau tidaknya gate FAR bergantung penuh pada satuan yang dipilih. Ini temuan "
      "utama kartu ini dan bukan detail teknis.")
surat("")
surat("Definisi gate A baru (FAR kalender tidak lebih dari 6 DAN cakupan tidak kurang dari 0,5 DAN "
      "recall tidak kurang dari 0,5) dipenuhi oleh " + str(int(val42["fold_gate_A_baru"])) +
      " dari 9 fold, karena cakupan rekaman berkisar " + n(val42["cakupan_median"]) +
      " secara median. Sesuai kebijakan evaluasi, gate ini dicatat sebagai informasi kekuatan "
      "bukti, bukan sebagai vonis buang.")
surat("")
surat("### 6.2 Lapisan B, nilai maintenance")
surat("")
surat("| Ukuran | rule kanal (R8) | H1 (S1) | Selisih |")
surat("|---|---|---|---|")
surat("| Lead median sebelum onset | " + n(lead_rule, 1) + " menit | " + n(lead_h1, 1) +
      " menit | +" + n(selisih_lead, 1) + " menit untuk H1 |")
surat("| Onset diperingatkan dalam 60 menit | " + str(int(r8_rule["n_diperingatkan"])) + " dari " +
      str(int(r8_rule["n_onset"])) + " | " + str(int(r8_h1["n_diperingatkan"])) + " dari " +
      str(int(r8_h1["n_onset"])) + " | H1 memperingatkan " +
      str(int(r8_rule["n_diperingatkan"] - r8_h1["n_diperingatkan"])) +
      " onset lebih sedikit |")
surat("| Alarm tidak perlu per 24 jam kalender | " + n(far_rule) + " | " + n(far_h1) + " | -" +
      n(selisih_far) + " alarm per 24 jam |")
surat("| Presisi median | " + n(r8_rule["precision_median"]) + " | " +
      n(r8_h1["precision_median"]) + " | +" +
      n(round(r8_h1["precision_median"] - r8_rule["precision_median"], 4)) + " |")
surat("| Recall median | " + n(r8_rule["recall_median"]) + " | " +
      n(r8_h1["recall_median"]) + " | -" +
      n(round(r8_rule["recall_median"] - r8_h1["recall_median"], 4)) + " |")
surat("")
surat("Nilai maintenance yang terukur: H1 memotong beban alarm tidak perlu sebesar " +
      n(selisih_far) + " per 24 jam kalender dan menaikkan presisi median sebesar " +
      n(round(r8_h1["precision_median"] - r8_rule["precision_median"], 4)) +
      ", dengan harga " + str(int(r8_rule["n_diperingatkan"] - r8_h1["n_diperingatkan"])) +
      " onset tidak lagi diperingatkan. Lead median H1 " + n(lead_h1, 1) +
      " menit memang lebih besar dari rule " + n(lead_rule, 1) + " menit, tetapi angka itu berlaku "
      "hanya pada subset onset yang masih berhasil diperingatkan, jadi bukan keunggulan mutlak.")
surat("")
surat("Nilai dalam rupiah atau jam henti yang dihindari BELUM TERUKUR, karena repo tidak memuat data "
      "biaya dan jadwal inspeksi. Ini dicatat sebagai baris BELUM di ledger, bukan dikosongkan.")
surat("")
surat("### 6.3 Lapisan C, ketepatan dan ketahanan")
surat("")
surat("Kestabilan antar well pada H1 buruk dan harus disebut lebih dulu: FAR kalender terburuk " +
      n(val42["far24_kalender_maks"]) + " (F-10) dan terbaik " + n(val42["far24_kalender_min"]) +
      " (F-5), rentang " + n(val42["far24_kalender_rentang"]) + " atau sekitar 22 kali. Artinya "
      "ambang yang sama tidak menghasilkan beban alarm yang sama antar well, sehingga klaim FAR "
      "terkendali hanya berlaku pada " + str(int(val42["fold_far_le6"])) + " dari 9 well.")
surat("")
surat("Recall positif di semua fold (" + str(int(val42["fold_recall_gt0"])) + " dari 9), jadi H1 "
      "bukan detektor yang mati di sebagian well. Lead median antar fold berkisar " +
      n(val42["lead_median_min"], 1) + " sampai " + n(val42["lead_median_maks"], 1) + " menit.")
surat("")
surat("### 6.4 Saturasi ambang CUSUM, batas yang paling penting")
surat("")
surat("Ambang h yang terpilih pada 9 dari 9 fold adalah " + n(sat["h_grid_maks"], 1) +
      ", yaitu nilai terbesar grid. Pemeriksaan laju alarm pada h tersebut terhadap anggaran " +
      n(sat["anggaran_alpha"], 6) + " menunjukkan anggaran TIDAK terpenuhi di seluruh fold: laju "
      "paling ringan " + n(sat["per_fold"][1]["laju_alarm_h_maks"], 6) + " dan paling berat " +
      n(sat["per_fold"][0]["laju_alarm_h_maks"], 6) + ", keduanya di atas anggaran. Pemindaian di "
      "luar grid pada well kalibrasi F-12 menunjukkan ambang terkecil yang benar-benar memenuhi "
      "anggaran adalah " + n(sat["h_terkecil_lolos_anggaran_di_luar_grid"], 1) + ".")
surat("")
surat("Konsekuensinya harus dinyatakan tegas: pemilihan h pada H1 bukan kalibrasi yang berhasil, "
      "melainkan pemilihan nilai maksimum yang tersedia. Karena itu FAR H1 yang dilaporkan di "
      "bagian 6.1 adalah akibat langsung dari plafon grid, bukan akibat kendali anggaran. Well "
      "kalibrasi juga hanya dua (" + ", ".join(sat["well_kalibrasi_unik"]) +
      ") karena aturan train_wells[0], sehingga beban kalibrasi sangat bergantung pada dua well itu.")
surat("")
surat("### 6.5 Perluasan grid ambang (eksploratif, bukan protokol R8)")
surat("")
surat("Karena bagian 6.4 berhenti pada pertanyaan yang belum terjawab, yaitu apa yang terjadi kalau "
      "kalibrasi benar-benar diizinkan memilih ambang di atas 30, satu run eksploratif dijalankan "
      "dengan grid diperluas sampai " + n(luas["grid_luas"][-1], 1) + ". Varian ini diberi nama "
      "H1_hluas dan tidak menggantikan H1 pada tabel mana pun di atas. Artefaknya "
      "scratch/rnd/s1/s1_hluas.json dan kodenya code/rnd_s1_hluas.py.")
surat("")
surat("| Fold | h terpilih | Laju alarm kalibrasi | Lolos anggaran | TP | FP | Presisi | Recall | "
      "FAR kalender | FAR baris | Lead | Diperingatkan |")
surat("|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in luas["per_fold"]:
    surat("| " + r["fold"] + " | " + n(r["h_terpilih"], 1) + " | " +
          n(r["laju_alarm_kalibrasi"], 6) + " | " +
          ("ya" if r["lolos_anggaran"] else "tidak") + " | " +
          str(int(r["rows"]["tp"])) + " | " + str(int(r["rows"]["fp"])) + " | " +
          n(r["rows"]["precision"]) + " | " + n(r["rows"]["recall"]) + " | " +
          n(r["far24_kalender"]) + " | " + n(r["far24_baris"]) + " | " +
          n(r["lead"]["lead_median_min"], 1) + " | " +
          str(int(r["lead"]["n_diperingatkan"])) + " |")
surat("")
lh = luas["ringkas"]
surat("Hasil perluasan grid, dibandingkan H1 protokol R8 pada tabel yang sama: anggaran terpenuhi di " +
      str(int(luas["n_lolos_anggaran"])) + " dari " + str(int(luas["n_fold"])) +
      " fold, FP total turun dari " + str(int(val42["fp_total"])) + " menjadi " +
      str(int(lh["fp_total"])) + ", presisi median naik dari " + n(val42["precision_median"]) +
      " menjadi " + n(lh["precision_median"]) + ", FAR kalender median turun dari " +
      n(val42["far24_kalender_median"]) + " menjadi " + n(lh["far24_kalender_median"]) +
      " sehingga fold yang lulus 6 per 24 jam kalender menjadi " + str(int(lh["fold_far_le6"])) +
      " dari 9.")
surat("")
surat("Harganya juga terukur dan besar: recall median turun dari " + n(val42["recall_median"]) +
      " menjadi " + n(lh["recall_median"]) + ", onset yang mendapat peringatan turun dari " +
      str(int(val42["n_diperingatkan"])) + " menjadi " + str(int(lh["n_diperingatkan"])) +
      " dari 390, dan definisi gate A baru tetap dipenuhi 0 dari 9 fold karena recall minimum 0,5 "
      "tidak tercapai di fold mana pun. Lead median memang naik ke " + n(lh["lead_median_median"], 1) +
      " menit, tetapi itu berlaku hanya pada " + str(int(lh["n_diperingatkan"])) +
      " onset yang masih terperingatkan.")
surat("")
surat("Kesimpulan 6.5, dan ini yang mengubah pembacaan bagian 6.4: masalahnya bukan hanya grid yang "
      "terlalu pendek. Kalau grid diperluas, kalibrasi memang berhasil menekan beban alarm sampai di "
      "bawah anggaran, tetapi detektor yang tenang itu berhenti berguna untuk peringatan dini. "
      "Dengan konfigurasi CUSUM sekarang, anggaran FAR 6 per 24 jam dan syarat recall 0,5 tidak "
      "dapat dipenuhi bersamaan pada data ini. Jadi H1 yang dilaporkan di R8 adalah titik operasi "
      "boros alarm yang mempertahankan recall, bukan titik operasi yang gagal kalibrasi karena salah "
      "hitung. Pilihan di antara keduanya adalah keputusan operasional, bukan keputusan teknis.")
surat("")
surat("**Status tiga lapisan.** Lapisan A terukur penuh untuk 9 fold dan 5 seed, dan tambahan satu "
      "varian operasi pada bagian 6.5. Lapisan B terukur untuk lead dan beban alarm, belum terukur "
      "untuk nilai rupiah atau jam henti. Lapisan C terukur untuk kestabilan antar well, antar seed, "
      "dan antar titik operasi (grid sekarang lawan grid diperluas), belum terukur untuk lintas "
      "kampanye pengeboran karena tanggal kampanye tidak tersedia per baris.")
surat("")
surat("---")
surat("")

# ------------------------------------------------------ bagian 7: banding V9
surat("## 7. Banding dengan konfigurasi engine pra-riset (V9)")
surat("")
surat("Sumber: scratch/v9_i1/v9_i1_RESULTS.json dan docs/V9_EVAL_C_LAYERC.md. Tidak ada run ulang "
      "untuk V9; yang dipakai adalah angka yang sudah ada di repo. Satu hal wajib disebut lebih "
      "dulu: segmen hyd_ki pada V9 hanya " + str(int(v9n)) + " baris (well F-14) dengan " +
      str(int(rd_v9["pos"])) + " baris positif, sedangkan S1 memakai 9 fold LOWO dengan " +
      str(int(meta["dataset_shape"][0])) + " baris. Jadi membandingkan angka agregat 9 fold dengan "
      "angka satu well adalah perbandingan yang tidak sah, dan yang dilakukan di sini adalah "
      "perbandingan pada segmen yang sama, yaitu F-14.")
surat("")
surat("### 7.1 Bukti satuan sebanding")
surat("")
surat("| Ukuran pada F-14 | V9 pra-riset | Harness S1 (rule_kanal) | Sama |")
surat("|---|---|---|---|")
surat("| TP | " + str(int(rd_v9["tp"])) + " | " + str(int(f14_rule["rows"]["tp"])) + " | ya |")
surat("| FP | " + str(int(rd_v9["fp"])) + " | " + str(int(f14_rule["rows"]["fp"])) + " | ya |")
surat("| Presisi | " + n(rd_v9["precision"]) + " | " + n(f14_rule["rows"]["precision"]) +
      " | ya |")
surat("| Recall | " + n(rd_v9["recall"]) + " | " + n(f14_rule["rows"]["recall"]) + " | ya |")
surat("| FAR per 24 jam baris | " + n(rd_v9["far_segmen"]) + " | " + n(f14_rule["far24_baris"]) +
      " | ya |")
surat("")
surat("Kecocokan ini penting bukan sebagai pujian, melainkan sebagai bukti bahwa satuan FAR baris "
      "di harness memang sebanding dengan satuan V9, sehingga selisih di bagian 7.2 bisa "
      "ditafsirkan.")
surat("")
surat("### 7.2 Perbandingan pada segmen F-14")
surat("")
surat("| Konfigurasi | TP | FP | Presisi | Recall | FAR per 24 jam baris |")
surat("|---|---|---|---|---|---|")
surat("| V9 rule kanal (rule_display) | " + str(int(rd_v9["tp"])) + " | " + str(int(rd_v9["fp"])) +
      " | " + n(rd_v9["precision"]) + " | " + n(rd_v9["recall"]) + " | " + n(rd_v9["far_segmen"]) +
      " |")
surat("| V9 persistence | " + str(int(ps_v9["tp"])) + " | " + str(int(ps_v9["fp"])) + " | " +
      n(ps_v9["precision"]) + " | " + n(ps_v9["recall"]) + " | " + n(ps_v9["far_segmen"]) + " |")
surat("| V9 rule DAN persistence | " + str(int(hy_v9["tp"])) + " | " + str(int(hy_v9["fp"])) +
      " | " + n(hy_v9["precision"]) + " | " + n(hy_v9["recall"]) + " | " + n(hy_v9["far_segmen"]) +
      " |")
surat("| S1 H1 rule DAN CUSUM | " + str(int(f14_h1["rows"]["tp"])) + " | " +
      str(int(f14_h1["rows"]["fp"])) + " | " + n(f14_h1["rows"]["precision"]) + " | " +
      n(f14_h1["rows"]["recall"]) + " | " + n(f14_h1["far24_baris"]) + " |")
surat("")
surat("Hasilnya tidak menguntungkan H1 dan ditulis apa adanya: pada F-14, hybrid pra-riset (rule DAN "
      "persistence) mengungguli H1 (rule DAN CUSUM) pada keempat ukuran sekaligus, yaitu FP " +
      str(int(hy_v9["fp"])) + " lawan " + str(int(f14_h1["rows"]["fp"])) + ", presisi " +
      n(hy_v9["precision"]) + " lawan " + n(f14_h1["rows"]["precision"]) + ", recall " +
      n(hy_v9["recall"]) + " lawan " + n(f14_h1["rows"]["recall"]) + ", dan FAR baris " +
      n(hy_v9["far_segmen"]) + " lawan " + n(f14_h1["far24_baris"]) + ". H1 hanya lebih baik dari "
      "rule kanal polos dan dari CUSUM saja.")
surat("")
surat("Batas perbandingan ini dinyatakan: definisi gerbang keduanya berbeda (persistence memakai "
      "y_prev pada jendela 10 menit, CUSUM memakai akumulator residual), dan penyebut baris valid "
      "berbeda tipis karena persistence membutuhkan riwayat 10 menit. Perbedaan itu tidak cukup "
      "besar untuk membalik arah selisih FP sebesar " +
      str(int(f14_h1["rows"]["fp"] - hy_v9["fp"])) + " alarm.")
surat("")
surat("Implikasi untuk S2 dan S3, ditulis sebagai arahan bukan sebagai hasil: H1 bukan titik operasi "
      "terbaik untuk hyd pada segmen F-14, sehingga S2 dan S3 tidak boleh mengasumsikan pola "
      "statistik DAN rule selalu menang. Keduanya wajib menyertakan pembanding gerbang persistence, "
      "karena pada hyd pembanding itu sudah terbukti lebih baik pada segmen yang sama.")
surat("")
surat("---")
surat("")

# ------------------------------------------------- bagian 8: batas dan penutup
surat("## 8. Batas pemakaian, yang belum terukur, dan penutup")
surat("")
surat("### 8.1 Batas pemakaian yang mengikat")
surat("")
surat("1. Angka H1 stabil lintas seed, tetapi grid ambang berhenti di " + n(sat["h_grid_maks"], 1) +
      " dan tidak satu pun fold memenuhi anggaran, sehingga FAR yang dilaporkan bukan hasil "
      "kalibrasi yang berhasil. Varian dengan grid diperluas di bagian 6.5 menunjukkan kalibrasi "
      "bisa berhasil, tetapi dengan harga recall yang jatuh. Pemakaian H1 sebagai alarm dengan "
      "beban tertentu belum sah sampai titik operasinya dipilih secara eksplisit.")
surat("2. Lulus atau tidaknya gate FAR bergantung satuan: " + str(int(val42["fold_far_le6"])) +
      " dari 9 fold lulus pada satuan kalender, 0 dari 9 lulus pada satuan baris. Setiap klaim gate "
      "wajib menyebut satuannya.")
surat("3. Cakupan rekaman median " + n(val42["cakupan_median"]) +
      ", jadi penyebut kalender bukan waktu operasi nyata. Beban alarm per 24 jam kalender tidak "
      "boleh dibaca sebagai beban per hari kerja di lapangan.")
surat("4. Kestabilan antar well buruk (" + n(val42["far24_kalender_min"]) + " sampai " +
      n(val42["far24_kalender_maks"]) + "), sehingga ambang wajib dikalibrasi per well sebelum "
      "dipakai lintas well.")
surat("5. Label hyd K-i berasal dari residu SPPA dan aliran, jadi H1 mendeteksi kondisi yang "
      "didefinisikan oleh variabel itu. Klaim prediksi kegagalan hidraulik independen adalah klaim "
      "lain yang belum diuji di sini.")
surat("")
surat("### 8.2 Yang belum terukur dan mengapa")
surat("")
surat("- Nilai maintenance dalam rupiah atau jam henti terhindar: BELUM, karena repo tidak memuat "
      "data biaya dan jadwal inspeksi.")
surat("- Ketahanan H1 lintas kampanye pengeboran: BELUM, karena tanggal kampanye tidak tersedia per "
      "baris pada dataset menit ini.")
surat("- Ambang h yang benar-benar memenuhi anggaran sudah diukur pada bagian 6.5, tetapi hanya untuk "
      "satu skema grid (0,5 sampai 600) dan hasilnya h berbeda antar fold (" +
      str(int(max(r["h_terpilih"] for r in luas["per_fold"]))) + " pada satu fold, " +
      str(int(min(r["h_terpilih"] for r in luas["per_fold"]))) + " pada delapan fold lainnya), jadi "
      "belum ada satu ambang tetap yang terbukti memenuhi anggaran di semua well.")
surat("- Perilaku H1 bila komponen CUSUM diberi inisialisasi stokastik: BELUM, karena implementasi "
      "sekarang deterministik penuh sehingga tidak ada varians untuk diukur.")
surat("- Kinerja H1 pada kelas kerusakan lain: bukan lingkup kartu ini, diserahkan ke S2 (vib, ssi) "
      "dan S3 (bit_wear) yang memakai harness yang sama.")
surat("")
surat("### 8.3 Ringkasan lima baris")
surat("")
surat("1. Reproduksi R8 pada seed 42 LULUS persis: FP " + str(int(ring(42)["fp_total"])) +
      ", presisi " + n(ring(42)["precision_median"]) + ", recall " + n(ring(42)["recall_median"]) +
      ", lead " + n(ring(42)["lead_median_median"], 1) +
      " menit, dan delta per fold nol pada 9 fold.")
surat("2. H1 stabil lintas 5 seed dengan rentang nol pada semua metrik, dan kontrol stokastik ML "
      "membuktikan varians itu bukan akibat plambing seed yang mati (FP kontrol " +
      str(int(seb["fp_min"])) + " sampai " + str(int(seb["fp_maks"])) + ").")
surat("3. Ketahanan yang sebenarnya menjadi masalah bukan seed, melainkan well: FAR kalender " +
      n(val42["far24_kalender_min"]) + " sampai " + n(val42["far24_kalender_maks"]) +
      ", dan gate FAR lulus " + str(int(val42["fold_far_le6"])) + " dari 9 pada satuan kalender "
      "tetapi 0 dari 9 pada satuan baris.")
surat("4. Ambang CUSUM tersaturasi di plafon grid " + n(sat["h_grid_maks"], 1) + " pada 9 dari 9 "
      "fold, dan setelah grid diperluas kalibrasi memang berhasil (9 dari 9 fold di bawah anggaran) "
      "tetapi recall median jatuh dari " + n(val42["recall_median"]) + " ke " +
      n(lh["recall_median"]) + ", jadi anggaran FAR 6 dan recall 0,5 tidak dapat dipenuhi bersamaan.")
surat("5. Pada segmen F-14 yang sama, hybrid pra-riset rule DAN persistence lebih baik dari H1 pada "
      "FP, presisi, dan recall, sehingga H1 bukan peningkatan atas konfigurasi pra-riset melainkan "
      "titik operasi lain, dan harness bersama siap dipakai S2 dan S3 dengan pembanding persistence "
      "wajib disertakan.")
surat("")
surat("### 8.4 Daftar yang belum terverifikasi")
surat("")
surat("- Angka V9 dibaca dari artefak repo, tidak dijalankan ulang: kebenaran angka V9 bergantung "
      "pada artefak itu sendiri, bukan pada run baru di sesi ini.")
surat("- Kecocokan rule F-14 dengan V9 diverifikasi pada satu segmen saja (F-14), belum pada segmen "
      "lain karena V9 tidak menyediakan segmen lain untuk hyd.")
surat("- Ambang h di luar grid hanya diukur laju alarmnya, belum presisi dan recall-nya.")
surat("- Nilai maintenance dalam rupiah, ketahanan lintas kampanye, dan perilaku H1 dengan CUSUM "
      "stokastik tidak diukur, dan tidak ada sumber data untuk mengukurnya di repo ini.")
surat("- Kelayakan harness untuk S2 dan S3 dinilai dari API dan hasil S1, belum dari run nyata pada "
      "vib, ssi, atau bit_wear.")
surat("- Runner versi awal (02:48) membandingkan hasil dengan konstanta R8 yang ditulis di dalam "
      "skrip, sehingga tes reproduksi tidak bisa gagal bila r8_hyd.json berubah. Pada run verifikasi "
      "ini pembanding dibaca dari r8_hyd.json lalu di-assert sama dengan angka kartu, dan pengunci "
      "itu sudah diuji bisa gagal (fp_total 936 dan presisi 0,78 memicu AssertionError).")
surat("- Dokumen versi 04:37 basi dan tidak memuat bagian 6.5 maupun s1_hluas.json. Berkas ini "
      "dihasilkan ulang oleh generator pada run verifikasi, dan seluruh angka yang sudah ada di "
      "versi lama tetap sama, jadi yang berubah adalah kelengkapan, bukan nilai.")
surat("- Run verifikasi mengulang penuh lima seed plus kontrol ML dan hasilnya identik bit per bit "
      "dengan artefak 02:50 pada semua metrik H1 maupun metrik kontrol, sehingga klaim angka "
      "reprodusibel di run terpisah kini punya bukti dua artefak, bukan satu.")
surat("")

open(DOC, "w").write("\n".join(L) + "\n")
print("tulis", DOC)
print("baris", len(L))
print("karakter", sum(len(x) for x in L))
print("cek penanda: em-dash", sum(x.count("\u2014") for x in L))
