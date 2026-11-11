#!/bin/sh
# Gerbang commit. Hanya pemeriksa angka yang berhak menolak commit, karena
# hanya itu yang objektif: angka yang tidak cocok dengan registry selalu salah.
#
# Pemeriksa gaya, isi, dan entitas hanya melapor. Uji pada 2026-11-10 terhadap
# label dari pengguna menunjukkan tiga cacat yang membuat ketiganya tidak layak
# memblokir:
#   - gerbang frasa: recall 0 dari 10 kalimat yang pengguna sebut sampah;
#   - gerbang entitas: memblokir 6 user story yang justru diwajibkan, karena
#     user story memakai kata "saya";
#   - sampah yang diberi angka lolos gerbang isi, jadi aturan itu bisa diakali
#     dengan menaburkan angka, dan itu merusak naskah.
set -e
cd "$(git rev-parse --show-toplevel)"

if ! out=$(python3 tools/periksa_angka.py 2>&1); then
  echo "$out" | tail -3
  echo "GERBANG: angka tidak konsisten, commit ditolak"
  exit 1
fi

echo "--- laporan gaya (tidak memblokir) ---"
python3 tools/periksa_gaya.py | tail -4 || true
echo "--- laporan isi (tidak memblokir) ---"
python3 tools/periksa_isi.py | tail -1 || true
echo "--- laporan entitas (tidak memblokir) ---"
python3 tools/periksa_entitas.py | tail -1 || true
echo "GERBANG: angka lolos"
