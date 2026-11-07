#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helper verifikasi MD == JSON (T2-e): docs/V2_ML_BEAT_CANARY_TS.md vs .json.

Setiap angka yang DITULIS di MD dicek terhadap JSON hasil eksekusi:
  H1 klaim headline (P1/P2/P3/P4/P7, gate, unit, diagnostik) via regex
  H2 tabel §1 gate per varian
  H3 tabel §4 hasil per fold (7 fold x 12 kolom)
  H4 tabel §5 pooled + kalibrasi (9 varian x 10 kolom)
  H5 tabel §2 sampling per fold
  H6 tabel §7b sensitivitas S1
Keluaran: PASS/FAIL per cek, exit 0 bila semua cocok.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1")
MD = BASE / "docs" / "V2_ML_BEAT_CANARY_TS.md"
JS = BASE / "docs" / "V2_ML_BEAT_CANARY_TS.json"
KEYS = ["log_G", "rf_G", "hgb_G", "log_E", "rf_E", "hgb_E",
        "log_F", "rf_F", "hgb_F"]

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""),
          flush=True)
    return bool(ok)


def num(s: str):
    """'0,1494' -> 0.1494 · '4.274.005' -> 4274005 · '1323' -> 1323."""
    s = s.strip().replace("**", "")
    if re.fullmatch(r"-?\d+,\d+", s):
        return float(s.replace(",", "."))
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s):
        return int(s.replace(".", ""))
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    return None


def same(a, b) -> bool:
    """MD (dibulatkan) vs JSON: toleransi pembulatan 4 desimal / int persis."""
    if a is None or b is None:
        return a == b
    if isinstance(b, bool) or isinstance(a, bool):
        return a == b
    if isinstance(b, int) and not isinstance(b, bool):
        return int(a) == b
    return abs(float(a) - float(b)) <= 5e-5 + abs(float(b)) * 1e-9


def section(md: str, start: str, end: str = "\n## ") -> str:
    i = md.find(start)
    if i < 0:
        return ""
    j = md.find(end, i + len(start))
    return md[i:j if j > 0 else len(md)]


def table(sec: str, header_prefix: str) -> list:
    """Baris DATA tabel: header dgn prefix tsb, lalu semua baris '|' berikutnya
    (baris pemisah '---' dilewati). Header ikut dikembalikan sbg baris pertama
    hanya bila cocok; pemanggil memakai seluruh hasil sbg data."""
    lines = sec.splitlines()
    idx = next((i for i, l in enumerate(lines) if l.startswith(header_prefix)), None)
    if idx is None:
        return []
    rows = []
    for l in lines[idx + 1:]:
        if not l.startswith("|"):
            break
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if cells and cells[0].startswith("---"):
            continue
        rows.append(cells)
    return rows


def main() -> int:
    md = MD.read_text(encoding="utf-8")
    R = json.load(open(JS))
    P4 = R["p4_desain_baru"]
    K = R["koreksi_t2e"]
    Q = R["kekosongan_jendela"]
    G = P4["gate"]
    S = P4["sensitivity"]
    U = P4["units"]
    D = P4["diagnostics"]

    # ---------- H1 klaim headline ----------
    h1 = [
        ("P1 total 192", rf"→ \*\*{num_fmt(Q['total_jendela_2h_kosong'])} unit\*\*",
         Q["total_jendela_2h_kosong"]),
        ("P1 pos/neg 191+1",
         rf"\*\*{num_fmt(Q['total_jendela_2h_kosong'])} unit\*\* "
         rf"\({Q['positif']['jendela_2h_kosong']} positif \+ "
         rf"{Q['negatif_kontrol_kampanye_asli']['jendela_2h_kosong']} negatif\)",
         True),
        ("P1 NaN-G == 192",
         rf"Unit NaN varian G = {Q['total_unit_NaN_varian_G']} — ekivalen",
         Q["total_unit_NaN_varian_G"]),
        ("P2 n_eval_neg 6617",
         rf"benar = {K['P2']['baru_n_eval_neg']} negatif \+ "
         rf"{K['P2']['n_eval_pos']} positif = {K['P2']['n_eval_total']} unit",
         K["P2"]["baru_n_eval_neg"]),
        ("P2 total neg 6618",
         rf"dari total {K['P2']['n_neg_total']} negatif",
         K["P2"]["n_neg_total"]),
        ("P3 counter kontrol",
         rf"kontrol rows_scanned = {num_fmt(K['P3']['kontrol']['rows_scanned'])} "
         rf"\(violations {K['P3']['kontrol']['violations']}\)",
         K["P3"]["kontrol"]["rows_scanned"]),
        ("P3 counter event",
         rf"event T10 rows_scanned = {num_fmt(K['P3']['event']['rows_scanned'])} "
         rf"\(violations {K['P3']['event']['violations']}\)",
         K["P3"]["event"]["rows_scanned"]),
        ("P3 counter event (§2, cakupan terpisah)",
         rf"event T10 rows_scanned = {num_fmt(P4['anti_leakage_event']['rows_scanned'])}",
         P4["anti_leakage_event"]["rows_scanned"]),
        ("P4 unit lolos 467/661",
         rf"positif {U['n_pos']}/{U['n_pos_semua_event']} lolos",
         U["n_pos"]),
        ("P4 gugur 194",
         rf"{U['n_pos_gugur_ketersediaan']} gugur: "
         rf"{Q['positif']['jendela_2h_kosong']} kosong-2h",
         U["n_pos_gugur_ketersediaan"]),
        ("P4 kontrol 6617/6618",
         rf"kontrol {Q['negatif_kontrol_kampanye_asli']['non_kosong_semua']}/"
         rf"{Q['negatif_kontrol_kampanye_asli']['n_unit']}",
         Q["negatif_kontrol_kampanye_asli"]["non_kosong_semua"]),
        ("gate target", rf"≥ target \*\*{cz(G['target_macro'])}\*\*",
         G["target_macro"]),
        ("gate canary", rf"canary time-based = {cz(G['canary_macro'])}",
         G["canary_macro"]),
        ("gate verdict",
         rf"VERDICT T2-e \(desain P4\): {re.escape(G['verdict_t2d'])}",
         G["verdict_t2d"]),
        ("P7 fix prediksi serial", r"rfm\.n_jobs = 1 setelah fit", True),
        ("units prev pooled",
         rf"Prevalensi pooled unit = {cz(U['prevalence'])}",
         U["prevalence"]),
        ("gugur 194 + 2660",
         rf"Unit gugur syarat ketersediaan: {D['gugur_ketersediaan']['positif_dibuang']} "
         rf"positif \+ {D['gugur_ketersediaan']['negatif_dibuang']} negatif",
         D["gugur_ketersediaan"]["positif_dibuang"]),
        ("S1 unit longgar",
         rf"S1 set longgar\*\*: {S['n_unit_set_panjang']} unit = "
         rf"{S['n_pos_set_panjang']} positif \+ {S['n_neg_set_panjang']} negatif",
         S["n_unit_set_panjang"]),
        ("S2 macro", rf"macro AUPRC = {cz(S['missingness_only_macro_pr_auc'])}",
         S["missingness_only_macro_pr_auc"]),
        ("S2 pooled", rf"pooled = {cz(S['missingness_only_pooled_pr_auc'])}",
         S["missingness_only_pooled_pr_auc"]),
        ("S2 flag pos/neg",
         rf"flag pos {S['n_flag_kosong_pos']} vs neg {S['n_flag_kosong_neg']}",
         S["n_flag_kosong_pos"]),
        ("canary-sens", rf"Canary-sens = {cz(S['canary'])}", S["canary"]),
        ("target-sens", rf"target-sens = {cz(S['target'])}", S["target"]),
        ("limitasi S2 ditulis", r"Limitasi S2 \(wajib baca\)", True),
        ("diagnostik NaN-G pos",
         rf"varian G: pos {D['frac_nan_sel_G_pos']:.6f}",
         D["frac_nan_sel_G_pos"]),
        ("diagnostik 0 unit kosong",
         rf"jendela-2h kosong = {D['n_unit_kampanye_jendela_2h_kosong']}, "
         rf"jendela-30m kosong = {D['n_unit_kampanye_jendela_30m_kosong']}",
         D["n_unit_kampanye_jendela_2h_kosong"]),
    ]
    bad = []
    for name, pat, val in h1:
        m = re.search(pat, md)
        if not m:
            bad.append(f"{name}:pola tak ditemukan")
            continue
        if val is not True and isinstance(val, (int, float)) and m.lastindex:
            got = num(m.group(1))
            if not same(got, val):
                bad.append(f"{name}:{got}!={val}")
    check("H1 klaim headline MD == JSON (%d klaim)" % len(h1),
          not bad, "; ".join(bad[:4]) if bad else "semua cocok")

    # ---------- H2 tabel §1 gate ----------
    sec1 = section(md, "## 1. Kriteria T2")
    rows = [r for r in table(sec1, "| Varian |")
            if r[0] not in ("Varian",) and not r[0].startswith("---")]
    bad = []
    for r in rows:
        if len(r) < 7:
            continue
        key = f"{r[1]}_{r[0]}"
        v = G["per_variant"].get(key)
        if v is None:
            bad.append(f"{key}:tidak ada di JSON")
            continue
        if not same(num(r[2]), v["macro"]):
            bad.append(f"{key} macro {r[2]}!={v['macro']}")
        if r[3].strip() != v["wins_vs_canary"]:
            bad.append(f"{key} wins {r[3]}!={v['wins_vs_canary']}")
        if (r[4].strip() == "ya") != bool(v["pass_target"]):
            bad.append(f"{key} ≥target {r[4]}")
        lolos = "❌" if not v["LOLOS"] else "✅"
        if r[6].strip() != lolos:
            bad.append(f"{key} LULUS {r[6]}!={lolos}")
    check("H2 tabel §1 gate == JSON (%d baris)" % len(rows),
          len(rows) == 6 and not bad, "; ".join(bad[:4]) or f"{len(rows)} baris")

    # ---------- H3 tabel §4 per fold ----------
    sec4 = section(md, "## 4. Hasil per fold")
    rows = [r for r in table(sec4, "| Fold |")
            if r[0] != "Fold" and not r[0].startswith("---")]
    bad = []
    for r in rows:
        fold = r[0]
        for i, k in enumerate(KEYS, start=3):
            if fold not in P4["folds"][k]:
                bad.append(f"{fold}/{k}:fold tak ada")
                continue
            fj = P4["folds"][k][fold]
            if not same(num(r[i]), fj["pr_auc"]):
                bad.append(f"{fold}/{k} pr_auc {r[i]}!={fj['pr_auc']}")
        base = P4["folds"]["log_G"].get(fold)
        if base is None:
            continue
        if not same(num(r[1]), base["n"]):
            bad.append(f"{fold} n {r[1]}!={base['n']}")
        if not same(num(r[2]), base["prev"]):
            bad.append(f"{fold} prev {r[2]}!={base['prev']}")
    check("H3 tabel §4 fold == JSON (7 x 12 sel)",
          len(rows) == 7 and not bad,
          "; ".join(bad[:4]) if bad else f"{len(rows)} baris x 12")

    # ---------- H4 tabel §5 pooled ----------
    sec5 = section(md, "## 5. Pooled")
    rows = [r for r in table(sec5, "| Model |")
            if r[0] != "Model" and not r[0].startswith("---")]
    bad = []
    for r in rows:
        k = r[0]
        if k not in P4["pooled"]:
            bad.append(f"{k}:tak ada")
            continue
        p = P4["pooled"][k]
        exp = [p["pr_auc"], P4["macro"][k], p["prev"], p["lift"],
               p["r_at_p20"], p["r_at_p50"], p["brier"], p["ece"], p["f1"]]
        for i, e in enumerate(exp, start=1):
            if not same(num(r[i]), e):
                bad.append(f"{k} kolom{i} {r[i]}!={e}")
    check("H4 tabel §5 pooled == JSON (9 x 10 sel)",
          len(rows) == 9 and not bad,
          "; ".join(bad[:4]) if bad else f"{len(rows)} baris x 10")

    # ---------- H5 tabel §2 sampling ----------
    sec2 = section(md, "## 2. Desain P4")
    rows = [r for r in table(sec2, "| Fold | n_pos berdata |")
            if r[0] != "Fold" and not r[0].startswith("---")]
    bad = []
    lbl = {"F-14": "F-14", "F-15A": "F-15A", "F-15 (S)": "F-15_S",
           "F-5": "F-5", "F-7": "F-7", "F-9": "F-9", "F-9A": "F-9_A"}
    for r in rows:
        f = lbl.get(r[0], r[0])
        sm = P4["sampling"].get(f)
        if sm is None:
            bad.append(f"{r[0]}:tak ada")
            continue
        if not same(num(r[1]), sm["n_pos"]) or not same(num(r[2]), sm["n_neg"]):
            bad.append(f"{r[0]} n_pos/n_neg {r[1]}/{r[2]} != {sm['n_pos']}/{sm['n_neg']}")
        if not same(num(r[3]), sm["p_natural_2h"]):
            bad.append(f"{r[0]} p_f {r[3]}!={sm['p_natural_2h']}")
        if not same(num(r[5]), sm["quiet_pool"]):
            bad.append(f"{r[0]} pool {r[5]}!={sm['quiet_pool']}")
    check("H5 tabel §2 sampling == JSON (7 baris)",
          len(rows) == 7 and not bad,
          "; ".join(bad[:4]) if bad else f"{len(rows)} baris")

    # ---------- H6 tabel §7b sensitivitas ----------
    sec7b = section(md, "## 7b. Sensitivitas")
    rows = [r for r in table(sec7b, "| Varian |")
            if r[0] != "Varian" and not r[0].startswith("---")]
    bad = []
    for r in rows:
        key = f"{r[1]}_{r[0]}"
        v = S["per_variant"].get(key)
        if v is None:
            bad.append(f"{key}:tak ada")
            continue
        if not same(num(r[2]), v["macro"]):
            bad.append(f"{key} macro {r[2]}!={v['macro']}")
        if r[3].strip() != v["wins_vs_canary"]:
            bad.append(f"{key} wins {r[3]}!={v['wins_vs_canary']}")
        lolos = "❌" if not v["LOLOS"] else "✅"
        if r[6].strip() != lolos:
            bad.append(f"{key} LULUS-sens {r[6]}!={lolos}")
    check("H6 tabel §7b S1 == JSON (%d baris)" % len(rows),
          len(rows) == 6 and not bad, "; ".join(bad[:4]) or f"{len(rows)} baris")

    n_pass = sum(1 for _, ok in RESULTS if ok)
    print(f"\n{n_pass}/{len(RESULTS)} PASS")
    return 0 if n_pass == len(RESULTS) else 1


def num_fmt(v) -> str:
    return f"{int(v):,}".replace(",", ".")


def cz(x) -> str:
    return f"{x:.4f}".replace(".", ",")


if __name__ == "__main__":
    sys.exit(main())
