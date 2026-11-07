import csv, collections, datetime, json

p = "/mnt/d/Capstone 1(v2)/data/volve/labels_curated_v2.csv"
rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
print("n_rows:", len(rows))
print("COLS:", list(rows[0].keys()))

print("\n=== SAMPLE ROW 0 ===")
for k, v in rows[0].items():
    print(f"  {k!r}: {v!r}")

print("\n=== category ===")
for k, v in collections.Counter(r["category"] for r in rows).most_common():
    print(f"{v:5d}  {k}")

print("\n=== state_detail ===")
for k, v in collections.Counter(r["state_detail"] for r in rows).most_common():
    print(f"{v:5d}  {k}")

for col in ["bha_relevant", "outcome", "component", "wellbore", "severity", "confidence", "source"]:
    if col in rows[0]:
        print(f"\n=== {col} ===")
        for k, v in collections.Counter(r[col] for r in rows).most_common(15):
            print(f"{v:5d}  {k}")

# duration sanity
def mins(r):
    try:
        a = datetime.datetime.fromisoformat(r["act_start"])
        b = datetime.datetime.fromisoformat(r["act_end"])
        return (b - a).total_seconds() / 60.0
    except Exception:
        return None

bad_parse, neg, over, ok = 0, 0, 0, 0
neg_rows, over_rows = [], []
for i, r in enumerate(rows):
    m = mins(r)
    if m is None:
        bad_parse += 1
        continue
    if m < 0:
        neg += 1
        neg_rows.append((i, r["act_start"], r["act_end"], m))
    elif m > 720 * 60:
        over += 1
        over_rows.append((i, r["act_start"], r["act_end"], round(m / 60, 2)))
    else:
        ok += 1

print("\n=== DURASI ===")
print("bad_parse", bad_parse, "neg", neg, "over720h", over, "ok", ok)
print("neg rows:", neg_rows[:10])
print("over rows:", over_rows[:20])

# any comments column with keywords?
for col in rows[0]:
    if "comment" in col.lower() or "desc" in col.lower() or "note" in col.lower() or "text" in col.lower():
        nonempty = sum(1 for r in rows if (r[col] or "").strip())
        print(f"\n=== {col} nonempty={nonempty} sample ===")
        for r in rows[:3]:
            print("   ", (r[col] or "")[:200])
