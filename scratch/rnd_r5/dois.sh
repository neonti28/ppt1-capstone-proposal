#!/usr/bin/env bash
# R5 — verifikasi DOI: status resolusi doi.org + metadata Crossref.
set -u
OUT="/mnt/d/Capstone 1(v2)/scratch/rnd_r5/doi_check.txt"
: > "$OUT"
DOIS=(
  "10.1093/biomet/41.1-2.100"
  "10.1093/biomet/58.3.509"
  "10.1109/ICDM.2008.17"
  "10.1145/342009.335388"
  "10.1109/ICDM.2016.0085"
  "10.1162/089976601750264965"
  "10.1137/1.9781611972771.42"
  "10.1145/2689746.2689747"
  "10.1214/09-AOAS282"
  "10.1080/01621459.1951.10500769"
)
for d in "${DOIS[@]}"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" -L --max-time 25 "https://doi.org/$d" || echo "ERR")
  meta=$(curl -s --max-time 25 "https://api.crossref.org/works/$d" \
     | python3 -c "import sys,json;
d=json.load(sys.stdin)['message']
a=d.get('author',[{}])[0]
print('|'.join([str(a.get('family','?')),str(a.get('given','?')),
 str((d.get('issued',{}).get('date-parts') or [[None]])[0][0]),
 (d.get('title') or ['?'])[0],
 (d.get('container-title') or ['?'])[0],
 str(d.get('volume','?')), str(d.get('page','?'))]))" 2>/dev/null || echo "CROSSREF_FAIL")
  printf "%s\t%s\t%s\n" "$d" "$code" "$meta" >> "$OUT"
  printf "%s\t%s\t%s\n" "$d" "$code" "$meta"
done
