#!/usr/bin/env python3
"""Audit claim boundaries for the Capstone maintenance project.

This is a read-only, standard-library audit. It does not train a model or change
project data. It verifies whether the existing proxy labels are circular, which
fixed fuzzy constants are present, and whether the labeled file contains fields
needed for prospective failure prognosis (time, RUL, maintenance, or failure).

Run from /mnt/d/Capstone 1:
    python3 code/10_audit_maintenance_claim.py \
      --csv data/USROP_labeled.csv \
      --code code/06_xgb_fuzzy.py \
      --json docs/10_AUDIT_RESULTS.json
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=Path, default=Path("data/USROP_labeled.csv"))
    parser.add_argument("--code", type=Path, default=Path("code/06_xgb_fuzzy.py"))
    parser.add_argument("--json", type=Path, default=Path("docs/10_AUDIT_RESULTS.json"))
    return parser.parse_args()


def finite_number(raw: str | None) -> float | None:
    if raw is None or raw == "":
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def percentile(values: list[float], q: float) -> float:
    """Linear percentile, matching the behavior used for the observed labels."""
    ordered = sorted(values)
    if not ordered:
        raise ValueError("Cannot calculate a percentile from an empty sequence")
    position = (len(ordered) - 1) * q / 100.0
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def find_unique_number(text: str, pattern: str) -> float:
    matches = re.findall(pattern, text)
    if len(matches) != 1:
        raise ValueError(f"Expected one match for {pattern!r}, found {len(matches)}")
    return float(matches[0])


def read_numeric_column(path: Path, column: str) -> Iterable[tuple[int, float]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if column not in (reader.fieldnames or []):
            raise KeyError(f"Column {column!r} is absent from {path}")
        for line_number, row in enumerate(reader, start=2):
            value = finite_number(row.get(column))
            if value is not None:
                yield line_number, value


def main() -> None:
    args = parse_args()
    code_text = args.code.read_text(encoding="utf-8")

    mse_positive = [value for _, value in read_numeric_column(args.csv, "MSE") if value > 0]
    roc_positive = [
        value for _, value in read_numeric_column(args.csv, "ROC_coef") if value > 0
    ]
    mse_p75 = percentile(mse_positive, 75)
    roc_p25 = percentile(roc_positive, 25)

    observed_counts: Counter[str] = Counter()
    reconstructed_counts: Counter[str] = Counter()
    mismatch_count = 0
    row_count = 0
    fieldnames: list[str] = []
    with args.csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        for row in reader:
            row_count += 1
            mse = finite_number(row.get("MSE"))
            roc = finite_number(row.get("ROC_coef"))
            observed = row.get("label", "")
            if mse is None or roc is None:
                mismatch_count += 1
                continue
            if mse > mse_p75:
                reconstructed = "high_MSE_bit_wear"
            elif roc < roc_p25:
                reconstructed = "low_ROP_efficiency"
            else:
                reconstructed = "normal"
            observed_counts[observed] += 1
            reconstructed_counts[reconstructed] += 1
            mismatch_count += observed != reconstructed

    lower_names = [name.lower() for name in fieldnames]
    time_like = [
        name
        for name in fieldnames
        if any(
            token in name.lower()
            for token in ("time", "timestamp", "date", "hour", "minute", "second", "rul")
        )
    ]
    event_like = [
        name
        for name in fieldnames
        if any(
            token in name.lower()
            for token in ("failure", "fault", "maintenance", "workover", "failure_mode")
        )
    ]

    # Verify the fixed-form fuzzy constants in the actual implementation.
    weight_match = re.search(
        r"badness\s*=\s*([0-9.]+)\s*\*\s*mse_bad\s*\+\s*"
        r"([0-9.]+)\s*\*\s*roc_bad\s*\+\s*([0-9.]+)\s*\*\s*d_bad",
        code_text,
    )
    if not weight_match:
        raise ValueError("Could not locate the fuzzy weighted aggregation in the code")
    weights = [float(item) for item in weight_match.groups()]
    health_thresholds = [
        float(item)
        for item in re.findall(r"health\s*<\s*([0-9]+)", code_text)
    ]

    result = {
        "scope": {
            "csv": str(args.csv.resolve()),
            "fuzzy_code": str(args.code.resolve()),
            "read_only": True,
        },
        "dataset": {
            "rows": row_count,
            "columns": len(fieldnames),
            "fieldnames": fieldnames,
            "time_like_fields": time_like,
            "failure_or_maintenance_fields": event_like,
        },
        "proxy_label_audit": {
            "mse_p75_positive_values": mse_p75,
            "roc_p25_positive_values": roc_p25,
            "observed_counts": dict(observed_counts),
            "reconstructed_counts": dict(reconstructed_counts),
            "mismatches": mismatch_count,
            "reconstruction_accuracy": (row_count - mismatch_count) / row_count,
            "interpretation": (
                "Labels are deterministic functions of MSE and ROC_coef. Accuracy on "
                "these labels measures rule reconstruction/consistency, not prospective "
                "failure prediction."
            ),
        },
        "fuzzy_audit": {
            "membership_shape": "linear clipped badness functions; no true rule base",
            "weights": weights,
            "health_thresholds_in_ascending_source_order": health_thresholds,
            "interpretation": (
                "The implementation calculates a current-condition health score using "
                "fixed-form weights and cutoffs. It does not forecast failure time or RUL."
            ),
        },
        "claim_boundary": {
            "supported": [
                "The folder contains a fixed-form fuzzy current-health indicator.",
                "The folder contains a classifier for rule-derived proxy labels.",
                "The labeled USROP file has no verified time, RUL, failure, or maintenance target.",
            ],
            "not_supported": [
                "The model predicts actual BHA failure.",
                "The 0.955 accuracy is external validation of maintenance outcomes.",
                "The folder prototype is the Halliburton deployed system.",
                "The project is already a selected predictive-maintenance solution.",
            ],
        },
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"rows={row_count}")
    print(f"mse_p75={mse_p75:.12g}")
    print(f"roc_p25={roc_p25:.12g}")
    print(f"label_reconstruction_mismatches={mismatch_count}")
    print(f"label_reconstruction_accuracy={(row_count - mismatch_count) / row_count:.6f}")
    print(f"time_like_fields={time_like}")
    print(f"failure_or_maintenance_fields={event_like}")
    print(f"fuzzy_weights={weights}")
    print(f"health_thresholds={health_thresholds}")
    print(f"wrote={args.json.resolve()}")


if __name__ == "__main__":
    main()
