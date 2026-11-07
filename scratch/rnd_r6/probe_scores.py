"""R6: apakah JSON ML/STAT menyimpan vektor skor? (dibutuhkan DeLong berpasangan)."""
import json
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1(v2)/scratch")
FILES = [
    "v9_e_ml/v9_e_ML_vib_RESULTS.json",
    "v9_e_ml/v9_e_ML_shk_RESULTS.json",
    "v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json",
    "v9_e_stat/v9_e_stat_04_fisher_pearson_RESULTS.json",
    "v9_eval_b/v9_eval_b_RESULTS.json",
    "v9_eval_c/v9_eval_c_RESULTS.json",
]
SCORE_KEYS = ("score", "scores", "proba", "prob", "y_prob", "y_score", "pred", "preds",
              "scores_pos", "scores_neg", "roc", "fpr", "tpr", "thresholds")


def scan(o, path="$", depth=0, hits=None):
    if hits is None:
        hits = []
    if depth > 6:
        return hits
    if isinstance(o, dict):
        for k, v in o.items():
            kl = str(k).lower()
            if any(s == kl or s in kl for s in SCORE_KEYS):
                n = len(v) if hasattr(v, "__len__") else 1
                hits.append((f"{path}.{k}", type(v).__name__, n))
            scan(v, f"{path}.{k}", depth + 1, hits)
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]):
            scan(v, f"{path}[{i}]", depth + 1, hits)
    return hits


for f in FILES:
    P = BASE / f
    if not P.exists():
        print(f, "-> TIDAK ADA")
        continue
    d = json.loads(P.read_text(encoding="utf-8"))
    hits = scan(d)
    print(f"\n=== {f} (top keys: {list(d.keys())[:10]})")
    if not hits:
        print("   TIDAK ADA kunci bernuansa skor/ROC")
    for h in hits[:25]:
        print("   ", h)
