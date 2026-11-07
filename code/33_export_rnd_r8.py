#!/usr/bin/env python3
"""Export the newest RND research output (board rnd-algo-2026, R8) for the dashboard.

Reads : scratch/rnd/r8/r8_agg.json        (tasks, candidates, per fold numbers)
        scratch/rnd/r8/r8_doi.json        (citation records, copied verbatim)
        scratch/rnd/s6_digest.md          (wave 2 PM digest, first lines only)
Writes: dashboard/data/rnd_r8.json

Aggregation only. Every number is either copied from the R8 JSON or a pooled or
median summary of the numbers that are already in it; nothing is recomputed,
smoothed or invented.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)")
SRC = BASE / "scratch" / "rnd" / "r8" / "r8_agg.json"
DOI = BASE / "scratch" / "rnd" / "r8" / "r8_doi.json"
DIGEST = BASE / "scratch" / "rnd" / "s6_digest.md"
OUT = BASE / "dashboard" / "data" / "rnd_r8.json"

CANDIDATE_LABEL = {
    "H1_stat_dan_rule": "Statistic and rule, both must fire",
    "H1b_stat_atau_rule": "Statistic or rule, either may fire",
    "rule_kanal": "Channel rule only",
    "stat_cusum": "Cusum statistic only",
    "ML_saja": "Machine learning only",
    "H2_stat_dan_rule": "Statistic and rule, both must fire",
    "H2b_stat_atau_rule": "Statistic or rule, either may fire",
    "H4_tiga_komponen": "Rule, statistic and ML together",
    "H4b_strict_ML_dan_stat_dan_rule": "Strict AND of ML, statistic and rule",
    "ML_default": "Machine learning with its default threshold",
    "H2_ML_dan_stat": "Machine learning and statistic, both must fire",
    "H2b_ML_dan_stat_atau_rule": "Machine learning and statistic, or the rule",
    "H3a_GWO_objF1": "Grey wolf tuned for F1",
    "H3b_GWO_objBacc": "Grey wolf tuned for balanced accuracy",
}


def pool(values):
    """Pooled counts and fold level medians for one candidate."""
    folds = [v for v in values if isinstance(v, dict)]
    tp = sum(int(v.get("tp") or 0) for v in folds)
    fp = sum(int(v.get("fp") or 0) for v in folds)
    fn = sum(int(v.get("fn") or 0) for v in folds)
    pos = sum(int(v.get("n_pos") or 0) for v in folds)
    prec = [v["precision"] for v in folds if v.get("precision") is not None]
    rec = [v.get("recall") for v in folds if v.get("recall") is not None]
    far = [v["far24"] for v in folds if v.get("far24") is not None]
    lead = [v["lead"]["lead_median_min"] for v in folds
            if isinstance(v.get("lead"), dict) and v["lead"].get("lead_median_min") is not None]
    prev = [v["prev"] for v in folds if v.get("prev") is not None]
    bacc = [v["bacc"] for v in folds if v.get("bacc") is not None]
    out = {
        "n_fold": len(folds),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "n_pos": pos,
        "precision_pool": round(tp / (tp + fp), 4) if (tp + fp) else None,
        "recall_pool": round(tp / pos, 4) if pos else None,
        "precision_median": round(statistics.median(prec), 4) if prec else None,
        "recall_median": round(statistics.median(rec), 4) if rec else None,
        "far24_median": round(statistics.median(far), 3) if far else None,
        "far24_min": round(min(far), 3) if far else None,
        "far24_max": round(max(far), 3) if far else None,
        "lead_median_min": round(statistics.median(lead), 1) if lead else None,
        "folds_with_recall": sum(1 for v in folds if (v.get("recall") or 0) > 0),
        "folds_with_alarm": sum(1 for v in folds if (v.get("tp") or 0) + (v.get("fp") or 0) > 0),
        "folds_far_le6": sum(1 for v in folds if (v.get("far24") is not None and v["far24"] <= 6)),
    }
    out["prev_median"] = round(statistics.median(prev), 5) if prev else None
    out["bacc_median"] = round(statistics.median(bacc), 4) if bacc else None
    out["bacc_folds"] = [round(b, 4) for b in bacc]
    if out["precision_pool"] is not None and out["prev_median"]:
        out["lift"] = round(out["precision_pool"] / out["prev_median"], 2)
    else:
        out["lift"] = None
    return out


def main() -> int:
    src = json.loads(SRC.read_text())
    doi = json.loads(DOI.read_text()) if DOI.exists() else []

    tasks = {}
    for task, block in src["task"].items():
        candidates = {}
        for name, model in (block.get("model") or {}).items():
            folds = model.get("per_fold") or {}
            agg = pool(folds.values())
            agg["label"] = CANDIDATE_LABEL.get(name, name.replace("_", " "))
            agg["folds"] = {k: {
                "precision": v.get("precision"), "recall": v.get("recall"),
                "tp": v.get("tp"), "fp": v.get("fp"), "n_pos": v.get("n_pos"),
                "far24": v.get("far24"), "auprc": v.get("auprc"),
                "lead_median_min": (v.get("lead") or {}).get("lead_median_min"),
            } for k, v in folds.items()}
            candidates[name] = agg
        tasks[task] = {
            "seed": block.get("seed"),
            "alpha_budget": block.get("alpha_budget"),
            "elapsed_s": block.get("elapsed_s"),
            "candidates": candidates,
            "derived": src.get("turunan", {}).get(task),
        }

    digest_head = []
    if DIGEST.exists():
        for line in DIGEST.read_text().splitlines()[:40]:
            line = line.strip()
            if line and not line.startswith("#"):
                digest_head.append(line)
            if len(digest_head) >= 6:
                break

    out = {
        "source": str(SRC.relative_to(BASE)),
        "board": "rnd-algo-2026",
        "generated": "2026-10-27",
        "tasks": tasks,
        "doi": doi,
        "s6_digest_head": digest_head,
    }
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"written {OUT} ({OUT.stat().st_size} bytes)")
    for task, block in tasks.items():
        print(f"  {task}: {len(block['candidates'])} candidates, "
              f"derived keys {list((block['derived'] or {}).keys())[:5]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
