#!/usr/bin/env python3
"""Export the V9-I1 engine result into the shape the dashboard reads.

Reads   : scratch/v9_i1/v9_i1_RESULTS.json
Writes  : dashboard/data/engine_v9_i1.json

Only re-shapes and counts. No value is invented, rescaled, or smoothed: every
number in the output is copied from the source JSON or counted from it.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scratch" / "v9_i1" / "v9_i1_RESULTS.json"
OUT = ROOT / "dashboard" / "data" / "engine_v9_i1.json"

LAYER_ORDER = ["L0", "L1", "L2", "L3"]
LAYER_LABEL = {
    "L0": "L0 Confirm status",
    "L1": "L1 Supervised warning",
    "L2": "L2 Trend score",
    "L3": "L3 Human / unavailable",
}
ENGINE_NAME = {
    "vib": "Vibration",
    "ssi": "Stick-slip",
    "shk": "Shock, bit bounce",
    "stuck": "Stuck pipe",
    "hyd": "Hydraulic",
    "bit_wear": "Bit wear",
    "tool_wear": "Tool wear",
}

TIER_COLOR = {
    "PERINGATAN-BERPENGAWAS": "#E2142E",
    "TREN": "#FBB632",
    "BELUM LAYAK PAKAI": "#AEB7C0",
    "ALARM-OTOMATIS": "#FC282D",
}


def head_metrics(h: dict) -> dict | None:
    m = h.get("metrik_segmen")
    if not m:
        return None
    return {
        "n": m.get("n"),
        "pos": m.get("pos"),
        "neg": m.get("neg"),
        "tp": m.get("tp"),
        "fp": m.get("fp"),
        "fn": m.get("fn"),
        "precision": m.get("precision"),
        "recall": m.get("recall"),
        "far": m.get("far_segmen"),
    }


def main() -> None:
    src = json.loads(SRC.read_text(encoding="utf-8"))

    heads_flat: list[dict] = []
    engines_out: list[dict] = []
    for e in src["engines"]:
        heads = []
        for h in e["heads"]:
            row = {
                "engine": e["engine"],
                "head": h["head"],
                "layer": h.get("layer"),
                "tier": h.get("tier"),
                "klaim": h.get("klaim"),
                "human_review": bool(h.get("human_review_required")),
                "head_utama": bool(h.get("head_utama")),
                "n_windows": h.get("n_windows"),
                "n_aktif": h.get("n_aktif"),
                "frac_aktif": h.get("frac_aktif"),
                "lead_menit": h.get("lead_menit"),
                "auprc": h.get("auprc_segmen"),
                "n_nodata": h.get("n_nodata"),
                "definisi": h.get("definisi"),
                "badge_far": h.get("badge_far"),
                "keyakinan": h.get("keyakinan"),
                "batas": h.get("batas_pemakaian"),
                "status": h.get("status"),
                "alasan": h.get("alasan"),
                "metrics": head_metrics(h),
            }
            heads.append(row)
            heads_flat.append(row)

        engines_out.append(
            {
                "engine": e["engine"],
                "display_name": ENGINE_NAME.get(e["engine"], e["engine"]),
                "klaim_tugas": e.get("klaim_tugas"),
                "jenis_tugas": e.get("jenis_tugas"),
                "sumber_tier": e.get("sumber_tier"),
                "n_heads": len(heads),
                "heads": heads,
            }
        )

    counts = src["decision_layer"]["ringkasan"]
    layers = [
        {
            "key": k,
            "label": LAYER_LABEL[k],
            "value": counts.get(k, 0),
            "items": src["decision_layer"]["layers"].get(k, []),
        }
        for k in LAYER_ORDER
    ]

    tier_counts: dict[str, int] = {}
    for h in heads_flat:
        tier_counts[h["tier"]] = tier_counts.get(h["tier"], 0) + 1
    tiers = [
        {"label": t, "value": c, "color": TIER_COLOR.get(t, "#6E7989")}
        for t, c in sorted(tier_counts.items(), key=lambda kv: -kv[1])
    ]

    capability = []
    for p in src["profil_kapabilitas"]:
        a = p.get("lapisan_A_deteksi", {})
        b = p.get("lapisan_B_nilai_maintenance", {})
        c = p.get("lapisan_C_ketepatan", {})
        capability.append(
            {
                "engine": p["engine"],
                "jenis_tugas": p.get("jenis_tugas"),
                "klaim_tugas": p.get("klaim_tugas"),
                "a_heads": a.get("head_dengan_metrik", 0),
                "a_precision": a.get("presisi_maks"),
                "a_recall": a.get("recall_maks"),
                "a_far_min": a.get("far_min"),
                "b_status": b.get("status"),
                "b_lead": b.get("lead_menit") or {},
                "b_alasan": b.get("alasan"),
                "c_heads": c.get("head_peringatan_L1", []),
                "kekuatan": p.get("kekuatan_bukti"),
                "layak_untuk": p.get("layak_untuk", []),
                "belum_untuk": p.get("belum_untuk", []),
            }
        )

    berbagi = src["nilai_maintenance"]
    review = [
        {
            "engine": r["engine"],
            "head": r["head"],
            "far": r.get("far_per_24jam"),
            "per_shift": r.get("tinjauan_per_shift_8jam"),
        }
        for r in berbagi.get("beban_tinjauan_L1", [])
    ]

    downtime = [
        {"label": k, "hours": v}
        for k, v in berbagi.get("jam_henti_per_sebab", {}).items()
        if k != "success"
    ]
    downtime.sort(key=lambda r: -r["hours"])

    activity = [
        {"label": k, "hours": v}
        for k, v in sorted(berbagi.get("jam_per_kode", {}).items(), key=lambda kv: -kv[1])
    ]

    segments = [
        {
            "engine": k,
            "n": v.get("n"),
            "rentang_menit": v.get("rentang_menit"),
        }
        for k, v in src["segmen_info"].items()
    ]

    utama = next((h for h in heads_flat if h["head_utama"]), None)

    limits = [
        "No rupiah cost data exists in the repository, so no saving is stated in money.",
        "No work order numbers exist, so stopped hours cannot be mapped to a single alarm.",
        "FAR in the review load block is the F-14 segment figure, not the cross fold median.",
        "Four Random Forest heads only run with --ml; without the flag their status is TIDAK DIJALANKAN.",
        "The hyd K-ii claim (kick / loss) is still BELUM TERSEDIA DI PROTOTIPE.",
    ]

    sources = [
        {"label": "Engine output", "path": "scratch/v9_i1/v9_i1_RESULTS.json"},
        {"label": "Wave 2 verdict", "path": "docs/RND_S6_PM_WAVE2.md"},
        {"label": "Engine integration note", "path": "docs/RND_ENGINE_S6_INTEGRATION.md"},
        {"label": "Audit note status", "path": "docs/RND_S5_DEFECT_STATUS.md"},
        {"label": "Provenance ledger", "path": "docs/RND_PROVENANCE_LEDGER.md"},
        {"label": "Evaluation policy", "path": "docs/RND_EVALUATION_POLICY.md"},
    ]

    payload = {
        "meta": src["meta"],
        "keputusan_akhir": src["keputusan_akhir"],
        "human_review_required": src["human_review_required"],
        "kpi": {
            "engines": src["meta"]["n_engine"],
            "heads": len(heads_flat),
            "heads_with_metrics": sum(1 for h in heads_flat if h["metrics"]),
            "l1_warnings": src["decision_layer"]["nperingatan_l1"],
            "auto_alarm_slots": src["decision_layer"]["auto_critical_alarm_slots"],
            "human_review_heads": sum(1 for h in heads_flat if h["human_review"]),
        },
        "utama": utama,
        "layers": layers,
        "tiers": tiers,
        "engines": engines_out,
        "heads": heads_flat,
        "capability": capability,
        "review_load": review,
        "downtime": downtime,
        "activity": activity,
        "segments": segments,
        "maintenance": {
            "sumber": berbagi.get("sumber"),
            "n_record": berbagi.get("n_record_aktivitas"),
            "total_jam": berbagi.get("total_jam_tercatat"),
            "success_jam": berbagi.get("jam_henti_per_sebab", {}).get("success"),
            "batas": berbagi.get("batas"),
        },
        "limits": limits,
        "sources": sources,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print("engines", payload["kpi"]["engines"], "heads", payload["kpi"]["heads"],
          "l1", payload["kpi"]["l1_warnings"], "alarm_slots", payload["kpi"]["auto_alarm_slots"])
    print("tiers", [(t['label'], t['value']) for t in tiers])
    print("layers", [(l['key'], l['value']) for l in layers])
    print("heads_with_metrics", payload["kpi"]["heads_with_metrics"],
          "human_review", payload["kpi"]["human_review_heads"])
    print("utama", utama["engine"], utama["head"], utama["metrics"]["precision"],
          utama["metrics"]["recall"], utama["metrics"]["far"], utama["lead_menit"])


if __name__ == "__main__":
    main()
