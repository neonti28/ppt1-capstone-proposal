# KEBIJAKAN EVALUASI Detektor (mengikat R7, R8, E4, PM)

Sumber primer: `/mnt/d/Capstone 1/Evaluasi User.txt` (5.090 byte, dibaca 2026-10-27 10:40 WIB).
Kebijakan ini menimpa setiap kalimat di plan R&D yang memperlakukan gate C/A/B sebagai gerbang
biner "lolos atau buang".

## 1. Tidak ada gate biner

Gate dipakai untuk menyatakan **kekuatan bukti kemampuan prediksi**, bukan untuk memutuskan
apakah sebuah detektor boleh dipakai sama sekali. Detektor yang tidak melewati gate tetap dicatat
sebagai informasi kemampuan, batas penggunaan, dan kekuatan bukti.

## 2. Tiga lapisan penilaian, bukan satu ambang

- **Lapisan A, apakah deteksi bekerja:** precision, recall, false alarm, waktu deteksi, sesuai
  tugas masing-masing detektor.
- **Lapisan B, apakah deteksi memberi nilai maintenance:** peringatan datang sebelum kondisi
  memburuk, ada waktu untuk bertindak, mengurangi pemeriksaan yang tidak perlu. Waktu peringatan
  terhadap kejadian nyata adalah ukuran utama.
- **Lapisan C, apakah cukup tepercaya:** hasil bertahan pada periode, kondisi operasi, dan
  peralatan berbeda; kualitas sensor, perubahan kondisi, dan ketidakpastian ditangani.

satu mode boleh layak untuk pemantauan tren tetapi belum layak mengeluarkan alarm kritis
otomatis. Itu keputusan yang sah, bukan kegagalan sistem.

## 3. Detektor tidak harus sama antar kerusakan

Untuk kerusakan x boleh detektor a, untuk kerusakan y boleh detektor a atau detektor lain. Setiap
kelas kerusakan (vib, ssi, shk, stuck, hyd, bit_wear, tool_wear) dinilai dengan kriteria dan
baseline yang relevan untuk tugasnya sendiri.

## 4. Hybrid dan perpaduan tiga komponen diizinkan

Detektor boleh rule based, statistical, persistence, anomaly detection, supervised ML, atau
campuran. Perpaduan tiga sekaligus (ML + metaheuristik + statistik) diizinkan dan harus diuji
sebagai kandidat tersendiri, bukan dianggap varian dari satu mode.

Bentuk hybrid yang wajib dipertimbangkan minimal:

1. **Statistik + rule**: detektor perubahan (CUSUM/Page-Hinkley) yang memicu pemeriksaan rule kanal.
2. **ML + statistik**: skor ML dikalibrasi conformal, gerbang akhir memakai residu statistik.
3. **Metaheuristik + ML**: bobot atau ambang ML dipilih GWO/WOA/PSO, dibandingkan dengan setelan default.
4. **Tiga komponen**: rule kanal sebagai gerbang, statistik sebagai penstabil, ML sebagai pemeringkat.

## 5. Baseline per tugas

Perbandingan selalu memakai baseline yang relevan untuk tugas itu, bukan satu baseline universal.
Untuk hyd K-i baseline yang sudah terukur: persistence P 0,615-0,793, hybrid FP 2.091 menjadi 927,
FAR 14,6-58,4. Untuk tool_wear, baseline adalah regime bengkel 469 jendela.

## 6. Empat kelas yang gagal tidak dibuang

- **stuck:** persistence menang untuk klasifikasi status, tetapi detektor masih berguna untuk onset,
  durasi abnormal, atau kegagalan kembali normal. Target itu diuji terpisah.
- **hyd:** label berasal dari SPPA dan aliran, jadi detektor berguna untuk mendeteksi atau
  merekonstruksi kondisi yang didefinisikan variabel itu; klaim prediksi kegagalan hidraulik
  independen adalah klaim lain yang butuh uji sendiri.
- **shk:** kelas positif langka bukan alasan menolak detektor; pertanyaannya apakah kejadian
  relevan ditemukan dengan alarm palsu yang bisa ditangani.
- **tool_wear:** model yang belum terbukti generalisasi lintas alat tetap berguna untuk pemantauan
  alat yang dikenal; klaim lintas alat adalah klaim tambahan.

## 7. Keberhasilan dinilai di tingkat alat

Keberhasilan diukur pada tingkat alat predictive maintenance secara keseluruhan, bukan dari
jumlah model ML yang melewati satu gate. Validitas data, pengujian temporal, dan transparansi
ketidakpastian tetap wajib.

## 8. Konsekuensi untuk dokumen yang sudah ada

`docs/RND_E3_HASIL.md` menyatakan tidak ada finalis yang memenuhi gate A. Itu tetap benar sebagai
pernyataan kemampuan, tetapi **tidak boleh** dibaca sebagai vonis buang. R7, R8, E4, dan PM wajib
menilai ulang dengan lapisan A/B/C per tugas, termasuk kandidat hybrid pada §4.
