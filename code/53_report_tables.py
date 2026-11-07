#!/usr/bin/env python3
"""T9 — Tabel markdown untuk docs/V3_WITSML_PARSE_REPORT.md (semua angka dari qc/JSON hasil eksekusi)."""
import glob
import json
import os
import re

OUT = "/mnt/d/Capstone 1/data/volve/witsml_parsed"
SCAN = "/home/neonti/.hermes/cache/scratch/t9_scan_all.json"
MAP = "/home/neonti/.hermes/cache/scratch/t9_map.json"

FOLD_LABEL = {
    "F-9_A": "NO 15/9-F-9 A", "F-7": "NO 15/9-F-7", "F-14": "NO 15/9-F-14",
    "F-15A": "NO 15/9-F-15 A", "F-15_S": "NO 15/9-F-15",
    "F-5": "NO 15/9-F-5", "F-9": "NO 15/9-F-9",
    "VAR_F-15A_folder": "NO 15/9-F-15 A (varian folder)", "VAR_F-5_alt": "NO 15/9-F-5 (varian folder)",
}
ORDER = ["F-9_A", "F-7", "F-14", "F-15A", "F-15_S", "F-5", "F-9", "VAR_F-15A_folder", "VAR_F-5_alt"]

CAND = {
    "standpipe pressure": r"^(SPP|STANDPIPE|PUMP.?P|DISCH.?P)",
    "flow (pump/flowline)": r"^(FLOW|PUMP|SV.?FLOW|DV.?FLOW|FLOWRATE)",
    "WOB": r"^(WOB|WEIGHT.?ON)",
    "torque": r"^(TORQ|TORQUE|TQ)",
    "RPM": r"^(RPM|ROT)",
    "mudlog gas": r"^(TG|TOTAL.?GAS|C[1-5]$|GAS|CH4|MGAS)",
    "pit volume": r"^(PIT|TK|TANK|PUMP.?SUCTION)",
    "hookload": r"^(HKLD|HOOK|HKL)",
    "ROP": r"^(ROP)",
    "depth (TVD/MD)": r"^(DEPTH|DEP|TVD|MD|BIT.?DEPTH|TVDSS)",
    "mud weight": r"^(MW|MUD.?W|dens)",
}


def load(name):
    p = os.path.join(OUT, f"{name}.qc.json")
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    qcs = {os.path.basename(p)[:-len(".qc.json")]: json.load(open(p))
           for p in glob.glob(os.path.join(OUT, "*.qc.json"))}
    order = [n for n in ORDER if n in qcs] + sorted(n for n in qcs if n not in ORDER)

    print("### A. Ringkasan parse per sumur\n")
    print("| output | folder sumber | identity (nameWellbore) | file time/depth | cluster(batch) | baris | kanal | kanal>=50% | rentang UTC (start -> end) | runtime s |")
    print("|---|---|---|---:|---:|---:|---:|---:|---|---:|")
    for n in order:
        q = qcs[n]
        nb = sum(1 for c in q.get("clusters", []) if c.get("n_batches", 1) > 1)
        print(f"| `{n}.csv` | {q.get('folder')} | {q.get('name_wellbore')} | "
              f"{q.get('n_time_files')}/{q.get('n_depth_files')} | "
              f"{q.get('n_clusters')}{' (split)' if nb else ''} | {q.get('n_rows_final'):,} | "
              f"{q.get('n_columns_excl_timestamp')} | {q.get('n_channels_ge_50pct')} | "
              f"{q.get('t_min_utc')} -> {q.get('t_max_utc')} | {q.get('runtime_s')} |".replace(",", "."))

    print("\n### A2. Integritas timestamp (verifikasi back-to-back atas CSV)\n")
    print("| output | duplikat/boundary terdeteksi | overlap dihapus | split batch | batch > cap | verify: baris | verify: tidak naik | verify: NAT | sorted+unique |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for n in order:
        q = qcs[n]
        v = q.get("verify_timestamp")
        if isinstance(v, dict) and "ok" in v:
            vs = f"{v['n_rows']:,} | {v['n_ts_not_strictly_increasing']} | {v['n_nat_timestamp']} | {q.get('timestamp_sorted_unique')}".replace(",", ".")
        elif isinstance(v, dict) and "error" in v:
            vs = f"ERROR: {v['error']} | - | - | {q.get('timestamp_sorted_unique')}"
        else:
            vs = "belum diverifikasi parser (run lama) -> lihat code/52_verify_witsml_parse.py"
        print(f"| `{n}.csv` | {q.get('boundary_duplicate_ts')} | {q.get('n_boundary_overlap_removed', 'n/a')} | "
              f"{q.get('n_batches_split', 0)} | {q.get('n_batches_over_cap', 0)} | {vs} |")

    print("\n### B. Varian folder per sumur target (chung time-based, dari t9_scan_all.json)\n")
    scan = {d["folder"]: d for d in json.load(open(SCAN))}
    mp = json.load(open(MAP))
    targets = {"F-9 A": ["F-9 A"], "F-7": ["9-F-7"], "F-14": ["9-F-14"],
               "F-15A": ["9-F-15 ", "9-F-15A"], "F-15(S)": ["9-F-15S"],
               "F-5": ["9-F-5"], "F-9": ["9-F-9 "]}
    print("| target | folder kandidat | wellbore di chunk | time chunks | dipilih sebagai |")
    print("|---|---|---|---:|---|")
    inv = {v: k for k, v in mp.items()}
    for t, keys in targets.items():
        cands = []
        for f, d in scan.items():
            if any(k in f + " " for k in keys) or any(f.endswith(k.strip()) for k in keys):
                cands.append((f, d))
        for f, d in sorted(cands, key=lambda x: -x[1]["time"]):
            sel = inv.get(f, "-")
            print(f"| {t} | `{f}` | {'; '.join(d['wellbores'])} | {d['time']} | {sel} |")

    print("\n### C. Kehadiran kandidat kanal fitur (dari qc.channels + fill_rate; '-' = tidak ada)\n")
    hdr = "| kandidat | " + " | ".join(f"{n}" for n in order) + " |"
    print(hdr)
    print("|" + "---|" * (len(order) + 1))
    for label, pat in CAND.items():
        rx = re.compile(pat, re.I)
        row = [label]
        for n in order:
            q = qcs[n]
            hits = [c for c in q.get("channels", []) if rx.match(c.strip())]
            if not hits:
                row.append("-")
                continue
            fr = q.get("fill_rate", {})
            best = sorted(hits, key=lambda c: -fr.get(c, 0))[:3]
            row.append("<br>".join(f"`{c}` {int(round(fr.get(c, 0) * 100))}%" for c in best))
        print("| " + " | ".join(row) + " |")

    print("\n### D. Kanal dengan fill-rate >= 50% per sumur (fitur inti)\n")
    for n in order:
        q = qcs[n]
        fr = q.get("fill_rate", {})
        ge = sorted([c for c, v in fr.items() if v >= 0.5], key=lambda c: -fr[c])
        print(f"- **{n}** ({len(ge)} kanal): " + ", ".join(f"`{c}`" for c in ge))

    print("\n### E. Coverage label (dari _coverage.json, dijalankan code/51_witsml_coverage.py)")
    cov_p = os.path.join(OUT, "_coverage.json")
    if os.path.exists(cov_p):
        cov = json.load(open(cov_p))
        print("\n| fold | label wellbore | n label | n ber-tanggal | dalam rentang overall | dalam rentang cluster | % | event_date min..max |")
        print("|---|---|---:|---:|---:|---:|---:|---|")
        for k in ORDER:
            if k not in cov or "n_labels" not in cov.get(k, {}):
                continue
            c = cov[k]
            print(f"| {k} | {c['label_wellbore']} | {c['n_labels']} | {c['n_labels_dated']} | "
                  f"{c['n_in_overall_range']} | {c['n_in_cluster_ranges']} | {c['coverage_pct_cluster']} | "
                  f"{c['event_date_min']} .. {c['event_date_max']} |")
    else:
        print("(belum ada — jalankan code/51_witsml_coverage.py dulu)")


if __name__ == "__main__":
    main()
