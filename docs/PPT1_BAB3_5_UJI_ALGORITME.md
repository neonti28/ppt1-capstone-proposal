# BAB III 3.5: UJI TAMBAHAN PEMILIHAN ALGORITME: PENCARIAN OTOMATIS DAN KOMBINASI KANDIDAT

Subbab ini melaporkan dua uji tambahan atas pemilihan algoritme pada Bab III. Pertama, pencarian hyperparameter otomatis (H2O AutoML) diadu dengan Random Forest yang dipakai sebagai detektor utama. Kedua, seluruh kandidat hasil pencarian otomatis digabung untuk melihat apakah gabungan mengalahkan satu model terbaik. Naskah teknis lengkap ada di `docs/PPT1_ABLAT_AUTOML.md` bagian 1 sampai 6, dengan bukti mentah di `docs/evidence/` dan `docs/evidence/pred/`.

## 3.5.1 Pertanyaan yang diuji

1. Apakah pencarian otomatis dengan anggaran komputasi besar mengalahkan Random Forest antar hiperparameter kontrak: pada data kejadian, alias pemilihan otomatis memberi keunggulan atau tidak.
2. Bila satu model pilihan otomatis kalah, apakah kekurangan itu dapat ditutup dengan menggabungkan seluruh kandidat yang dihasilkan pencarian otomatis.
3. Apakah masih ada cacat data yang harus dibereskan lebih dulu sebelum keluarga algoritme tertentu dapat dipakai.

## 3.5.2 Setelan uji

| Parameter | Nilai |
|---|---|
| Data uji | 4.619 baris, 480 fitur, 243 positif (5,3 persen), label kategori enam bukti kegagalan |
| Skema verifikasi | leave-one-well-out pada 7 sumur (`F-14`, `F-15A`, `F-15_S`, `F-5`, `F-7`, `F-9`, `F-9_A`) |
| Anggaran pencarian otomatis | `max_models` 100, `max_runtime_secs` 600 per sumur, `sort_metric` AUCPR, `balance_classes` benar, `seed` 42 |
| Lapisan internal | CV 6 fold dengan `fold_column` yaitu sumur |
| Sumber daya | 18 inti CPU, heap JVM 2 GB |
| Lantai pembanding | prevalensi mayoritas per sumur, 0,029 sampai 0,080 |

## 3.5.3 Hasil: satu model pilihan otomatis kalah, gabungan kandidat menang

Rata-rata AUPRC di 7 sumur, dengan pemilihan kandidat hanya memakai AUCPR CV internal (sumur uji tidak dilihat saat memilih):

| Pasangan | Rata-rata AUPRC |
|---|---|
| Gabungan median seluruh kandidat AutoML | **0,1525** |
| Gabungan median top-10 kandidat | 0,1524 |
| Gabungan peringkat rata-rata top-5 | 0,1519 |
| Rata-rata seluruh kandidat | 0,1470 |
| Baseline Random Forest antar hiperparameter | 0,1392 |
| Leader tunggal AutoML (pilihan CV internal) | 0,1325 |
| Baseline regresi logistik | 0,1061 |
| Lantai mayoritas | 0,0579 |

Tiga pernyataan yang dapat diklaim dari tabel itu:

1. **Leader tunggal AutoML kalah dari Random Forest** (0,1325 lawan 0,1392). Ini menutup klaim bahwa pencarian otomatis otomatis lebih baik.
2. **Gabungan median seluruh kandidat AutoML mengalahkan Random Forest** dengan selisih +0,0133 AUPRC atau 9,6 persen relatif, dan menang pada 5 dari 7 sumur.
3. **Kenaikan terbesar ada pada sumur berprevalensi terendah.** F-15A memiliki 24 positif dari 476 baris; AUPRC naik dari 0,0948 menjadi 0,1748, yaitu 84 persen relatif.

Sifat kesalahannya juga berbeda, dan ini bagian yang paling berguna secara operasional. Pada sumur terburuknya, leader tunggal jatuh serendah 0,0360 di bawah Random Forest, sedangkan gabungan median hanya 0,0029 di bawah. Artinya manfaat utama gabungan bukan menaikkan angka tertinggi, melainkan **menghapus risiko salah pilih satu model** di antara kandidat yang selisihnya sangat kecil.

Batas atas bila seleksi boleh memakai informasi sumur uji (dilabeli oracle, bukan hasil yang boleh diklaim): pemilihan greedy 0,1681 dan kandidat tunggal terbaik per sumur 0,1605. Sisa ruang perbaikan di atas gabungan median adalah 0,0156, dan ruang itu tidak dapat diambil tanpa melihat sumur uji.

## 3.5.4 Mengapa satu model pilihan otomatis kalah: pemilihannya tidak terbukti andal

Tiga pengukuran pada leaderboard internal, dihitung dari skor tersimpan per kandidat:

| Besaran | Nilai | Makna |
|---|---|---|
| Selisih antar kandidat pada leaderboard internal (rerata sebaran nilai 5 teratas) | 0,0053 | Kandidat teratas hampir tidak terbedakan oleh CV internal |
| Jarak AUPRC CV leader ke AUPRC sumur uji | 0,0789 rata-rata | Resolusi yang diminta untuk pemilihan 15 kali lebih besar daripada yang ditawarkan CV internal |
| Korelasi Spearman lintas sumur antara AUPRC CV internal leader dan AUPRC uji leader | -0,3929 (7 titik, p 0,383) | Skor CV leader tidak menunjuk sumur yang akan berkinerja baik |

Tiga pembacaan yang perlu dibedakan:

1. **Pemenang leaderboard ditentukan di dalam noise.** Selisih antar kandidat (0,0053) jauh di bawah jarak CV ke hasil uji (0,0789), sehingga "leader" tidak terbukti berbeda secara terukur dari kandidat lainnya, dan menambah jumlah model, inti CPU, atau durasi tidak memperbaiki pemilihan. Pada pengujian F-14, menaikkan anggaran dari 400 menjadi 600 detik justru menurunkan AUPRC sumur uji dari 0,1045 menjadi 0,0848.
2. **Lintas sumur, skor CV leader tidak prediktif.** Korelasinya negatif (-0,3929), sehingga membandingkan kualitas model antar sumur menggunakan leaderboard internal tidak sah.
3. **Di dalam satu sumur, korelasinya lemah dan tidak konsisten**: rerata korelasi peringkat internal terhadap hasil uji adalah +0,28, positif pada 4 dari 7 sumur dan negatif pada sisanya. Jadi pemilihan satu kandidat di dalam satu sumur tidak terbukti bocor secara menyeluruh, tetapi juga tidak terbukti andal; yang benar-benar bocor adalah komparabilitasnya lintas sumur.

Karena itu klaim "AutoML lebih baik" dilarang ditulis tanpa skema seleksi yang netral terhadap prevalensi.

## 3.5.5 Hasil tambahan: DeepLearning gagal karena cacat data, bukan karena engine

Seluruh kandidat DeepLearning gagal dilatih pada 7 sumur. Uji sebab-akibat dijalankan tiga tahap pada klaster terpisah:

| Tahap | Perlakuan | Hasil |
|---|---|---|
| A | data apa adanya | GAGAL, model tidak stabil secara numerik |
| B | potong di persentile 99,9 per kolom | GAGAL, batas persentile masih 2,26e+27 dan 107 kolom memuat nilai ekstrem |
| C | potong di persentile 99 per kolom | BERHASIL, model konvergen dengan `pr_auc` 0,08 pada CV internal |

Akar masalahnya ada pada data: **30 sel memuat nilai absolut di atas 10^20, yaitu 25 sel pada berkas fitur kontrol dan 5 sel pada berkas fitur kejadian, semuanya kolom SPPA (w2h dan w6h berikut turunannya), dengan nilai maksimum 9,524e+30** (baris 1756 sampai 1759 pada berkas kontrol). Itu 35 orde di atas rentang fitur lain (seluruh fitur lain berada dalam rentang 0 sampai 1). Contoh: `std` 2,89e+29 dan `mean` 1,07e+28. Selain itu ada 188.872 sel kosong (9,9 persen) pada 438 dari 480 kolom, terbanyak pada `burstiness` dan `trend_rho` yang kosong 67 sampai 81 persen.

Model berbasis pohon (GBM, XGBoost, DRF, XRT) tidak terpengaruh karena pemisahannya berbasis peringkat nilai. Jaringan saraf menstandardisasi setiap kolom lalu mengalikan bobot, sehingga satu nilai 10^30 menghancurkan gradien. Setelah perbaikan, DeepLearning dapat dilatih, tetapi `pr_auc` 0,08 masih di bawah Random Forest 0,1008 pada sumur yang sama. Jadi perbaikan data membuat keluarga itu **dapat dipakai**, bukan **lebih baik**.

## 3.5.6 Implikasi untuk pemilihan algoritme pada Bab III dan Bab IV

1. **Random Forest antar hiperparameter tetap menjadi detektor utama** di setiap mode, dengan status teruji dan bukan preferensi.
2. **Bila pencarian otomatis dipakai, kandidatnya harus digabung, bukan diambil pemenangnya.** Strategi yang terukur terbaik adalah median seluruh kandidat (atau median top-10, yang selisihnya hanya 0,0001 AUPRC).
3. **Syarat mutu data masuk ke rancangan**: kanal SPPA dan turunannya harus dipotong pada persentile 99 per kolom, atau dibuang bila tidak diperlukan, sebelum keluarga model linear dan jaringan saraf dipakai.
4. **Batas klaim angka**: 0,1525 lawan 0,1392 hanya berlaku pada 7 sumur data mitra dengan 9 sampai 12 kandidat per sumur, bukan pada 100 model, karena AutoML hanya sempat membangun sebanyak itu dalam 600 detik.

## 3.5.7 Batas yang harus dinyatakan

1. **Belum diuji**: penggabungan berbobot hasil pembelajaran (stacking). AutoML ber-`fold_column` tidak membentuk StackedEnsemble, dan prediksi out-of-fold per fold belum tersimpan.
2. **Belum diuji**: anggaran lebih besar, misalnya 1.800 detik per sumur, untuk mendapatkan puluhan kandidat. Seluruh angka gabungan di subbab ini berasal dari 9 sampai 12 kandidat.
3. **Cakupan**: hanya 7 sumur data mitra. Hasil ini tidak boleh diperluas menjadi klaim tentang sumur lain atau tentang data di luar lingkup 1.4.
4. **Aturan pelaporan**: memilih strategi gabungan berdasarkan hasil sumur uji lalu merata-ratakannya adalah kebocoran. Yang sah dilaporkan adalah rata-rata satu strategi tetap di seluruh sumur, seperti pada tabel 3.5.3.

## 3.5.8 Rujukan jejak

| Berkas | Isi |
|---|---|
| `docs/PPT1_ABLAT_AUTOML.md` | Naskah teknis lengkap: tabel per sumur, temuan T1 sampai T4, perintah reproduksi |
| `docs/evidence/h2o_kontrol.json` | Hasil AutoML 7 sumur termasuk leaderboard internal dan setelan |
| `docs/evidence/baseline_only.json` | Baseline Random Forest, regresi logistik, dan mayoritas per sumur |
| `docs/evidence/dl_klipp99.json` | Hasil uji tahap C setelah pemotongan persentile 99 |
| `docs/evidence/pred/ensemble_hasil.json` | Hasil seluruh strategi kombinasi pada jalur adil dan jalur oracle |
| `docs/evidence/pred/<sumur>.npz` | Skor mentah setiap kandidat AutoML per sumur |
| `docs/PPT1_LEDGER_ANGKA.md` | Baris E01 sampai E08 (pencarian otomatis dan DeepLearning), F01 sampai F06 (kombinasi kandidat) |

Reproduksi:

```bash
export JAVA_HOME=$HOME/.local/jdk17
java -Xmx3G -jar ~/.venvs/h2o/lib/python3.12/site-packages/h2o/backend/bin/h2o.jar \
  -ip 127.0.0.1 -port 54322 -name h2o_ens -nthreads 18 &
~/.venvs/h2o/bin/python scratch/h2o_eksperimen.py F-14 F-15A F-15_S F-5 F-7 F-9 F-9_A
~/.venvs/h2o/bin/python scratch/h2o_pred_semua.py
~/.venvs/h2o/bin/python scratch/h2o_ensemble_analisis.py
```
