#!/usr/bin/env bash
# R6: verifikasi DOI lewat Crossref + status landing doi.org. Output mentah ke file.
set -u
OUT="/mnt/d/Capstone 1(v2)/scratch/rnd_r6/doi_verify_r6.json"
TMP="/tmp/r6_doi"
mkdir -p "$TMP"
: > "$OUT"

DOIS=(
  "10.2307/2531595"
  "10.1214/aos/1176344552"
  "10.1111/j.2517-6161.1995.tb02031.x"
  "10.1080/01621459.1927.10502953"
  "10.1007/BF02295996"
  "10.1007/978-3-642-40994-3_29"
  "10.1371/journal.pone.0118432"
  "10.1148/radiology.143.1.7063747"
  "10.1023/A:1024068626366"
  "10.1162/089976698300017197"
  "10.1525/collabra.33267"
  "10.2307/2340521"
  "10.2307/4615733"
)

echo "[" >> "$OUT"
first=1
for D in "${DOIS[@]}"; do
  CR=$(curl -sS -m 25 -H "Accept: application/json" "https://api.crossref.org/works/${D}")
  HTTP_DOI=$(curl -sS -m 25 -o /dev/null -w "%{http_code}" -L "https://doi.org/${D}")
  TITLE=$(printf '%s' "$CR" | python3 -c 'import sys,json;
d=json.load(sys.stdin)
m=d.get("message",{})
t=(m.get("title") or [""])[0]
a=(m.get("author") or [{}])
a0=a[0] if a else {}
print(t.replace("|","/"))
print(a0.get("family","?")+", "+a0.get("given","?"))
print((m.get("container-title") or ["?"])[0].replace("|","/"))
print((m.get("issued",{}).get("date-parts") or [["?"]])[0][0])
print(m.get("DOI","?"))
print(m.get("type","?"))' 2>/dev/null)
  [ $first -eq 1 ] || echo "," >> "$OUT"
  first=0
  python3 - "$D" "$HTTP_DOI" <<'PY' >> "$OUT"
import sys, json
doi, http = sys.argv[1], sys.argv[2]
lines = sys.stdin if False else None
PY
  T=$(printf '%s\n' "$TITLE" | sed -n '1p')
  A=$(printf '%s\n' "$TITLE" | sed -n '2p')
  C=$(printf '%s\n' "$TITLE" | sed -n '3p')
  Y=$(printf '%s\n' "$TITLE" | sed -n '4p')
  RT=$(printf '%s\n' "$TITLE" | sed -n '6p')
  J=$(python3 -c "import json,sys;print(json.dumps({'doi':sys.argv[1],'http_doi_org':sys.argv[2],'crossref_title':sys.argv[3],'author_first':sys.argv[4],'container':sys.argv[5],'year':sys.argv[6],'type':sys.argv[7]},ensure_ascii=False))" "$D" "$HTTP_DOI" "$T" "$A" "$C" "$Y" "$RT")
  echo -n "$J" >> "$OUT"
  echo "OK $D http=$HTTP_DOI | $A | $Y | $T"
done
echo "" >> "$OUT"
echo "]" >> "$OUT"
echo "--- json ditulis: $OUT"
python3 -c "import json;d=json.load(open('$OUT'));print('n=',len(d))"
