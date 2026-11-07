import re, json, pathlib, collections

led = pathlib.Path("docs/RND_PROVENANCE_LEDGER.md")
lines = led.read_text(encoding="utf-8", errors="replace").splitlines()
print("ledger bytes", led.stat().st_size, "lines", len(lines))

pref = re.compile(r"^\|\s*(S\d)-")
counts = collections.Counter()
badcols = collections.defaultdict(list)
ids = collections.defaultdict(list)
for i, l in enumerate(lines, 1):
    m = pref.match(l)
    if not m:
        continue
    card = m.group(1)
    counts[card] += 1
    cells = [c for c in l.strip().strip("|").split("|")]
    if len(cells) != 7:
        badcols[card].append((i, len(cells)))
    ids[card].append(cells[0].strip())

print("counts per prefix:", dict(sorted(counts.items())))
for card in sorted(badcols):
    print(f"  {card}: rows with !=7 cells: {len(badcols[card])} first={badcols[card][:5]}")
for card in sorted(ids):
    v = ids[card]
    dup = [k for k, c in collections.Counter(v).items() if c > 1]
    print(f"  {card}: n={len(v)} unique={len(set(v))} dup={dup[:5]} first={v[0]} last={v[-1]}")

# block headers mentioning a card prefix
print("-- section headers --")
for i, l in enumerate(lines, 1):
    if l.startswith("#"):
        print(f"  {i}: {l[:120]}")
