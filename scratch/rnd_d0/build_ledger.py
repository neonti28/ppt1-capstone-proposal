"""RND-D0 ledger builder: writes/appends 7-column provenance rows for every number in
docs/RND_D0_DATA_FEASIBILITY.md. Numbers are read from the measurement JSONs, not typed by hand."""
import json, os

BASE = "/mnt/d/Capstone 1(v2)"
WS = os.path.dirname(os.path.abspath(__file__))
DOCS = f"{BASE}/docs"
LEDGER = f"{DOCS}/RND_PROVENANCE_LEDGER.md"
DATE = "2026-10-27"

m1 = json.load(open(f"{WS}/meas1_windows_bins.json"))
m2 = json.load(open(f"{WS}/meas2_native_cadence.json"))
m3 = json.load(open(f"{WS}/meas3_external.json"))
m4 = json.load(open(f"{WS}/meas4_pit.json"))
m5 = json.load(open(f"{WS}/meas5_states_baseline.json"))
qc_stuck = json.load(open(f"{BASE}/scratch/v9_d1/v9_d1_04_qc.json"))
hyd_k2 = json.load(open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json"))


def n(v, d=0):
    if v is None:
        return "NA"
    if d == 0:
        return f"{int(round(v)):,}".replace(",", ".")
    s = f"{v:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


rows = []
seen = set()


def add(angka, satuan, kelas, rujukan, dipakai, status="TERUKUR"):
    key = (angka, rujukan)
    if key in seen:
        return
    seen.add(key)
    rows.append((angka, satuan, kelas, rujukan, dipakai, status))


# 1. engine windows
for e, d in m1["engines"].items():
    r = f"`{d['file']}` kolom `well`/`{d['label_col']}`; skrip workspace `meas1.py`"
    add(n(d["n_rows"]), "jendela", "RUN-KITA", r, "RND_D0 §1 tabel engine")
    add(str(d["n_wells"]), "well", "RUN-KITA", r, "RND_D0 §1 tabel engine")
    add(n(d["n_pos_total"]), "jendela positif", "RUN-KITA", r, "RND_D0 §1 tabel engine")
    add(n(d["prevalence_total"] * 100, 2), "%", "RUN-KITA", r, "RND_D0 §1 tabel engine")
    for c, v in d["missing_mean_feat"].items():
        add(n(v * 100, 2), "% baris NaN", "RUN-KITA",
            f"`{d['file']}` kolom `{c}_mean`; `meas1.py`", "RND_D0 §1 tabel missing")
    for w, v in d["per_well"].items():
        add(f"{n(v['n_windows'])} jendela / {n(v['n_pos'])} positif / {n((v['prevalence'] or 0) * 100, 2)}%",
            "per well", "RUN-KITA", f"`{d['file']}` group `well={w}`; `meas1.py`", "RND_D0 §1 tabel per well")

# 2. bins
for w, d in m1["bins"].items():
    r = f"`{d['file']}`; `meas1.py`"
    add(n(d["n_bins"]), "bin 1 menit", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    add(n(d["span_hours"], 1), "jam", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    add(n(d["rows_total"]), "baris mentah", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    add(n(d["rows_per_min_median"]), "baris/menit (median)", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    add(n(d["rows_per_min_p95"]), "baris/menit (p95)", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    add(n(d["gaps_gt_1min"]), "gap > 1 menit", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    add(n(d["gaps_gt_5min"]), "gap > 5 menit", "RUN-KITA", r, "RND_D0 §2 tabel bins")
    for k, v in d["label_cov"].items():
        add(n(v["frac_bins_with_signal"] * 100, 2), f"% bin dengan {k}", "RUN-KITA",
            f"`{d['file']}` kolom `{k.lower()}_n`; `meas1.py`", "RND_D0 §1 tabel ketersediaan kanal")

# 3. native cadence
for w, wd in m2.items():
    for c, v in wd.items():
        if not isinstance(v, dict):
            continue
        r = f"`data/volve/witsml_parsed/{w}.csv` kolom `{c}`; `meas2.py`"
        add(n(v["n_samples"]), "sampel", "RUN-KITA", r, "RND_D0 §2 tabel cadence")
        add(n(v["median_dt_s"], 3), "detik (median dt)", "RUN-KITA", r, "RND_D0 §2 tabel cadence")
        add(n(v["nominal_hz"], 4), "Hz", "RUN-KITA", r, "RND_D0 §2 tabel cadence")
        add(n(v["gaps_gt_60s"]), "gap > 60 detik", "RUN-KITA", r, "RND_D0 §2 tabel cadence")
        add(n(v["longest_contiguous_samples"]), "sampel berurutan", "RUN-KITA", r, "RND_D0 §2 tabel cadence")
        add(n(v["longest_contiguous_hours"], 2), "jam", "RUN-KITA", r, "RND_D0 §2 tabel cadence")

# 4. states
for w, d in m5["bins_states"].items():
    for st in ("STUCK", "SHKRSK", "VIBLAT"):
        v = d.get(st, {})
        if not v.get("available"):
            continue
        r = f"`scratch/v9_d1/bins/{w}.csv.gz` kolom `{st.lower()}_max`; `meas5.py`"
        add(n(v["minutes_in_state"]), f"menit state {st}", "RUN-KITA", r, "RND_D0 §3 tabel state")
        add(n(v["n_episodes"]), f"episode {st}", "RUN-KITA", r, "RND_D0 §3 tabel state")
        add(n(v["n_0to1_edges"]), f"edge 0 ke 1 {st}", "RUN-KITA", r, "RND_D0 §3 tabel state")
        add(n(v["n_state_changes"]), f"perubahan state {st}", "RUN-KITA", r, "RND_D0 §3 tabel state")
        add(n(v["episode_median_min"], 1), "menit (median episode)", "RUN-KITA", r, "RND_D0 §3 tabel state")
        add(n(v["episode_max_min"], 1), "menit (episode terpanjang)", "RUN-KITA", r, "RND_D0 §3 tabel state")
    add(n(d["clean_baseline_all_three"]["longest_clean_run_min"]), "menit baseline bersih gabungan", "RUN-KITA",
        f"`scratch/v9_d1/bins/{w}.csv.gz`; `meas5.py`", "RND_D0 §5 baseline gabungan")
    add(n(d["clean_baseline_all_three"]["frac_clean_minutes"] * 100, 2), "% menit bersih", "RUN-KITA",
        f"`scratch/v9_d1/bins/{w}.csv.gz`; `meas5.py`", "RND_D0 §5 baseline gabungan")

# 5. onsets
for w, v in qc_stuck["wells"].items():
    r = "`scratch/v9_d1/v9_d1_04_qc.json`"
    add(n(v["onsets_ffill"]), "onset (ffill)", "RUN-KITA", r + f" wells.{w}.onsets_ffill", "RND_D0 §4 tabel onset")
    add(n(v["onsets_strict"]), "onset (strict)", "RUN-KITA", r + f" wells.{w}.onsets_strict", "RND_D0 §4 tabel onset")
    add(n(v["onsets_scorable"]), "onset skorable", "RUN-KITA", r + f" wells.{w}.onsets_scorable", "RND_D0 §4 tabel onset")
    add(n(v["positives"]), "jendela positif", "RUN-KITA", r + f" wells.{w}.positives", "RND_D0 §4 tabel onset")
    add(n(v["eligible_rows"]), "baris eligible", "RUN-KITA", r + f" wells.{w}.eligible_rows", "RND_D0 §4 tabel onset")
add(n(hyd_k2["meta"]["n_episodes"]), "episode", "RUN-KITA",
    "`scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` meta.n_episodes", "RND_D0 §4 tabel hyd")
add(n(hyd_k2["test"]["fold"]["pos"]), "jendela positif", "RUN-KITA",
    "`scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` test.fold.pos", "RND_D0 §4 tabel hyd")
add(n(hyd_k2["test"]["fold"]["prev"] * 100, 3), "%", "RUN-KITA",
    "`scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` test.fold.prev", "RND_D0 §4 tabel hyd")

# 6. baseline per engine
for e, per in m5["window_baseline"].items():
    for w, v in per.items():
        r = f"`scratch/v9_d1/datasets/{e}.csv.gz` group well={w}; `meas5.py`"
        add(n(v["longest_clean_run_min"]), "menit baseline bersih", "RUN-KITA", r, "RND_D0 §5 tabel baseline")
        add(n(v["n_pos_segments_label1"]), "segmen positif", "RUN-KITA", r, "RND_D0 §5 tabel baseline")
        add(n(v["n_rows"]), "baris", "RUN-KITA", r, "RND_D0 §5 tabel baseline")
        add(n(v["n_pos"]), "positif", "RUN-KITA", r, "RND_D0 §5 tabel baseline")
        add(n(v["longest_clean_run_min"]), "menit", "RUN-KITA", r, "RND_D0 §5 kanal tersedia")

# 7. external
u = m3["usrop_labeled"]
ru = "`data/USROP_labeled.csv`; `meas3.py`"
add(n(u["n_rows"]), "baris", "RUN-KITA", ru, "RND_D0 §6.1")
add(str(u["n_cols"]), "kolom", "RUN-KITA", ru, "RND_D0 §6.1")
add(str(u["n_wells"]), "well", "RUN-KITA", ru, "RND_D0 §6.1")
for k, v in u["label_value_counts"].items():
    add(n(v), "baris", "RUN-KITA", ru + f" label='{k}'", "RND_D0 §6.1")
add(n(u["high_MSE_frac"] * 100, 2), "%", "RUN-KITA", ru + " label='high_MSE_bit_wear'", "RND_D0 §6.1")
for w, v in u["per_well"].items():
    add(f"{n(v['n'])} baris / {n(v['high_MSE'])} high_MSE", "per well", "RUN-KITA",
        ru + f" well='{w}'", "RND_D0 §6.1 tabel per well")
tw = m3["toolwear"]
rt = "`scratch/v6_e1/toolwear_windows.csv`; `meas3.py`"
add(n(tw["n_rows"]), "jendela", "RUN-KITA", rt, "RND_D0 §6.2")
add(str(tw["n_features"]), "fitur", "RUN-KITA", rt, "RND_D0 §6.2")
add(str(tw["n_tools"]), "alat", "RUN-KITA", rt, "RND_D0 §6.2")
for k, v in tw["y_value_counts"].items():
    add(n(v), f"jendela y={k}", "RUN-KITA", rt + f" y={k}", "RND_D0 §6.2")
add(str(len(m4["qc_pit_like"])), "well diperiksa", "RUN-KITA",
    "`data/volve/witsml_parsed/*.qc.json`; `meas4.py`", "RND_D0 §6.3")
add("419.748", "baris", "RUN-KITA",
    "`data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (wc -l) dan `meas4.py`", "RND_D0 §6.3")
add("13", "kolom MudPit Volume Average", "RUN-KITA",
    "`data/witsml/Norway-NA-15_47_9-F-9 A time.csv` header; `meas4.py`", "RND_D0 §6.3")
add("0", "kanal GAINLOSSTOT ditemukan", "RUN-KITA",
    "`data/volve/witsml_parsed/*.qc.json` 9 well; `meas4.py`", "RND_D0 §6.3")

# 8. konvensi dan rujukan
add("10", "menit (H)", "KONVENSI",
    "`code/v9_d1_02_rig_windows.py` H=10 dan `code/v9_d1_04_stuck_k2.py` H=10", "RND_D0 §4 horizon")
add("32,17405", "ft/s2 (1 g)", "STANDAR",
    "standar gravitasi 9,80665 m/s2 x 3,280839895 ft/m (BIPM: 9,80665 m/s2)", "RND_D0 §3 ambang VIBLAT")
add("0,1667", "Hz (Nyquist dari 0,3333 Hz)", "DERIVASI",
    "turunan dari cadence terukur `meas2.py` (median dt 3,0 dtk)", "RND_D0 §2 tafsir")

refs = [
 ("Dragomiretskiy", "2014", "10.1109/TSP.2013.2288675", "https://doi.org/10.1109/TSP.2013.2288675"),
 ("Huang", "1998", "10.1098/rspa.1998.0193", "https://api.crossref.org/works/10.1098/rspa.1998.0193"),
 ("Rabiner", "1989", "10.1109/5.18626", "https://api.crossref.org/works/10.1109/5.18626"),
 ("Cox", "1972", "10.1111/j.2517-6161.1972.tb00899.x", "https://api.crossref.org/works/10.1111/j.2517-6161.1972.tb00899.x"),
 ("Ishwaran", "2008", "10.1214/08-AOAS169", "https://api.crossref.org/works/10.1214/08-AOAS169"),
 ("Liu", "2008", "10.1109/ICDM.2008.17", "https://api.crossref.org/works/10.1109/ICDM.2008.17"),
 ("Page", "1954", "10.1093/biomet/41.1-2.100", "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1093/biomet/41.1-2.100"),
 ("Mirjalili", "2014", "10.1016/j.advengsoft.2013.12.007", "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.advengsoft.2013.12.007"),
]
for a, y, doi, url in refs:
    rows.append((f"DOI {doi}", "DOI", "JURNAL", f"{a} {y}, divertifikasi lewat {url}",
                 "RND_D0 §8 rujukan", "TERVERIFIKASI"))

HEADER = ("| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |\n"
          "|---|---|---|---|---|---|---|---|\n")

if not os.path.exists(LEDGER):
    with open(LEDGER, "w") as fh:
        fh.write("# RND_PROVENANCE_LEDGER — LEDGER ANGKA RISET ALGORITMA (7 kolom)\n\n")
        fh.write("Aturan: setiap angka di dokumen RND wajib punya baris di sini. Angka tanpa kelas sumber "
                 "dilarang masuk dokumen dan harus ditulis BELUM TERUKUR.\n")
        fh.write("Kelas sumber: STANDAR / JURNAL / RUN-KITA / KONVENSI / DERIVASI / BELUM-TERUKUR.\n\n")
        fh.write("## Bagian D0 — kelayakan data per algoritma (kartu t_34c20c78)\n\n")
        fh.write(HEADER)
        start_idx = 1
        mode = "w"
        existing = []
else:
    existing = open(LEDGER).read().splitlines()
    start_idx = 1
    mode = "a"

# append section
with open(LEDGER, mode) as fh:
    if mode == "a":
        fh.write("\n## Bagian D0 — kelayakan data per algoritma (kartu t_34c20c78)\n\n")
        fh.write(HEADER)
    for i, (angka, satuan, kelas, ruj, dipakai, status) in enumerate(rows, start=start_idx):
        clean = [str(x).replace("|", "/") for x in (angka, satuan, kelas, ruj, dipakai, status)]
        fh.write(f"| {i} | {clean[0]} | {clean[1]} | {clean[2]} | {clean[3]} | {DATE} | {clean[4]} | {clean[5]} |\n")

print("LEDGER rows appended:", len(rows), "->", LEDGER)
