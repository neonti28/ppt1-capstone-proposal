import json, os, subprocess
B="/mnt/d/Capstone 1(v2)"
print("=== run logs (first lines) ===")
for f in sorted(os.listdir(B+"/scratch/v9_e_stat")):
    if f.endswith("run_log.txt"):
        print("---",f)
        for i,l in enumerate(open(B+"/scratch/v9_e_stat/"+f)):
            if i<4: print("   ",l.rstrip())
print("=== datasets ===")
import pandas as pd
d=pd.read_csv(B+"/scratch/v9_d1/datasets/stuck_k2.csv.gz")
print("stuck_k2 rows",len(d),"wells",sorted(d.well.unique()))
t=pd.read_csv(B+"/scratch/v6_e1/toolwear_windows.csv")
print("toolwear rows",len(t),"tools",sorted(t.tool.unique()),"runs",sorted(t.run.unique()))
print("toolwear feat cols",len([c for c in t.columns if c not in ["tool","run","file","start_sample","y"]]))
# hyd_ki dataset
h=pd.read_csv(B+"/scratch/v9_d1/datasets/hyd_ki.csv.gz")
print("hyd_ki rows",len(h),"wells",len(h.well.unique()))
