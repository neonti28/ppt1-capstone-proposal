#!/bin/bash
# JALANKAN SEMUA ENGINE V9 — satu perintah menjalankan seluruh 7 mesin / 27 head
# Lokasi: /mnt/d/Capstone 1(v2)/code/jalankan_semua.sh
# Pakai   : bash "/mnt/d/Capstone 1(v2)/code/jalankan_semua.sh"
set -u
cd "/mnt/d/Capstone 1(v2)" || exit 1
LOG="scratch/jalankan_semua.log"
mkdir -p scratch
echo "== MULAI $(date '+%F %T') ==" | tee "$LOG"

run () {
  echo; echo "############ $1 ############" | tee -a "$LOG"
  shift
  "$@" 2>&1 | tee -a "$LOG"
  echo "-> exit ${PIPESTATUS[0]}" | tee -a "$LOG"
}

# 1. RULE + PERSISTENCE + HIBRIDA (5 kelas status + onset + bitwear/toolwear + hyd k2)
run "RULE_01 status vib/ssi/shk/stuck_k1/hyd_ki" python3 code/v9_e_RULE_01_status.py
run "RULE_02 stuck onset (4 well)"               python3 code/v9_e_RULE_02_stuck_onset.py
run "RULE_03 bit_wear + tool_wear"               python3 code/v9_e_RULE_03_bitwear_toolwear.py
run "RULE_04 hyd K-ii (z-pit)"                   python3 code/v9_e_RULE_04_hyd_k2.py

# 2. STATISTIK
run "STAT_01 hyd K-i"                            python3 code/v9_e_STAT_01_hyd_ki.py
run "STAT_02 stuck E2 (q95 train)"               python3 code/v9_e_STAT_02_stuck_e2.py
run "STAT_03 tool_wear (SSE+perm+kalibrasi)"     python3 code/v9_e_STAT_03_tool_wear.py
run "STAT_04 Fisher/Pearson hyd K-ii"            python3 code/v9_e_STAT_04_fisher_pearson.py

# 3. ML (hanya 4 engine yang mengizinkan RF; hyd_ki dilarang)
run "ML vib"      python3 code/v9_e_ML_01_train.py --engine vib --determinism-check
run "ML ssi"      python3 code/v9_e_ML_01_train.py --engine ssi
run "ML shk"      python3 code/v9_e_ML_01_train.py --engine shk
run "ML stuck_k2" python3 code/v9_e_ML_01_train.py --engine stuck_k2

# 4. PROTOTIPE ALAT (27 head, satu laporan)
run "PROTOTIPE i1 (semua head + ML)" python3 code/v9_i1_run.py --well F-14 --ml

# 5. VERIFIKATOR (13 cek)
run "VERIFIER 13 cek" python3 code/v9_i1_verify.py

echo; echo "== SELESAI $(date '+%F %T') — lihat $LOG dan scratch/v9_e_*/ *_RESULTS.json ==" | tee -a "$LOG"
