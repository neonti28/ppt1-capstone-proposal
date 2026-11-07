#!/usr/bin/env bash
# Harvest Crossref via curl (urllib di WSL hang; curl terbukti 1,1 s/req).
set -u
cd "$(dirname "$0")"
mkdir -p raw
UA="RND-R1-research/1.0 (mailto:rnd@example.invalid)"
SEL="DOI,title,author,issued,container-title,is-referenced-by-count"
i=0
while IFS='|' read -r slug term; do
  [ -z "$slug" ] && continue
  for dom in "fault diagnosis" "bearing fault" "drilling" "predictive maintenance" "vibration"; do
    q=$(printf '%s %s' "$term" "$dom" | sed 's/ /+/g')
    out="raw/${slug}__$(printf '%s' "$dom" | tr ' ' '_').json"
    if [ ! -s "$out" ]; then
      curl -s -m 25 -A "$UA" "https://api.crossref.org/works?query.bibliographic=${q}&filter=from-pub-date:2019-01-01,type:journal-article&rows=25&select=${SEL}" -o "$out"
      i=$((i+1))
      printf '.'
      sleep 0.4
    fi
  done
done <<'EOF'
gwo|grey wolf optimizer
woa|whale optimization algorithm
pso|particle swarm optimization
ssa|sparrow search algorithm
hho|harris hawks optimization
epo|emperor penguin optimizer
sma|slime mould algorithm
bgwo|binary grey wolf optimizer
eo|equilibrium optimizer
hbo|honey badger optimization
horse|horse herd optimization
slime|slime mould optimization
EOF
echo
echo "requests=$i files=$(ls raw | wc -l) bytes=$(du -sh raw | cut -f1)"
