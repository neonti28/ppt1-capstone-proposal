import json
r8=json.load(open("scratch/rnd/r8/r8_hyd.json"))
SEHARUSNYA=dict(fp_total=935, precision_median=0.7789, recall_median=0.5638,
                lead_median=11.5, tp_total=3804, n_onset=390, n_diperingatkan=219)
def bangun(r):
    ring=r["ringkas"]["H1_stat_dan_rule"]; rows=[x for x in r["rows"] if x["model"]=="H1_stat_dan_rule"]
    return dict(fp_total=int(ring["fp_total"]), precision_median=float(ring["precision_median"]),
                recall_median=float(ring["recall_median"]), lead_median=float(ring["lead_median_median"]),
                tp_total=int(ring["tp_total"]),
                n_onset=int(sum(x["lead"]["n_onset"] for x in rows)),
                n_diperingatkan=int(sum(x["lead"]["n_diperingatkan"] for x in rows)))
def uji(r,label):
    try:
        v=bangun(r)
        for k,val in SEHARUSNYA.items():
            assert abs(float(v[k])-float(val))<=1e-9, f"{k}: kartu {val} != file {v[k]}"
        print(f"{label}: LOLOS (tidak ada beda)")
    except AssertionError as e:
        print(f"{label}: GAGAL sesuai harapan -> {e}")
uji(json.loads(json.dumps(r8)), "r8 asli")
m=json.loads(json.dumps(r8)); m["ringkas"]["H1_stat_dan_rule"]["fp_total"]=936
uji(m, "r8 fp_total diubah 936")
m2=json.loads(json.dumps(r8)); m2["ringkas"]["H1_stat_dan_rule"]["precision_median"]=0.78
uji(m2, "r8 presisi diubah 0,78")
