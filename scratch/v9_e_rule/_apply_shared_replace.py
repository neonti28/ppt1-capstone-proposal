"""Terapkan repair stuck_k2 ke path bersama (atomic) + backup original."""
import os
import shutil

BASE = "/mnt/d/Capstone 1"
SHARED = f"{BASE}/scratch/v9_d1/datasets/stuck_k2.csv.gz"
REPAIR = f"{BASE}/scratch/v9_e_rule/repair/stuck_k2.csv.gz"
BAK = f"{BASE}/scratch/v9_e_rule/stuck_k2_ORIG_nanmeta.csv.gz"

if not os.path.exists(BAK):
    shutil.copy2(SHARED, BAK)
    print("backup ->", BAK)
tmp = SHARED + ".tmp_repair"
shutil.copy2(REPAIR, tmp)
os.replace(tmp, SHARED)  # atomic: pembaca dapat file lama ATAU baru utuh
print("atomic replace ->", SHARED)
print("size:", os.path.getsize(SHARED))
