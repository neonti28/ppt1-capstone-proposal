import json
d = json.load(open('/mnt/d/Capstone 1(v2)/scratch/rnd/r8/r8_hyd.json'))
print("keys:", list(d.keys()))
print("seed:", d.get("seed"), "alpha:", d.get("alpha_budget"), "elapsed:", d.get("elapsed_s"))
print("n rows:", len(d["rows"]))
print(json.dumps(d["ringkas"], indent=1))
# per fold H1
for r in d["rows"]:
    if r["model"] == "H1_stat_dan_rule":
        print(r["fold"], "fp", r["rows"]["fp"], "tp", r["rows"]["tp"],
              "P", round(r["rows"]["precision"],4), "R", round(r["rows"]["recall"],4),
              "far24", r["far24_kalender"], "lead", r["lead"]["lead_median_min"],
              "nonset", r["lead"]["n_onset"], "warn", r["lead"]["n_diperingatkan"], "h", r["h_terpilih"])
