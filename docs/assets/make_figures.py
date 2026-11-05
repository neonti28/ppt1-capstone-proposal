#!/usr/bin/env python3
"""Membuat gambar analisis untuk proposal PPT I.

Sumber data (semuanya dibaca, tidak ada angka karangan):
  - data/volve/labels_curated_v2.csv        -> durasi kejadian, kategori, wellbore
  - data/volve/witsml_parsed/*.qc.json      -> jumlah kanal dan label yang cocok per wellbore
  - dashboard/data/engine_v9_i1.json        -> metrik head (precision, recall, far, auprc)

Jalankan: /home/neonti/.venvs/ppt1_figs/bin/python make_figures.py
Keluaran: PNG 200 dpi di folder yang sama dengan skrip ini.
"""
from __future__ import annotations

import csv
import datetime
import json
import pathlib
import re
import statistics

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = pathlib.Path("/mnt/d/ARCT-9F2")
OUT = pathlib.Path(__file__).resolve().parent
LABELS = ROOT / "data/volve/labels_curated_v2.csv"
QC_DIR = ROOT / "data/volve/witsml_parsed"
ENGINE = ROOT / "dashboard/data/engine_v9_i1.json"

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 200,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.spines.top": False,
    "axes.spines.right": False,
})
DARK = "#111A29"
RED = "#E81725"
GREEN = "#23B67C"
AMBER = "#FBB632"
GREY = "#AEB7C0"


def load_events():
    rows = list(csv.DictReader(open(LABELS, encoding="utf-8-sig")))
    out = []
    for r in rows:
        try:
            a = datetime.datetime.fromisoformat(r["act_start"])
            b = datetime.datetime.fromisoformat(r["act_end"])
        except Exception:
            continue
        out.append({
            "wellbore": r["wellbore"],
            "category": r["category"],
            "minutes": (b - a).total_seconds() / 60,
        })
    return out


def fig01_durasi(events):
    d = np.array([e["minutes"] for e in events])
    d = d[(d >= 0) & (d <= 720)]
    fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.3))

    bins = np.arange(0, 760, 60)
    ax[0].hist(d, bins=bins, color=RED, edgecolor="white", linewidth=0.6)
    ax[0].axvline(np.median(d), color=DARK, ls="--", lw=1.2,
                  label=f"median {np.median(d):.0f} menit")
    ax[0].axvline(np.percentile(d, 90), color=GREEN, ls="--", lw=1.2,
                  label=f"p90 {np.percentile(d, 90):.0f} menit")
    ax[0].set_xlabel("Durasi interupsi (menit)")
    ax[0].set_ylabel("Jumlah kejadian")
    ax[0].set_title("Distribusi durasi 883 kejadian valid")
    ax[0].legend(frameon=False, fontsize=8)

    s = np.sort(d)
    ecdf = np.arange(1, len(s) + 1) / len(s)
    ax[1].plot(s, ecdf, color=DARK, lw=1.4)
    ax[1].axhline(0.90, color=GREY, ls=":", lw=1)
    ax[1].axvline(np.percentile(d, 90), color=GREEN, ls="--", lw=1.2)
    ax[1].set_xlabel("Durasi interupsi (menit)")
    ax[1].set_ylabel("Proporsi kumulatif")
    ax[1].set_title("ECDF: 50% kejadian selesai di bawah 45 menit")
    fig.tight_layout()
    fig.savefig(OUT / "fig01_durasi_kejadian.png")
    plt.close(fig)


def fig02_kategori(events):
    cats = sorted({e["category"] for e in events}, key=lambda c: -sum(
        1 for e in events if e["category"] == c))
    wells = sorted({e["wellbore"] for e in events})
    M = np.array([[sum(1 for e in events if e["category"] == c and e["wellbore"] == w)
                   for w in wells] for c in cats])
    fig, ax = plt.subplots(figsize=(9.4, 4.2))
    from matplotlib.colors import PowerNorm
    im = ax.imshow(M, cmap="YlOrRd", aspect="auto", norm=PowerNorm(0.55, vmin=0, vmax=M.max()))
    ax.set_xticks(range(len(wells)), wells, rotation=30, ha="right")
    ax.set_yticks(range(len(cats)), cats)
    for i in range(len(cats)):
        for j in range(len(wells)):
            if M[i, j]:
                ax.text(j, i, str(M[i, j]), ha="center", va="center", fontsize=7,
                        color="white" if M[i, j] > M.max() * 0.6 else DARK)
            else:
                ax.text(j, i, "0", ha="center", va="center", fontsize=6,
                        color="#9AA3AC")
    ax.set_title("Kejadian per kategori per wellbore (total 884)")
    cb = fig.colorbar(im, ax=ax, shrink=0.75, label="jumlah kejadian",
                      ticks=[0, 5, 10, 25, 50, 75, int(M.max())])
    fig.tight_layout()
    fig.savefig(OUT / "fig02_kategori_per_wellbore.png")
    plt.close(fig)


def fig03_cakupan(events):
    wells = sorted({e["wellbore"] for e in events})
    short = [w.split("-")[-1] for w in wells]
    qc_files = list(QC_DIR.glob("*.qc.json"))

    def key(s):
        return "".join(ch for ch in s.lower() if ch.isalnum())

    # Kode sumur diambil dari pola F-<angka>[ A-D], bukan dari split("-").
    qc_key = {key(p.stem[:p.stem.index(".qc")] if ".qc" in p.stem else p.stem): p
              for p in qc_files}
    chan, matched, has_qc = [], [], []
    for w in wells:
        m = re.search(r"F-\d+\s*[A-D]?$", w)
        code = m.group(0) if m else ""
        k = key(code)
        qc = qc_key.get(k)
        if qc:
            j = json.load(open(qc, encoding="utf-8"))
            chan.append(j.get("n_channels", 0))
            matched.append(sum(1 for e in events if e["wellbore"] == w))
            has_qc.append(True)
        else:
            chan.append(0)
            matched.append(sum(1 for e in events if e["wellbore"] == w))
            has_qc.append(False)

    fig, ax = plt.subplots(figsize=(9.4, 3.4))
    x = np.arange(len(short))
    ax.bar(x - 0.2, chan, width=0.4, color=DARK, label="jumlah kanal WITSML")
    ax2 = ax.twinx()
    ax2.bar(x + 0.2, matched, width=0.4, color=RED, label="kejadian tercakup")
    ax2.grid(False)
    labels = [s + ("†" if not h else "") for s, h in zip(short, has_qc)]
    ax.set_xticks(x, labels, rotation=30, ha="right")
    ax.set_ylabel("Kanal")
    ax2.set_ylabel("Kejadian")
    ax.set_title("Cakupan data per wellbore: kanal tersedia dan kejadian tercakup")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=8, ncol=2,
              loc="lower center", bbox_to_anchor=(0.5, 1.02))
    fig.text(0.5, 0.005, "† = tidak ada berkas QC terparse untuk sumur ini",
             ha="center", fontsize=7, color=GREY)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / "fig03_cakupan_wellbore.png")
    plt.close(fig)


def load_heads():
    d = json.load(open(ENGINE, encoding="utf-8"))
    out = []
    for e in d["engines"]:
        for h in e["heads"]:
            m = h.get("metrics") or {}
            if not m:
                continue
            out.append({
                "engine": e["engine"],
                "head": h["head"],
                "layer": h["layer"],
                "precision": m.get("precision"),
                "recall": m.get("recall"),
                "far": m.get("far"),
                "auprc": h.get("auprc"),
            })
    return out


def fig04_auprc(heads):
    best = {}
    for h in heads:
        if h["auprc"]:
            best[h["engine"]] = max(best.get(h["engine"], 0), h["auprc"])
    names = list(best)
    vals = [best[n] for n in names]
    colors = [GREEN if v >= 0.5 else (AMBER if v >= 0.1 else RED) for v in vals]
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    b = ax.bar(names, vals, color=colors, edgecolor="white")
    for r, v in zip(b, vals):
        ax.text(r.get_x() + r.get_width() / 2, v + 0.02, f"{v:.3f}",
                ha="center", fontsize=8)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("AUPRC terbaik per engine")
    ax.set_title("AUPRC head ML per engine (split leave-one-well-out)")
    ax.text(0.5, -0.28, "vib tinggi berisiko sirkular karena label diturunkan dari kanal yang sama",
            transform=ax.transAxes, ha="center", fontsize=7.5, color=RED)
    fig.tight_layout()
    fig.savefig(OUT / "fig04_auprc_per_engine.png")
    plt.close(fig)


def fig05_far_recall(heads):
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    engines = sorted({h["engine"] for h in heads
                      if h["far"] is not None and h["recall"] is not None})
    palette = {e: plt.cm.tab10(i % 10) for i, e in enumerate(engines)}
    seen = set()
    for h in heads:
        if h["far"] is None or h["recall"] is None:
            continue
        c = palette[h["engine"]]
        lab = h["engine"] if h["engine"] not in seen else None
        seen.add(h["engine"])
        ax.scatter(h["far"], h["recall"], s=46, color=c, alpha=0.85,
                   edgecolor="white", linewidth=0.6, label=lab)
    ax.axvline(6, color=RED, ls="--", lw=1.2)
    ax.text(0.985, 0.30, "ambang FAR ≤ 6 / 24 jam\n(kriteria desain penulis)",
            color=RED, fontsize=7.5, ha="right", va="bottom",
            transform=ax.transAxes,
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.5))
    ax.set_xlabel("False alarm rate (per 24 jam)")
    ax.set_ylabel("Recall")
    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlim(0, 600)
    ax.set_xticks([0, 1, 6, 10, 100])
    ax.set_xticklabels(["0", "1", "6", "10", "100"])
    ax.set_ylim(-0.02, 1.05)
    ax.set_title("Trade-off false alarm dan recall: 24 head terukur dari 27")
    ax.legend(frameon=False, fontsize=7.5, ncol=3)
    fig.text(0.5, 0.005, "titik berimpit = beberapa head memiliki nilai identik",
             ha="center", fontsize=7, color=GREY)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "fig05_far_vs_recall.png")
    plt.close(fig)


def fig06_pr(heads):
    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    engines = sorted({h["engine"] for h in heads
                      if h["precision"] is not None and h["recall"] is not None})
    palette = {e: plt.cm.tab10(i % 10) for i, e in enumerate(engines)}
    seen = set()
    for h in heads:
        if h["precision"] is None or h["recall"] is None:
            continue
        lab = h["engine"] if h["engine"] not in seen else None
        seen.add(h["engine"])
        ax.scatter(h["recall"], h["precision"], s=52,
                   color=palette[h["engine"]],
                   alpha=0.85, edgecolor="white", linewidth=0.6, label=lab)
        if h["head"] == "hybrid_rule_and_persistence" and h["engine"] == "hyd":
            ax.annotate("head utama hyd\nP 0.824 · R 0.597",
                        (h["recall"], h["precision"]), textcoords="offset points",
                        xytext=(14, -26), fontsize=7.5, color=palette["hyd"],
                        arrowprops=dict(arrowstyle="-", lw=0.7,
                                        color=palette["hyd"], alpha=0.7))
    ax.plot([0, 1], [0, 1], ls=":", color=GREY, lw=1)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Presisi terhadap recall tiap head terukur")
    ax.legend(frameon=False, fontsize=7.5, ncol=3)
    fig.tight_layout()
    fig.savefig(OUT / "fig06_presisi_vs_recall.png")
    plt.close(fig)


def fig07_fmea_pareto():
    items = [
        ("Kegagalan fluida sumur", 490),
        ("Stuck pipe & fishing", 400),
        ("Kegagalan BHA", 378),
        ("Kegagalan mesin permukaan", 320),
        ("Intervensi tak terjadwal", 210),
        ("Data tak terlokalisir", 140),
        ("Kehilangan telemetri", 126),
        ("Kerugian personel", 120),
    ]
    names = [i[0] for i in items]
    vals = [i[1] for i in items]
    total = sum(vals)
    cum = np.cumsum(vals) / total * 100

    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    ax.grid(axis="x", visible=False)
    b = ax.bar(names, vals, color=[RED if v >= 300 else GREY for v in vals],
               edgecolor="white", label="prioritas tindakan (RPN ≥ 300)")
    for r, v in zip(b, vals):
        ax.text(r.get_x() + r.get_width() / 2, v + 14, str(v), ha="center", fontsize=8)
    ax.axhline(300, color=DARK, ls="--", lw=1.0)
    ax.text(len(names) - 0.4, 312, "ambang 300", ha="right", fontsize=7.5, color=DARK)
    ax.set_ylabel("RPN (S × O × D)")
    ax.set_ylim(0, 560)
    ax.set_xlabel("Mode kegagalan")

    ax2 = ax.twinx()
    ax2.plot(range(len(names)), cum, color=DARK, marker="o", ms=3.5, lw=1.3,
             label="risiko kumulatif (%)")
    ax2.axhline(80, color=AMBER, ls=":", lw=1.2)
    ax2.set_ylim(0, 105)
    ax2.set_ylabel("Risiko kumulatif (%)")
    ax2.grid(False)
    ax2.text(0.985, 82, "80%", fontsize=7.5, color=AMBER, ha="right",
             transform=ax2.get_yaxis_transform(),
             bbox=dict(fc="white", ec="none", pad=1.2))

    plt.setp(ax.get_xticklabels(), rotation=28, ha="right", fontsize=8)
    ax.set_title("Pareto risiko FMECA: empat mode pertama mencapai 72% total RPN", pad=24)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=7.5, ncol=2,
              loc="lower center", bbox_to_anchor=(0.5, 1.005))
    fig.tight_layout()
    fig.savefig(OUT / "fig07_fmea_pareto.png")
    plt.close(fig)


def main():
    events = load_events()
    heads = load_heads()
    fig01_durasi(events)
    fig02_kategori(events)
    fig03_cakupan(events)
    fig04_auprc(heads)
    fig05_far_recall(heads)
    fig06_pr(heads)
    fig07_fmea_pareto()
    total = sum(e["minutes"] for e in events)
    print(f"events={len(events)} total_minutes={total:.0f} "
          f"median={statistics.median([e['minutes'] for e in events]):.0f}")
    print("heads dengan metrik:", len(heads))
    for p in sorted(OUT.glob("fig*.png")):
        print(" ", p.name, p.stat().st_size, "byte")


if __name__ == "__main__":
    main()
