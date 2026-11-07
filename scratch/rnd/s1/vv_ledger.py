import re, collections
L="docs/RND_PROVENANCE_LEDGER.md"
hdr=None
cnt=collections.Counter()
bad=collections.Counter()
prefix_cols=collections.defaultdict(set)
for ln in open(L):
    s=ln.rstrip("\n")
    if not s.startswith("|"): continue
    cells=[c for c in s.strip().strip("|").split("|")]
    n=len(cells)
    if hdr is None:
        hdr=cells; print("HEADER:",[c.strip() for c in cells],"n=",n); continue
    if set(s.replace("|","").replace("-","").replace(":","").strip())<= set(): pass
    if all(set(c.strip())<=set("-: ") for c in cells): continue
    pref=cells[0].strip().split("-")[0]
    prefix_cols[pref].add(n)
    cnt[n]+=1
print("\nSEBARAN JUMLAH SEL PER BARIS:", dict(cnt))
print("\nPREFIX -> jumlah sel yang dipakai:")
for p in sorted(prefix_cols, key=lambda x:-len(prefix_cols[x])):
    print(f"  {p:6s} {sorted(prefix_cols[p])}")
