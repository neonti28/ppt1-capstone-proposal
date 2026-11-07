import json
import urllib.request
import urllib.error

DOIS = [
    "10.1145/2382577.2382579",      # Kaufman leakage
    "10.1016/j.patter.2023.100804",  # Kapoor & Narayanan leakage
    "10.1371/journal.pone.0118432",  # Saito & Rehmsmeier PR curve
    "10.1145/1143844.1143874",      # Davis & Goadrich
    "10.1109/TII.2019.2950661",     # ? cek
    "10.1016/j.ress.2020.106889",   # ? cek
]
out = {}
for d in DOIS:
    rec = {"doi": d}
    try:
        u = f"https://api.crossref.org/works/{d}"
        with urllib.request.urlopen(u, timeout=25) as r:
            m = json.load(r)["message"]
        rec["crossref_http"] = 200
        rec["title"] = (m.get("title") or [""])[0][:160]
        rec["container"] = (m.get("container-title") or [""])[0][:80]
        rec["year"] = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        auth = m.get("author") or []
        rec["author1"] = (auth[0].get("family", "") if auth else "")
    except urllib.error.HTTPError as e:
        rec["crossref_http"] = e.code
    except Exception as e:
        rec["crossref_http"] = repr(e)[:80]
    try:
        req = urllib.request.Request(f"https://doi.org/{d}", method="HEAD",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r2:
            rec["doi_resolve"] = r2.status
    except Exception as e:
        rec["doi_resolve"] = repr(e)[:60]
    out[d] = rec
    print(json.dumps(rec, ensure_ascii=False))
json.dump(out, open("/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b/e0_doi.json", "w"),
          indent=1, ensure_ascii=False)
