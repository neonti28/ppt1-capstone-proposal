import json
import subprocess
from pathlib import Path

ROOT = Path("/mnt/d/Capstone 1(v2)")
BODY = ROOT / "scratch/website_bodies"
BOARD = "website-v9-swarm"

CARDS = [
    ("W1 · Shell dan layout", "w1_shell.md", 10),
    ("W2 · Data dan provenance", "w2_data.md", 9),
    ("W3 · Isi sepuluh tampilan", "w3_views.md", 9),
    ("W4 · Interaksi dan aksesibilitas", "w4_app.md", 8),
    ("V1 · Auditor independen", "v1_audit.md", 7),
    ("S1 · Integrasi dan verdict akhir", "s1_final.md", 6),
]


def run(args):
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(args)}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p.stdout.strip()


ids = {}
for title, body_file, prio in CARDS:
    args = [
        "hermes", "kanban", "--board", BOARD, "create", title,
        "--body-file", str(BODY / body_file),
        "--assignee", "default",
        "--workspace", f"dir:{ROOT}",
        "--initial-status", "blocked",
        "--priority", str(prio),
        "--max-runtime", "3600",
        "--skill", "antislop",
        "--skill", "antislop-ui",
        "--skill", "antislop-layoutmobile",
        "--json",
    ]
    out = run(args)
    data = json.loads(out)
    task_id = data.get("id") or data.get("task_id")
    if not task_id:
        raise SystemExit(f"No id in output: {out}")
    ids[title.split(" ")[0]] = task_id
    print(f"{title}: {task_id}")

# Wire V1 after all four builders, then S1 after V1.
for key in ["W1", "W2", "W3", "W4"]:
    run(["hermes", "kanban", "--board", BOARD, "link", ids[key], ids["V1"]])
run(["hermes", "kanban", "--board", BOARD, "link", ids["V1"], ids["S1"]])

(ROOT / "scratch/website_cards.json").write_text(json.dumps(ids, indent=2), encoding="utf-8")
print(json.dumps(ids, indent=2))
