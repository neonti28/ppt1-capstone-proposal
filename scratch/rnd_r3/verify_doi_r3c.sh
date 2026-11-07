#!/usr/bin/env bash
# Verifikasi langsung 6 DOI kandidat: status Crossref, tahun, penulis pertama, judul.
set -u
B="https://api.crossref.org/works"
UA="rnd-r3/1.0 (mailto:rnd@example.org)"
for d in "$@"; do
  body=$(curl -s --max-time 25 -H "User-Agent: $UA" "$B/$d")
  st=$(printf '%s' "$body" | grep -o '"status":"[a-z]*"' | head -1)
  ti=$(printf '%s' "$body" | grep -o '"title":\[[^]]*\]' | head -1)
  yr=$(printf '%s' "$body" | grep -o '"published-print":{"date-parts":\[\[[0-9]*' | head -1 | grep -o '[0-9]*$')
  [ -z "${yr:-}" ] && yr=$(printf '%s' "$body" | grep -o '"issued":{"date-parts":\[\[[0-9]*' | head -1 | grep -o '[0-9]*$')
  fa=$(printf '%s' "$body" | grep -o '"author":\[{"[^]]*' | grep -o '"family":"[^"]*"' | head -1)
  reg=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -I "https://doi.org/$d")
  printf '%s | doi.org=%s | %s | tahun=%s | %s | %s\n' "$d" "$reg" "${st:-NONE}" "${yr:-NA}" "${fa:-NA}" "${ti:-NA}"
done
