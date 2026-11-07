import json, urllib.request, urllib.error, ssl
DOIS = [
 ("Vovk 2005 Algorithmic Learning in a Random World", "10.1007/b106715"),
 ("Chen & Guestrin 2016 XGBoost", "10.1145/2939672.2939785"),
 ("DeLong 1988 comparing AUC", "10.2307/2531595"),
 ("Liu 2008 Isolation Forest", "10.1109/ICDM.2008.17"),
 ("Page 1954 continuous inspection", "10.1093/biomet/41.1-2.100"),
 ("Romano 2019 conformalized quantile regression", "10.1214/18-AOS1801"),
 ("Niculescu-Mizil 2005 predicting good probabilities", "10.1145/1102351.1102430"),
 ("Teale 1965 concept of specific energy", "10.1016/0148-9062(65)90022-7"),
]
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
out=[]
for label, doi in DOIS:
    rec={"label":label,"doi":doi}
    try:
        req=urllib.request.Request("https://api.crossref.org/works/"+doi, headers={"User-Agent":"rnd-e1-check/1.0 (mailto:rnd@example.org)"})
        with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
            rec["crossref_http"]=r.status
            m=json.loads(r.read().decode())
            msg=m.get("message",{})
            rec["title"]=(msg.get("title") or [""])[0]
            auth=msg.get("author") or []
            rec["first_author"]=((auth[0].get("family","") if auth else ""))
            rec["year"]=(msg.get("issued",{}).get("date-parts",[[None]])[0] or [None])[0]
            rec["container"]=(msg.get("container-title") or [""])[0]
    except urllib.error.HTTPError as e:
        rec["crossref_http"]=e.code
    except Exception as e:
        rec["crossref_http"]="ERR:"+str(e)[:80]
    # layer 1: registration, redirects OFF
    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*a,**k): return None
    op=urllib.request.build_opener(NoRedir)
    try:
        req2=urllib.request.Request("https://doi.org/"+doi, method="HEAD")
        with op.open(req2, timeout=25) as r:
            rec["doi_org_http"]=r.status
    except urllib.error.HTTPError as e:
        rec["doi_org_http"]=e.code
    except Exception as e:
        rec["doi_org_http"]="ERR:"+str(e)[:60]
    out.append(rec)
json.dump(out, open("doi_check.json","w"), indent=1, ensure_ascii=True)
for r in out:
    print(r["doi"], "| doi.org", r.get("doi_org_http"), "| Crossref", r.get("crossref_http"), "|", r.get("first_author"), r.get("year"), "|", (r.get("title") or "")[:70])
