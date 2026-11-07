import csv, re

csvrows = list(csv.DictReader(open('/mnt/d/Capstone 1/docs/V2_TSPP_AE_SCORES.csv')))
doc = open('/mnt/d/Capstone 1/docs/V2_ML_RESULTS.md').read()
tbl = re.findall(r'^\| (TSPP[^|]+\.csv) \| ([\d.]+) \| (\d+) \| ([\d,]+) \| ([\d,]+)% \| ([\d,]+)% \|$', doc, re.M)
print("baris tabel cocok pola:", len(tbl))
assert len(tbl) == 6, "jumlah baris tabel bukan 6"
ok = True
for c, t in zip(csvrows, tbl):
    f = t[0].strip()
    rows = int(t[1].replace('.', ''))
    mc = int(t[2])
    err = t[3].replace(',', '.')
    shr = float(t[4].replace(',', '.')) / 100
    sz = float(t[5].replace(',', '.')) / 100
    checks = [
        (f == c['file'], "file %s vs %s" % (f, c['file'])),
        (rows == int(c['rows']), "rows %s vs %s" % (rows, c['rows'])),
        (mc == int(c['matched_cols']), "cols %s vs %s" % (mc, c['matched_cols'])),
        (round(float(c['err_median']), 4) == round(float(err), 4), "err %s vs %s" % (err, c['err_median'])),
        (round(float(c['share_above_threshold']) * 100, 1) == round(shr * 100, 1),
         "share %s vs %s" % (shr, c['share_above_threshold'])),
        (round(float(c['share_rows_any_z_gt3']) * 100, 1) == round(sz * 100, 1),
         "z %s vs %s" % (sz, c['share_rows_any_z_gt3'])),
    ]
    for good, msg in checks:
        if not good:
            ok = False
            print("  MISMATCH:", msg)
    print(("PASS " if all(g for g, _ in checks) else "FAIL ") + f)
print("ALL ROWS IDENTIK:", ok)
for n in ["0,1218", "0,0457", "0,0267", "0,0796", "0,0750", "0,1721", "0,1005",
          "0,058", "0,110", "0,151", "0,256", "0,044", "157", "0,2386", "0,0804", "0,1032"]:
    print(n, "count:", doc.count(n))
print("grep 138033:", len(re.findall(r'138033|138\.033', doc)))
