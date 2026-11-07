import csv, collections, json, datetime

p = "/mnt/d/Capstone 1(v2)/data/volve/labels_curated_v2.csv"
rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
print("n_rows:", len(rows))

cat = collections.Counter(r["category"] for r in rows)
print("\n=== category ===")
for k, v in cat.most_common():
    print(f"{v:5d}  {k}")

print("\n=== state_detail top 30 ===")
sd = collections.Counter(r["state_detail"] for r in rows)
for k, v in sd.most_common(30):
    print(f"{v:5d}  {k}")

print("\n=== bha_relevant ===")
print(collections.Counter(r["bha_relevant"] for r in rows))

print("\n=== outcome ===")
for k, v in collections.Counter(r["outcome"] for r in rows).most_common():
    print(f"{v:5d}  {k}")

print("\n=== component ===")
for k, v in collections.Counter(r["component"] for r in rows).most_common():
    print(f"{v:5d}  {k}")

print("\n=== wellbore ===")
for k, v in collections.Counter(r["wellbore"] for r in rows).most_common():
    print(f"{v:5d}  {k}")

def mins(r):
    try:
        a = datetime.datetime.fromisoformat(r["act_start"])
        b = datetime.datetime.fromisoformat(r["act_end"])
        return (b - a).total_seconds() / 60.0
    except Exception:
        return None

print("\n=== durasi per category (menit) ===")
agg = collections.defaultdict(list)
for r in rows:
    m = mins(r)
    if m is not None and m >= 0:
        agg[r["category"]].append(m)
tot = 0
for k, v in sorted(agg.items(), key=lambda kv: -sum(kv[1])):
    s = sum(v)
    tot += s
    v2 = sorted(v)
    print(f"{k:35s} n={len(v):4d} sum={s:9.0f} mean={s/len(v):7.1f} median={v2[len(v2)//2]:7.1f} max={max(v):7.0f}")
print("TOTAL menit:", tot, "jam:", round(tot/60, 1))

print("\n=== rentang tanggal ===")
ds = sorted(r["event_date"] for r in rows if r["event_date"])
print(ds[0], "->", ds[-1])
