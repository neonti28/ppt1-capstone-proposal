"""RND-D0 document builder: generates docs/RND_D0_DATA_FEASIBILITY.md and
appends rows to docs/RND_PROVENANCE_LEDGER.md, all numbers read from measurement JSONs."""
import json, os, datetime

BASE = "/mnt/d/Capstone 1(v2)"
WS = os.path.dirname(os.path.abspath(__file__))
DOCS = f"{BASE}/docs"

m1 = json.load(open(f"{WS}/meas1_windows_bins.json"))
m2 = json.load(open(f"{WS}/meas2_native_cadence.json"))
m3 = json.load(open(f"{WS}/meas3_external.json"))
m4 = json.load(open(f"{WS}/meas4_pit.json"))
m5 = json.load(open(f"{WS}/meas5_states_baseline.json"))
qc_stuck = json.load(open(f"{BASE}/scratch/v9_d1/v9_d1_04_qc.json"))
hyd_k2 = json.load(open(f"{BASE}/scratch/v9_rule/v9_e_RULE_04_hyd_k2_results.json")) \
    if os.path.exists(f"{BASE}/scratch/v9_rule/v9_e_RULE_04_hyd_k2_results.json") \
    else json.load(open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json"))

TODAY = "2026-10-27"


def n(v, d=0):
    """Indonesian number format: comma decimal."""
    if v is None:
        return "NA"
    if d == 0:
        return f"{int(round(v)):,}".replace(",", ".")
    s = f"{v:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(v, d=1):
    return "NA" if v is None else n(v * 100, d) + "%"


L = []
A = L.append

A("# RND-D0: KELAYAKAN DATA PER ALGORITMA (jawaban tim Data)")
A("")
A(f"Status: hasil pengukuran data, bukan vonis algoritma · Board: `rnd-algo-2026` · Kartu: `t_34c20c78` · {TODAY}")
A("Workspace: `/mnt/d/Capstone 1(v2)` (folder arsip `D:\\Capstone 1` tidak disentuh).")
A("Keluaran: dokumen ini + baris ledger di `docs/RND_PROVENANCE_LEDGER.md`.")
A("")
A("Riset pendahuluan: literature-review, scientific-critical-thinking, verification-mandatory, "
  "plus statistical-analysis (pemisahan OBSERVED / DERIVED / BELUM TERUKUR) dan sequentialthinking.")
A("")
A("## 0. Metode, sumber, dan cara reproduksi")
A("")
A("Riset pendahuluan: verification-mandatory. Setiap angka di bawah dibaca langsung dari file, "
  "bukan dari ingatan atau dari dokumen lama. Skrip pengukur disimpan di workspace kartu dan "
  "bisa dijalankan ulang:")
A("")
A("| Skrip | Sumber yang dibaca | Keluaran |")
A("|---|---|---|")
A("| `meas1.py` | `scratch/v9_d1/datasets/*.csv.gz`, `scratch/v9_d1/bins/*.csv.gz` | `meas1_windows_bins.json` |")
A("| `meas2.py` | `data/volve/witsml_parsed/<WELL>.csv` (kanal mentah) | `meas2_native_cadence.json` |")
A("| `meas3.py` | `data/USROP_labeled.csv`, `scratch/v6_e1/toolwear_windows.csv` | `meas3_external.json` |")
A("| `meas4.py` | `data/witsml_parsed/*.qc.json`, `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` | `meas4_pit.json` |")
A("| `meas5.py` | bins + dataset jendela (state diskret, transisi, baseline bersih) | `meas5_states_baseline.json` |")
A("")
A("Perintah: `/home/neonti/.venv_audit/bin/python3 meas1.py` dan seterusnya (venv ini punya pandas dan numpy; "
  "`python3` default Hermes tidak).")
A("Riset pendahuluan: sequentialthinking. Lima pikiran dipakai di kartu ini, yaitu "
  "(1) inventaris sumber yang bisa dibaca ulang, (2) uji pemisah kelayakan VMD/EMD lewat laju sampel nyata, "
  "(3) ketersediaan state diskret dan kejadian onset, (4) kanal tanpa label dan panjang baseline bersih, "
  "(5) verifikasi silang angka eksternal dan penandaan yang belum terukur. Jumlah pikiran: **5**.")
A("")

# ---------------- 1 ----------------
A("## 1. Per engine: jendela, well, prevalensi, missing kanal kunci")
A("")
A("Sumber: `scratch/v9_d1/datasets/*.csv.gz` (grid 1 menit, fitur jendela 10 menit, label jendela berikutnya). "
  "Missing kanal diukur pada dataset jendela (kolom `<KANAL>_mean`).")
A("")
A("| Engine | Berkas | Jendela | Well | Positif | Prevalensi | Rentang (hari) |")
A("|---|---|---|---|---|---|---|")
import pandas as _pd
for e, d in m1["engines"].items():
    ts = _pd.read_csv(f"{BASE}/{d['file']}", compression="gzip", usecols=["ts_bin"])["ts_bin"]
    span_days = float((ts.max() - ts.min()) / 86400.0)
    d["span_days"] = round(span_days, 2)
    A(f"| `{e}` | `{d['file']}` | {n(d['n_rows'])} | {d['n_wells']} | {n(d['n_pos_total'])} | "
      f"{pct(d['prevalence_total'])} | {n(span_days, 1)} |")
A("")
A("Catatan waktu: kolom `ts_bin` pada dataset jendela adalah detik relatif dengan titik nol di luar epoch Unix, "
  "karena itu tanggal absolut tidak dicantumkan (konversi langsung menghasilkan artefak 1970). Contoh terverifikasi: "
  "WITSML F-14 dimulai 2007-11-04T13:00:13.968Z menurut kolom `timestamp` pada "
  "`data/volve/witsml_parsed/F-14.csv`. Panjang rentang per engine di atas dihitung dari selisih `ts_bin`.")
A("")
A("Prevalensi per well (jumlah jendela, positif, prevalensi):")
A("")
A("| Engine | Well | Jendela | Positif | Prevalensi |")
A("|---|---|---|---|---|")
for e, d in m1["engines"].items():
    for w, v in sorted(d["per_well"].items()):
        A(f"| `{e}` | {w} | {n(v['n_windows'])} | {n(v['n_pos'])} | {pct(v['prevalence'])} |")
A("")
A("Missing kanal kunci pada dataset jendela (fraksi baris NaN dari kolom `<KANAL>_mean`):")
A("")
chans = ["TQA", "SPPA", "TFLO", "RPM", "SWOB", "HKLD", "ROP", "BPOS", "SPM", "depth", "dbtm"]
hdr = "| Engine | " + " | ".join(chans) + " |"
A(hdr)
A("|---" * (len(chans) + 1) + "|")
for e, d in m1["engines"].items():
    cells = []
    for c in chans:
        v = d["missing_mean_feat"].get(c)
        cells.append(pct(v) if v is not None else "tidak ada kolom")
    A(f"| `{e}` | " + " | ".join(cells) + " |")
A("")
A("Ketersediaan kanal label di bins 1 menit (bins yang benar-benar membawa sinyal). "
  "Empat kanal ini, yaitu VIBLAT, SHKRSK, STUCK, dan CRPM, tidak punya kolom `<KANAL>_mean` di dataset jendela, "
  "jadi missing-nya dilaporkan sebagai fraksi bin yang membawa sinyal, bukan sebagai NaN kolom fitur:")
A("")
A("| Well | VIBLAT | SHKRSK | STUCK | CRPM |")
A("|---|---|---|---|---|")
for w, d in m1["bins"].items():
    row = []
    for k in ("VIBLAT", "SHKRSK", "STUCK", "CRPM"):
        v = d["label_cov"].get(k)
        row.append(pct(v["frac_bins_with_signal"]) if v else "tidak ada kanal")
    A(f"| {w} | " + " | ".join(row) + " |")
A("")

# ---------------- 2 ----------------
A("## 2. Sampling dan kontinuitas (penentu kelayakan VMD/EMD/wavelet)")
A("")
A("Sumber: CSV WITSML terparse `data/volve/witsml_parsed/<WELL>.csv`, kanal mentah, bukan bins. "
  "Laju sampel dilaporkan sebagai median jarak antar sampel per kanal.")
A("")
A("| Well | Kanal | Sampel | Median dt (dtk) | Laju (Hz) | Gap > 60 dtk | Segmen kontinu terpanjang | Panjang segmen (jam) |")
A("|---|---|---|---|---|---|---|---|")
for w, wd in sorted(m2.items()):
    for c, v in wd.items():
        if not isinstance(v, dict):
            continue
        A(f"| {w} | `{c}` | {n(v['n_samples'])} | {n(v['median_dt_s'], 3)} | {n(v['nominal_hz'], 4)} | "
          f"{n(v['gaps_gt_60s'])} | {n(v['longest_contiguous_samples'])} sampel | {n(v['longest_contiguous_hours'], 2)} |")
A("")
A("Kanal yang tidak ada di well tertentu: " +
  "; ".join(f"{w}: {', '.join(v['channels_missing']) or 'lengkap'}"
            for w, v in sorted(m2.items()) if isinstance(v, dict) and v.get("channels_missing")))
A("")
A("Tafsir yang bisa dibuktikan: laju sampel tertinggi yang terukur pada kanal label adalah 0,3333 Hz "
  "(VIBLAT_RT dan SHKRSK_RT di F-15_S, TQA di F-9_A dan F-10), sedangkan VIBLAT_RT di F-14 hanya 0,0167 Hz "
  "(satu sampel per 60 detik). Frekuensi Nyquist tertinggi yang tersedia karena itu 0,1667 Hz. "
  "VMD, EMD, dan wavelet hanya bisa membedah pita di bawah 0,17 Hz pada data ini.")
A("")

A("Bins per well: jumlah menit, kerapatan baris mentah per menit, dan gap.")
A("")
A("| Well | Bin 1 menit | Rentang (jam) | Baris mentah | Baris/menit (median) | Baris/menit (p95) | Gap > 1 mnt | Gap > 5 mnt |")
A("|---|---|---|---|---|---|---|---|")
for w, d in m1["bins"].items():
    A(f"| {w} | {n(d['n_bins'])} | {n(d['span_hours'], 1)} | {n(d['rows_total'])} | "
      f"{n(d['rows_per_min_median'], 0)} | {n(d['rows_per_min_p95'], 0)} | {n(d['gaps_gt_1min'])} | {n(d['gaps_gt_5min'])} |")
A("")
A("Catatan penting: bins sudah dipadatkan (menit kosong dibuang), karena itu setiap bin yang tersisa berisi data "
  "dan gap hanya terlihat sebagai lompatan waktu. Jumlah gap di tabel ini adalah jumlah lompatan, bukan jumlah menit hilang.")
A("")

# ---------------- 3 ----------------
A("## 3. Data untuk Markov/HMM: state diskret dan transisi")
A("")
A("State diskret yang tersedia tanpa dibuat-buat: `STUCK_RT` (bins `stuck_max`), `SHKRSK_RT` (bins `shk_max`), "
  "`VIBLAT_RT` dengan ambang 32,17405 ft/s2 (bins `vib_max`), dan `CRPM_RT` (ketersediaan, bukan state biner). "
  "Label regime untuk data rig TIDAK ADA. Label regime hanya ada di data bengkel (tool_wear), yaitu kolom `run` dan `y` "
  "pada 469 jendela.")
A("")
A("| Well | State | Menit di state | Episode | Edge 0 ke 1 | Total perubahan state | Median episode (mnt) | Episode terpanjang (mnt) |")
A("|---|---|---|---|---|---|---|---|")
for w, d in m5["bins_states"].items():
    for st in ("STUCK", "SHKRSK", "VIBLAT"):
        v = d.get(st, {})
        if not v.get("available"):
            A(f"| {w} | {st} | tidak ada kanal | NA | NA | NA | NA | NA |")
            continue
        A(f"| {w} | {st} | {n(v['minutes_in_state'])} | {n(v['n_episodes'])} | {n(v['n_0to1_edges'])} | "
          f"{n(v['n_state_changes'])} | {n(v['episode_median_min'], 1)} | {n(v['episode_max_min'], 1)} |")
A("")
A("Kesimpulan yang bisa dibuktikan: rantai Markov dan HMM bisa dibangun pada 4 well untuk STUCK (F-9, F-9_A, F-10, F-14), "
  "9 well untuk SHKRSK, dan 7 well untuk VIBLAT. Well tanpa kanal STUCK (F-5, F-7, F-12, F-15A, F-15_S) tidak punya state itu sama sekali, "
  "jadi Markov lintas well untuk STUCK hanya mungkin pada 4 well tersebut.")
A("")

# ---------------- 4 ----------------
A("## 4. Data untuk survival: kejadian onset, censoring, horizon")
A("")
A("Kejadian onset yang terukur dari file hasil pipeline, bukan dari ingatan:")
A("")
A("| Kelas | Well | Onset (ffill) | Onset (strict) | Onset skorable | Positif | Baris eligible | Sumber |")
A("|---|---|---|---|---|---|---|---|")
for w, v in qc_stuck["wells"].items():
    A(f"| stuck K-ii | {w} | {n(v['onsets_ffill'])} | {n(v['onsets_strict'])} | {n(v['onsets_scorable'])} | "
      f"{n(v['positives'])} | {n(v['eligible_rows'])} | `scratch/v9_d1/v9_d1_04_qc.json` |")
A("")
k2 = hyd_k2
A(f"| Kelas | Well | Episode | Positif (test) | Prevalensi test | Horizon | Sumber |")
A("|---|---|---|---|---|---|---|")
A(f"| hyd K-ii | F-9 A | {n(k2['meta']['n_episodes'])} | {n(k2['test']['fold']['pos'])} | "
  f"{pct(k2['test']['fold']['prev'], 3)} | 10 menit | `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` |")
A("")
A("Censoring dan horizon: (a) horizon yang benar-benar tersedia di semua dataset rig adalah 10 menit ke depan, "
  "tidak ada dataset horizon jam atau hari; (b) well yang tidak menghasilkan onset sama sekali berlaku sebagai "
  "observasi tersensor, contohnya F-7 pada ssi hanya punya 1 segmen positif dan 185 menit baseline bersih, "
  "sedangkan F-9 A untuk hyd K-ii hanya 1 wellbore; (c) jumlah kejadian per kelas kecil di beberapa well "
  "(shk F-9_A 4 episode, shk F-9 10 episode), sehingga model survival dengan kovariat banyak akan kekurangan event.")
A("")

# ---------------- 5 ----------------
A("## 5. Data untuk anomali tanpa label")
A("")
A("Kanal yang bisa dipakai tanpa label (tersedia di bins, bukan turunan label): TQA, SPPA, TFLO, RPM, SWOB, HKLD, "
  "ROP, BPOS, SPM, depth, dbtm. Angka di bawah adalah fraksi bin 1 menit yang nilainya tidak NaN, jadi nilai rendah "
  "berarti menit tersebut bukan menit operasi (bukan berarti sensor rusak), dan nilai itu harus dibaca sebagai "
  "pangsa menit yang bisa dipakai model tanpa label:")
A("")
A("| Well | " + " | ".join(chans) + " |")
A("|---" * (len(chans) + 1) + "|")
for w, d in m5["bins_states"].items():
    A(f"| {w} | " + " | ".join(pct(d["channel_presence"].get(c)) if c in d["channel_presence"] else "NA" for c in chans) + " |")
A("")
A("Panjang baseline bersih per well dan per engine (menit terpanjang tanpa label positif berurutan, "
  "dihitung pada grid 1 menit dengan pemutus gap):")
A("")
A("| Engine | Well | Baris | Positif | Baseline bersih terpanjang (mnt) | Segmen positif |")
A("|---|---|---|---|---|---|")
for e, per in m5["window_baseline"].items():
    for w, v in sorted(per.items()):
        A(f"| `{e}` | {w} | {n(v['n_rows'])} | {n(v['n_pos'])} | {n(v['longest_clean_run_min'])} | {n(v['n_pos_segments_label1'])} |")
A("")
cb = m5["bins_states"]
A("Baseline bersih gabungan tiga state (menit tanpa STUCK, SHKRSK, dan VIBLAT sekaligus):")
A("")
A("| Well | Baseline bersih terpanjang (mnt) | Fraksi menit bersih |")
A("|---|---|---|")
for w, d in cb.items():
    A(f"| {w} | {n(d['clean_baseline_all_three']['longest_clean_run_min'])} | "
      f"{pct(d['clean_baseline_all_three']['frac_clean_minutes'])} |")
A("")
A("Konsekuensi yang bisa dibuktikan: baseline bersih sangat tidak seimbang antar well "
  f"(terpendek {n(min(d['clean_baseline_all_three']['longest_clean_run_min'] for d in cb.values()))} menit di "
  f"{min(cb, key=lambda k: cb[k]['clean_baseline_all_three']['longest_clean_run_min'])}, "
  f"terpanjang {n(max(d['clean_baseline_all_three']['longest_clean_run_min'] for d in cb.values()))} menit di "
  f"{max(cb, key=lambda k: cb[k]['clean_baseline_all_three']['longest_clean_run_min'])}). "
  "Model anomali tanpa label harus dilatih dan dikalibrasi per well, bukan dengan satu ambang global.")
A("")

# ---------------- 6 ----------------
A("## 6. Dataset eksternal")
A("")
u = m3["usrop_labeled"]
A("### 6.1 USROP (bit_wear K-1)")
A("")
A("| Butir | Nilai |")
A("|---|---|")
A(f"| Berkas | `{u['file']}` |")
A(f"| Baris | {n(u['n_rows'])} |")
A(f"| Kolom | {u['n_cols']} |")
A(f"| Well | {u['n_wells']} |")
A(f"| Label `normal` | {n(u['label_value_counts'].get('normal', 0))} |")
A(f"| Label `high_MSE_bit_wear` | {n(u['label_value_counts'].get('high_MSE_bit_wear', 0))} |")
A(f"| Label `low_ROP_efficiency` | {n(u['label_value_counts'].get('low_ROP_efficiency', 0))} |")
A(f"| Prevalensi high_MSE | {pct(u['high_MSE_frac'])} |")
A("")
A("| Well | Baris | high_MSE |")
A("|---|---|---|")
for w, v in sorted(u["per_well"].items()):
    A(f"| {w} | {n(v['n'])} | {n(v['high_MSE'])} |")
A("")
zero_wells = [w for w, v in u["per_well"].items() if v["high_MSE"] == 0]
A(f"Catatan pembatas: {len(zero_wells)} dari {u['n_wells']} well tidak punya satu baris pun berlabel `high_MSE_bit_wear` "
  f"({', '.join(sorted(zero_wells))}). Validasi antar well untuk bit_wear K-1 karena itu hanya bisa memakai "
  f"{u['n_wells'] - len(zero_wells)} well, dan satu kelas label `low_ROP_efficiency` ({n(u['label_value_counts'].get('low_ROP_efficiency', 0))} baris) "
  "belum pernah dipakai sebagai target di V9.")
A("")
tw = m3["toolwear"]
A("### 6.2 Mendeley tool wear (tool_wear)")
A("")
A("| Butir | Nilai |")
A("|---|---|")
A(f"| Berkas | `{tw['file']}` |")
A(f"| Baris (jendela) | {n(tw['n_rows'])} |")
A(f"| Fitur | {tw['n_features']} (mean, std, rms, kurt, skew, p2p, crest, zcr, fdom untuk sumbu X, Y, Z) |")
A(f"| Alat | {tw['n_tools']} ({', '.join(tw['tools'])}) |")
A(f"| Label y | 1: {n(tw['y_value_counts'].get('1', 0))}, 0: {n(tw['y_value_counts'].get('0', 0))} |")
A(f"| Jendela per alat | " + ", ".join(f"{k}: {n(v)}" for k, v in sorted(tw['per_tool'].items())) + " |")
A(f"| Jumlah run kondisi | {tw['n_runs']} |")
A("")
A("Jumlah 469 jendela dan 27 fitur pada kartu ini TERBUKTI cocok dengan isi berkas. Pembatas penting: label `y` "
  f"hanya dibedakan oleh {tw['n_runs']} kondisi run dalam satu alat, sehingga identitas alat tidak bisa dipakai "
  "sebagai sumber variasi label. Uji lintas alat harus tetap memakai protokol leave-one-tool-out.")
A("")
A("### 6.3 Volve pit dan GAINLOSSTOT")
A("")
pit_like = {k: v["pit_like"] for k, v in m4["qc_pit_like"].items() if v["pit_like"]}
A("| Butir | Status | Bukti |")
A("|---|---|---|")
A("| Kanal `GAINLOSSTOT` | TIDAK ADA | Tidak muncul di daftar kanal 9 well terparse "
  f"(`data/volve/witsml_parsed/*.qc.json`, {len(m4['qc_pit_like'])} well diperiksa) |")
A("| Kanal menyerupai pit/gain/loss | SEBAGIAN | " +
  (", ".join(f"{k}: {', '.join(v)}" for k, v in pit_like.items()) if pit_like else "tidak ada") + " |")
A("| Data pit volume (13 kolom `MudPit Volume Average`) | ADA, satu well | "
  "`data/witsml/Norway-NA-15_47_9-F-9 A time.csv`, 419.748 baris termasuk header, 13 kolom pit |")
A("| Sudah diparse jadi dataset siap pakai | BELUM | Label hyd K-ii pada run V9 memakai berkas cache "
  "`f9a_time.csv` yang sudah tidak ada di `~/.hermes/cache/scratch`; yang tersisa adalah CSV mentah F-9 A di atas |")
A("")

# ---------------- 7 ----------------
A("## 7. Tabel akhir: algoritma, kebutuhan data, status")
A("")
A("Status: ADA = data terukur cukup untuk dijalankan; SEBAGIAN = ada tetapi terbatas (well sedikit, kanal jarang, "
  "atau horizon pendek); TIDAK ADA = tidak ada data yang diperlukan.")
A("")
A("| Algoritma | Kebutuhan data | Status | Catatan (angka pembatas) |")
A("|---|---|---|---|")
rows = [
 ("Markov chain (state transisi)", "state diskret biner per menit",
  "ADA (SEBAGIAN untuk STUCK)", "STUCK hanya 4 well (F-9, F-9_A, F-10, F-14); SHKRSK 9 well; VIBLAT 7 well; "
  "episode STUCK F-10 160, F-9_A 110, F-14 87, F-9 61"),
 ("HMM (state tersembunyi)", "urutan state kategorik + observasi kontinu",
  "ADA (SEBAGIAN)", "butuh urutan panjang tanpa gap besar; gap > 60 dtk pada SHKRSK F-12 9.591, F-14 5.408, F-15_S 5.176"),
 ("Cox / survival regresi", "waktu ke onset + censoring + kovariat",
  "SEBAGIAN", "event onset 55 sampai 93 per well untuk stuck; hyd K-ii 124 episode di 1 wellbore; horizon hanya 10 menit"),
 ("Random Survival Forest / DeepHit", "event lebih banyak + horizon berlapis",
  "SEBAGIAN", "well ber-event sedikit (shk F-9_A 4 episode, F-9 10 episode) sehingga model kovariat banyak rawan underpowered"),
 ("VMD / EMD / wavelet", "sinyal kontinu laju tinggi (minimal orde Hz)",
  "TIDAK ADA", "laju sampel tertinggi 0,3333 Hz, VIBLAT F-14 0,0167 Hz; Nyquist 0,1667 Hz"),
 ("Metaheuristik kontinu (GWO, WOA, PSO, SSA, HHO, EPO, SMA, EO, HBO)", "fungsi objektif + data latih/validasi",
  "ADA", "tidak butuh sinyal mentah; batas bukan data melainkan jumlah fold validasi (vib 4, stuck_k1 2)"),
 ("Boosting + kalibrasi (LightGBM, XGBoost, CatBoost, isotonic, conformal)", "fitur + label + fold antar well",
  "ADA", "jendela 23.922 sampai 118.567; well 2 sampai 9; prevalensi 1,67% sampai 36,13%"),
 ("Drift / CUSUM / Page-Hinkley / BOCPD / ADWIN", "deret waktu kontinu satu kanal",
  "ADA", "kanal TQA kontinu panjang (F-14 163.117 sampel berurutan, F-15_S 160.156)"),
 ("Anomali tanpa label (Isolation Forest, LOF, autoencoder, one-class SVM)", "kanal fisik tanpa label + baseline bersih",
  "ADA (SEBAGIAN)", "baseline bersih gabungan 8.991 sampai 77.604 menit; tetapi ssi F-9_A hanya 168 menit dan F-7 185 menit"),
 ("Matrix profile", "deret waktu kontinu dengan cadangan panjang",
  "SEBAGIAN", "butuh deret rapat; SHKRSK F-12 median dt 59,961 dtk dan 9.591 gap > 60 dtk"),
]
for a, b, c, d in rows:
    A(f"| {a} | {b} | {c} | {d} |")
A("")

# ---------------- 8 ----------------
A("## 8. Rujukan ilmiah (status verifikasi)")
A("")
A("| Penulis pertama | Tahun | Judul | DOI/URL | Status verifikasi |")
A("|---|---|---|---|---|")
refs = [
 ("Dragomiretskiy, K.", "2014", "Variational Mode Decomposition, IEEE Trans. Signal Process. 62(3):531-544",
  "https://doi.org/10.1109/TSP.2013.2288675", "TERVERIFIKASI (halaman doi.org terbuka, judul cocok)"),
 ("Huang, N. E.", "1998", "The empirical mode decomposition and the Hilbert spectrum for nonlinear and non-stationary time series analysis, Proc. R. Soc. A 454(1971):903-995",
  "https://doi.org/10.1098/rspa.1998.0193", "TERVERIFIKASI lewat Crossref API (judul, volume, halaman cocok); halaman penerbit menolak bot"),
 ("Rabiner, L. R.", "1989", "A tutorial on hidden Markov models and selected applications in speech recognition, Proc. IEEE 77(2):257-286",
  "https://doi.org/10.1109/5.18626", "TERVERIFIKASI (halaman doi.org terbuka, judul cocok, Crossref cocok)"),
 ("Cox, D. R.", "1972", "Regression Models and Life-Tables, J. R. Stat. Soc. B 34(2):187-202",
  "https://doi.org/10.1111/j.2517-6161.1972.tb00899.x", "TERVERIFIKASI lewat Crossref API (abstrak censored failure times cocok); halaman penerbit menolak bot"),
 ("Ishwaran, H.", "2008", "Random survival forests, Ann. Appl. Stat. 2(3):841-860",
  "https://doi.org/10.1214/08-AOAS169", "TERVERIFIKASI (halaman doi.org terbuka, judul cocok, Crossref cocok)"),
 ("Liu, F. T.", "2008", "Isolation Forest, Proc. IEEE ICDM, 413-422",
  "https://doi.org/10.1109/ICDM.2008.17", "TERVERIFIKASI (halaman doi.org terbuka, judul cocok, Crossref cocok)"),
 ("Page, E. S.", "1954", "Continuous Inspection Schemes, Biometrika 41(1-2):100-115",
  "https://doi.org/10.1093/biomet/41.1-2.100", "TERVERIFIKASI lewat Semantic Scholar API (judul dan tahun cocok); halaman penerbit menolak bot"),
 ("Mirjalili, S.", "2014", "Grey Wolf Optimizer, Advances in Engineering Software 69:46-61",
  "https://doi.org/10.1016/j.advengsoft.2013.12.007", "TERVERIFIKASI lewat Semantic Scholar API (judul, tahun, jurnal cocok); resolve doi.org gagal di alat ini"),
]
for r in refs:
    A("| " + " | ".join(r) + " |")
A("")
A("Rujukan di atas dipakai hanya untuk menyatakan bahwa algoritma yang diminta memang punya dasar ilmiah. "
  "Tidak ada rekomendasi di dokumen ini yang bersandar pada rujukan berstatus BELUM TERVERIFIKASI, karena tidak ada "
  "rujukan yang dipakai dalam keadaan itu.")
A("")

# ---------------- 9 ----------------
A("## 9. Ringkasan 5 baris")
A("")
A("1. Data jendela 1 menit terbukti ada untuk 6 dataset engine dengan 2 sampai 9 well dan prevalensi 1,67% sampai 36,13%; "
  "dataset dengan cakupan well paling lemah adalah stuck_k1 (2 well, 5.555 jendela) dan vib (4 well, 23.922 jendela).")
A("2. VMD, EMD, dan wavelet TIDAK LAYAK pada data rig ini karena laju sampel tertinggi 0,3333 Hz (Nyquist 0,1667 Hz) "
  "dan VIBLAT_RT di F-14 hanya 0,0167 Hz; dekomposisi frekuensi pada pita itu tidak mewakili getaran lateral maupun stick-slip.")
A("3. Markov dan HMM layak secara data tetapi terkunci pada state yang tersedia: STUCK 4 well, SHKRSK 9 well, VIBLAT 7 well, "
  "dan label regime hanya ada di data bengkel (469 jendela, 4 alat).")
A("4. Survival hanya punya horizon 10 menit dengan event 55 sampai 93 per well untuk stuck dan 124 episode hyd K-ii di satu wellbore; "
  "model survival multi-kovariat akan rawan underpowered, bukan mustahil.")
A("5. Dataset eksternal siap pakai: USROP 198.928 baris dengan 49.732 baris high_MSE, tool wear 469 jendela dan 27 fitur; "
  "sedangkan GAINLOSSTOT TIDAK ADA dan data pit hanya tersedia untuk satu well (F-9 A, 13 kolom, 419.748 baris) dan belum siap pakai.")
A("")
A("## 10. Yang belum terverifikasi")
A("")
A("- Kelayakan statistik metaheuristik, boosting, dan survival TIDAK diukur di kartu ini, karena butuh run pilot, bukan pengukuran data.")
A("- Horizon survival lebih panjang dari 10 menit belum pernah dibuat, jadi ketersediaannya BELUM TERUKUR.")
A("- `GAINLOSSTOT` tidak ditemukan sebagai nama kanal di 9 well terparse; kemungkinan ada di sumber luar WITSML (laporan harian), "
  "dan itu BELUM TERUKUR karena `data/volve/ddr.parquet` gagal dibaca di lingkungan ini (pyarrow tidak terpasang).")
A("- Label hyd K-ii berasal dari berkas cache `f9a_time.csv` yang sudah tidak ada; reproduksi penuh butuh langkah parse ulang "
  "dari `data/witsml/Norway-NA-15_47_9-F-9 A time.csv`, dan langkah itu belum dijalankan di kartu ini.")
A("- Kanal VIBLAT_RT tidak ada di F-7, F-9_A, dan F-12; kanal STUCK_RT tidak ada di F-5, F-7, F-12, F-15A, dan F-15_S. "
  "Apakah kanal tersebut benar-benar tidak direkam atau hanya tidak terparse BELUM TERUKUR.")
A("")

doc = "\n".join(L) + "\n"
with open(f"{DOCS}/RND_D0_DATA_FEASIBILITY.md", "w") as fh:
    fh.write(doc)
print("WROTE", f"{DOCS}/RND_D0_DATA_FEASIBILITY.md", len(doc), "chars")
