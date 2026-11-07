"""EDA + Baseline ML — USROP labeled data.
Membaca USROP_labeled.csv, EDA, Leave-One-Well-Out baseline (LR, RF), feature importance.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
import warnings
warnings.filterwarnings("ignore")

pd.set_option("display.max_columns", None)

def main():
    df = pd.read_csv("data/USROP_labeled.csv")
    print("=== DATA ===")
    print(f"Shape: {df.shape}")
    print(f"Labels: {df['label'].value_counts().to_dict()}")
    print(f"Wells: {df['well'].nunique()}")

    feature_cols = [
        "Measured Depth m", "Weight on Bit kkgf", "Average Standpipe Pressure kPa",
        "Average Surface Torque kN.m", "Rate of Penetration m/h", "Average Rotary Speed rpm",
        "Mud Flow In L/min", "Mud Density In g/cm3", "Diameter mm", "Average Hookload kkgf",
        "Hole Depth (TVD) m", "USROP Gamma gAPI", "MSE", "D_exp", "ROC_coef",
    ]

    X = df[feature_cols].copy()
    y = df["label"].copy()
    wells = df["well"].copy()

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    print(f"Mapping: {dict(zip(le.classes_, range(len(le.classes_))))}")

    X = X.replace([np.inf, -np.inf], np.nan).fillna(X.median())

    # ---- EDA ----
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    corr = X.corr()
    sns.heatmap(corr, cmap="RdBu_r", center=0, ax=axes[0, 0],
                xticklabels=[c[:10] for c in feature_cols],
                yticklabels=[c[:10] for c in feature_cols])
    axes[0, 0].set_title("Feature Correlation")
    axes[0, 0].tick_params(labelsize=6)

    pd.crosstab(df["well"].str[:18], df["label"], normalize="index").plot(
        kind="bar", stacked=True, ax=axes[0, 1], color=["green", "red", "orange"])
    axes[0, 1].set_title("Label Distribution per Well")
    axes[0, 1].tick_params(axis="x", rotation=45, labelsize=7)

    X_box = X.copy()
    X_box["label"] = y
    X_box.boxplot(column=["MSE", "D_exp", "ROC_coef"], by="label", ax=axes[1, 0])
    axes[1, 0].set_title("Physics Features by Label")
    axes[1, 0].set_yscale("symlog")

    axes[1, 1].scatter(X["ROC_coef"], X["MSE"], c=y_enc, s=3, alpha=0.2, cmap="RdYlGn_r")
    axes[1, 1].set_title("ROC coef vs MSE (colored by label)")
    axes[1, 1].set_xlim(0, 0.002)
    axes[1, 1].set_ylim(0, 500000)
    plt.tight_layout()
    plt.savefig("data/EDA_full.png", dpi=80, bbox_inches="tight")
    print("Saved: data/EDA_full.png")

    # ---- Baseline: Leave-One-Well-Out ----
    print("\n=== LEAVE-ONE-WELL-OUT ===")
    logo = LeaveOneGroupOut()
    scaler = StandardScaler()
    for name, model in [
        ("Logistic Regression", LogisticRegression(max_iter=1000)),
        ("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ]:
        accs, f1s = [], []
        for tr, te in logo.split(X, y_enc, groups=wells):
            Xtr = scaler.fit_transform(X.iloc[tr])
            Xte = scaler.transform(X.iloc[te])
            model.fit(Xtr, y_enc[tr])
            pred = model.predict(Xte)
            accs.append((pred == y_enc[te]).mean())
            f1s.append(f1_score(y_enc[te], pred, average="weighted"))
        print(f"{name}: Acc={np.mean(accs):.3f}+-{np.std(accs):.3f} | F1={np.mean(f1s):.3f}+-{np.std(f1s):.3f}")
        print(f"  per fold: {[f'{a:.3f}' for a in accs]}")

    # ---- Feature importance ----
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(scaler.fit_transform(X), y_enc)
    imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("\n=== FEATURE IMPORTANCE ===")
    print(imp.to_string())

    fig, ax = plt.subplots(figsize=(10, 6))
    imp.plot(kind="barh", ax=ax, color="steelblue")
    ax.set_title("Feature Importance (Random Forest)")
    plt.tight_layout()
    plt.savefig("data/feature_importance.png", dpi=80, bbox_inches="tight")
    print("Saved: data/feature_importance.png")

if __name__ == "__main__":
    main()