#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
code/43_verify_sensor_increment.py — helper verifikasi acceptance T2b (task t_b925f329)

Acceptance (dicek PM/auditor):
  (a) 0 angka karangan           — semua angka MD == JSON, dihitung ulang dari JSON
  (b) garis acuan F1 0,058/0,110/0,151/0,256 tetap ada
  (c) framing §3.3 verbatim      — substring MD == substring V2_PM_AUDIT.md
  (d) TIDAK ada klaim "model mengalahkan canary"
  (e) 1 kampanye saja, TANPA loop tuning (log tunggal, tanpa target absolut)

Cek yang dijalankan (semua dari file di disk; exit 0 = semua PASS):
  1. Artefak ada & log memuat SELESAI + EXIT 0; verdict log == verdict JSON.
  2. Tabel fold §3 (Δ10) + §4 (Δ30): tiap sel (n, prev, 6 pr_auc, 3 delta) == JSON.
  3. Tabel ringkasan §5 (6 baris) == JSON delta field.
  4. HITUNG ULANG dari fold JSON: delta per fold, macro, menang/seri/kalah,
     sign test eksak dua sisi, aturan mayoritas -> == tersimpan di JSON.
  5. Verdict JSON (per pasangan + keseluruhan, 2 lengan) == hitung ulang aturan.
  6. Tabel kalibrasi §7 (Brier/ECE/gap/fold-mean) == JSON.
  7. Garis acuan F1: 0,058 | 0,110 | 0,151 | 0,256 ada di MD.
  8. Framing §3.3 di MD identik karakter-demi-karakter dgn V2_PM_AUDIT.md.
  9. CROSS-CHECK INDEPENDEN: model md+sensor & replika md-only di JSON ini
     fold+pooled == JSON kampanye 40 (A1/A3/A4/B1/D1); crosscheck all_equal True.
 10. B1 beku: macro-LOWO log_md @Δ10 == 0.2265 (referensi frozen T1).
 11. Disclaimer klaim: kalimat "TIDAK membuktikan model mengalahkan canary" ada;
     pola klaim beat-canary positif TIDAK ada; "0.2465" tidak ada (tanpa target);
     protocol tuning == "TIDAK ADA".
 12. Verdict MD (Kesimpulan (i)/(ii)) == verdict JSON.

Output: stdout + exit 0/1.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MD_P = BASE / "docs" / "V2_SENSOR_INCREMENT.md"
JSON_P = BASE / "docs" / "V2_SENSOR_INCREMENT.json"
LOG_P = BASE / "docs" / "V2_SENSOR_INCREMENT_RUN_LOG.txt"
PM_P = BASE / "docs" / "V2_PM_AUDIT.md"
REF40_P = BASE / "docs" / "V2_ML_BEAT_CANARY.json"

FAILS: list[str] = []

PAIRS = {"log": ("log_md", "log_md_sensor"),
         "rf": ("rf_md", "rf_md_sensor"),
         "hgb": ("hgb_md", "hgb_md_sensor")}
MODELS = ["log_md", "log_md_sensor", "rf_md", "rf_md_sensor", "hgb_md", "hgb_md_sensor"]
MAP40 = {"log_md": "B1_canary_md", "log_md_sensor": "A4_log_row",
         "rf_md_sensor": "A1_rf_row", "hgb_md": "D1_hgb_md_diag",
         "hgb_md_sensor": "A3_hgb_row"}
SHORT = {"USROP_A 0 N-NA_F-9_Ad.csv": "F-9A", "USROP_A 1 N-S_F-7d.csv": "F-7",
         "USROP_A 2 N-SH_F-14d.csv": "F-14", "USROP_A 3 N-SH-F-15d.csv": "F-15A",
         "USROP_A 4 N-SH_F-15Sd.csv": "F-15 (S)", "USROP_A 5 N-SH-F-5d.csv": "F-5",
         "USROP_A 6 N-SH_F-9d.csv": "F-9"}
WELLS = sorted(SHORT, key=lambda w: w)  # urutan iterasi kampanye 42 (sorted(set(wells)))


def check(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'} | {name}" + (f" — {detail}" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def section(md: str, a: str, b: str) -> str:
    ia = md.find(a)
    ib = md.find(b)
    if ia < 0 or ib < 0 or ib <= ia:
        return ""
    return md[ia:ib]


def cells_of(line: str) -> list[str]:
    return [c.strip() for c in line.split("|") if c.strip() != ""]


def sign_p(wins: int, losses: int):
    n = wins + losses
    if n == 0:
        return None, 0
    k = min(wins, losses)
    p = 2.0 * sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return round(min(1.0, p), 4), n


def main() -> None:
    for p in (MD_P, JSON_P, LOG_P, PM_P, REF40_P,
              BASE / "code" / "42_sensor_increment.py", Path(__file__)):
        check(f"ada & tak kosong: {p.name}", p.exists() and p.stat().st_size > 0)

    md = MD_P.read_text(encoding="utf-8")
    log = LOG_P.read_text(encoding="utf-8")
    pm = PM_P.read_text(encoding="utf-8")
    res = json.loads(JSON_P.read_text(encoding="utf-8"))
    ref = json.loads(REF40_P.read_text(encoding="utf-8"))

    # ---- 1. log markers + verdict log == JSON
    check("log: memuat SELESAI", "SELESAI" in log)
    check("log: memuat EXIT 0", "EXIT 0" in log)
    mvd = re.search(r"VERDICT d10: (\S+)", log)
    check("log verdict d10 == JSON verdict",
          bool(mvd) and mvd.group(1) == res["verdict"]["overall_d10"],
          f"log={mvd and mvd.group(1)} json={res['verdict']['overall_d10']}")
    mvd30 = re.search(r"VERDICT d30: (\S+)", log)
    check("log verdict d30 == JSON verdict",
          bool(mvd30) and mvd30.group(1) == res["verdict"]["overall_d30"])
    check("log: crosscheck all_equal True",
          "all_equal=True" in log, log[log.find("CROSSCHECK"):log.find("CROSSCHECK") + 120]
          if "CROSSCHECK" in log else "baris CROSSCHECK tak ada")

    # ---- 2. tabel fold §3 (d10) + §4 (d30) == JSON
    s3 = section(md, "## 3.", "## 4.")
    s4 = section(md, "## 4.", "## 5.")
    check("§3 & §4 ada", bool(s3) and bool(s4))
    row_re = re.compile(r"^\| (F-9A|F-7|F-14|F-15A|F-15 \(S\)|F-5|F-9) \|(.*)$", re.M)
    rows3 = row_re.findall(s3)
    rows4 = row_re.findall(s4)
    check("§3: 7 baris fold", len(rows3) == 7, f"{len(rows3)}")
    check("§4: 7 baris fold", len(rows4) == 7, f"{len(rows4)}")
    miss = []
    for arm, rows in (("d10", rows3), ("d30", rows4)):
        for i, w in enumerate(WELLS):
            if i >= len(rows) or rows[i][0] != SHORT[w]:
                miss.append(f"{arm} baris-{i}: label {i < len(rows) and rows[i][0]} != {SHORT[w]}")
                continue
            cells = cells_of(rows[i][1])
            fb = res[arm]["folds"]["log_md"][w]
            expect = [str(fb["n"]), str(fb.get("prev", "NA"))]
            for pair in ("log", "rf", "hgb"):
                mo, ms = PAIRS[pair]
                expect += [str(res[arm]["folds"][mo][w].get("pr_auc", "NA")),
                           str(res[arm]["folds"][ms][w].get("pr_auc", "NA")),
                           str(res[arm]["delta"][pair]["per_fold"][w]["delta"])]
            if cells != expect:
                miss.append(f"{arm}/{SHORT[w]}: MD={cells} JSON={expect}")
    check("tabel fold §3+§4 MD == JSON (14 baris x 11 sel)", not miss, "; ".join(miss[:3]))

    # ---- 3. tabel ringkasan §5 == JSON
    s5 = section(md, "## 5.", "## 6.")
    check("§5 ada", bool(s5))
    miss5 = []
    for arm in ("d10", "d30"):
        for pair in ("log", "rf", "hgb"):
            m = re.search(rf"^\| {pair} \| {arm} \|(.*)$", s5, re.M)
            if not m:
                miss5.append(f"{pair}/{arm}: baris tak ada")
                continue
            d = res[arm]["delta"][pair]
            expect = [str(d["macro_md_only"]), str(d["macro_md_sensor"]),
                      str(d["macro_delta"]), str(d["wins_delta_gt_0"]),
                      str(d["n_delta_le_0"]), str(d["n_valid"]),
                      str(d["sign_p_two_sided"]),
                      "ya" if d["majority_delta_le_0"] else "tidak",
                      d["verdict_pair"]]
            got = cells_of(m.group(1))
            if got != expect:
                miss5.append(f"{pair}/{arm}: MD={got} JSON={expect}")
    check("tabel ringkasan §5 MD == JSON (6 baris x 9 sel)", not miss5, "; ".join(miss5[:3]))

    # ---- 4. HITUNG ULANG delta/macro/sign-test dari fold JSON
    recompute_ok = True
    detail = []
    for arm in ("d10", "d30"):
        for pair, (mo, ms) in PAIRS.items():
            stored = res[arm]["delta"][pair]
            deltas = []
            for w in sorted(res[arm]["folds"][mo]):
                a = res[arm]["folds"][mo][w].get("pr_auc")
                b = res[arm]["folds"][ms][w].get("pr_auc")
                if a is None or b is None:
                    continue
                deltas.append(round(b - a, 4))
            n = len(deltas)
            wins = sum(1 for d in deltas if d > 0)
            ties = sum(1 for d in deltas if d == 0)
            losses = n - wins - ties
            p, nsign = sign_p(wins, losses)
            macro = round(sum(deltas) / n, 4) if n else None
            nle0 = losses + ties
            ok = (stored["macro_delta"] == macro
                  and stored["wins_delta_gt_0"] == wins
                  and stored["ties_delta_eq_0"] == ties
                  and stored["losses_delta_lt_0"] == losses
                  and stored["n_delta_le_0"] == nle0
                  and stored["n_valid"] == n
                  and stored["sign_p_two_sided"] == p
                  and stored["majority_delta_le_0"] == (nle0 > n / 2 if n else None))
            if not ok:
                recompute_ok = False
                detail.append(f"{arm}/{pair}")
    check("hitung ulang delta+sign test dari fold JSON == tersimpan",
          recompute_ok, ", ".join(detail))

    # ---- 5. aturan verdict == verdict tersimpan
    v_ok = True
    v_det = []
    for arm in ("d10", "d30"):
        per = {}
        for pair in ("log", "rf", "hgb"):
            d = res[arm]["delta"][pair]
            exp = ("i_sensor_tidak_menambah_nilai" if d["majority_delta_le_0"]
                   else "ii_delta_positif_terbatas") if d["majority_delta_le_0"] is not None else "tidak_valid"
            per[pair] = exp
            if res["verdict"]["per_pair"][arm][pair] != exp:
                v_ok = False
                v_det.append(f"{arm}/{pair}")
        overall = ("i_sensor_tidak_menambah_nilai_di_mayoritas_fold_semua_pasangan"
                   if all(x == "i_sensor_tidak_menambah_nilai" for x in per.values())
                   else "ii_delta_positif_terbatas_di_sebagian_pasangan")
        if res["verdict"][f"overall_{arm}"] != overall:
            v_ok = False
            v_det.append(f"{arm}/overall")
    check("aturan verdict dihitung ulang == verdict JSON", v_ok, ", ".join(v_det))
    if res["verdict"]["overall_d10"].startswith("i_"):
        check("MD memuat Kesimpulan (i)", "Kesimpulan (i)" in md)
    else:
        check("MD memuat Kesimpulan (ii)", "Kesimpulan (ii)" in md)

    # ---- 6. tabel kalibrasi §7 == JSON
    s7 = section(md, "## 7.", "## 8.")
    check("§7 ada", bool(s7))
    miss7 = []
    for arm in ("d10", "d30"):
        for m in MODELS:
            mm = re.search(rf"^\| {re.escape(m)} \| {arm} \|(.*)$", s7, re.M)
            if not mm:
                miss7.append(f"{m}/{arm}: baris tak ada")
                continue
            p = res[arm]["pooled"][m]
            expect = [str(p["brier"]), str(p["ece"]),
                      str(p["reliability_max_gap"]), str(p["brier_fold_mean"])]
            got = cells_of(mm.group(1))
            if got != expect:
                miss7.append(f"{m}/{arm}: MD={got} JSON={expect}")
    check("tabel kalibrasi §7 MD == JSON (12 baris x 4 sel)", not miss7, "; ".join(miss7[:3]))
    check("§7 menyebut poin 10 §9 (kalibrasi)", "poin 10" in s7)

    # ---- 7. garis acuan F1
    check("garis acuan F1 0,058 | 0,110 | 0,151 | 0,256 ada di MD",
          all(s in md for s in ("0,058", "0,110", "0,151", "0,256")))
    check("JSON menyimpan f1_always_positive == {0.058,0.110,0.151,0.256}",
          res["reference"]["f1_always_positive"] == {"5": 0.058, "10": 0.110,
                                                     "15": 0.151, "30": 0.256}
          or res["reference"]["f1_always_positive"] == {5: 0.058, 10: 0.110,
                                                        15: 0.151, 30: 0.256})

    # ---- 8. framing §3.3 verbatim
    pm_q = re.search(r"Pipeline predictive maintenance \(event nyata.*?baseline tersebut\.", pm, re.S)
    md_q = re.search(r"Pipeline predictive maintenance \(event nyata.*?baseline tersebut\.", md, re.S)
    check("framing §3.3 identik dgn PM audit", bool(pm_q) and bool(md_q)
          and pm_q.group(0) == md_q.group(0),
          f"pm={bool(pm_q)} md={bool(md_q)}")

    # ---- 9. cross-check independen vs kampanye 40
    check("JSON crosscheck_campaign40.all_equal == True",
          res["crosscheck_campaign40"].get("all_equal") is True)
    cc_miss = []
    for mine, theirs in MAP40.items():
        for arm in ("d10", "d30"):
            for w in res[arm]["folds"][mine]:
                v1 = res[arm]["folds"][mine][w].get("pr_auc")
                v2 = ref[arm]["folds"][theirs][w].get("pr_auc")
                if v1 != v2:
                    cc_miss.append(f"{mine} vs {theirs} {arm}/{SHORT.get(w, w)}: {v1}!={v2}")
            if res[arm]["pooled"][mine]["pr_auc"] != ref[arm]["pooled"][theirs]["pr_auc"]:
                cc_miss.append(f"{mine} vs {theirs} {arm} pooled pr_auc beda")
            if res[arm]["pooled"][mine]["macro_pr_auc"] != ref[arm]["pooled"][theirs]["macro_pr_auc"]:
                cc_miss.append(f"{mine} vs {theirs} {arm} macro beda")
    check("replay fold+pooled md+sensor & replika md-only == kampanye 40 (independen)",
          not cc_miss, "; ".join(cc_miss[:3]))

    # ---- 10. frozen canary reference
    check("B1 beku: macro-LOWO log_md @d10 == 0.2265",
          res["d10"]["pooled"]["log_md"]["macro_pr_auc"] == 0.2265,
          str(res["d10"]["pooled"]["log_md"]["macro_pr_auc"]))

    # ---- 11. klaim / target / tuning
    check("disclaimer: 'TIDAK membuktikan model mengalahkan canary' ada di MD",
          "TIDAK membuktikan model mengalahkan canary" in md)
    bad = re.findall(r"(?:berhasil|mampu|telah|berhasil mengalahkan) mengalahkan canary", md)
    check("tidak ada klaim positif beat-canary", not bad, str(bad))
    check("tidak ada 'T2: PASS' di MD", "T2: PASS" not in md)
    check("tanpa target absolut: '0.2465' tidak ada di MD", "0.2465" not in md)
    check("protocol tuning == TIDAK ADA (JSON)",
          str(res["protocol"].get("tuning", "")).startswith("TIDAK ADA"))
    check("MD menyebut 'tanpa tuning'", "tanpa tuning" in md)
    check("satu file log kampanye (tanpa run ganda di log)",
          log.count("42_sensor_increment.py — T2b") <= 1)

    # ---- 12. integritas definisi fitur
    check("JSON: last_md identik md (diagnosis terukur)",
          res["feature_definition"]["last_md_identik_md"] is True)
    check("MD menyebut diagnosis last_md==md", "TERBUKTI identik persis" in md)

    print("\n" + ("=" * 60))
    if FAILS:
        print(f"VERIFIKASI: {len(FAILS)} GAGAL -> {FAILS}")
        sys.exit(1)
    print("VERIFIKASI: SEMUA CHECK PASS (exit 0)")


if __name__ == "__main__":
    main()
