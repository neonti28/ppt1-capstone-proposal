
import json, os, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score

BASE="/mnt/d/Capstone 1(v2)"
OUT=f"{BASE}/scratch/rnd/s2"; os.makedirs(OUT, exist_ok=True)
FEATS=[c for c in ["TQA_mean","TQA_std","TQA_slope","SPPA_mean","SPPA_std","SPPA_slope","TFLO_mean","TFLO_std","TFLO_slope","RPM_mean","RPM_std","RPM_slope","SWOB_mean","SWOB_std","SWOB_slope","feat_ts_max"]]

def run(name, label, alpha=0.10):
    d=pd.read_csv(f"{BASE}/scratch/v9_d1/datasets/{name}.csv.gz")
    d=d.sort_values(["well","ts_bin"]).reset_index(drop=True)
    F=[c for c in FEATS if c in d.columns]
    X=d[F].astype(float).fillna(0.0).values
    y=d[label].astype(int).values
    wells=sorted(d["well"].unique())
    folds=[]
    for w in wells:
        te=d["well"].values==w; tr=~te
        if y[te].sum()==0 or y[tr].sum()==0: continue
        sc=StandardScaler().fit(X[tr]); Xtr=sc.transform(X[tr]); Xte=sc.transform(X[te])
        clf=LogisticRegression(max_iter=2000, class_weight="balanced", C=1.0).fit(Xtr,y[tr])
        p_tr=clf.predict_proba(Xtr)[:,1]; p_te=clf.predict_proba(Xte)[:,1]
        thr=float(np.quantile(p_tr, 1-alpha))
        ml=(p_te>=thr).astype(int)
        # stat gate: SPPA_mean z-score from train distribution
        j=F.index("SPPA_mean") if "SPPA_mean" in F else 0
        mu, sd = X[tr][:,j].mean(), X[tr][:,j].std() or 1.0
        z=np.abs((X[te][:,j]-mu)/sd)
        st=(z>=2.0).astype(int)
        hyb=(ml & st).astype(int)
        def m(pred):
            tp=int(((pred==1)&(y[te]==1)).sum()); fp=int(((pred==1)&(y[te]==0)).sum())
            fn=int(((pred==0)&(y[te]==1)).sum())
            return dict(tp=tp, fp=fp, fn=fn, precision=round(tp/(tp+fp),4) if tp+fp else 0.0,
                        recall=round(tp/(tp+fn),4) if tp+fn else 0.0, n_pos=int(y[te].sum()), n=int(te.sum()))
        folds.append(dict(well=w, n=int(te.sum()), n_pos=int(y[te].sum()),
                          auprc=round(float(average_precision_score(y[te], p_te)),4),
                          prev=round(float(y[te].mean()),4),
                          ml=m(ml), stat=m(st), hybrid=m(hyb),
                          thr=round(thr,4), alpha=alpha))
    def agg(k, f):
        v=[x[k][f] for x in folds]
        return dict(median=round(float(np.median(v)),4), min=round(float(np.min(v)),4), max=round(float(np.max(v)),4))
    res=dict(dataset=name, label=label, rows=int(len(d)), wells=wells, folds=folds,
             agg={k:{f:agg(k,f) for f in ["precision","recall","fp"]} for k in ["ml","stat","hybrid"]},
             auprc_median=round(float(np.median([x["auprc"] for x in folds])),4),
             prev_median=round(float(np.median([x["prev"] for x in folds])),4))
    json.dump(res, open(f"{OUT}/s2_{name}.json","w"), indent=1)
    print(name, "rows",res["rows"],"folds",len(folds),"AUPRC",res["auprc_median"],"prev",res["prev_median"])
    for k in ["ml","hybrid","stat"]:
        print("  ",k, res["agg"][k])
    return res

v=run("vib","y_vib"); s=run("ssi","y_ssi")
