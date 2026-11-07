#!/usr/bin/env python3
"""
21_curate_labels.py — Kurasi 884 event non-sukses jadi label BHA terkurasi (V2).

Reproducible, deterministik. Tidak ada input manual.

Input :
  data/volve/usrop_wellbores_events.csv   (884 event non-sukses)
  data/volve/ddr.parquet                   (1.759 DDR; sumber comments penuh)
Output:
  data/volve/labels_curated.csv            (884 baris + kolom kurasi)

Skema (lihat docs/V2_LABEL_CURATION.md untuk narasi lengkap):
  1. Join event -> aktivitas DDR via (wellbore, act_start == dTimStart)
     untuk mengambil comments PENUH (CSV asli terpotong 300 char).
  2. Sinyal deterministik per baris:
       - has_fail   : pola kegagalan/masalah dalam narasi
       - bha_hits   : equipment BHA/downhole (bit, jar, MWD, drill string, ...)
       - wl_hits    : intervensi wireline/completion (tractor, toolstring, ...)
       - sf_hits    : equipment permukaan/rig (PRS, TDS, tongs, pump, ...)
       - well_hits  : kondisi sumur/fluid (losses, LCM, kick)
  3. Urutan aturan (first match menang) -> category, bha_relevant, evidence.
"""

import re
import sys
import pandas as pd

BASE = "/mnt/d/Capstone 1"
EVENTS = f"{BASE}/data/volve/usrop_wellbores_events.csv"
DDR = f"{BASE}/data/volve/ddr.parquet"
OUT = f"{BASE}/data/volve/labels_curated.csv"

# ---------------------------------------------------------------------------
# 1. Muat data + join comments penuh
# ---------------------------------------------------------------------------

def load_joined() -> pd.DataFrame:
    ev = pd.read_csv(EVENTS)
    ddr = pd.read_parquet(DDR)

    rows = []
    for _, r in ddr.iterrows():
        _a = r["activity"]
        for a in ([] if _a is None else _a):
            rows.append({
                "wellbore": r["nameWellbore"],
                "dTimStart": a.get("dTimStart"),
                "code_act": a.get("proprietaryCode"),
                "state_act": a.get("stateDetailActivity"),
                "comments_full": a.get("comments"),
            })
    act = pd.DataFrame(rows)

    ev["act_start_dt"] = pd.to_datetime(ev["act_start"], utc=True, format="ISO8601")
    act["dTimStart_dt"] = pd.to_datetime(act["dTimStart"], utc=True, format="ISO8601",
                                         errors="coerce")

    m = ev.merge(act, how="left",
                 left_on=["wellbore", "act_start_dt"],
                 right_on=["wellbore", "dTimStart_dt"])
    n_unmatched = int(m["comments_full"].isna().sum())
    if len(m) != len(ev) or n_unmatched:
        sys.exit(f"FATAL: join gagal — rows={len(m)} (expected {len(ev)}), "
                 f"unmatched={n_unmatched}")
    # Kode/state dari aktivitas harus identik dengan CSV sumber
    mismatch = int((m["code"] != m["code_act"]).sum() + (m["state_detail"] != m["state_act"]).sum())
    if mismatch:
        sys.exit(f"FATAL: code/state_detail tidak cocok antara CSV dan parquet: {mismatch}")
    m["comments_full"] = m["comments_full"].fillna("").str.strip()
    return m


# ---------------------------------------------------------------------------
# 2. Pola kata kunci (TRANSPARAN — daftar eksplisit, tanpa ML)
# ---------------------------------------------------------------------------

# Kegagalan/masalah. "broke out" (operasi normal) dikecualikan.
FAIL = {
    "trouble":      r"trouble[- ]?(shoot|shooted|shooting|shot|shooting)|troubleshoot\w*",
    "problem":      r"problems?\b",
    "fail":         r"fail(ed|ure|s)?\b|mal[- ]?function",
    "fault":        r"fault(y|s)?\b|short in\b",
    "broken":       r"\bbroke off\b|\bbroken\b|bursted|burst(ed)?\b|cracked",
    "damage":       r"damag\w+|deformed\b|corrod\w+",
    "worn":         r"\bworn\b|\bwear\b(?! ?bushing)",
    "bent":         r"\bbent\b",
    "leak":         r"leak(y|s|age|ed)?\b",
    "stuck_word":   r"\bstuck\b",
    "notable":      r"not able|unable|no success|no go\b|no sucess|without sucess|without success|no good test|\bnegative\b|could not|cannot|can't",
    "repaired":     r"repair(ed|s)?\b|rectif\w+",
    "stopped":      r"stopped\b|shut ?down\b|black ?out\b|halted\b|abort\w*",
    "lost":         r"lost communication|lost weight|lost returns|lost circ",
    "error":        r"\berror\b|mis[- ]?match",
    "jammed":       r"jam(med|ming)?\b|\bsheared\b",
    "parted":       r"parted\b|screwed out underneath|came apart",
    "no_success":   r"no success|not working|did not work|without success|had problems|having problems",
    "abort2":       r"aborted\b|negative result|no indication|not functioning",
    "changeout":    r"chang(ed|e) (out|over)\b",
    "missing":      r"\bmissing\b",
    "noise":        r"unusual noise|noise from|noisy",
    "overheat":     r"overheat\w+|over heated",
    "blocked":      r"\bblocked\b|\bblockage\b",
    "loosened":     r"loosen(ed|ing)?\b|dropped object",
    "stopop":       r"stop(ped|s)? (operation|drilling|displacement|circulation|rih|pumps|rotat)",
    "power":        r"power (supply|syncron\w*|failure|shut\w*|cut|distribution)|mainpower|lost power",
    "notpossible":  r"not possible|unsuc\w+|unsuccess\w+|no fualts",
    "override":     r"\boverride\b|force signal",
    "wrong":        r"wrong (line-?up|position|direction)",
    "washedout":    r"wash(ed)? out\b",
    "marks":        r"vertical marks|deep marks",
}
FAIL_EXCLUDE = [r"no wear", r"no damage", r"not damage", r"no leak", r"without any problem",
                r"none found", r"no loose", r"no restriction", r"no drag",
                r"not able to be observed|could not be observed"]

# Downhole / BHA (drilling)
DOWNHOLE = {
    "stuck_packoff": r"pack[- ]?off|packed off|tight hole|\bstuck\b(?!\s*finger)(?!\s*in master)",
    "fishing":       r"\bfish(es|ing|ed)?\b|left in hole|overshot(?! packer)|grapple|junk",
    "bit":           r"\bbit\b|undergauge|roller cone",
    "jar":           r"jarred|jarring|functioned jar|hydraulic jar|\bjars?\b",
    "drill_string":  r"drill ?string|drillstring|drill ?collar|drillcollar|heavy weight drill|hw ?dp|dc/jar|\bdc\b",
    "mwd_lwd":       r"\bmwd\b|\blwd\b|gmwd|ubho|xceed|powerdrive|power ?pulse|gyro tool|ecoscope",
    "motor":         r"mud ?motor|mudmotor|bend to \d",
    "bha_word":      r"\bbha\b",
    "hole_cond":     r"wash ?out\b",
    "downhole_tool": r"multi cycle|mcvb|bypass valve|whipstock|mill assembly|window mill|water melon mill|jarring toolstring|pulling tool|lock down sub",
}

# Rule DOWNHOLE yang secara intrinsik = insiden (bukan sekadar penyebutan
# equipment). Match rule ini + narasi mengandungnya -> dianggap ada sinyal
# kegagalan, dan jadi prioritas saat lokasi bentrok (bukan incidental).
ADVERSE_RULES = {"stuck_packoff", "fishing"}

# Wireline / completion intervention (downhole TAPI bukan BHA pengeboran)
WIRELINE = {
    "tractor":       r"tractor",
    "toolstring":    r"toolstring|tool string|toolcatcher",
    "wl":            r"\bwl\b|wireline|w/l ",
    "perf":          r"perforat\w+|\bguns?\b|firing head|shooting depth",
    "winch_cable":   r"winch|\bcable\b|add-on drum|spool\w*",
    "lubricator":    r"lubricator|\bqts\b|\bqst\b",
    "completion":    r"liner hanger|running tool|ball seat|\bpbr\b|me-plug|timelock|dhsv|packer element|tubing bonnet",
}

# Permukaan / rig / wellhead surface
SURFACE = {
    "prs":           r"\bprs\b|pipe racking",
    "hts_pdm":       r"\bhts\b|\bpdm\b|power rollers",
    "tds":           r"\btds\b|top drive|rotating link|wash ?pipe|ibop|saver sub",
    "tongs":         r"\btongs?\b|roughneck|\birn\b|\bir\b\b|spinner|make up high torque|torque wrench|iron rough",
    "elevator":      r"elevators?\b|elevator|\bbails?\b",
    "slips":         r"slips?\b|ps-?21|ps-?30|ps ?21|ps ?30|master ?bushings?|autoslips|auto slips",
    "drawworks":     r"draw ?works|crown block|drill line|deadline|block calibrated|calibrated block|travelling block|traveling block",
    "mudpump":       r"mud pump|mill pump|transfer pump|\bmp[- ]?[123]\b|stand ?pipe|fluid end|liner spray|suction dampner|suction module",
    "winch_hoist":   r"winch|tugger|crane|skidding",
    "control":       r"\bzms\b|vicis|control system|joystick|profibus|\bvfd\b|plc|siemens|interlock|smart zone|encoder",
    "hydraulic":     r"hydraulic|hpu|\bhoses?\b|solenoid|pump unit",
    "electrical":    r"electric\w*|generator|transformer|circuit|ex-panel|relay|power pack|voltage|power (supply|syncron\w*|distribution|shut)|mainpower|process ?modul|prosess ?modul",
    "floor_derrick": r"rig floor|drill ?floor|drillfloor|derrick|finger ?board|finger on|catwalk|moon ?pool|cantilever|setback",
    "valve_manifold": r"kill manifold|choke manifold|cement unit|manifold|hopper|bulk tank|shaker|centrifuge|line test|\bhcr\b",
    "bop_riser":     r"\bbop\b|riser|diverter|wellhead|\bxmt\b|test plug|multi ?bowl|wear ?bushing|dsdv|\bsv\b|hmv",
    "other_surface": r"fingerboard|conveyer|conveyor|iso tank|potable|air comp|nitrogen unit|spooler|stool|anchor|crown|deadman|dead man|vfd|flood|light|winch brake|drum|cutting skip|purge system",
}

# Kondisi sumur / fluid (downhole, tapi BUKAN kegagalan equipment)
WELLBORE = {
    "losses":       r"lost circulation|loss of circulation|losses\b|lcm|loss free|losing mud|lost mud|lost returns",
    "kick_wc":      r"\bkick\b|well control|sidpp|kill line|gas kick",
}

def _hit(text: str, patterns: dict) -> list:
    """Return (rule_name, matched_substring) untuk tiap pola yang match."""
    out = []
    for name, pat in patterns.items():
        mo = re.search(pat, text, flags=re.I)
        if mo:
            out.append((name, mo.group(0)))
    return out


def _has_fail(text: str) -> tuple:
    if any(re.search(p, text, flags=re.I) for p in FAIL_EXCLUDE):
        # ada negasi — tetap cari pola fail lain yang bukan bagian dari negasi
        pass
    hits = []
    for name, pat in FAIL.items():
        mo = re.search(pat, text, flags=re.I)
        if not mo:
            continue
        # cek apakah match berada dalam frasa negasi
        start = max(0, mo.start() - 12)
        window = text[start:mo.end() + 6]
        if any(re.search(p, window, flags=re.I) for p in FAIL_EXCLUDE):
            continue
        hits.append((name, mo.group(0)))
    return hits


def _snippet(text: str, mo_re: str, width: int = 70) -> str:
    mo = re.search(mo_re, text, flags=re.I)
    if not mo:
        return text[:width]
    s = max(0, mo.start() - width // 2)
    frag = text[s:mo.end() + width // 2]
    return ("…" if s > 0 else "") + frag.strip() + ("…" if mo.end() + width // 2 < len(text) else "")


# ---------------------------------------------------------------------------
# 3. Klasifikasi (urutan aturan, first match menang)
# ---------------------------------------------------------------------------

def classify(row: pd.DataFrame) -> dict:
    txt = row["comments_full"]
    low = txt.lower()
    code = row["code"]
    state = row["state_detail"]

    fail_hits = _has_fail(low)
    dh_hits = _hit(low, DOWNHOLE)
    wl_hits = _hit(low, WIRELINE)
    sf_hits = _hit(low, SURFACE)
    well_hits = _hit(low, WELLBORE)
    adverse = any(n in ADVERSE_RULES for n, _ in dh_hits)
    has_fail = bool(fail_hits) or adverse

    def ev(rule, match):
        return f"[{rule}] \"{match}\" | \"{_snippet(low, re.escape(match))}\""

    def rules_str():
        parts = []
        for label, hits in (("fail", fail_hits), ("bha", dh_hits), ("wl", wl_hits),
                            ("surface", sf_hits), ("well", well_hits)):
            if hits:
                parts.append(f"{label}=" + ",".join(n for n, _ in hits))
        return "; ".join(parts) if parts else "no_rule_matched"

    # --- Aturan pendek (kode/state) — menang atas keyword ---
    if state == "injury":
        return dict(category="safety_personnel", bha_relevant="no",
                    evidence=f"[state_detail=injury] \"{txt[:90]}\"",
                    match_rules=rules_str())
    if state == "stuck equipment" or code == "interruption -- fish":
        pat = r"stuck|pack[- ]?off|fish\w*|junk|jarred|parted"
        mo = re.search(pat, low, flags=re.I)
        mtxt = mo.group(0) if mo else code
        return dict(category="bha_stuck_fishing", bha_relevant="yes",
                    evidence=ev("rule_code_state", mtxt), match_rules=rules_str())
    if state in ("circulation loss", "mud loss") or code == "interruption -- well control":
        pat = r"losses|lcm|lost circulation|circulation loss|loss free"
        mo = re.search(pat, low, flags=re.I)
        mtxt = mo.group(0) if mo else (state if state != "equipment failure" else code)
        return dict(category="wellbore_fluid", bha_relevant="no",
                    evidence=ev("rule_code_state", mtxt), match_rules=rules_str())

    # --- Urutan keyword ---
    cats = []
    if dh_hits:
        cats.append("bha")
    if wl_hits:
        cats.append("wl")
    if sf_hits:
        cats.append("surface")
    if well_hits:
        cats.append("well")

    if not has_fail:
        # Narasi tidak memuat sinyal kegagalan -> jangan dipaksa
        first = (dh_hits + wl_hits + sf_hits + well_hits)
        if first:
            e = ev(f"no_fail_signal/{first[0][0]}", first[0][1])
        else:
            e = "[no_fail_signal] narasi rutin/tanpa kata kunci kegagalan"
        return dict(category="routine_no_failure_evidence", bha_relevant="uncertain",
                    evidence=e, match_rules=rules_str())

    # Ada sinyal kegagalan: lokasi equipment menentukan kategori
    if len(cats) == 1:
        only = cats[0]
    elif len(cats) == 0:
        only = "none"
    else:
        only = "mixed"

    if only == "bha":
        cat = "bha_stuck_fishing" if any(n in ("stuck_packoff", "fishing") for n, _ in dh_hits) \
            else "bha_downhole_equipment"
        rule, mt = dh_hits[0]
        return dict(category=cat, bha_relevant="yes", evidence=ev(rule, mt),
                    match_rules=rules_str())
    if only == "wl":
        rule, mt = wl_hits[0]
        return dict(category="wireline_completion_intervention", bha_relevant="no",
                    evidence=ev(rule, mt), match_rules=rules_str())
    if only == "surface":
        rule, mt = sf_hits[0]
        return dict(category="surface_rig_equipment", bha_relevant="no",
                    evidence=ev(rule, mt), match_rules=rules_str())
    if only == "well":
        rule, mt = well_hits[0]
        return dict(category="wellbore_fluid", bha_relevant="no",
                    evidence=ev(rule, mt), match_rules=rules_str())
    if only == "mixed":
        # Prioritas: rule ADVERSE (stuck/pack-off/fishing) hampir tidak pernah
        # incidental — menang atas penyebutan equipment lain.
        if adverse:
            rule, mt = next((x for x in dh_hits if x[0] in ADVERSE_RULES))
            return dict(
                category="bha_stuck_fishing", bha_relevant="yes",
                evidence=ev(rule, mt) +
                         " || prioritas: rule_adverse_dh menang atas penyebutan incidental lain",
                match_rules=rules_str())
        joined = "; ".join(f"{c}:" + ",".join(n for n, _ in
                         {"bha": dh_hits, "wl": wl_hits, "surface": sf_hits,
                          "well": well_hits}[c]) for c in cats)
        first_hit = (dh_hits + wl_hits + sf_hits + well_hits)[0]
        return dict(category="mixed_evidence", bha_relevant="uncertain",
                    evidence=ev("mixed", first_hit[1]) + f" || lokasi: {joined}",
                    match_rules=rules_str())
    # failure ada tapi tidak ada equipment yang teridentifikasi
    rule, mt = fail_hits[0]
    return dict(category="failure_unlocated", bha_relevant="uncertain",
                evidence=ev("fail_only", mt), match_rules=rules_str())


# ---------------------------------------------------------------------------
# 4. Jalankan + laporan
# ---------------------------------------------------------------------------

def main():
    df = load_joined()
    res = pd.DataFrame([classify(r) for _, r in df.iterrows()])

    out = pd.DataFrame({
        "event_id": range(1, len(df) + 1),
        "wellbore": df["wellbore"],
        "event_date": df["act_start"].astype(str).str[:10],
        "act_start": df["act_start"],
        "act_end": df["act_end"],
        "ddr_date_start": df["ddr_date_start"],
        "md": df["md"],
        "md_valid": (df["md"].notna() & (df["md"] > 0)),
        "source_code": df["code"],
        "state_detail": df["state_detail"],
        "category": res["category"],
        "bha_relevant": res["bha_relevant"],
        "evidence": res["evidence"],
        "match_rules": res["match_rules"],
        "comments_full": df["comments_full"],
        "comments_trunc300": df["comments"],
    })
    out.to_csv(OUT, index=False, encoding="utf-8")

    # ---- laporan ----
    n = len(out)
    print(f"=== OUTPUT: {OUT} ===")
    print(f"baris: {n} (expected 884) | md_valid: {int(out['md_valid'].sum())} | "
          f"md==0: {int((out['md'] == 0).sum())} | md NaN: {int(out['md'].isna().sum())}")
    print("\n--- distribusi category ---")
    vc = out["category"].value_counts()
    for k, v in vc.items():
        print(f"{v:5d}  {v / n * 100:5.1f}%  {k}")
    print("\n--- distribusi bha_relevant ---")
    for k, v in out["bha_relevant"].value_counts().items():
        print(f"{v:5d}  {v / n * 100:5.1f}%  {k}")
    print("\n--- category x bha_relevant ---")
    print(pd.crosstab(out["category"], out["bha_relevant"]).to_string())
    print("\n--- coverage per wellbore (semua | yes | uncertain) ---")
    ct = pd.crosstab(out["wellbore"], out["bha_relevant"])
    for c in ("yes", "no", "uncertain"):
        if c not in ct:
            ct[c] = 0
    ct["total"] = ct.sum(axis=1)
    print(ct[["total", "yes", "no", "uncertain"]].to_string())
    print("\n--- md_valid per kategori ---")
    print(out.groupby("category")["md_valid"].agg(["sum", "count"]).to_string())
    print("\n--- tahun (event_date) ---")
    print(out["event_date"].str[:4].value_counts().sort_index().to_string())
    print("\n--- contoh evidence per kategori (masing-masing 2) ---")
    for c in out["category"].unique():
        sub = out[out["category"] == c].head(2)
        for _, r in sub.iterrows():
            print(f"  [{c}] {r['event_date']} {r['wellbore']}: {r['evidence'][:200]}")


if __name__ == "__main__":
    main()
