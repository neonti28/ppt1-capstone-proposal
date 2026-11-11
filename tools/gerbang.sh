#!/bin/sh
# Gerbang commit. Hanya pemeriksa angka yang berhak menolak commit, karena
# hanya itu yang objektif: angka yang tidak cocok dengan registry selalu salah.
#
# Pemeriksa gaya dan isi hanya melapor. Uji pada 2026-11-10 menunjukkan dua
# cacat yang membuat keduanya tidak layak memblokir:
#   - positif palsu: paragraf teknis yang benar diblokir hanya karena memakai
#     frasa "alih-alih", sementara paragraf itu menjelaskan mekanisme sirkularitas;
#   - positif palsu kedua: sampah yang diberi angka lolos, jadi aturan ini bisa
#     diakali dengan menaburkan angka, dan itu justru merusak naskah.
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
echo "GERBANG: angka lolos"
