"""XGBoost + Fuzzy Health Index — USROP labeled data.
- XGBoost baseline (Leave-One-Well-Out) vs RF/LR
- Fuzzy logic health index (0-100) dari MSE, ROP coef, D_exp
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore")


def fuzzy_health_index(mse, roc, d_exp, mse_p75, roc_p25, d_exp_med):
    """Fuzzy logic: MSE ↑ = buruk, ROC coef ↓ = buruk, D_exp deviasi = buruk.
    Output skor 0-100 (100 = sehat).
    Membership: trapesium sederhana (tidak perlu skfuzzy).
    """
    # MSE membership (0 = bagus, 1 = buruk)
    mse_bad = np.clip((mse - mse_p75 * 0.5) / (mse_p75 * 1.5 - mse_p75 * 0.5 + 1e-9), 0, 1)
    # ROC coef membership
    roc_bad = np.clip((roc_p25 * 1.5 - roc) / (roc_p25 * 1.5 - roc_p25 * 0.1 + 1e-9), 0, 1)
    # D_exp deviasi membership
    d_bad = np.clip(np.abs(d_exp - d_exp_med) / (d_exp_med * 2 + 1e-9), 0, 1)

    # Weighted fuzzy aggregation (min-max / weighted average sederhana)
    badness = 0.5 * mse_bad + 0.35 * roc_bad + 0.15 * d_bad
    health = 100 * (1 - badness)
    return health


def main():
    df = pd.read_csv("data/USROP_labeled.csv")
    feature_cols = [
        "Measured Depth m", "Weight on Bit kkgf", "Average Standpipe Pressure kPa",
        "Average Surface Torque kN.m", "Rate of Penetration m/h", "Average Rotary Speed rpm",
        "Mud Flow In L/min", "Mud Density In g/cm3", "Diameter mm", "Average Hookload kkgf",
        "Hole Depth (TVD) m", "USROP Gamma gAPI", "MSE", "D_exp", "ROC_coef",
    ]
    X = df[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(df[feature_cols].median())
    y = LabelEncoder().fit_transform(df["label"])
    wells = df["well"]
    logo = LeaveOneGroupOut()
    scaler = StandardScaler()

    print("=== MODEL COMPARISON (Leave-One-Well-Out) ===")
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "XGBoost": xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=6,
                                     random_state=42, n_jobs=-1, eval_metric="mlogloss",
                                     tree_method="hist"),
    }
    for name, model in models.items():
        accs, f1s = [], []
        for tr, te in logo.split(X, y, groups=wells):
            Xtr = scaler.fit_transform(X.iloc[tr])
            Xte = scaler.transform(X.iloc[te])
            model.fit(Xtr, y[tr])
            pred = model.predict(Xte)
            accs.append((pred == y[te]).mean())
            f1s.append(f1_score(y[te], pred, average="weighted"))
        print(f"{name}: Acc={np.mean(accs):.3f}+-{np.std(accs):.3f} | F1={np.mean(f1s):.3f}+-{np.std(f1s):.3f}")
        print(f"  folds: {[f'{a:.3f}' for a in accs]}")

    # ---- Fuzzy Health Index ----
    print("\n=== FUZZY HEALTH INDEX ===")
    mse = df["MSE"].values
    roc = df["ROC_coef"].values
    d_exp = df["D_exp"].values
    mse_p75 = np.percentile(mse[mse > 0], 75)
    roc_p25 = np.percentile(roc[roc > 0], 25)
    d_exp_med = np.median(d_exp[d_exp > 0])

    health = fuzzy_health_index(mse, roc, d_exp, mse_p75, roc_p25, d_exp_med)
    df["health_index"] = health

    print(f"Health Index: mean={health.mean():.1f}, median={np.median(health):.1f}, "
          f"min={health.min():.1f}, max={health.max():.1f}")
    print(f"\nHealth Index per label:")
    print(df.groupby("label")["health_index"].describe()[["mean", "50%", "min", "max"]])

    # Threshold → rekomendasi maintenance
    df["maintenance_recommendation"] = np.where(
        health < 40, "MAINTENANCE SEGERA",
        np.where(health < 70, "PERAWATAN RUTIN / MONITOR", "NORMAL / SEHAT"))
    print(f"\nRekomendasi:")
    print(df["maintenance_recommendation"].value_counts())

    df.to_csv("data/USROP_health.csv", index=False)
    print("\nSaved: data/USROP_health.csv")

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    df["health_index"].hist(bins=50, ax=axes[0], color="steelblue")
    axes[0].set_title("Health Index Distribution")
    axes[0].set_xlabel("Health Index (0-100)")
    df.groupby("label")["health_index"].plot(kind="kde", ax=axes[1], legend=True)
    axes[1].set_title("Health Index density by label")
    axes[1].set_xlabel("Health Index")
    axes[1].legend(["high_MSE_bit_wear", "low_ROP_efficiency", "normal"])
    plt.tight_layout()
    plt.savefig("data/health_index.png", dpi=80, bbox_inches="tight")
    print("Saved: data/health_index.png")


if __name__ == "__main__":
    main()