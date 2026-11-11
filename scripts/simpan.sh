#!/bin/sh
# Simpan dan kirim ke GitHub dalam satu langkah.
# Pakai: sh scripts/simpan.sh "pesan commit"
set -e
pesan="${1:-perbarui dokumen}"
git add -A docs
git commit -m "$pesan" || echo "tidak ada perubahan untuk di-commit"
git push origin HEAD:main
git rev-parse HEAD
git ls-remote origin refs/heads/main
