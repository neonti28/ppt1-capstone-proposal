#!/usr/bin/env bash
# Verifikasi DOI dua lapis: (1) registrasi doi.org tanpa redirect, (2) metadata Crossref.
# Keluaran: satu baris per DOI -> status registrasi | status crossref | tahun | penulis1 | judul
set -u
OUT="$HOME/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_1fe4eed0/doi_verify_r3.tsv"
: > "$OUT"

check() {
  doi="$1"
  reg=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -I "https://doi.org/$doi" 2>/dev/null)
  body=$(curl -s --max-time 20 "https://api.crossref.org/works/$doi" 2>/dev/null)
  cr=$(printf '%s' "$body" | grep -o '"status":"[a-z]*"' | head -1)
  title=$(printf '%s' "$body" | sed -n 's/.*"title":\["\([^"]*\)"\].*/\1/p' | head -1)
  year=$(printf '%s' "$body" | sed -n 's/.*"published-print":{"date-parts":\[\[\([0-9]*\).*/\1/p' | head -1)
  if [ -z "$year" ]; then
    year=$(printf '%s' "$body" | sed -n 's/.*"issued":{"date-parts":\[\[\([0-9]*\).*/\1/p' | head -1)
  fi
  auth=$(printf '%s' "$body" | sed -n 's/.*"author":\[{"affiliation":\[\],"family":"\([^"]*\)".*/\1/p' | head -1)
  if [ -z "$auth" ]; then
    auth=$(printf '%s' "$body" | sed -n 's/.*"family":"\([^"]*\)".*/\1/p' | head -1)
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$doi" "$reg" "${cr:-NONE}" "$year" "$auth" "$title" | tee -a "$OUT"
}

while read -r d; do
  [ -z "$d" ] && continue
  check "$d"
done <<'LIST'
10.1109/TSP.2013.2288675
10.1098/rspa.1998.0193
10.1002/cpa.3160410705
10.1007/BF00994018
10.1109/ICDM.2016.0179
10.1016/j.sigpro.2015.09.041
10.1016/j.sigpro.2013.04.015
10.3390/electronics12061290
10.1016/j.advengsoft.2013.12.007
10.1016/j.advengsoft.2016.01.008
10.2118/127413-MS
10.1016/j.ymssp.2015.04.021
LIST
echo "WROTE $OUT"
