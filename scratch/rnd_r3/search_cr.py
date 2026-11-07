import json, urllib.request, urllib.parse, time

QUERIES = [
 ("matrix_profile_yeh", "Matrix Profile I All Pairs Similarity Joins for Time Series"),
 ("vmd_bearing_svm", "variational mode decomposition support vector machine bearing fault diagnosis"),
 ("vmd_gwo_bearing", "grey wolf optimizer variational mode decomposition bearing fault"),
 ("drilling_vibration_ml", "drilling vibration machine learning stuck pipe prediction"),
 ("wavelet_bearing_cnn", "wavelet transform bearing fault diagnosis convolutional"),
]
for tag,q in QUERIES:
    url="https://api.crossref.org/works?"+urllib.parse.urlencode({
        "query.bibliographic":q,"rows":6,
        "select":"DOI,title,author,issued,container-title,is-referenced-by-count","mailto":"neonti@example.org"})
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"rnd-verify/1.0"})
        with urllib.request.urlopen(req,timeout=30) as r:
            items=json.load(r)["message"]["items"]
        print("=== ",tag," | ",q)
        for it in items:
            au=it.get("author") or [{}]
            fa=" ".join(x for x in [au[0].get("family",""),au[0].get("given","")] if x)
            yr=""
            for k in ("published-print","published-online","issued"):
                if it.get(k,{}).get("date-parts"):
                    yr=it[k]["date-parts"][0][0]; break
            print(f"  {it['DOI']} | {yr} | {fa} | {(it.get('title') or [''])[0][:110]} | {(it.get('container-title') or [''])[0][:50]} | cit={it.get('is-referenced-by-count')}")
    except Exception as e:
        print("ERR",tag,e)
    time.sleep(0.5)
