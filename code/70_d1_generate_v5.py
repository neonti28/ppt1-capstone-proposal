"""D1 generator — mass synthetic labeled runs from rig_telemetry_sim (Capstone V5, J1).

Card: t_2ba30073. Produces data/sim_v5/<class>/<run_id>/ per run:
  surface_telemetry.csv + pipe_tally.csv + surveys.csv + events.json
  + ground_truth.json + run_metadata.json + scenario.json + label.json
and one manifest row per run in data/sim_v5/manifest.csv.

Class design (each parameter verified separable in pilots d1_pilot/d1_pilot2,
seed 4242, see docs/V5_D1_GENERATOR.md):
  normal_soft    : UCS U(2,5) MPa, baseline everything else
  hard_formation : UCS U(15,40) MPa (formation condition, NOT BHA damage)
  high_friction  : decomposed hydraulics + bha_resistance_kpa_per_m3_min_squared
                   U(800,2200) -> SPP/DIFP anomaly (FK2-style torque_drag friction
                   VERIFIED inert on this vertical short-hole config)
  bit_wear       : bit.cutting_efficiency U(0.10,0.40)
  low_rpm        : rotary_speed_command_rpm U(20,40)
  low_pump       : pump_speed_command_spm U(50,80)

Anti-leakage measures: per-run seeded interval length U(40,80) m (hard: U(15,30)),
rpm/spm jitter on every class. n_rows/duration remain ROP-correlated by physics;
they are flagged LEAKY (ban list) in docs/V5_D1_GENERATOR.md, not features.

Label provenance (acceptance b): class_label = the injected physical parameter
recorded in label.json + manifest; linkage to the run is the canonical scenario
hash chain: sha256(canonical JSON of scenario) == run_metadata.provenance
.canonical_scenario_hash == ground_truth.run.canonical_scenario_hash (re-verified
per run by this script and again by 71_d1_verify_v5.py).

Determinism (acceptance d): all randomness derives from (master_seed, class, index);
the simulator itself is byte-deterministic per scenario+seed (R1 t_ec3b9280).
Regenerating any run with the same args reproduces byte-identical files.

Usage:
  python 70_d1_generate_v5.py [--runs-per-class 200] [--workers 8] [--master-seed 20261010]
"""
import argparse
import concurrent.futures
import csv
import hashlib
import json
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/mnt/d/Capstone 1")
TEMPLATE = ROOT / "data/sim-fault/FK0_normal.json"
OUT_ROOT = ROOT / "data/sim_v5"
CLI = Path.home() / ".hermes/cache/scratch/r1-rigsim-venv/bin/rig-telemetry-sim"
SIM_VERSION = "rig-telemetry-sim 0.1.0a1"

BASE_START_MD = 300.0

CLASSES = ("normal_soft", "hard_formation", "high_friction", "bit_wear",
           "low_rpm", "low_pump")


def canonical_hash(data: dict) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sample_params(cls: str, rng: random.Random) -> dict:
    """Seeded physical-parameter draw for one run of one class."""
    p = {
        "ucs_pa": rng.uniform(2e6, 5e6),
        "cutting_efficiency": 1.0,
        "bha_resistance_kpa_per_m3_min_squared": 0.0,
        "rotary_speed_command_rpm": rng.uniform(60.0, 80.0),
        "pump_speed_command_spm": rng.uniform(110.0, 130.0),
        "interval_len_m": rng.uniform(40.0, 80.0),
    }
    if cls == "hard_formation":
        p["ucs_pa"] = rng.uniform(15e6, 40e6)
        p["interval_len_m"] = rng.uniform(15.0, 30.0)
    elif cls == "high_friction":
        p["bha_resistance_kpa_per_m3_min_squared"] = rng.uniform(800.0, 2200.0)
    elif cls == "bit_wear":
        p["cutting_efficiency"] = rng.uniform(0.10, 0.40)
    elif cls == "low_rpm":
        p["rotary_speed_command_rpm"] = rng.uniform(20.0, 40.0)
    elif cls == "low_pump":
        p["pump_speed_command_spm"] = rng.uniform(50.0, 80.0)
    return p


def build_scenario(cls: str, params: dict, seed: int) -> dict:
    sc = json.loads(TEMPLATE.read_text())
    end_md = BASE_START_MD + round(params["interval_len_m"], 3)
    sc["name"] = f"d1-{cls}"
    sc["seed"] = seed
    sc["run"]["end_md_m"] = end_md
    # well plan must cover [start_md, end_md]
    sc["well_plan"]["stations"] = [
        {"md_m": 0.0, "inclination": 0.0, "azimuth": 0.0},
        {"md_m": end_md, "inclination": 0.0, "azimuth": 0.0},
    ]
    sc["formation"]["intervals"][0]["ucs_pa"] = round(params["ucs_pa"], 1)
    sc.setdefault("bit", {})["cutting_efficiency"] = round(params["cutting_efficiency"], 4)
    if params["bha_resistance_kpa_per_m3_min_squared"] > 0:
        sc.setdefault("hydraulics", {}).update({
            "pressure_model": "decomposed",
            "bha_resistance_kpa_per_m3_min_squared":
                round(params["bha_resistance_kpa_per_m3_min_squared"], 1),
        })
    sc["schedule"]["rotary_speed_command_rpm"] = round(
        params["rotary_speed_command_rpm"], 2)
    sc["schedule"]["pump_speed_command_spm"] = round(
        params["pump_speed_command_spm"], 2)
    return sc


def generate_one(cls: str, idx: int, master_seed: int) -> dict:
    run_id = f"{cls}_r{idx:04d}"
    run_dir = OUT_ROOT / cls / run_id
    row = {"run_id": run_id, "class_label": cls, "index": idx}
    if (run_dir / "surface_telemetry.csv").exists() \
            and (run_dir / "label.json").exists():
        row["status"] = "skipped_existing"
    else:
        rng = random.Random(f"{master_seed}:{cls}:{idx}")
        params = sample_params(cls, rng)
        seed = master_seed * 1000 + CLASSES.index(cls) * 250 + idx
        sc = build_scenario(cls, params, seed)
        if run_dir.exists():
            shutil.rmtree(run_dir)
        # CLI refuses an existing output dir -> generate into a temp sibling,
        # then move the export set into the final run dir.
        tmp_dir = run_dir.with_name(run_dir.name + ".tmp")
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir)
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        scen_file = tmp_dir.with_suffix(".json")  # scenario lives beside tmp dir
        scen_file.write_text(json.dumps(sc, indent=2))
        t0 = time.time()
        proc = subprocess.run(
            [str(CLI), "generate", str(scen_file), "--output", str(tmp_dir),
             "--no-parquet"],
            capture_output=True, text=True,
        )
        row["wall_s"] = round(time.time() - t0, 2)
        if proc.returncode != 0:
            row["status"] = f"failed_rc{proc.returncode}"
            row["error"] = proc.stderr.strip()[:300]
            return row
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        tmp_dir.rename(run_dir)
        scen_file.rename(run_dir / "scenario.json")
        # provenance + physical label, hash-chained to the run outputs below
        label = {
            "class_label": cls,
            "injected_parameters": {
                "formation.ucs_pa": sc["formation"]["intervals"][0]["ucs_pa"],
                "bit.cutting_efficiency": sc["bit"]["cutting_efficiency"],
                "hydraulics.bha_resistance_kpa_per_m3_min_squared":
                    sc.get("hydraulics", {}).get(
                        "bha_resistance_kpa_per_m3_min_squared", 0.0),
                "schedule.rotary_speed_command_rpm":
                    sc["schedule"]["rotary_speed_command_rpm"],
                "schedule.pump_speed_command_spm":
                    sc["schedule"]["pump_speed_command_spm"],
                "run.end_md_m": sc["run"]["end_md_m"],
            },
            "seed": seed,
            "canonical_scenario_hash": canonical_hash(sc),
            "label_semantics": (
                "formation condition (not BHA damage)" if cls == "hard_formation"
                else "BHA hydraulic restriction anomaly" if cls == "high_friction"
                else "equipment/operating fault class"),
            "generator": "70_d1_generate_v5.py",
        }
        (run_dir / "label.json").write_text(json.dumps(label, indent=2))
        row["status"] = "ok"

    # common manifest fields (also for skipped_existing)
    label = json.loads((run_dir / "label.json").read_text())
    csv_path = run_dir / "surface_telemetry.csv"
    gt = json.loads((run_dir / "ground_truth.json").read_text())
    meta = json.loads((run_dir / "run_metadata.json").read_text())
    ip = label["injected_parameters"]
    row.update({
        "seed": label["seed"],
        "ucs_pa": ip["formation.ucs_pa"],
        "cutting_efficiency": ip["bit.cutting_efficiency"],
        "bha_resistance_kpa": ip["hydraulics.bha_resistance_kpa_per_m3_min_squared"],
        "rpm_cmd": ip["schedule.rotary_speed_command_rpm"],
        "spm_cmd": ip["schedule.pump_speed_command_spm"],
        "start_md_m": BASE_START_MD,
        "end_md_m": ip["run.end_md_m"],
        "canonical_scenario_hash": label["canonical_scenario_hash"],
        "csv_sha256": sha256_file(csv_path),
        "n_rows": sum(1 for _ in csv_path.open()) - 1,
        "sim_version": SIM_VERSION,
    })
    # hash-chain integrity: label <-> scenario file <-> run outputs
    scen = json.loads((run_dir / "scenario.json").read_text())
    chain_ok = (
        canonical_hash(scen) == label["canonical_scenario_hash"]
        == meta["provenance"]["canonical_scenario_hash"]
        == gt["run"]["canonical_scenario_hash"]
        and meta["seed"] == label["seed"]
    )
    row["hash_chain_ok"] = chain_ok
    if not chain_ok:
        row["status"] = "hash_chain_mismatch"
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-per-class", type=int, default=200)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--master-seed", type=int, default=20261010)
    args = ap.parse_args()

    if not CLI.exists():
        print(f"FATAL: CLI not found: {CLI}")
        return 2
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    jobs = [(cls, i) for cls in CLASSES for i in range(args.runs_per_class)]
    print(f"generating {len(jobs)} runs ({len(CLASSES)} classes x "
          f"{args.runs_per_class}) with {args.workers} workers")
    rows = []
    t0 = time.time()
    with concurrent.futures.ProcessPoolExecutor(args.workers) as ex:
        futs = {ex.submit(generate_one, cls, i, args.master_seed): (cls, i)
                for cls, i in jobs}
        for n, fut in enumerate(concurrent.futures.as_completed(futs), 1):
            rows.append(fut.result())
            if n % 100 == 0:
                print(f"  {n}/{len(jobs)} done, elapsed {time.time()-t0:.0f}s",
                      flush=True)

    rows.sort(key=lambda r: (r["class_label"], r["index"]))
    manifest = OUT_ROOT / "manifest.csv"
    fields = sorted({k for r in rows for k in r})
    with open(manifest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    ok = sum(r["status"] in ("ok", "skipped_existing") for r in rows)
    failed = [r for r in rows if r["status"] not in ("ok", "skipped_existing")]
    print(f"manifest: {manifest} ({len(rows)} rows, {ok} ok, {len(failed)} failed)")
    for r in failed[:10]:
        print("  FAIL", r["run_id"], r["status"], r.get("error", ""))
    print(f"total wall {time.time()-t0:.0f}s")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
