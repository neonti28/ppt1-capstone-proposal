import json
p="/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb"
nb=json.load(open(p))
cells=nb["cells"]
print("total cells:", len(cells))
print("nbformat:", nb.get("nbformat"), nb.get("nbformat_minor"))
from collections import Counter
print(Counter(c["cell_type"] for c in cells))
for i,c in enumerate(cells):
    src="".join(c["source"])
    first=src.strip().split("\n")[0][:90] if src.strip() else "(empty)"
    print(i, c["cell_type"], "|", first)
