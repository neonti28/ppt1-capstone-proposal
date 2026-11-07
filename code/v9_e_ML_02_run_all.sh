#!/bin/bash
# V9-E_ML driver — jalankan 4 engine berurutan, log ke console
set -e
cd "/mnt/d/Capstone 1"
for e in vib ssi shk stuck_k2; do
  echo "############ ENGINE $e ############"
  python3 code/v9_e_ML_01_train.py --engine "$e" $( [ "$e" = vib ] && echo --determinism-check )
done
echo "ALL DONE"
