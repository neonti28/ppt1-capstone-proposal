import json, urllib.request, urllib.parse, sys, time

DOIS = [
 ("Dragomiretskiy2014_VMD","10.1109/TSP.2013.2288675"),
 ("Huang1998_EMD","10.1098/rspa.1998.0193"),
 ("Mirjalili2014_GWO","10.1016/j.advengsoft.2013.12.007"),
 ("Mirjalili2016_WOA","10.1016/j.advengsoft.2016.01.008"),
 ("Rakthanmanon2012_DTW","10.1145/2339530.2339576"),
 ("Yeh2016_MatrixProfile","10.1109/ICDM.2016.0172"),
 ("Reckmann2010_DrillingVib","10.2118/127413-MS"),
 ("Torrence1998_Wavelet","10.1175/1520-0477(1998)079<0061:APGTWA>2.0.CO;2"),
]
out=[]
for tag,doi in DOIS:
    url="https://api.crossref.org/works/"+urllib.parse.quote(doi)
    rec={"tag":tag,"doi":doi,"crossref":"","title":"","year":"","first_author":"","container":""}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"rnd-verify/1.0 (mailto:neonti@example.org)"})
        with urllib.request.urlopen(req,timeout=25) as r:
            j=json.load(r)["message"]
            rec["crossref"]=str(r.status)
            rec["title"]=(j.get("title") or [""])[0]
            rec["container"]=(j.get("container-title") or [""])[0]
            for k in ("published-print","published-online","issued"):
                if j.get(k,{}).get("date-parts"):
                    rec["year"]=j[k]["date-parts"][0][0]; break
            au=j.get("author") or []
            if au:
                rec["first_author"]=" ".join(x for x in [au[0].get("family",""),au[0].get("given","")] if x)
    except Exception as e:
        rec["crossref"]="ERR "+str(e)[:90]
    out.append(rec)
    print(json.dumps(rec,ensure_ascii=False))
    time.sleep(0.4)
json.dump(out,open("doi_crossref.json","w"),ensure_ascii=False,indent=1)
