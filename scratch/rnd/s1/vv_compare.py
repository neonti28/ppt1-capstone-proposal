import json
old=json.load(open("scratch/rnd/s1/bak/s1_hyd_seeds_0250.json"))
new=json.load(open("scratch/rnd/s1/s1_hyd_seeds.json"))
def h1(d):
    out={}
    for s in ("42","7","13","21","33"):
        r=d["per_seed"][s]["ringkas"]
        out[s]=tuple(sorted((k,v) for k,v in r.items()))
    return out
a,b=h1(old),h1(new)
print("H1 ringkas identik antar run:", a==b)
def ctl(d):
    k=d["kontrol_stokastik"]["per_seed"]; out={}
    for s in ("42","7","13","21","33"):
        r=k[s]["ringkas"]; out[s]=tuple(sorted((kk,vv) for kk,vv in r.items()))
    return out
c1,c2=ctl(old),ctl(new)
print("Kontrol ML identik antar run:", c1==c2)
if c1!=c2:
    for s in c1:
        for (k1,v1),(k2,v2) in zip(c1[s],c2[s]):
            if (k1,v1)!=(k2,v2): print("  beda",s,k1,v1,"->",v2)
print()
print("reproduksi semua_lulus:", new["reproduksi"]["semua_lulus"])
print("terbit_sumber:", new["reproduksi"]["terbit_sumber"])
print("terbit_r8:", json.dumps(new["reproduksi"]["terbit_r8"]))
print("delta:", json.dumps(new["reproduksi"]["delta"]))
print("n_fold_berbeda_maks:", new["n_fold_berbeda_maks"])
print("lintas_seed rentang semua 0:", all(v["rentang"]==0 for v in new["lintas_seed"].values()))
print("kontrol sebaran:", json.dumps(new["kontrol_stokastik"]["sebaran"]))
