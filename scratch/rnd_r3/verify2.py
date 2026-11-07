import json, urllib.request, urllib.parse, time
DOIS = [
 ("Yeh2016_MatrixProfileI_A","10.1109/ICDM.2016.0179"),
 ("Yeh2016_MatrixProfileI_B","10.1109/ICDM.2016.0085"),
 ("Dragomiretskiy2014_VMD","10.1109/TSP.2013.2288675"),
 ("Huang1998_EMD","10.1098/rspa.1998.0193"),
 ("Torrence1998_Wavelet","10.1175/1520-0477(1998)079<0061:APGTWA>2.0.CO;2"),
 ("Rakthanmanon2012_DTW","10.1145/2339530.2339576"),
 ("Mirjalili2014_GWO","10.1016/j.advengsoft.2013.12.007"),
 ("Mirjalili2016_WOA","10.1016/j.advengsoft.2016.01.008"),
]
for tag,doi in DOIS:
    url="https://api.crossref.org/works/"+urllib.parse.quote(doi)
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"rnd-verify/1.0 (mailto:neonti@example.org)"})
        with urllib.request.urlopen(req,timeout=25) as r:
            j=json.load(r)["message"]
            au=j.get("author") or [{}]
            fa=" ".join(x for x in [au[0].get("family",""),au[0].get("given","")] if x)
            yr=""
            for k in ("published-print","published-online","issued"):
                if j.get(k,{}).get("date-parts"): yr=j[k]["date-parts"][0][0]; break
            print(f"{tag} | {doi} | HTTP {r.status} | {yr} | {fa} | {(j.get('title') or [''])[0][:95]} | {(j.get('container-title') or [''])[0][:45]}")
    except Exception as e:
        print(f"{tag} | {doi} | ERR {str(e)[:80]}")
    time.sleep(0.4)
