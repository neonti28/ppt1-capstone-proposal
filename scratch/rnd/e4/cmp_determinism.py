import json

base = "/mnt/d/Capstone 1(v2)/scratch/rnd/e4"
a = json.load(open(f"{base}/e4_summary_run1.json"))
b = json.load(open(f"{base}/e4_summary.json"))

print("elapsed run1", a["elapsed_s"], "run2", b["elapsed_s"])
print("n_fitur", a["n_fitur"], b["n_fitur"])
print("assert_r7_1 run1", a["assert_r7_1"])
print("assert_r7_1 run2", b["assert_r7_1"])

IDENTICAL = True
keys = sorted(set(a["ringkas"]) | set(b["ringkas"]))
print("\n%-26s %-22s %-22s %s" % ("varian", "field", "run1", "run2"))
for k in keys:
    ra, rb = a["ringkas"].get(k, {}), b["ringkas"].get(k, {})
    for f in sorted(set(ra) | set(rb)):
        va, vb = ra.get(f), rb.get(f)
        same = (va == vb)
        if not same:
            IDENTICAL = False
            print("%-26s %-22s %-22s %s  BEDA" % (k, f, va, vb))
print("\nSEMUA ANGKA RINGKASAN IDENTIK:", IDENTICAL)
