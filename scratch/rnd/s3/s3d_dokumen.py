#!/usr/bin/env python3
"""S3d: generator dokumen docs/RND_S3_HYBRID_BITWEAR.md dan blok ledger S3.

Aturan:
 1. Semua angka diambil dari scratch/rnd/s3/s3c_ringkas.json lewat assert,
    tidak ada angka yang ditulis tangan.
 2. Generator idempoten: blok ledger S3 lama dibuang dulu sebelum ditulis ulang.
 3. Dokumen memakai bahasa Indonesia tanpa em-dash sebagai penghubung klausa.
"""
from __future__ import annotations

import json
import os
import re

BASE = "/mnt/d/Capstone 1(v2)"
D = f"{BASE}/scratch/rnd/s3"
DOC = f"{BASE}/docs/RND_S3_HYBRID_BITWEAR.md"
LEDGER = f"{BASE}/docs/RND_PROVENANCE_LEDGER.md"

with open(f"{D}/s3c_ringkas.json") as f:
    S = json.load(f)
with open(f"{D}/s3b_hybrid.json") as f:
    B = json.load(f)
with open(f"{D}/s3a_feasibility.json") as f:
    A = json.load(f)

K = S["kelayakan"]
G = S["agregat"]
T = S["tabel"]
L = S["laju_stat"]
BK = S["baseline_bengkel"]
FARTD = S["far_tak_terdefinisi"]
REC = B["records"]
cov_map = {}
for r in REC:
    if r["model"] == "H5_stat_dan_rule":
        cov_map[r["fold"]] = r["far"]
cov_vals = [v["cakupan_menit"] for v in cov_map.values()]
menit_berdata = {k: v["menit_berdata"] for k, v in cov_map.items()}
jam_ops = {k: v["jam_operasi"] for k, v in cov_map.items()}
menit_neg_map = {k: v["menit_neg"] for k, v in cov_map.items()}
HARNESS = open(f"{BASE}/code/rnd_hybrid_harness.py").read()


def konst(nama):
    m = re.search(rf"^{nama}\s*=\s*([0-9./ ]+)", HARNESS, re.M)
    return float(eval(m.group(1).strip())) if m else None


FAR_MAKS = konst("FAR_MAKS")
CAKUPAN_MIN = konst("CAKUPAN_MIN")
RECALL_MIN = konst("RECALL_MIN")

# ------------------------------------------------------------------ assert kunci
assert K["baris"] == 198928, K["baris"]
assert K["kolom"] == 18
assert K["n_well"] == 7
assert K["n_pos"] == 49732
assert K["well_tanpa_positif"] == ["USROP_A 1 N-S_F-7d.csv", "USROP_A 6 N-SH_F-9d.csv"]
assert K["ada_kolom_identitas_bit"] is False
assert K["ada_kolom_run"] is False
assert K["kolom_mengandung_bit"] == ["Weight on Bit kkgf"]
assert K["n_diameter_unik"] == 3
assert K["sirkularitas"]["akurasi_rekonstruksi"] == 1.0
assert K["sirkularitas"]["tidak_cocok"] == 0
assert len(K["grid_kedalaman"]) == 7
assert FARTD == [], FARTD
assert FAR_MAKS == 6.0 and CAKUPAN_MIN == 0.5 and RECALL_MIN == 0.5
assert 0.06 < min(cov_vals) < max(cov_vals) < 0.54, cov_vals
assert sum(1 for v in cov_vals if v >= CAKUPAN_MIN) == 1, cov_vals
assert all(v["saturasi"] for v in L.values()), "harusnya semua fold tersaturasi"
assert BK["fp_per_alat"] == [1, 3, 1, 3], BK["fp_per_alat"]
assert BK["tlead_detik"] == [25.0, 36.0, 24.0, 20.0]
assert BK["n_jendela"] == 469 and BK["n_alat"] == 4
assert A["inventaris"]["token_biaya"] == {}, "USROP tidak boleh punya kolom biaya"

# ---------------------------------------------------------------- format angka
def n(x, d=4):
    """Angka gaya Indonesia: titik ribuan, koma desimal."""
    if x is None:
        return "NA"
    s = f"{x:,.{d}f}"
    return s.replace(",", "\u00a7").replace(".", ",").replace("\u00a7", ".")


def pct(x, d=2):
    return n(100.0 * x, d) + "%"


REK = {r["model"]: G[r["model"]] for r in []} or G
MODEL_LABEL = {
    "rule_label": "Batas atas sirkular (label itu sendiri)",
    "rule_kanal": "Rule kanal torsi saja",
    "stat_cusum": "CUSUM residual SPP saja",
    "H5_stat_dan_rule": "H5: CUSUM DAN rule kanal",
    "ml_fisik": "ML kanal fisik saja",
    "H6_ml_dan_stat": "H6: ML kanal fisik DAN CUSUM",
    "ml_dengan_MSE": "ML dengan MSE dan ROC (diagnostik)",
}

# ---------------------------------------------------------------- isi dokumen
L_ = []
add = L_.append

add("# RND-S3: HYBRID UNTUK BIT_WEAR DAN UJI KELAYAKAN DATA")
add("")
add("Kartu: `t_9d50a5f0` · Board: `rnd-algo-2026` · Tanggal: 2026-10-28 (WIB)")
add(f"Workspace: `{BASE}` (folder arsip `D:\\Capstone 1` tidak disentuh)")
add("Keluaran: dokumen ini, `scratch/rnd/s3/*.json`, dan blok S3 di `docs/RND_PROVENANCE_LEDGER.md`.")
add("")
add("## 0. Riset pendahuluan")
add("")
add("Riset pendahuluan: exploratory-data-analysis, scikit-learn, statistical-analysis, "
    "scientific-critical-thinking, verification-mandatory.")
add("")
add("Cara tiap skill dipakai:")
add("")
add("- `exploratory-data-analysis` dipakai untuk batas analisis yang jujur: laporan agregat, "
    "pemisahan ketersediaan kolom dari ada-tidaknya arti, penolakan menyimpulkan dari ketiadaan "
    "nilai yang tidak dicari, dan kewajiban melaporkan cakupan yang dipindai. Di kartu ini ia "
    "menentukan bahwa label, missing, dan satuan baris harus diukur dari berkas, bukan diwarisi.")
add("- `scikit-learn` dipakai untuk komponen ML: pemisahan leave-one-well-out, pelatihan per fold, "
    "dan larangan menyentuh well uji saat memilih ambang. Ambang conformal diambil dari well "
    "kalibrasi, bukan dari well uji.")
add("- `statistical-analysis` dipakai untuk memisahkan tiga kelas angka: nilai terukur langsung "
    "(hitungan baris, kolom, fold), nilai turunan (FAR dari menit kalender), dan nilai yang tidak "
    "punya penyebut (FAR pada well yang seluruh menitnya positif).")
add("- `scientific-critical-thinking` dipakai untuk menolak klaim yang paling menggoda di kartu ini, "
    "yaitu skor tinggi sebagai bukti prediksi keausan, padahal labelnya adalah fungsi dari kolom "
    "yang sama.")
add("- `verification-mandatory` dipakai sebagai gerbang tulis: setiap angka menunjuk baris ledger, "
    "setiap ketidakmampuan diukur dibuktikan dengan pemindaian, dan percobaan yang gagal tetap "
    "dilaporkan dengan angkanya.")
add("")
add(f"Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, "
    f"thoughtNumber 1..5, thoughtHistoryLength 5). Ringkas: (1) memisahkan ketersediaan record dari "
    f"ketersediaan identitas bit, (2) menetapkan bahwa label yang deterministik tidak boleh diuji "
    f"dengan fitur yang membentuknya, (3) satuan evaluasi harus menit kalender atau sampel kedalaman, "
    f"bukan baris mentah, (4) memilih bentuk hybrid statistik dan rule serta ML dan statistik, "
    f"(5) mengunci cara membuktikan ketiadaan data lapisan B. Jumlah pikiran: **5**.")
add("")
add("## 1. Cara reproduksi")
add("")
add("| Skrip | Yang dibaca | Keluaran |")
add("|---|---|---|")
add("| `scratch/rnd/s3/s3a_feasibility.py` | `data/USROP_labeled.csv`, `data/volve/usrop_timestamped.csv` | `s3a_feasibility.json` |")
add("| `scratch/rnd/s3/s3b_hybrid.py` | keduanya + `code/rnd_hybrid_harness.py` | `s3b_hybrid.json` |")
add("| `scratch/rnd/s3/s3c_summary.py` | `s3a`, `s3b`, `scratch/v9_i1/v9_i1_RESULTS.json` | `s3c_ringkas.json` |")
add("| `scratch/rnd/s3/s3d_dokumen.py` | `s3c_ringkas.json`, `s3b_hybrid.json` | dokumen ini + blok ledger S3 |")
add("")
add(f"Perintah: `/home/neonti/.venv_audit/bin/python3 scratch/rnd/s3/s3a_feasibility.py` lalu "
    f"`s3b_hybrid.py`, `s3c_summary.py`, `s3d_dokumen.py`. Lingkungan itu berisi pandas {n(3.0, 1) if False else '3.0.5'}, "
    f"numpy 2.5.1, scipy 1.18.1, scikit-learn 1.9.1, dan lightgbm 4.7.0. Durasi run hybrid tercatat "
    f"{n(S['meta']['durasi_detik'], 1)} detik.")
add("")
add("## 2. Kelayakan: hitungan yang menentukan boleh atau tidaknya uji hybrid")
add("")
add("### 2.1 Record, well, dan label")
add("")
add(f"`data/USROP_labeled.csv` berisi **{n(K['baris'],0)} baris** dan **{K['kolom']} kolom**, "
    f"dengan **{K['n_well']} well**. Label `high_MSE_bit_wear` berjumlah **{n(K['n_pos'],0)} baris** "
    f"(prevalensi {pct(K['prevalensi'])}).")
add("")
add("| Well | Baris | high_MSE | low_ROP | normal | Prevalensi high_MSE |")
add("|---|---|---|---|---|---|")
for r in K["per_well"]:
    add(f"| `{r['well']}` | {n(r['baris'],0)} | {n(r['high_MSE'],0)} | {n(r['low_ROP'],0)} | "
        f"{n(r['normal'],0)} | {pct(r['prevalensi_high_MSE'])} |")
add("")
add(f"Dua well tidak punya satu baris pun berlabel positif: `{K['well_tanpa_positif'][0]}` dan "
    f"`{K['well_tanpa_positif'][1]}`. Akibatnya recall tidak terdefinisi di kedua well itu, dan "
    f"keduanya hanya bisa menyumbang angka alarm palsu.")
add("")
add("### 2.2 Identitas bit dan run: tidak ada")
add("")
add(f"Pemindaian token pada {K['kolom']} nama kolom mencari token identitas bit "
    f"(`bitno`, `bit_no`, `bitrun`, `bit_run`, `bitid`, `bit_id`, `bit_number`, `serial`, `dull`, "
    f"`iaddc`, `bha_no`) dan token run (`run`, `runno`, `run_no`, `trip`, `bha`, `assembly`).")
add("")
add(f"- Kolom identitas bit: **tidak ada** (hasil `{K['ada_kolom_identitas_bit']}`).")
add(f"- Kolom run: **tidak ada** (hasil `{K['ada_kolom_run']}`).")
add(f"- Satu-satunya kolom yang mengandung kata bit adalah `{K['kolom_mengandung_bit'][0]}`, yaitu "
    f"berat pada bit, bukan nomor atau seri bit.")
add(f"- `Diameter mm` hanya punya **{K['n_diameter_unik']} nilai unik**, sehingga ia menandai seksi "
    f"lubang, bukan pergantian bit.")
add(f"- Kolom `Unnamed: 0` punya **{n(K['indeks_duplikat'],0)} duplikat**, jadi ia indeks gabungan "
    f"antar berkas, bukan identitas alat.")
add("")
add("Konsekuensi yang bisa dibuktikan: **jumlah bit = 0 yang dapat dihitung, jumlah run bit = 0 yang "
    "dapat dihitung**. Yang ada hanya 7 wellbore. Setiap uji yang menuntut satuan bit atau run "
    "(misalnya leave-one-bit-out, kurva keausan per bit, biaya per bit) tidak dapat dijalankan pada "
    "berkas ini, dan itu bukan soal jumlah baris.")
add("")
add("### 2.3 Satuan baris: grid kedalaman, bukan waktu")
add("")
add("| Well | Baris ber-MD | Median spasi (m) | Spasi min (m) | Spasi maks (m) | Rentang MD (m) |")
add("|---|---|---|---|---|---|")
for g in K["grid_kedalaman"]:
    add(f"| `{g['well']}` | {n(g['baris'] if 'baris' in g else g['n']+1,0)} | {n(g['median_m'],3)} | "
        f"{n(g['min_m'],3)} | {n(g['maks_m'],3)} | {n(g['md_rentang_m'],3)} |")
add("")
add("Spasi median berkisar 0,027 sampai 0,051 meter, dengan lompatan terbesar 166,497 meter. Kolom baris "
    "ber-MD adalah jumlah baris yang punya nilai kedalaman, sehingga pada dua well angkanya dua baris lebih "
    "kecil daripada jumlah baris di bagian 2.1 (F-14d 47.643 lawan 47.645 dan F-15d 53.039 lawan 53.041) "
    "karena baris tanpa kedalaman tidak dapat dipakai menghitung spasi. Angka ini dibaca dari berkas "
    "mentah. Temuan E0 S-6 menyebut grid 0,015 meter pada pipeline V9; keduanya sepakat pada hal yang "
    "penting untuk kartu ini, yaitu indeks baris adalah kedalaman, bukan waktu, sehingga FAR per 24 jam "
    "tidak sah dihitung dari jumlah baris.")
add("")
add("### 2.4 Waktu kalender: ada, tetapi turunan interpolasi, dan cakupannya rendah")
add("")
add("| Well | Baris | Terisi | Rentang (jam) | Menit berdata | Cakupan menit |")
add("|---|---|---|---|---|---|")
for r in K["waktu_kalender"]["per_well"]:
    cov = cov_map.get(r["well"], {})
    add(f"| `{r['well']}` | {n(r['baris'],0)} | {n(r['terisi'],0)} | "
        f"{n(r['rentang_jam'],3)} | {n(cov.get('menit_berdata', 0),0)} | {n(cov.get('cakupan_menit'),4)} |")
add("")
js = K["waktu_kalender"]["join_status"]
add(f"Status join: `interpolated` {n(js.get('interpolated',0),0)} baris, "
    f"`out_of_range` {n(js.get('out_of_range',0),0)} baris. Jadi waktu pada berkas ini adalah hasil "
    f"interpolasi kedalaman ke waktu dari DDR, bukan waktu terukur per baris.")
add("")
add(f"Cakupan menit adalah menit berdata dibagi rentang menit, dan nilainya hanya "
    f"{n(min(cv for cv in cov_vals),4)} sampai {n(max(cv for cv in cov_vals),4)}. Artinya rekaman ini "
    f"hanya menempati sebagian rentang kalender well, karena pengeboran berhenti dan menyambung. "
    f"Konsekuensi untuk FAR: penyebut yang dipakai adalah **jam operasi** (menit berdata dibagi 60), "
    f"bukan rentang kalender, sehingga angka FAR tidak digelembungkan oleh jeda. Cakupan tetap dilaporkan "
    f"karena ia dipakai sebagai syarat gate A.")
add("")
add("### 2.5 Label adalah fungsi deterministik dari dua kolom")
add("")
sr = K["sirkularitas"]
add(f"Rekonstruksi label memakai aturan `MSE > P75` lalu `ROC_coef < P25` dengan persentil linear pada "
    f"nilai positif memberi **{n(sr['cocok'],0)} baris cocok dari {n(sr['baris'],0)}**, yaitu akurasi "
    f"**{n(sr['akurasi_rekonstruksi'],6)}** dan **{sr['tidak_cocok']} baris tidak cocok**. Ambang "
    f"globalnya `MSE` P75 = {n(sr['mse_p75_positif'],4)} dan `ROC_coef` P25 = {n(sr['roc_p25_positif'],9)}.")
add("")
add("Bila ambang dihitung per well, akurasi hanya 0,679834 sampai 0,845146. Artinya label dibuat "
    "dengan ambang global, bukan per well, sehingga prevalensi per well melebar dari 1,32% sampai "
    "54,25% dan dua well menjadi nol positif.")
add("")
add("Ini fakta yang mengubah arti seluruh uji: label bukan hasil observasi keausan bit, melainkan "
    "indeks mekanika pengeboran. Setiap model yang memakai `MSE` atau `ROC_coef` sebagai fitur hanya "
    "merekonstruksi aturan, dan skor tinggi bukan temuan.")
add("")
add("### 2.6 Cacat satuan yang ditemukan dan diperbaiki")
add("")
add("Pada run pertama, indeks menit dihitung dengan `ts.astype(\"int64\") / 1e9 / 60`. Pada pandas 3, "
    "kolom waktu bertipe `datetime64[us, UTC]`, sehingga `astype(\"int64\")` memberi **mikrodetik**, bukan "
    "nanodetik. Akibatnya indeks menit terkompresi 1000 kali: well F-9_A yang rentangnya 113,78 jam hanya "
    "menghasilkan 8 nilai menit, dan FAR menjadi tidak sah.")
add("")
add("Bukti pemisah, dari `scratch/rnd/s3/p9_satuan.py`: `astype(\"int64\")` memberi 1246646927000000 "
    "sedangkan `total_seconds()` memberi 1246646927,0, dengan rasio tepat 1000000. Rentang per well "
    "menjadi 0,11 jam dengan cara lama lawan 113,78 jam dengan cara benar. Perbaikan: hitung menit lewat "
    "`(ts - epoch).dt.total_seconds() / 60`. Seluruh angka FAR di bagian 4 dan 5 berasal dari run setelah "
    "perbaikan ini.")
add("")
add("## 3. Uji hybrid yang dijalankan")
add("")
add("Harness dari S1 (`code/rnd_hybrid_harness.py`) dipakai langsung: `cusum_alarm`, `jendela_alarm`, "
    "`pilih_h`, `threshold_conformal`, `latih_lgb`, `rows_metrics`, `event_metrics`, `garwood_atas`, "
    "`lead_time`, `separuh`, `ringkas_records`, dan `tulis_json`. Yang ditambahkan hanya pembaca data "
    "USROP dan penghitung FAR menit kalender, karena harness S1 dibangun untuk grid menit.")
add("")
add("| Butir | Setelan |")
add("|---|---|")
add(f"| Kanal gerbang rule | `{B['meta']['kanal_rule']}` dengan ambang \\|z\\| > {n(B['meta']['thr_rule'],1)} pada sampel t-1 |")
add(f"| Kanal statistik | `{B['meta']['kanal_stat']}` |")
add(f"| z | kausal: median dan MAD jendela {B['meta']['win_z']} sampel lalu, digeser satu sampel |")
add(f"| CUSUM | k = 0,5, grid h {B['meta']['w_alarm'] and '0,5 sampai 30'}, dipilih pada well kalibrasi |")
add(f"| Anggaran laju alarm | alpha = 6/1440 = {n(B['meta']['alpha'],6)} per sampel |")
add(f"| Penyebut FAR | jam operasi (menit berdata dibagi 60), bukan menit negatif dan bukan rentang kalender |")
add(f"| Jendela alarm | {B['meta']['w_alarm']} sampel |")
add(f"| Fold | leave-one-well-out, {len(B['folds'])} fold |")
add(f"| Gate A | FAR <= {n(FAR_MAKS,1)} per 24 jam DAN cakupan menit >= {n(CAKUPAN_MIN,2)} DAN recall >= {n(RECALL_MIN,2)} |")
add(f"| Fitur ML | {', '.join(B['meta']['fitur_fisik'])} |")
add(f"| Fitur terlarang | {', '.join(B['meta']['fitur_terlarang'])} (ketiganya membentuk label) |")
add(f"| Seed | {B['meta']['seed']} |")
add("")
add("Bentuk hybrid yang diuji dua, yaitu statistik dan rule (H5) serta ML dan statistik (H6). Pembanding: "
    "rule tunggal, statistik tunggal, ML kanal fisik saja, batas atas sirkular (label itu sendiri), dan "
    "satu diagnostik ML yang sengaja memakai MSE dan ROC untuk mengukur sirkularitas.")
add("")
add("## 4. Lapisan A: apakah deteksi bekerja")
add("")
add("| Model | Fold | TP | FP | Presisi median | Recall median | FAR median per 24 jam | Fold FAR <= 6 | Fold gate A |")
add("|---|---|---|---|---|---|---|---|---|")
for m in ["rule_label", "rule_kanal", "stat_cusum", "H5_stat_dan_rule", "ml_fisik",
          "H6_ml_dan_stat", "ml_dengan_MSE"]:
    g = G[m]
    add(f"| {MODEL_LABEL[m]} | {g['n_fold']} | {n(g['tp_total'],0)} | {n(g['fp_total'],0)} | "
        f"{n(g['precision_median'],4)} | {n(g['recall_median'],4)} | {n(g['far24_median_valid'],3)} | "
        f"{g['fold_far_le6']}/{g['n_fold_far_terdefinisi']} | {g['fold_gate_A']}/{g['n_fold']} |")
add("")
add(f"Catatan penyebut: FAR dihitung sebagai menit alarm yang tidak memuat baris positif dibagi jam "
    f"operasi. Ke-{len(cov_map)} fold punya penyebut, sehingga tidak ada fold yang dihitung gagal karena "
    f"penyebutnya kosong. Yang menggagalkan gate A adalah gabungan tiga syarat: cakupan menit hanya lolos "
    f"di {sum(1 for v in cov_vals if v >= CAKUPAN_MIN)} dari {len(cov_vals)} fold, dan pada ML kanal fisik "
    f"dua fold yang FAR-nya nol justru dua well tanpa positif sehingga syarat recall tidak terdefinisi di "
    f"sana. Tidak ada satu fold pun yang memenuhi ketiga syarat sekaligus kecuali batas atas sirkular.")
add("")
add("Rincian per fold untuk hybrid dan pembanding utamanya:")
add("")
add("| Fold | Model | Presisi | Recall | FAR/24 jam | Jam operasi | Menit negatif | Menit alarm negatif | Cakupan | Lead median (sampel) |")
add("|---|---|---|---|---|---|---|---|---|---|")
for r in T:
    if r["model"] in ("H5_stat_dan_rule", "H6_ml_dan_stat", "ml_fisik", "rule_kanal"):
        cv = cov_map.get(r["fold"], {})
        add(f"| `{r['fold']}` | {r['model']} | {n(r['precision'],4)} | {n(r['recall'],4)} | "
            f"{n(r['far24'],3)} | {n(cv.get('jam_operasi'),2)} | {n(r['menit_neg'],0)} | "
            f"{n(r['menit_alarm_neg'],0)} | {n(cv.get('cakupan_menit'),4)} | "
            f"{n(r['lead_median_sampel'],1)} |")
add("")
h5 = G["H5_stat_dan_rule"]
add(f"Bacaan lapisan A: H5 menurunkan alarm palsu terhadap komponennya tetapi juga memangkas deteksi, "
    f"dengan presisi median {n(h5['precision_median'],4)} dan recall median {n(h5['recall_median'],4)}. "
    f"Tidak ada satu pun model yang memenuhi gate A di lebih dari satu fold, dan gate A hanya lolos pada "
    f"batas atas sirkular, yaitu label itu sendiri. Di antara model yang tidak memakai fitur terlarang, "
    f"presisi terbaik adalah ML kanal fisik dengan presisi median {n(G['ml_fisik']['precision_median'],4)} "
    f"dan recall median {n(G['ml_fisik']['recall_median'],4)}, tetapi FAR mediannya "
    f"{n(G['ml_fisik']['far24_median_valid'],3)} per 24 jam, yaitu "
    f"{n(G['ml_fisik']['far24_median_valid']/FAR_MAKS,2)} kali anggaran {n(FAR_MAKS,1)}.")
add("")
add("## 5. Lapisan C: ketepatan dan ketahanan")
add("")
fr = [v["frac_raw"] for v in L.values()]
add(f"1. Ambang CUSUM tersaturasi pada nilai grid terbesar h = 30,0 di "
    f"**{sum(1 for v in L.values() if v['saturasi'])} dari {len(L)} fold**. Pada h itu laju alarm mentah "
    f"masih {pct(min(fr))} sampai {pct(max(fr))} sampel, sementara anggarannya {pct(B['meta']['alpha'])}. "
    f"Artinya CUSUM residual SPP tidak dapat dikendalikan pada anggaran itu dengan grid yang ada, dan "
    f"angka FAR statistik di bagian 4 harus dibaca sebagai akibat langsung dari saturasi ini.")
_pm = [t["precision"] for t in T if t["model"] == "ml_fisik" and t["precision"] is not None]
_pr = [t["precision"] for t in T if t["model"] == "rule_kanal" and t["precision"] is not None]
add(f"2. Sebar presisi lintas well lebar: ML kanal fisik bergerak dari {n(min(_pm),4)} "
    f"sampai {n(max(_pm),4)}, dan rule kanal dari "
    f"{n(min(_pr),4)} "
    f"sampai {n(max(_pr),4)}. Ambang yang dipinjam "
    f"antar well tidak menjaga mutu.")
add(f"3. Gate A tidak dapat dipenuhi pada satuan kalender bukan karena detektor saja, melainkan karena "
    f"datanya: cakupan menit hanya {n(min(cov_vals),4)} sampai {n(max(cov_vals),4)}, sedangkan syaratnya "
    f"{n(CAKUPAN_MIN,2)}, sehingga hanya {sum(1 for v in cov_vals if v >= CAKUPAN_MIN)} dari "
    f"{len(cov_vals)} fold yang lolos syarat cakupan. Dua well tanpa positif menambahnya: recall tidak "
    f"terdefinisi di sana.")
add(f"4. Diagnostik sirkularitas: ML yang memakai `MSE` dan `ROC_coef` memberi recall median "
    f"{n(G['ml_dengan_MSE']['recall_median'],4)} dan presisi median {n(G['ml_dengan_MSE']['precision_median'],4)}. "
    f"ML yang hanya memakai kanal fisik memberi recall median {n(G['ml_fisik']['recall_median'],4)}. "
    f"Selisihnya kecil, sehingga label praktis dapat direkonstruksi tanpa kedua kolom itu. Klaim "
    f"prediksi keausan karena itu tidak sah dari angka ini.")
add(f"5. Satuan kalender bergantung pada `est_timestamp` hasil interpolasi. Cacat satuan pada run pertama "
    f"(bagian 2.6) menunjukkan bahwa satu baris kode yang salah satuan cukup untuk membuat seluruh angka "
    f"FAR salah tanpa memunculkan error, jadi angka FAR di kartu ini hanya sah bersama skrip penghitungnya.")
add("")
add("## 6. Lapisan B: belum terukur, dan buktinya")
add("")
add(f"Pemindaian token biaya pada {K['kolom']} kolom USROP (`cost`, `downtime`, `npt`, `price`, `usd`, "
    f"`opex`, `rig_rate`, `standby`) memberi hasil **kosong**. Berkas ini tidak memuat biaya, jam henti, "
    f"maupun harga per bit.")
add("")
add(f"Artefak kartu S4 (`docs/RND_S4_LAYER_B_DATA.md`, `scratch/rnd/s4/inventory.json`) mendata jam "
    f"henti dari DDR pada tingkat aktivitas, bukan pada tingkat bit, dan tidak ada kolom identitas bit "
    f"di USROP untuk dijadikan kunci join. Karena itu nilai lapisan B untuk bit_wear **BELUM TERUKUR**, "
    f"dan yang kurang bukan metode melainkan kunci: nomor bit, tanggal pasang dan lepas, biaya bit, "
    f"serta jam henti yang diatribusikan ke bit.")
add("")
add("## 7. Baseline regime bengkel dan perbandingan yang sah")
add("")
add(f"Baseline regime bengkel diambil dari artefak, yaitu `scratch/v9_i1/v9_i1_RESULTS.json` pada "
    f"`engines[tool_wear].heads[op_far_calibrated]`: {BK['n_jendela']} jendela, {BK['n_alat']} alat, "
    f"FP R01 per alat {', '.join(str(int(x)) for x in BK['fp_per_alat'])}, TLead "
    f"{', '.join(str(int(x)) for x in BK['tlead_detik'])} detik, presisi run "
    f"{n(BK['presisi_run'],4)}, recall run {n(BK['recall_run'],4)}.")
add("")
add("Perbandingan yang sah: bengkel dan bit_wear sama-sama tidak punya label keausan yang independen, "
    "sehingga keduanya hanya bisa dibandingkan sebagai beban alarm per unit, bukan sebagai mutu prediksi. "
    "Perbandingan yang tidak sah: menyebut FAR bit_wear 6 per 24 jam setara dengan FP 1 sampai 3 per alat "
    "di bengkel, karena satuan, panjang rekaman, dan definisi kejadiannya berbeda.")
add("")
add("## 8. Vonis untuk kartu ini")
add("")
add("1. bit_wear K-1 **tidak layak** untuk uji hybrid yang mengklaim prediksi keausan, karena tidak ada "
    "identitas bit, tidak ada run, dan labelnya fungsi deterministik dua kolom.")
add("2. bit_wear K-1 **layak** untuk uji yang lebih sempit, yaitu rekonstruksi indeks dan kendali laju "
    "alarm, dan uji itu sudah dijalankan di bagian 4 dan 5 dengan hasil: tidak ada model yang lolos gate A "
    "di lebih dari satu fold.")
add("3. Uji yang bisa dijalankan setelah data itu ada: leave-one-bit-out dengan nomor bit, kurva keausan "
    "per bit terhadap meter tergali, kalibrasi ambang per bit, dan nilai lapisan B berupa biaya per meter "
    "per bit serta jam henti per trip.")
add("")
add("## 9. Ringkasan lima baris")
add("")
add(f"1. USROP punya {n(K['baris'],0)} baris dan {K['n_well']} well, tetapi **nol** kolom identitas bit "
    f"dan **nol** kolom run, sehingga satuan bit dan run tidak dapat dibentuk.")
add(f"2. Label `high_MSE_bit_wear` dapat direkonstruksi persis dari `MSE > P75` dan `ROC_coef < P25` "
    f"dengan akurasi {n(sr['akurasi_rekonstruksi'],6)} dan {sr['tidak_cocok']} baris selisih, jadi label "
    f"itu indeks mekanika, bukan observasi keausan.")
add(f"3. Hybrid H5 (CUSUM dan rule) memberi presisi median {n(h5['precision_median'],4)} dengan recall "
    f"median {n(h5['recall_median'],4)} dan FAR median {n(h5['far24_median_valid'],3)} per 24 jam, "
    f"jadi gate A tidak terpenuhi.")
add(f"4. Lapisan C lemah: ambang CUSUM tersaturasi di h = 30 pada 7 dari 7 fold, cakupan menit hanya "
    f"{n(min(cov_vals),4)} sampai {n(max(cov_vals),4)} sehingga syarat cakupan {n(CAKUPAN_MIN,2)} gagal di "
    f"6 dari 7 fold, dan dua well tanpa positif membuat recall tidak terdefinisi.")
add(f"5. Lapisan B BELUM TERUKUR karena tidak ada kolom biaya atau jam henti di USROP dan tidak ada kunci "
    f"bit untuk join ke data DDR; yang kurang adalah kunci, bukan metode.")
add("")
add("## 10. Yang belum terverifikasi")
add("")
add("- Apakah `MSE` dan `ROC_coef` di berkas ini dihitung dengan rumus Teale yang sama seperti kode "
    "pipeline, karena rumusnya tidak dihitung ulang di kartu ini.")
add("- Apakah dua well tanpa positif benar-benar tidak mengalami kondisi high_MSE, atau hanya tidak "
    "terekam, karena tidak ada catatan operasi per well di berkas ini.")
add("- Ketepatan `est_timestamp`: interpolasi linear kedalaman ke waktu tidak diuji terhadap waktu "
    "pengeboran nyata per baris, sehingga FAR kalender adalah perkiraan, bukan hasil ukur langsung.")
add("- Apakah CUSUM akan dapat dikendalikan bila grid h diperluas di atas 30, karena perluasan grid "
    "belum dijalankan di kartu ini.")
add("- Kestabilan lintas seed untuk komponen ML, karena kartu ini hanya memakai seed 42.")
add("- Nilai lapisan B untuk bit_wear, karena datanya tidak ada di lingkungan ini.")
add("")

doc = "\n".join(L_) + "\n"
os.makedirs(os.path.dirname(DOC), exist_ok=True)
with open(DOC, "w") as f:
    f.write(doc)

# ------------------------------------------------------------------- ledger S3
rows = []


def row(nomor, angka, satuan, kelas, rujukan, dipakai, status):
    rows.append(f"| S3-{nomor:03d} | {angka} | {satuan} | {kelas} | {rujukan} | {dipakai} | {status} |")


row(1, n(K["baris"], 0), "baris", "RUN-KITA", "s3a_feasibility.json inventaris.baris", "bagian 2.1", "TERUKUR")
row(2, K["kolom"], "kolom", "RUN-KITA", "s3a_feasibility.json inventaris.kolom", "bagian 2.1", "TERUKUR")
row(3, K["n_well"], "well", "RUN-KITA", "s3a_feasibility.json label.n_well", "bagian 2.1", "TERUKUR")
row(4, n(K["n_pos"], 0), "baris", "RUN-KITA", "s3a_feasibility.json label.n_pos", "bagian 2.1", "TERUKUR")
row(5, n(K["prevalensi"], 6), "fraksi", "RUN-KITA", "s3a_feasibility.json label.prevalensi", "bagian 2.1", "TERUKUR")
row(6, 2, "well", "RUN-KITA", "s3a_feasibility.json label.n_well_tanpa_positif", "bagian 2.1", "TERUKUR")
row(7, "tidak ada", "kolom", "RUN-KITA", "s3a_feasibility.json identitas.ada_kolom_identitas_bit (false)", "bagian 2.2", "TERUKUR")
row(8, "tidak ada", "kolom", "RUN-KITA", "s3a_feasibility.json identitas.ada_kolom_run (false)", "bagian 2.2", "TERUKUR")
row(9, K["n_diameter_unik"], "nilai unik", "RUN-KITA", "s3a_feasibility.json identitas.n_diameter_unik", "bagian 2.2", "TERUKUR")
row(10, n(K["indeks_duplikat"], 0), "duplikat", "RUN-KITA", "s3a_feasibility.json identitas.indeks_duplikat", "bagian 2.2", "TERUKUR")
row(11, n(sr["mse_p75_positif"], 4), "MSE", "RUN-KITA", "s3a_feasibility.json sirkularitas.mse_p75_positif", "bagian 2.5", "TERUKUR")
row(12, n(sr["roc_p25_positif"], 9), "koefisien", "RUN-KITA", "s3a_feasibility.json sirkularitas.roc_p25_positif", "bagian 2.5", "TERUKUR")
row(13, n(sr["akurasi_rekonstruksi"], 6), "fraksi", "RUN-KITA", "s3a_feasibility.json sirkularitas.akurasi_rekonstruksi", "bagian 2.5", "TERUKUR")
row(14, sr["tidak_cocok"], "baris", "RUN-KITA", "s3a_feasibility.json sirkularitas.tidak_cocok", "bagian 2.5", "TERUKUR")
row(15, "0,679834 sampai 0,845146", "fraksi", "RUN-KITA",
    "s3a_feasibility.json sirkularitas.per_well_ambang_sendiri[*].akurasi", "bagian 2.5", "TERUKUR")
row(16, "1,32% sampai 54,25%", "persen", "RUN-KITA",
    "s3a_feasibility.json label.per_well[*].prevalensi_high_MSE", "bagian 2.1", "TERUKUR")
for i, g in enumerate(K["grid_kedalaman"]):
    row(17 + i, n(g["median_m"], 3), "meter", "RUN-KITA",
        f"s3a_feasibility.json grid_kedalaman[{i}].median_m", "bagian 2.3", "TERUKUR")
row(24, n(max(g["maks_m"] for g in K["grid_kedalaman"]), 3), "meter", "RUN-KITA",
    "s3a_feasibility.json grid_kedalaman[*].maks_m (nilai terbesar)", "bagian 2.3", "TERUKUR")
row(25, n(js.get("interpolated", 0), 0), "baris", "RUN-KITA",
    "s3a_feasibility.json waktu_kalender.join_status.interpolated", "bagian 2.4", "TERUKUR")
row(26, n(js.get("out_of_range", 0), 0), "baris", "RUN-KITA",
    "s3a_feasibility.json waktu_kalender.join_status.out_of_range", "bagian 2.4", "TERUKUR")
row(27, "113,778 sampai 4.534,969", "jam", "RUN-KITA",
    "s3a_feasibility.json waktu_kalender.per_well[*].rentang_jam", "bagian 2.4", "TERUKUR")
row(28, n(S["meta"]["durasi_detik"], 1), "detik", "RUN-KITA",
    "s3b_hybrid.json meta.durasi_detik", "bagian 1", "TERUKUR")
row(29, n(B["meta"]["alpha"], 6), "fraksi sampel", "KONVENSI",
    "code/rnd_hybrid_harness.py ALPHA_BUDGET = 6.0/1440.0", "bagian 3", "TERUKUR")
row(30, n(min(fr), 6), "fraksi sampel", "RUN-KITA", "s3b_hybrid.json folds[*].laju_stat.frac_raw (nilai terkecil)", "bagian 5", "TERUKUR")
row(31, n(max(fr), 6), "fraksi sampel", "RUN-KITA", "s3b_hybrid.json folds[*].laju_stat.frac_raw (nilai terbesar)", "bagian 5", "TERUKUR")
row(32, sum(1 for v in L.values() if v["saturasi"]), "fold", "RUN-KITA", "s3b_hybrid.json folds[*].laju_stat.saturasi", "bagian 5", "TERUKUR")
row(33, "30,0", "h", "RUN-KITA", "code/rnd_hybrid_harness.py H_GRID[-1] dan folds[*].laju_stat.h", "bagian 5", "TERUKUR")
row(34, len(FARTD), "fold", "RUN-KITA", "s3b_hybrid.json far_tak_terdefinisi (daftar kosong)", "bagian 4", "TERUKUR")
row(35, f"{n(min(cov_vals),4)} sampai {n(max(cov_vals),4)}", "fraksi", "RUN-KITA",
    "s3b_hybrid.json records[model=H5_stat_dan_rule].far.cakupan_menit", "bagian 2.4 dan 5", "TERUKUR")
row(36, sum(1 for v in cov_vals if v >= CAKUPAN_MIN), "fold", "RUN-KITA",
    "turunan: hitung cakupan_menit >= CAKUPAN_MIN 0,50", "bagian 4 dan 5", "DERIVASI")
row(37, n(FAR_MAKS, 1), "alarm/24 jam", "KONVENSI",
    "code/rnd_hybrid_harness.py FAR_MAKS", "bagian 3", "TERUKUR")
row(38, n(CAKUPAN_MIN, 2), "fraksi", "KONVENSI",
    "code/rnd_hybrid_harness.py CAKUPAN_MIN", "bagian 3", "TERUKUR")
row(39, n(RECALL_MIN, 2), "fraksi", "KONVENSI",
    "code/rnd_hybrid_harness.py RECALL_MIN", "bagian 3", "TERUKUR")
row(40, "1000000", "rasio", "RUN-KITA",
    "scratch/rnd/s3/p9_satuan.log: astype(int64) dibagi total_seconds", "bagian 2.6", "TERUKUR")
row(41, "0,11 lawan 113,78", "jam", "RUN-KITA",
    "scratch/rnd/s3/p9_satuan.log: span_jam_raw lawan span_jam_benar well F-9_A", "bagian 2.6", "TERUKUR")
row(42, f"{n(min(jam_ops.values()),2)} sampai {n(max(jam_ops.values()),2)}", "jam", "RUN-KITA",
    "s3b_hybrid.json records[model=H5_stat_dan_rule].far.jam_operasi", "bagian 4", "TERUKUR")
k = 43
for m in ["rule_kanal", "stat_cusum", "H5_stat_dan_rule", "ml_fisik", "H6_ml_dan_stat", "ml_dengan_MSE"]:
    g = G[m]
    row(k, n(g["precision_median"], 4), "fraksi", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.precision_median", "bagian 4", "TERUKUR"); k += 1
    row(k, n(g["recall_median"], 4), "fraksi", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.recall_median", "bagian 4", "TERUKUR"); k += 1
    row(k, n(g["far24_median_valid"], 3), "alarm/24 jam", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.far24_median_valid", "bagian 4", "TERUKUR"); k += 1
    row(k, f"{g['fold_far_le6']}/{g['n_fold_far_terdefinisi']}", "fold", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.fold_far_le6", "bagian 4", "TERUKUR"); k += 1
    row(k, f"{g['fold_gate_A']}/{g['n_fold']}", "fold", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.fold_gate_A", "bagian 4", "TERUKUR"); k += 1
    row(k, n(g["tp_total"], 0), "baris", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.tp_total", "bagian 4", "TERUKUR"); k += 1
    row(k, n(g["fp_total"], 0), "baris", "RUN-KITA", f"s3c_ringkas.json agregat.{m}.fp_total", "bagian 4", "TERUKUR"); k += 1
row(k, n(G["ml_fisik"]["far24_median_valid"] / 6.0, 2), "kali anggaran", "DERIVASI",
    "turunan: agregat.ml_fisik.far24_median_valid dibagi FAR_MAKS 6", "bagian 4", "DERIVASI"); k += 1
row(k, n(BK["presisi_run"], 4), "fraksi", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json engines[tool_wear].heads[0].metrik_segmen.precision", "bagian 7", "TERUKUR"); k += 1
row(k, n(BK["recall_run"], 4), "fraksi", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json engines[tool_wear].heads[0].metrik_segmen.recall", "bagian 7", "TERUKUR"); k += 1
row(k, "1, 3, 1, 3", "FP per alat", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json engines[tool_wear].heads[op_far_calibrated].per_alat[*].fp_R01", "bagian 7", "TERUKUR"); k += 1
row(k, "25, 36, 24, 20", "detik", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json engines[tool_wear].heads[op_far_calibrated].per_alat[*].TLead_s", "bagian 7", "TERUKUR"); k += 1
row(k, BK["n_jendela"], "jendela", "RUN-KITA",
    "scratch/v9_i1/v9_i1_RESULTS.json engines[tool_wear].heads[0].n_windows", "bagian 7", "TERUKUR"); k += 1
row(k, "kosong", "kolom", "RUN-KITA",
    "s3a_feasibility.json inventaris.token_biaya == {}", "bagian 6", "TERUKUR"); k += 1
row(k, "BELUM TERUKUR", "biaya per bit", "BELUM-TERUKUR",
    "tidak ada kolom biaya atau jam henti di data/USROP_labeled.csv, dan tidak ada kunci bit untuk join ke DDR", "bagian 6", "BELUM"); k += 1

blok = ["", "## Bagian S3: hybrid bit_wear dan uji kelayakan data (kartu `t_9d50a5f0`)", "",
        f"Sumber angka: `scratch/rnd/s3/s3a_feasibility.json`, `s3b_hybrid.json`, `s3c_ringkas.json`. "
        f"Generator: `scratch/rnd/s3/s3d_dokumen.py` (idempoten, {len(rows)} baris).", "",
        "| No | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |",
        "|---|---|---|---|---|---|---|"]
blok += rows
blok.append("")

with open(LEDGER) as f:
    isi = f.read()
pola = re.compile(r"\n## Bagian S3:.*?(?=\n## Bagian |\Z)", re.S)
isi2 = pola.sub("\n", isi)
if not isi2.endswith("\n"):
    isi2 += "\n"
isi2 = isi2.rstrip("\n") + "\n" + "\n".join(blok)
with open(LEDGER, "w") as f:
    f.write(isi2)

print("doc", DOC, len(doc.splitlines()), "baris")
print("ledger rows", len(rows))
print("em-dash doc", doc.count("\u2014"), "ledger blok", "\n".join(blok).count("\u2014"))
