import json, re
BASE = "/mnt/d/Capstone 1(v2)/"
D = json.load(open(BASE + "scratch/rnd_e1/e1_scores.json"))
led = open(BASE + "docs/RND_PROVENANCE_LEDGER.md", encoding="utf-8").read().splitlines()
row = {}
for ln in led:
    m = re.match(r"\|\s*([A-Z0-9]+-\d+)\s*\|", ln)
    if m:
        row[m.group(1)] = ln
ID_RE = r"ledger ([A-Z0-9]+-\d+)"
# hanya angka yang membawa beban bukti: desimal, ribuan bertitik, atau persen
NUM_RE = r"\d+,\d+|\d{1,3}(?:\.\d{3})+"
bad = []
for k, a in D["matriks"].items():
    for e, c in a["sel"].items():
        al = c["alasan"]
        ids = re.findall(ID_RE, al)
        nums = re.findall(NUM_RE, al)
        if not ids:
            if nums:
                bad.append((k, e, "angka tanpa rujukan ledger", "", nums, al[:70]))
            continue
        for i in ids:
            if i not in row:
                bad.append((k, e, "ID tidak ada", i, nums, ""))
                continue
            if nums and not any(n in row[i] for n in nums):
                bad.append((k, e, "angka tidak ada di baris", i, nums, al[:70]))
print("violations:", len(bad))
for b in bad:
    print(b)
