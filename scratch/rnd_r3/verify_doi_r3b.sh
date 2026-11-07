#!/usr/bin/env bash
# Versi perbaikan: http -> https (Crossref membalas 301 pada http).
set -u
B="https://api.crossref.org/works"
UA="rnd-r3/1.0 (mailto:rnd@example.org)"

au() {
  echo "--- $1"
  curl -s --max-time 25 -H "User-Agent: $UA" "$B/$1" \
    | grep -o '"author":\[{"[^]]*' | grep -o '"family":"[^"]*"' | head -6
}

echo "===== AUTHOR: 10.3390/electronics12061290 ====="
au 10.3390/electronics12061290
echo "===== AUTHOR: 10.1109/TSP.2013.2288675 ====="
au 10.1109/TSP.2013.2288675
echo "===== AUTHOR: 10.1109/ICDM.2016.0179 ====="
au 10.1109/ICDM.2016.0179

echo
echo "===== SAKOE-CHIBA 1978 10.1109/TASSP.1978.1163055 ====="
curl -s --max-time 25 -H "User-Agent: $UA" "$B/10.1109/TASSP.1978.1163055" \
  | grep -o '"status":"[a-z]*"\|"title":\[[^]]*\]\|"family":"[^"]*"\|"date-parts":\[\[[0-9]*' | head -8

echo
echo "===== QUERY: Ratanamahatana Keogh learned constraints ====="
curl -s --max-time 30 -H "User-Agent: $UA" --get "$B" \
  --data-urlencode "query.bibliographic=Ratanamahatana Keogh making time series classification more accurate using learned constraints" \
  --data-urlencode "rows=3" \
  | grep -o '"DOI":"[^"]*"\|"title":\[[^]]*\]' | head -8

echo
echo "===== QUERY: VMD GWO SVM bearing ====="
curl -s --max-time 30 -H "User-Agent: $UA" --get "$B" \
  --data-urlencode "query.bibliographic=variational mode decomposition grey wolf optimizer support vector machine bearing fault diagnosis" \
  --data-urlencode "rows=5" \
  | grep -o '"DOI":"[^"]*"\|"title":\[[^]]*\]' | head -12

echo
echo "===== QUERY: WOA GWO hybrid ====="
curl -s --max-time 30 -H "User-Agent: $UA" --get "$B" \
  --data-urlencode "query.bibliographic=hybrid whale optimization algorithm grey wolf optimizer" \
  --data-urlencode "rows=4" \
  | grep -o '"DOI":"[^"]*"\|"title":\[[^]]*\]' | head -10
