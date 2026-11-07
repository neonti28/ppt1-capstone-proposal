import json
import subprocess
from pathlib import Path

ROOT = Path("/mnt/d/Capstone 1(v2)")
BODY = ROOT / "scratch/website_bodies"
BOARD = "website-v9-swarm"
ids = json.loads((ROOT / "scratch/website_cards.json").read_text())

specs = [
    ("R1 · Audit software-development", "r1_software.md", 6, ["dashboard-data-wiring","dogfood","systematic-debugging","requesting-code-review","test-driven-development","simplify-code"]),
    ("R2 · Audit sci dan provenance", "r2_sci.md", 6, ["scientific-critical-thinking","hypothesis-generation","statistical-analysis","experimental-design","literature-review","scientific-writing","scholar-evaluation"]),
]

new_ids = {}
for title, body_file, prio, skills in specs:
    args = ["hermes","kanban","--board",BOARD,"create",title,
            "--body-file",str(BODY/body_file),
            "--assignee","default",
            "--workspace",f"dir:{ROOT}",
            "--initial-status","blocked",
            "--priority",str(prio),
            "--max-runtime","1800"]
    for s in skills:
        args += ["--skill",s]
    args += ["--json"]
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"FAILED {title}\n{p.stdout}\n{p.stderr}")
    data = json.loads(p.stdout.strip())
    tid = data.get("id") or data.get("task_id")
    new_ids[title.split(" ")[0]] = tid
    print(title, tid)

# Link each new audit card as parent of V1.
for key in ["R1","R2"]:
    subprocess.run(["hermes","kanban","--board",BOARD,"link",new_ids[key],ids["V1"]], check=True)

# Update V1 body to mention R1/R2 outputs.
v1_body = (BODY/"v1_audit.md").read_text()
v1_body = v1_body.replace(
    "## Deliverable\nTulis `production/audit/V1_VERDICT.md`:",
    "## Input tambahan\nBaca juga `production/audit/R1_SOFTWARE.md` dan `production/audit/R2_SCI.md` bila sudah tersedia.\n\n## Deliverable\nTulis `production/audit/V1_VERDICT.md`:"
)
(BODY/"v1_audit.md").write_text(v1_body, encoding="utf-8")
p = subprocess.run(["hermes","kanban","--board",BOARD,"edit",ids["V1"],"--body",v1_body], text=True, capture_output=True)
print("V1 edit", p.returncode, p.stdout.strip()[-80:], p.stderr.strip()[-80:])

# Unblock audit cards so they can run.
for key in ["R1","R2"]:
    subprocess.run(["hermes","kanban","--board",BOARD,"unblock",new_ids[key]], check=True)

# Persist ids.
ids.update(new_ids)
(ROOT/"scratch/website_cards.json").write_text(json.dumps(ids, indent=2), encoding="utf-8")
print(json.dumps(new_ids, indent=2))
PY