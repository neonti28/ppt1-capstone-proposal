# DSS-4 PROTOKOL SWARM: SUARA BERBOBOT TUJUH ENGINE DAN EMPAT TINGKAT KEPUTUSAN

Kartu: `t_65702049` (DSS-4). Disusun 2026-10-31. Keluaran: berkas ini saja.
Posisi dalam rangkaian: [DSS1] menghitung keyakinan per klaim, [DSS3] memetakan ketidaksepakatan, [DSS2] menyusun antrean dan anggaran waktu. Berkas ini mengubah suara tujuh engine menjadi satu tingkat keputusan, dengan manusia sebagai pemutus. Tidak ada satu pun tingkat yang memicu tindakan otomatis.

## 0. Ringkasan

1. Tujuh engine, dua puluh tujuh kepala, sebelas klaim. Hitungan ini dibaca langsung dari [JSON] dan keluarannya ditempel di bagian 2.2.
2. Setiap kepala bersuara salah satu dari tiga: dukung, tolak, atau abstain. Abstain punya lima kode, dan kode itu dicetak, bukan diganti angka nol ([DSS1] bagian 4.2 ditambah kode AB-5 baru untuk kepala yang tidak pernah menyala).
3. Bobot suara memakai rumus yang sudah mengikat di [DSS1] bagian 3.2, yaitu `w_h = w_tier x w_layer x m_utama`. Ada satu temuan silang: empat baris tabel di [DSS1] menulis bobot 0,80 untuk kepala `persistence`, padahal rumus yang sama menghasilkan 0,40 karena tier `TREN`. Kedua versi dihitung di bagian 4.2 dan bagian 7.3, dan tingkat keputusannya tidak berubah pada keduanya.
4. Satu fungsi hanya boleh bersuara satu kali. Empat pasangan kepala terbukti identik metriknya di [JSON] (pola A [DSS3] bagian 5.1), jadi bobotnya dideduplikasi sebelum dijumlahkan (bagian 4.3).
5. Kepala yang tidak pernah menyala bukan suara penolakan, melainkan bisu. Di segmen ini ada empat kepala bisu, dan ssi menjadi contoh yang paling penting karena tiga dari empat kepalanya bisu (bagian 4.4).
6. Empat tingkat keputusan: TK-1 TENANG, TK-2 PANTAU, TK-3 TINJAU, TK-4 ESKALASI. Ambang dukungannya memakai batas pita yang sudah ada di [DSS1], yaitu 0,40 dan 0,60, bukan angka baru (bagian 5.1).
7. Siklus nyata pada segmen F-14 berakhir di TK-2 PANTAU dengan dukungan berbobot 18,23 persen setelah batas dominasi, satu klaim di pita P2, nol klaim di pita P3 ke atas, enam engine hadir, dan cakupan bobot 100 persen (bagian 7.1). TK-3 tidak tercapai karena syarat dua klaim P3 ke atas belum terpenuhi pada segmen ini, dan angka yang harus berubah disebutkan tepat (bagian 7.4).
8. Sembilan aturan konflik dan lima pemicu turunnya manusia ditulis di bagian 6, masing-masing dengan contoh nyata dari [JSON].
9. Lima fitur: SWARM-01 panel suara, SWARM-02 tangga tingkat, SWARM-03 meter kuorum, SWARM-04 diagram alur protokol, SWARM-05 buku konflik. Semuanya memperluas atau merujuk fitur katalog yang sudah ada ([KAT]), kecuali satu yang memang belum punya rumah di katalog.
10. Keputusan pemilik produk yang masih terbuka di [VR] bagian 8 soal jenis keluaran konsensus dijawab di sini: konsensus dihitung dari putusan kepala dan klaim mesin, bukan dari jajak pendapat manusia. Alasannya ada di bagian 9.5, dan konsekuensi datanya disebut di bagian 12.

## 1. Kepatuhan kerangka wajib

| Butir kerangka | Cara dipenuhi di berkas ini |
|---|---|
| 1. Alarm otomatis bukan tujuan | Empat tingkat keputusan semuanya berakhir pada manusia. Tidak ada tingkat yang mengirim notifikasi sendiri. Slot alarm otomatis di [JSON] baris 1414 bernilai 0 dan asersinya di [PIPE] baris 738. |
| 2. Setiap angka punya sumber | Angka proyek memakai berkas dan baris, misalnya [JSON] baris 1414. Angka turunan memakai perintah yang keluarannya ditempel di bagian 2 dan bagian 7. Angka literatur memakai kode LV1 sampai LV16 dari [VR] bagian 9. |
| 3. Tidak mengklaim tanpa bukti | Semua perintah hitung yang dipakai untuk mengisi tabel ditempel keluarannya apa adanya di bagian 2.2, 2.3, 7.1, dan 14. |
| 4. Kekurangan data jadi fitur | Kepala bisu menjadi kode abstain AB-5 yang tampil sebagai label (pola Dynamic Island), bukan dikurangi dari penyebut tanpa jejak. Klaim tanpa bobot menjadi AB-1. |
| 5. Pengguna, momen, masukan, keluaran, status bukti | Lima field itu ada di setiap fitur bagian 8, ditambah delapan field wajib lain dari kartu. |
| 6. Tidak menutup dengan kalimat menyerah | Ditutup oleh tabel syarat di bagian 12, yang menyebut apa yang harus tersedia agar tingkat di atas TK-2 bisa dicapai. |
| 7. Hanya .md di planning/ | Satu berkas keluaran, yaitu berkas ini. Tidak ada .py, .html, .json, .csv yang dibuat sebagai deliverable. |
| 8. Tanpa tanda pisah panjang | Diperiksa dengan `grep -cP` di bagian 14, hasilnya 0 untuk tanda pisah panjang dan 0 untuk tanda pisah pendek. Kutipan dari [JSON] yang memuat tanda pisah panjang ditulis ulang dengan koma, dan hal itu dicatat di bagian 13. |

## 2. Berkas masukan dan bukti pembacaan

### 2.1 Berkas yang dibuka, dengan ukuran byte dan jumlah baris

| Kode | Jalur | Byte | Baris | Yang diambil |
|---|---|---:|---:|---|
| [JSON] | `scratch/v9_i1/v9_i1_RESULTS.json` | 57.555 | 1.758 | Tujuh engine, 27 kepala, tier, lapisan, metrik segmen, `contoh_idx_aktif`, lapisan keputusan |
| [PIPE] | `code/v9_i1_pipeline.py` | 44.359 | 861 | REGISTRY tier, LAYERS, `AUTO_CRITICAL_SLOTS`, asersi `decision_layer` |
| [KAT] | `planning/01_KATALOG_FITUR.md` | 166.662 | 2.780 | Kode fitur induk: KEP-01, KEP-03, KEP-06, KEP-08, LIN-01 |
| [VR] | `planning/02_RISET_VISUALISASI.md` | 32.141 | 335 | Pemetaan jenis keluaran ke visual, LV1 sampai LV16, keputusan terbuka soal konsensus |
| [PM1] | `docs/V9_PM1_ARCHITECTURE.md` | 50.456 | 528 | Keputusan D-A1 sampai D-A7, gate kenaikan tier, diagram lima lapis |
| [DSS1] | `planning/03_SKOR_KEYAKINAN.md` | 66.698 | 1.060 | Rumus bobot `w_h`, lima pita, kode abstain AB-1 sampai AB-4 |
| [DSS2] | `planning/04_ANTREAN_TINJAUAN.md` | 95.168 | 1.428 | Beban tinjauan per shift, anggaran 30 menit, aturan deduplikasi baris |
| [DSS3] | `planning/05_KETIDAKSEPAKATAN.md` | 87.228 | 1.247 | Pola A sampai pola C, daftar kepala kembar dan bisu, dasar matriks kesepakatan |

Ukuran di atas dibaca dengan `stat -c '%s %n'` dan `wc -l` pada sesi ini, dan keluarannya ditempel di bagian 14 supaya bisa diperiksa ulang.

### 2.2 Perintah dan keluaran untuk struktur [JSON]

Perintah pertama, untuk memastikan berkasnya benar dan jumlah engine sesuai judul kartu:

```
$ jq -r 'to_entries[] | "\(.key) :: \(.value|type) :: \(if (.value|type)=="array" then (.value|length) elif (.value|type)=="object" then (.value|keys|join(",")) else (.value|tostring) end)"' scratch/v9_i1/v9_i1_RESULTS.json
meta :: object :: elapsed_s,generated_at,ml,n_engine,seed,segmen_rig,segmen_tool_wear,segmen_usrop,sumber_tier,task
segmen_info :: object :: hyd_ki,shk,ssi,stuck_k1,stuck_k2,vib
engines :: array :: 7
decision_layer :: object :: auto_critical_alarm_slots,keputusan_akhir,layers,nperingatan_l1,ringkasan
profil_kapabilitas :: array :: 7
nilai_maintenance :: object :: batas,beban_tinjauan_L1,jam_henti_per_sebab,jam_per_kode,n_record_aktivitas,sumber,total_jam_tercatat
human_review_required :: boolean :: true
keputusan_akhir :: string :: MANUSIA, alat ini menyiapkan status, peringatan, tren, dan bahan rencana inspeksi
```

Baris terakhir pada keluaran di atas adalah kutipan [JSON] baris 1758 dengan tanda pisah panjang diganti koma. Teks aslinya memakai tanda pisah panjang, dan penggantian itu dicatat di bagian 13.

Perintah kedua, menghitung jumlah engine, kepala, dan sebaran lapisan:

```
$ jq -r '.engines[] | "\(.engine) \(.heads|length)"' scratch/v9_i1/v9_i1_RESULTS.json | awk '{print; h+=$2; e++} END{print "engines="e" heads="h}'
vib 4
ssi 4
shk 4
stuck 6
hyd 4
bit_wear 2
tool_wear 3
engines=7 heads=27

$ jq '.decision_layer.ringkasan' scratch/v9_i1/v9_i1_RESULTS.json
{
  "L0": 5,
  "L1": 11,
  "L2": 9,
  "L3": 2
}
```

Lima ditambah sebelas ditambah sembilan ditambah dua sama dengan dua puluh tujuh, cocok dengan jumlah kepala. Perintah ketiga memeriksa konvensi `n_aktif = tp + fp` untuk dua puluh empat kepala bermetrik:

```
$ jq -r '.engines[] | .engine as $e | .heads[] | select(.metrik_segmen != null) | [$e, .head, (.n_aktif|tostring), ((.metrik_segmen.tp + .metrik_segmen.fp)|tostring), (if .n_aktif == (.metrik_segmen.tp + .metrik_segmen.fp) then "OK" else "MISMATCH" end)] | @tsv' scratch/v9_i1/v9_i1_RESULTS.json | awk -F'\t' '{...}' 
OK=24 MISMATCH=0
```

Baris per kepala tidak ditempel ulang di sini karena isinya panjang dan sudah ditempel utuh di [DSS3] bagian 2.3. Yang penting untuk berkas ini hanya hasil akhirnya: dua puluh empat kepala konsisten, nol ketidakcocokan.

### 2.3 Perintah hitung bobot, pita, dan dukungan

Perintah di bawah membaca [JSON], mengubahnya menjadi sepuluh kolom, lalu menghitung bobot per kepala dengan rumus [DSS1] bagian 3.2, mendeteksi kepala kembar dengan tanda tangan metrik, dan menjumlahkan dukungan per klaim. Programnya ditulis utuh di sini, bukan diringkas dengan titik-titik, supaya pembaca bisa menjalankannya ulang dan membandingkan hasilnya sendiri:

```bash
# jq menyiapkan sepuluh kolom: engine, head, tier, layer, klaim, n_windows,
# n_aktif, frac_aktif, tp, fp
jq -r '.engines[] | .engine as $e | .heads[]
       | [$e, .head, (.tier // "NULL"), (.layer // "NULL"), (.klaim // "-"),
          ((.n_windows // 0) | tostring),
          (if .n_aktif == null then "NULL" else (.n_aktif | tostring) end),
          ((.frac_aktif // 0) | tostring),
          ((.metrik_segmen.tp // 0) | tostring),
          ((.metrik_segmen.fp // 0) | tostring)]
       | @tsv' scratch/v9_i1/v9_i1_RESULTS.json \
| awk -F'\t' '
function wtier(t) { return (t == "PERINGATAN-BERPENGAWAS") ? 1.0 : ((t == "TREN") ? 0.5 : 0.0) }
function wlayer(l) { return (l == "L1") ? 1.0 : ((l == "L0") ? 0.8 : ((l == "L2") ? 0.5 : 0.0)) }
function wcap(e, k) {
  if (e == "vib")       return 0.4950
  if (e == "ssi")       return 0.5263
  if (e == "shk")       return 0.5188
  if (e == "stuck")     return 0.4562
  if (e == "hyd")       return (k == "K-i") ? 0.6100 : 0.5125
  if (e == "bit_wear")  return 0.2525
  if (e == "tool_wear") return 0.4550
  return 1.0000
}
function pita(x) { if (x >= 0.80) return "P5"; if (x >= 0.60) return "P4"
                   if (x >= 0.40) return "P3"; if (x >= 0.20) return "P2"; return "P1" }
{
  eng = $1; head = $2; tier = $3; lay = $4; kl = $5
  na = $7; fr = $8 + 0; tp = $9 + 0; fp = $10 + 0

  mult = (eng == "hyd" && head == "hybrid_rule_and_persistence") ? 1.5 : 1.0
  w    = wtier(tier) * wlayer(lay) * mult
  walt = (head == "persistence" && tier == "TREN") ? 0.80 : w

  sig = na "|" $8 "|" tp "|" fp
  dup = 0
  if (head == "hybrid_rule_and_persistence" && rsig[eng SUBSEP kl] == sig) dup = 1
  if (head == "rule_display") rsig[eng SUBSEP kl] = sig

  bisu = (na == "NULL" || na + 0 == 0) ? 1 : 0
  key  = eng "|" kl
  seen[key] = 1; keng[key] = eng; klab[key] = kl

  W[key]    += (dup == 0 && bisu == 0) ? w    : 0
  WALT[key] += (dup == 0 && bisu == 0) ? walt : 0
  KN[key]   += w * fr;    KD[key]   += w
  KNA[key]  += walt * fr; KDA[key]  += walt

  printf "%-9s %-28s %-24s %-3s w=%.2f w_alt=%.2f frac=%.4f dup=%d bisu=%d\n", \
         eng, head, tier, lay, w, walt, fr, dup, bisu
}
END {
  print "----- ringkasan per klaim -----"
  n = 0
  for (k in seen) { if (KD[k] == 0) continue
    n++
    ks[k] = KN[k] / KD[k]
    ka[k] = (KDA[k] == 0) ? ks[k] : KNA[k] / KDA[k]
    cp = wcap(keng[k], klab[k])
    kt[k] = (ks[k] < cp) ? ks[k] : cp
    pt[k] = pita(kt[k])
    vt[k] = (pt[k] == "P1") ? "TOLAK" : ((pt[k] == "P2") ? "DUKUNG-lemah" : "DUKUNG")
    ord[n] = k
  }
  for (i = 1; i <= n; i++) for (j = i + 1; j <= n; j++)
    if (kt[ord[j]] > kt[ord[i]] || (kt[ord[j]] == kt[ord[i]] && ord[j] < ord[i])) {
      t = ord[i]; ord[i] = ord[j]; ord[j] = t }
  for (i = 1; i <= n; i++) {
    k = ord[i]
    printf "%-14s K_seg=%.4f cap=%.4f K_tampil=%.4f %s W=%.2f W_alt=%.2f vote=%s\n", \
           k, ks[k], wcap(keng[k], klab[k]), kt[k], pt[k], W[k], WALT[k], vt[k]
    if (keng[k] != "tool_wear") {
      RIG += W[k]; RIGA += WALT[k]
      if (vt[k] ~ /^DUKUNG/) { RIGD += W[k]; RIGDA += WALT[k] }
    } else {
      BEN += W[k]; BENA += WALT[k]
      if (vt[k] ~ /^DUKUNG/) { BEND += W[k]; BENDA += WALT[k] }
    }
  }
  print "----- dewan rig (tanpa tool_wear) -----"
  printf "bobot tersedia=%.2f bobot dukung=%.2f S=%.4f (%.2f%%)\n", RIG, RIGD, RIGD / RIG, 100 * RIGD / RIG
  printf "DEWAN_BENGKEL_A S=%.4f (%.2f%%) dari %.2f\n",      BEND / BEN,  100 * BEND / BEN,  BEN
  printf "DEWAN_BENGKEL_B S=%.4f (%.2f%%) dari %.2f\n",      BENDA / BENA, 100 * BENDA / BENA, BENA
  printf "DEWAN_RIG_A S=%.4f (%.2f%%) dari %.2f\n",          RIGD / RIG,  100 * RIGD / RIG,  RIG
  printf "DEWAN_RIG_B S=%.4f (%.2f%%) dari %.2f\n",          RIGDA / RIGA, 100 * RIGDA / RIGA, RIGA
}'
```

Keluaran nyata dari jalankan ulang pada sesi ini, ditempel apa adanya. Baris ringkasan klaim diurutkan menurut `K_tampil` menurun supaya dua jalankan bisa dibandingkan; urutan itu satu-satunya beda dari jalankan pertama yang memakai urutan hash bawaan `awk`, sedangkan seluruh nilainya identik.

```
vib       rule_display                 PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.2715 dup=0 bisu=0
vib       persistence                  TREN                     L0  w=0.40 w_alt=0.80 frac=0.5742 dup=0 bisu=0
vib       hybrid_rule_and_persistence  PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.2715 dup=1 bisu=0
vib       rf_lowo                      TREN                     L2  w=0.25 w_alt=0.25 frac=0.6390 dup=0 bisu=0
ssi       rule_display                 PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0000 dup=0 bisu=1
ssi       persistence                  TREN                     L0  w=0.40 w_alt=0.80 frac=0.0057 dup=0 bisu=0
ssi       hybrid_rule_and_persistence  PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0000 dup=1 bisu=1
ssi       rf_lowo                      TREN                     L2  w=0.25 w_alt=0.25 frac=0.0000 dup=0 bisu=1
shk       rule_display                 PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0092 dup=0 bisu=0
shk       persistence                  TREN                     L0  w=0.40 w_alt=0.80 frac=0.0556 dup=0 bisu=0
shk       hybrid_rule_and_persistence  PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0092 dup=1 bisu=0
shk       rf_lowo                      TREN                     L2  w=0.25 w_alt=0.25 frac=0.0000 dup=0 bisu=1
stuck     rule_display                 PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0656 dup=0 bisu=0
stuck     persistence                  TREN                     L0  w=0.40 w_alt=0.80 frac=0.1409 dup=0 bisu=0
stuck     hybrid_rule_and_persistence  PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0656 dup=1 bisu=0
stuck     e1_2of3                      TREN                     L2  w=0.25 w_alt=0.25 frac=0.0033 dup=0 bisu=0
stuck     persistence_event            TREN                     L2  w=0.25 w_alt=0.25 frac=0.0000 dup=0 bisu=0
stuck     rf_lowo                      TREN                     L2  w=0.25 w_alt=0.25 frac=0.0004 dup=0 bisu=0
hyd       rule_display                 PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0937 dup=0 bisu=0
hyd       persistence                  PERINGATAN-BERPENGAWAS   L0  w=0.80 w_alt=0.80 frac=0.0842 dup=0 bisu=0
hyd       hybrid_rule_and_persistence  PERINGATAN-BERPENGAWAS   L1  w=1.50 w_alt=1.50 frac=0.0602 dup=0 bisu=0
hyd       k2_tidak_tersedia            BELUM LAYAK PAKAI        L3  w=0.00 w_alt=0.00 frac=0.0000 dup=0 bisu=1
bit_wear  persistence                  TREN                     L2  w=0.25 w_alt=0.80 frac=0.1032 dup=0 bisu=0
bit_wear  k2_onset_belum              BELUM LAYAK PAKAI        L3  w=0.00 w_alt=0.00 frac=0.0000 dup=0 bisu=1
tool_wear calib_5of27                  TREN                     L2  w=0.25 w_alt=0.25 frac=0.6503 dup=0 bisu=0
tool_wear op_far_calibrated            PERINGATAN-BERPENGAWAS   L1  w=1.00 w_alt=1.00 frac=0.0448 dup=0 bisu=0
tool_wear canary_3rms                  TREN                     L2  w=0.25 w_alt=0.25 frac=0.6013 dup=0 bisu=0
----- ringkasan per klaim -----
tool_wear|K-ii K_seg=0.6013 cap=0.4550 K_tampil=0.4550 P3 W=0.25 W_alt=0.25 vote=DUKUNG
vib|-          K_seg=0.3519 cap=0.4950 K_tampil=0.3519 P2 W=1.65 W_alt=2.05 vote=DUKUNG-lemah
tool_wear|K-i  K_seg=0.1659 cap=0.4550 K_tampil=0.1659 P1 W=1.25 W_alt=1.25 vote=TOLAK
bit_wear|K-1   K_seg=0.1032 cap=0.2525 K_tampil=0.1032 P1 W=0.25 W_alt=0.80 vote=TOLAK
stuck|K-i      K_seg=0.0782 cap=0.4562 K_tampil=0.0782 P1 W=1.40 W_alt=1.80 vote=TOLAK
hyd|K-i        K_seg=0.0762 cap=0.6100 K_tampil=0.0762 P1 W=3.30 W_alt=3.30 vote=TOLAK
shk|-          K_seg=0.0153 cap=0.5188 K_tampil=0.0153 P1 W=1.40 W_alt=1.80 vote=TOLAK
stuck|K-ii     K_seg=0.0012 cap=0.4562 K_tampil=0.0012 P1 W=0.75 W_alt=0.75 vote=TOLAK
ssi|-          K_seg=0.0009 cap=0.5263 K_tampil=0.0009 P1 W=0.40 W_alt=0.80 vote=TOLAK
----- dewan rig (tanpa tool_wear) -----
bobot tersedia=9.15 bobot dukung=1.65 S=0.1803 (18.03%)
DEWAN_BENGKEL_A S=0.1667 (16.67%) dari 1.50
DEWAN_BENGKEL_B S=0.1667 (16.67%) dari 1.50
DEWAN_RIG_A S=0.1803 (18.03%) dari 9.15
DEWAN_RIG_B S=0.1814 (18.14%) dari 11.30
```

Empat baris terakhir juga merupakan keluaran yang dipakai bagian 7.3, sehingga tabel sensitivitas di sana bisa diperiksa dari program yang sama tanpa perintah kedua.

Empat baris dengan `dup=1` adalah empat pasangan kepala kembar, dan pada keempatnya hibrida identik dengan `rule_display` pada engine yang sama: `vib`, `ssi`, `shk`, dan `stuck`. Enam baris dengan `bisu=1` terbagi dua. Empat di antaranya masih berbobot lebih dari nol, yaitu `ssi.rule_display` (1,00), `ssi.hybrid_rule_and_persistence` (1,00), `ssi.rf_lowo` (0,25), dan `shk.rf_lowo` (0,25); dua sisanya berbobot nol karena tier BELUM LAYAK PAKAI, yaitu `hyd.k2_tidak_tersedia` dan `bit_wear.k2_onset_belum`.

Satu koreksi tercatat di sini. Jalankan pertama menandai `ssi.rf_lowo` sebagai `dup=1`, dan itu keliru: deduplikasi hanya berlaku bagi kepala hibrida yang menyalin `rule_display`, sedangkan `rf_lowo` adalah kepala model terpisah. Pada jalankan ulang nilainya `dup=0`, dan angka `K_seg` tidak berubah karena kepala kembar tetap dihitung penuh pada perhitungan keyakinan (aturan di bagian 4.3 butir 1).

Dua klaim tidak muncul di daftar karena penyebutnya nol: `hyd|K-ii` dan `bit_wear|K-2`. Keduanya adalah abstain AB-1 dan dibahas di bagian 4.1.

### 2.4 Rentang waktu segmen, dan akibatnya pada satuan suara

| Segmen | Jendela | Indeks menit minimum | Indeks menit maksimum | Rentang menit |
|---|---:|---:|---:|---:|
| vib | 1.989 | 20.189.486 | 20.192.503 | 3.018 |
| ssi | 5.455 | 19.947.192 | 20.223.025 | 275.834 |
| shk | 11.205 | 19.906.551 | 20.224.235 | 317.685 |
| stuck K-i | 3.201 | 20.174.233 | 20.179.521 | 5.289 |
| stuck K-ii | 95.925 | 19.903.021 | 20.262.624 | 359.604 |
| hyd K-i | 10.401 | 19.906.551 | 20.224.229 | 317.679 |

Sumber tabel: [JSON] kunci `segmen_info`, dengan catatan di berkas yang sama bahwa indeks menit adalah indeks internal D1 dan asal kalender belum diverifikasi. Tiga akibat yang mengikat protokol ini:

1. Jendela setiap mesin adalah segmen berbeda dengan panjang berbeda. Indeks 429 pada `vib` bukan menit yang sama dengan indeks 429 pada `shk`. Karena itu suara antar mesin tidak boleh disandingkan pada tingkat indeks.
2. Segmen `vib` seluruhnya berada di dalam rentang `shk` dan `hyd` (20.189.486 sampai 20.192.503 berada di dalam 19.906.551 sampai 20.224.235), sedangkan `stuck` K-i hanya menempati 5.289 menit. Cakupan waktu yang tidak sama membuat suara antar mesin hanya sah pada satuan periode, bukan pada satuan jendela.
3. Satuan periode yang dipakai adalah shift 8 jam, yaitu 480 jendela 60 detik. Satuan ini sama dengan satuan beban tinjauan di [DSS2] bagian 5, sehingga dukungan dan beban bisa dibaca pada satu sumbu waktu tanpa menukar satuan.

Konsekuensi jujur: siklus antar mesin pada tingkat jendela belum dapat dihitung dari [JSON], karena deret per menit tidak diekspor. Yang dapat dihitung hari ini ada dua: siklus antar mesin pada tingkat segmen (bagian 7.1) dan siklus di dalam satu mesin pada tingkat jendela (bagian 7.2). Syarat untuk menaikkan resolusi ke shift ada di bagian 12 butir S-1.

## 3. Inventaris: tujuh engine, sebelas klaim, dua puluh tujuh kepala

| # | Engine | Klaim | Kepala | Lapisan kepala | Jendela | Sumber |
|---:|---|---|---|---|---:|---|
| 1 | `vib` | deteksi kondisi getaran lateral | rule_display, persistence, hybrid_rule_and_persistence, rf_lowo | L1, L0, L1, L2 | 1.989 | [JSON] baris 62 dan seterusnya |
| 2 | `ssi` | deteksi kondisi stick-slip torsional | rule_display, persistence, hybrid_rule_and_persistence, rf_lowo | L1, L0, L1, L2 | 5.455 | [JSON] kunci `engines[1]` |
| 3 | `shk` | deteksi anomali bit bounce | rule_display, persistence, hybrid_rule_and_persistence, rf_lowo | L1, L0, L1, L2 | 11.205 | [JSON] kunci `engines[2]` |
| 4 | `stuck` | K-i deteksi kondisi, K-ii prediksi onset | rule_display, persistence, hybrid_rule_and_persistence (K-i); e1_2of3, persistence_event, rf_lowo (K-ii) | L1, L0, L1; L2, L2, L2 | 3.201 dan 95.925 | [JSON] kunci `engines[3]` |
| 5 | `hyd` | K-i deteksi kondisi, K-ii prediksi kick atau loss | rule_display, persistence, hybrid_rule_and_persistence (K-i); k2_tidak_tersedia (K-ii) | L1, L0, L1; L3 | 10.401 dan 0 | [JSON] kunci `engines[4]`, kepala utama di baris 811 |
| 6 | `bit_wear` | K-1 deteksi kondisi, K-2 prediksi onset | persistence (K-1); k2_onset_belum (K-2) | L2; L3 | 47.645 dan 0 | [JSON] kunci `engines[5]` |
| 7 | `tool_wear` | K-i perubahan regime, K-ii ranking lintas alat | calib_5of27, op_far_calibrated (K-i); canary_3rms (K-ii) | L2, L1; L2 | 469 | [JSON] kunci `engines[6]` |

Jumlah kepala: empat ditambah empat ditambah empat ditambah enam ditambah empat ditambah dua ditambah tiga sama dengan dua puluh tujuh. Jumlah klaim: satu ditambah satu ditambah satu ditambah dua ditambah dua ditambah dua ditambah dua sama dengan sebelas. Angka sebelas cocok dengan keputusan [EVA] baris 31 yang dikutip [DSS1] bagian 3.5, yaitu tujuh engine dinilai pada sebelas klaim.

Dua engine memakai domain berbeda dan tidak boleh dijumlahkan dalam satu dewan:

| Dewan | Anggota | Alasan pemisahan |
|---|---|---|
| Dewan rig | `vib`, `ssi`, `shk`, `stuck`, `hyd`, `bit_wear` (enam engine, sembilan klaim) | Jendela 60 detik, FAR per 24 jam negatif, lead dalam menit |
| Dewan bengkel | `tool_wear` (satu engine, dua klaim) | Jendela 1 detik, FAR per menit, lead dalam detik, domain bengkel ([PM1] baris 132 keputusan D-A7) |

Pemisahan ini bukan kerapian administratif. [DSS1] bagian 3.5 butir 3 menolak penjumlahan lintas domain karena satuannya berbeda, dan [DSS2] bagian 2.3 tabrakan kedua menunjukkan akibatnya: satu angka FAR 2,096 bisa berarti 1 tinjauan atau 1.006 tinjauan tergantung satuan yang dibaca.

## 4. Suara: tiga jenis, lima kode abstain, satu bobot per kepala

### 4.1 Tiga jenis suara

| Suara | Kode | Syarat terpicu | Yang tercetak |
|---|---|---|---|
| Dukung | V-1 | Klaim punya `K_tampil` pada pita P2 ke atas (0,20 ke atas) | Pita, persen, jumlah kepala yang menyala, badge FAR |
| Tolak | V-2 | Klaim punya `K_tampil` di bawah 0,20 dan ada kepala yang dinilai | Pita P1, jumlah kepala yang dinilai, alasan penolakan terpendek |
| Abstain | V-3 | Salah satu kode AB di bawah | Kode, alasan, daftar kepala yang menunggu |

Abstain memakai empat kode yang sudah ditetapkan [DSS1] bagian 4.2 dan satu kode baru:

| Kode | Nama | Syarat | Contoh nyata di [JSON] |
|---|---|---|---|
| AB-1 | Tanpa kepala berskor | Jumlah bobot klaim sama dengan 0 | `hyd.hybrid` K-ii `k2_tidak_tersedia` (tier BELUM LAYAK PAKAI), `bit_wear.k2_onset_belum` |
| AB-2 | Data sensor kurang | `n_nodata` lebih dari 50 persen jendela | Tidak terpakai di segmen ini |
| AB-3 | Skor per jendela tidak tersedia | Hanya ringkasan min, median, maks | `vib.rf_lowo` dan `tool_wear.canary_3rms` untuk pemakaian per jendela |
| AB-4 | Klaim di lapis L3 | Tier BELUM LAYAK PAKAI atau lapisan L3 | Dua kepala di atas, sama dengan AB-1 pada kasus ini |
| AB-5 | Kepala bisu | `n_aktif` sama dengan 0 padahal klaim punya kepala lain yang menyala | `ssi.rule_display`, `ssi.hybrid_rule_and_persistence`, `ssi.rf_lowo`, `shk.rf_lowo` |

AB-5 adalah tambahan berkas ini, dan alasannya bukan kerapian. Tanpa AB-5, tiga kepala ssi yang tidak pernah menyala akan terbaca sebagai tiga penolakan berbobot 2,25, padahal artinya adalah kanal CRPM tidak tersedia pada 96,57 persen jendela ([DSS1] bagian 4.2 contoh AB-2). Angka 96,57 berasal dari [JSON] `ssi.rule_display.n_nodata` 5.268 dibagi 5.455 jendela.

### 4.2 Bobot: rumus yang mengikat, dan satu temuan silang

Rumus diambil apa adanya dari [DSS1] bagian 3.2:

```
w_h = w_tier x w_layer x m_utama

w_tier : PERINGATAN-BERPENGAWAS 1,00 | TREN 0,50 | BELUM LAYAK PAKAI 0,00
w_layer: L1 1,00 | L0 0,80 | L2 0,50 | L3 0,00
m_utama: 1,50 untuk kepala utama klaim, selain itu 1,00
```

Kepala utama hari ini satu: `hyd.hybrid_rule_and_persistence`, ditandai `"head_utama": true` di [JSON] baris 811.

Temuan silang. [DSS1] bagian 3.2 menulis bobot 0,80 untuk kepala `persistence` pada `vib`, `ssi`, `shk`, dan `stuck` K-i. Bila rumus di atas diterapkan pada kepala itu, hasilnya 0,40, karena tier `persistence` adalah `TREN` (0,50) dan lapisannya L0 (0,80). Kedua angka tidak dapat benar bersamaan. Periksaannya:

| Engine | Tier kepala `persistence` di [JSON] | Lapisan | Hitung dengan rumus | Angka tertulis di [DSS1] | Selisih |
|---|---|---|---:|---:|---|
| vib | TREN | L0 | 0,50 x 0,80 = 0,40 | 0,80 | 0,40 |
| ssi | TREN | L0 | 0,50 x 0,80 = 0,40 | 0,80 | 0,40 |
| shk | TREN | L0 | 0,50 x 0,80 = 0,40 | 0,80 | 0,40 |
| stuck K-i | TREN | L0 | 0,50 x 0,80 = 0,40 | 0,80 | 0,40 |
| hyd K-i | PERINGATAN-BERPENGAWAS | L0 | 1,00 x 0,80 = 0,80 | 0,80 | 0,00 |

Baris `hyd` K-i cocok, jadi kekeliruan hanya pada empat baris yang kepala `persistence`-nya bertier TREN. Dua kemungkinan penyebab: kolom bobot disalin dari baris hyd, atau penulis [DSS1] bermaksud memberi pengecualian bagi kepala status. [DSS1] tidak menulis pengecualian itu, sehingga yang mengikat adalah rumusnya.

Keputusan berkas ini: memakai rumus, karena rumus yang tertulis di [DSS1] sendiri dan karena tier serta lapisan berasal dari [PIPE] REGISTRY yang dijaga asersi. Versi 0,80 tetap dihitung sebagai pembanding di kolom `W_alt`, dan bagian 7.3 menunjukkan tingkat keputusan tidak berubah pada kedua versi. Dengan begitu, bila pemilik produk memutuskan sebaliknya, protokolnya tetap jalan tanpa dihitung ulang dari awal.

### 4.3 Satu fungsi, satu suara

[DSS3] bagian 5.1 membuktikan bahwa kepala `hybrid_rule_and_persistence` adalah fungsi yang sama dengan `rule_display` untuk tiga kelas, karena definisinya `rule(t0-1) AND persistence(t)` dan pada kelas definisi-kanal hasilnya identik. Bukti di [JSON]: empat pasangan punya `n_aktif`, `frac_aktif`, `tp`, dan `fp` yang sama persis.

| Engine | Pasangan kembar | n_aktif | frac_aktif | tp | fp | Bobot yang dibuang |
|---|---|---:|---:|---:|---:|---:|
| vib | rule dan hibrida | 540 | 0,2715 | 510 | 30 | 1,00 |
| ssi | rule dan hibrida | 0 | 0,0000 | 0 | 0 | 1,00 |
| shk | rule dan hibrida | 103 | 0,0092 | 55 | 48 | 1,00 |
| stuck K-i | rule dan hibrida | 210 | 0,0656 | 194 | 16 | 1,00 |

Tanpa deduplikasi, dukungan berbobot akan menghitung satu fungsi dua kali, dan empat engine akan tampak lebih yakin daripada buktinya. Ini persis kesalahan yang sudah dicatat [DSS2] bagian 2.3 tabrakan pertama pada konteks antrean, dan protokol ini memakai aturan yang sama.

Dua catatan penting soal deduplikasi:

1. Yang dideduplikasi adalah bobot suara, bukan perhitungan keyakinan. `K_tampil` tetap dihitung dengan semua kepala sesuai [DSS1] bagian 3.3, karena keyakinan per jendela memang gabungan semua kepala. Yang berubah hanya berapa kali satu fungsi boleh bersuara di dewan.
2. Kepala utama `hyd.hybrid` tidak dideduplikasi karena metriknya berbeda dari `hyd.rule_display` (626 lawan 975 jendela aktif), sehingga ia memang pembacaan kedua, bukan salinan.

### 4.4 Bisu bukan tolak

Kepala dengan `n_aktif` sama dengan 0 pada segmen ini:

| Engine | Kepala bisu | Bobot | Akibat pada klaim |
|---|---|---:|---|
| ssi | rule_display, hybrid_rule_and_persistence, rf_lowo | 2,25 | Klaim turun ke satu kepala, bobot 0,40, kode AB-5 sebagian |
| shk | rf_lowo | 0,25 | Klaim turun ke dua kepala, bobot 1,40 |

Untuk `ssi`, tiga kepala bisu berarti klaim hampir seluruhnya tidak dinilai. Protokolnya: klaim tetap muncul di panel dengan label "sebagian bisu 3 dari 4 kepala", bobotnya dihitung dari kepala yang bersuara, dan dukungannya tidak boleh dipakai untuk menaikkan tingkat di atas TK-2 (aturan H-3 di bagian 6.2). Membaca `ssi` sebagai "menolak dengan yakin" adalah salah tafsir yang paling mudah terjadi, dan bagian 10 mencatatnya sebagai butir pertama.

### 4.5 Bobot per klaim, dua versi

| Klaim | Kepala yang bersuara | Bobot A (rumus) | Bobot B (seperti tertulis [DSS1]) |
|---|---|---:|---:|
| vib | rule 1,00; persistence 0,40; rf 0,25 | 1,65 | 2,05 |
| ssi | persistence 0,40 | 0,40 | 0,80 |
| shk | rule 1,00; persistence 0,40 | 1,40 | 1,80 |
| stuck K-i | rule 1,00; persistence 0,40 | 1,40 | 1,80 |
| stuck K-ii | e1 0,25; persistence_event 0,25; rf 0,25 | 0,75 | 0,75 |
| hyd K-i | rule 1,00; persistence 0,80; hybrid 1,50 | 3,30 | 3,30 |
| hyd K-ii | tidak ada | 0,00 | 0,00 |
| bit_wear K-1 | persistence 0,25 | 0,25 | 0,80 |
| bit_wear K-2 | tidak ada | 0,00 | 0,00 |
| tool_wear K-i | calib 0,25; op_far 1,00 | 1,25 | 1,25 |
| tool_wear K-ii | canary 0,25 | 0,25 | 0,25 |
| **Dewan rig** | sembilan klaim | **9,15** | **11,30** |
| **Dewan bengkel** | dua klaim | **1,50** | **1,50** |

Angka 9,15 dan 11,30 dihitung ulang dari kolom di atas: 1,65 + 0,40 + 1,40 + 1,40 + 0,75 + 3,30 + 0,25 sama dengan 9,15; 2,05 + 0,80 + 1,80 + 1,80 + 0,75 + 3,30 + 0,80 sama dengan 11,30. Keduanya cocok dengan keluaran `bobot tersedia=9.15` pada bagian 2.3 dan dengan keluaran `DEWAN_RIG_B ... dari 11.30` pada bagian 7.3.

## 5. Kuorum, ambang, dan empat tingkat keputusan

### 5.1 Empat tingkat, ambang berupa angka

Tingkat keputusan diberi awalan TK supaya tidak tertukar dengan tiga sumbu lain yang sudah dipakai dokumen sebelumnya: lapisan pemakaian L0 sampai L3 dari [PIPE] baris 295 sampai 298, pita keyakinan P1 sampai P5 dari [DSS1] bagian 4.1, dan tier kepala dari [PIPE] REGISTRY.

| Tingkat | Nama | Syarat angka (semua wajib) | Yang terjadi |
|---|---|---|---|
| TK-1 | TENANG | Tidak ada klaim dengan `K_tampil` 0,20 ke atas | Tidak ada baris antrean baru. Jendela dicatat sebagai jendela tenang untuk hitungan beban |
| TK-2 | PANTAU | Ada minimal satu klaim pada pita P2 (0,20 sampai 0,39), atau dukungan berbobot S 0,20 ke atas, dan syarat TK-3 belum terpenuhi | Klaim itu masuk daftar pantau, bukan antrean kerja. Tidak ada notifikasi |
| TK-3 | TINJAU | Kuorum hadir 4 dari 7 engine, cakupan bobot 0,50 ke atas, minimal dua klaim pada pita P3 ke atas, S 0,40 ke atas, beban tinjauan pada shift itu 30 menit ke bawah | Satu baris antrean tinjauan per klaim P3 ke atas, wajib dikonfirmasi insinyur pengeboran dalam satu shift |
| TK-4 | ESKALASI | Semua syarat TK-3, ditambah minimal satu klaim pada pita P4 (0,60 ke atas), S 0,60 ke atas, FAR terukur klaim penentu 6 per 24 jam negatif ke bawah, lead terukur pada klaim itu, dan tidak ada konflik K-3 pada klaim penentu | Eskalasi ke supervisor pengeboran dan insinyur pengeboran, batas waktu satu jam, keputusan tetap manusia |

Tiga alasan ambangnya berbentuk angka itu, bukan selera:

1. Ambang 0,40 dan 0,60 adalah batas bawah pita P3 dan P4 di [DSS1] bagian 4.1. Dengan memakai batas yang sama, "dukungan dewan 40 persen" dan "satu klaim di pita P3" memakai bahasa yang sama, dan tidak ada angka baru yang lahir di berkas ini.
2. Syarat P4 pada TK-4 meneruskan aturan yang sudah ada: pita P4 berarti keyakinan kuat dan wajib konfirmasi operator ([DSS1] bagian 4.1 baris P4), dan [DSS2] bagian 5.2 menetapkan P4 tidak pernah ditunda.
3. Syarat FAR 6 per 24 jam meneruskan gate L1 di [PM1] baris 138 dan keputusan D-A6 di [PM1] baris 131. Angka 6 bukan ambang baru.

Peta tiga sumbu, supaya tidak dibaca bertumpuk:

| Sumbu | Skala | Arti | Siapa yang memutuskan |
|---|---|---|---|
| Tier kepala | PERINGATAN-BERPENGAWAS, TREN, BELUM LAYAK PAKAI | Mutu bukti satu kepala, dikunci [PIPE] REGISTRY | Pemilik arsitektur, lewat change control |
| Pita klaim | P1 sampai P5 | Keyakinan pada satu klaim, dari [DSS1] | Mesin, sebagai bahan |
| Tingkat dewan | TK-1 sampai TK-4 | Seberapa mendesak manusia melihat | Manusia, selalu |

### 5.2 Kuorum kehadiran dan cakupan bobot

Kuorum dihitung dua kali, karena satu angka kuorum selalu bisa dimanipulasi dengan mengubah siapa yang hadir.

```
Q_hadir   = jumlah engine yang punya minimal satu klaim bersuara (V-1 atau V-2)
Q_kuorum  = 4 dari 7 engine
C_bobot   = bobot klaim bersuara / bobot seluruh klaim dewan
C_minimum = 0,50
```

Empat dari tujuh dipilih karena itu mayoritas sederhana dari tujuh engine. Tiga dari tujuh akan membolehkan dua engine plus satu klaim kecil menentukan tingkat, dan itu terlalu longgar untuk alat yang seluruh klaimnya masih bertier PERINGATAN-BERPENGAWAS.

Pada segmen ini: engine bersuara enam dari tujuh (semua kecuali `tool_wear` yang masuk dewan bengkel), cakupan bobot 9,15 dibagi 9,15 sama dengan 1,00, sehingga kedua kuorum terpenuhi.

### 5.3 Batas atas bukti dan batas dominasi

Dua pengaman tambahan, keduanya berupa angka, dan keduanya pernah mengubah hasil di segmen ini.

Batas atas bukti. Tingkat dewan tidak boleh melampaui mutu bukti kelas tertinggi yang bersuara. Angka batasnya diambil dari [DSS1] bagian 3.4:

| Klaim | K_max | Pita tertinggi yang bisa dicapai |
|---|---:|---|
| vib | 0,4950 | P3 |
| ssi | 0,5263 | P3 |
| shk | 0,5188 | P3 |
| stuck K-i dan K-ii | 0,4562 | P3 |
| hyd K-i | 0,6100 | P4 |
| bit_wear K-1 | 0,2525 | P2 |
| tool_wear K-i dan K-ii | 0,4550 | P3 |

Akibatnya hari ini: TK-4 hanya bisa dicapai lewat `hyd` K-i, karena satu-satunya klaim yang batas atasnya menyentuh 0,60 adalah klaim itu. `bit_wear` tidak dapat menyumbang di atas P2 berapa pun skornya, dan itu memang yang tertulis di [DSS1] bagian 3.4.

Batas dominasi. Satu klaim tidak boleh menyumbang lebih dari 35 persen bobot dewan, karena satu engine dengan bobot terbesar bisa menentukan tingkat sendirian. Pemeriksaannya di segmen ini:

```
hyd K-i = 3,30 ; dewan rig = 9,15
pangsa = 3,30 / 9,15 = 36,07 persen  -> melewati batas 35 persen
bobot hyd K-i dipotong menjadi 0,35 x 9,15 = 3,2025
penyebut baru = 9,15 - 3,30 + 3,2025 = 9,0525
S = 1,65 / 9,0525 = 18,23 persen  (sebelum potong 18,03 persen)
```

Batas ini bukan hiasan: pada segmen ini klaim dengan bobot terbesar adalah `hyd` K-i, yaitu klaim yang juga punya kepala utama berbobot 1,50. Tanpa batas, satu klaim bisa memblokir atau memaksa tingkat.

### 5.4 Siapa memutuskan, dalam waktu berapa

| Tingkat | Pemutus | Batas waktu | Yang dicatat | Tindakan otomatis |
|---|---|---|---|---|
| TK-1 | Tidak ada pemutus | Tidak ada | Jendela tenang per shift | Tidak ada |
| TK-2 | Insinyur pengeboran, bila membuka daftar pantau | Akhir shift | Alasan tidak masuk antrean, bila diputuskan begitu | Tidak ada |
| TK-3 | Insinyur pengeboran | 1 shift (8 jam) | Satu baris LIN-01: waktu, aktor, keputusan, alasan | Tidak ada |
| TK-4 | Supervisor pengeboran bersama insinyur pengeboran | 1 jam | Satu baris LIN-01 ditambah panggilan lisan | Tidak ada |

Kolom terakhir diulang di setiap baris dengan sengaja. [JSON] baris 1414 menulis `auto_critical_alarm_slots` bernilai 0, [PIPE] baris 300 menulis `AUTO_CRITICAL_SLOTS = 0`, dan [PIPE] baris 738 menegaskan asersinya. Protokol ini tidak menambah satu pun jalur yang melewati manusia.

### 5.5 Mengapa empat tingkat ini bukan alarm

Tiga pemeriksaan, semuanya bisa diulang:

1. Tidak ada tingkat yang mengirim pesan sendiri. TK-3 dan TK-4 menghasilkan baris di antrean dan di log keputusan, keduanya dibaca manusia.
2. Setiap tingkat di atas TK-1 punya syarat yang belum terpenuhi hari ini untuk sebagian besar klaim. Pada segmen ini TK-1 sampai TK-4 semuanya bisa dihitung, dan hasilnya TK-2 (bagian 7.1).
3. Asersi di [PIPE] baris 722 menolak tier `ALARM-OTOMATIS` bila muncul di keluaran, dan asersi di baris 726 sampai 727 menolak peringatan L1 yang tidak mewajibkan tinjauan manusia. Protokol ini mewarisi kedua asersi itu, bukan menambah aturan lisan.

## 6. Aturan konflik, dan kapan manusia turun

### 6.1 Tujuh aturan konflik

| Kode | Nama | Aturan | Bukti yang memaksa aturan ini |
|---|---|---|---|
| K-1 | Kembar | Dua kepala dengan metrik identik dihitung satu suara | Empat pasangan identik, bagian 4.3; pola A [DSS3] bagian 5.1 |
| K-2 | Bisu | Kepala dengan `n_aktif` 0 menjadi abstain AB-5, bukan tolak | Empat kepala bisu, bagian 4.4 |
| K-3 | Saling meniadakan | Dua kepala setara berbeda putusan dihitung keduanya, tingkat dibatasi TK-2, pembaca diberi dua pembacaan | `hyd` indeks 0: rule menyala, persistence dan hibrida padam ([JSON] `contoh_idx_aktif` aturan mulai 0, dua lainnya mulai 20) |
| K-4 | Cakupan sebagian | Bila kepala konfirmasi (rule) diam tetapi kepala status (persistence) menyala, klaim dibatasi P2 | `stuck` indeks 0: persistence menyala, rule dan hibrida mulai 8, jadi padam di indeks 0 |
| K-5 | Dominasi bobot | Satu klaim tidak boleh melebihi 35 persen bobot dewan | `hyd` K-i 36,07 persen, bagian 5.3 |
| K-6 | Beda domain | `tool_wear` bersuara di dewan bengkel, tidak di dewan rig | Satuan jendela 1 detik lawan 60 detik, keputusan D-A7 [PM1] baris 132 |
| K-7 | Dua angka FAR | Bila satu kepala membawa dua angka FAR dengan populasi berbeda, TK-4 tertahan sampai keduanya direkonsiliasi | `hyd.hybrid` membawa FAR 4,10 per 24 jam dari lintas fold di medan `badge_far`, sementara `metrik_segmen` pada segmen F-14 bernilai 16,611 |

Aturan K-7 perlu penjelasan tambahan karena ia yang paling mudah diabaikan. Kedua angka itu bukan kontradiksi, tetapi juga tidak boleh saling menggantikan: 4,10 adalah FAR pada sembilan fold lintas well, sedangkan 16,611 adalah FAR pada segmen F-14 di [JSON]. Gate TK-4 meminta FAR terukur 6 ke bawah, dan angka mana yang dipakai menentukan lulus atau tidaknya `hyd` K-i. Protokolnya: tampilkan keduanya berdampingan dengan label populasinya, dan selama rekonsiliasi belum ada, TK-4 tidak dipakai untuk klaim itu. Ini penerapan aturan "dua pembacaan" yang sudah ada di KEP-06 ([KAT] baris 571).

### 6.2 Lima pemicu turunnya manusia

| Kode | Pemicu | Efek pada tingkat | Tindakan manusia |
|---|---|---|---|
| H-1 | Tingkat mencapai TK-3 atau TK-4 | Tidak ada, tingkat tetap | Insinyur pengeboran wajib menjawab dalam satu shift (TK-3) atau satu jam (TK-4) |
| H-2 | Konflik K-3 pada klaim penentu | Tingkat dibatasi TK-2 | Dua pembacaan ditampilkan berdampingan (literal dan ketat), manusia memilih |
| H-3 | Bobot klaim abstain 30 persen ke atas dari total dewan | Tingkat dibatasi TK-2 | Manusia memutuskan apakah data kanal perlu dilengkapi lebih dulu |
| H-4 | Klaim pendukung punya FAR di atas 6 per 24 jam | Tingkat dibatasi TK-2 | Manusia menimbang beban tinjauan; FAR tinggi adalah beban, bukan risiko ([DSS2] bagian 2.3) |
| H-5 | Dua angka FAR dengan populasi berbeda (K-7) | TK-4 tertahan | Pemilik data merekonsiliasi populasi angka sebelum eskalasi dipakai |

Pembatasan TK-2 dipilih sebagai rem, bukan TK-1. Alasannya: konflik dan data kurang tidak menghapus sinyal, sehingga menurunkannya ke TENANG akan menyembunyikan sesuatu yang nyata. Yang dicabut hanya hak naik ke antrean kerja, sampai manusia melihatnya.

### 6.3 Tabel ringkas konflik ke tingkat

| Keadaan pada siklus | Tingkat maksimum | Alasan |
|---|---|---|
| Tidak ada klaim P2 ke atas | TK-1 | Tidak ada yang perlu dilihat |
| Satu klaim P2, tanpa konflik | TK-2 | Bahan pantau, bukan antrean |
| Dua klaim P3 ke atas, konflik K-3 pada salah satunya | TK-2 | H-2 mencabut hak naik |
| Dua klaim P3 ke atas, tanpa konflik, beban di bawah 30 menit | TK-3 | Syarat lengkap |
| TK-3 ditambah satu klaim P4, FAR terukur di bawah 6, lead terukur | TK-4 | Syarat lengkap |
| Klaim P4 tetapi FAR hanya ada pada populasi berbeda | TK-3 | H-5 menahan satu langkah |
| Kuorum hadir di bawah 4 dari 7 | TK-2 | Suara belum mewakili dewan |
| Cakupan bobot di bawah 0,50 | TK-2 | Separuh bukti tidak hadir |

## 7. Satu siklus konsensus dengan angka nyata

### 7.1 Siklus tingkat segmen, langkah demi langkah

Segmen yang dipakai adalah segmen bawaan [JSON], yaitu F-14 dengan `seed` 42 dan `n_engine` 7 ([JSON] baris 14). Seluruh angka di bawah adalah keluaran perintah pada bagian 2.3.

Langkah 1, muat berkas dan periksa konvensi hitungan. Hasil: 24 kepala bermetrik konsisten, 0 ketidakcocokan.

Langkah 2, susun daftar klaim dan bobotnya setelah deduplikasi dan pembuangan kepala bisu. Hasil: sembilan klaim dewan rig dengan total bobot 9,15, dua klaim dewan bengkel dengan total 1,50.

Langkah 3, hitung `K_klaim` per klaim dengan rumus [DSS1] bagian 3.3 memakai `frac_aktif` sebagai derajat pada tingkat segmen. Kolom `s_h` di sini adalah `frac_aktif` yang dibaca langsung dari [JSON], bukan skor per jendela.

Langkah 4, potong dengan batas atas kelas dari bagian 5.3.

Langkah 5, petakan ke pita.

Langkah 6, tetapkan suara.

| Klaim | K_segmen | Batas atas | K_tampil | Pita | Suara | Bobot |
|---|---:|---:|---:|---|---|---:|
| vib | 0,3519 | 0,4950 | 0,3519 | P2 | V-1 Dukung | 1,65 |
| ssi | 0,0009 | 0,5263 | 0,0009 | P1 | V-2 Tolak, sebagian bisu | 0,40 |
| shk | 0,0153 | 0,5188 | 0,0153 | P1 | V-2 Tolak | 1,40 |
| stuck K-i | 0,0782 | 0,4562 | 0,0782 | P1 | V-2 Tolak | 1,40 |
| stuck K-ii | 0,0012 | 0,4562 | 0,0012 | P1 | V-2 Tolak | 0,75 |
| hyd K-i | 0,0762 | 0,6100 | 0,0762 | P1 | V-2 Tolak | 3,30 |
| hyd K-ii | tidak ada | 0,5125 | tidak ada | tidak ada | V-3 Abstain AB-1 | 0,00 |
| bit_wear K-1 | 0,1032 | 0,2525 | 0,1032 | P1 | V-2 Tolak | 0,25 |
| bit_wear K-2 | tidak ada | 0,2525 | tidak ada | tidak ada | V-3 Abstain AB-1 | 0,00 |

Dewan bengkel, dihitung terpisah:

| Klaim | K_segmen | Batas atas | K_tampil | Pita | Suara | Bobot |
|---|---:|---:|---:|---|---|---:|
| tool_wear K-i | 0,1659 | 0,4550 | 0,1659 | P1 | V-2 Tolak | 1,25 |
| tool_wear K-ii | 0,6013 | 0,4550 | 0,4550 | P3 | V-1 Dukung | 0,25 |

Langkah 7, jumlahkan dukungan berbobot dewan rig:

```
bobot dukung = 1,65 (hanya vib)
bobot bersuara = 9,15
S sebelum batas dominasi = 1,65 / 9,15 = 18,03 persen
S setelah batas dominasi = 1,65 / 9,0525 = 18,23 persen
```

Langkah 8, periksa kuorum. Engine bersuara: `vib`, `ssi`, `shk`, `stuck`, `hyd`, `bit_wear` sama dengan enam dari tujuh, memenuhi syarat 4. Cakupan bobot 1,00, memenuhi syarat 0,50. Tidak ada klaim dengan bobot abstain, sehingga H-3 tidak terpicu.

Langkah 9, tetapkan tingkat. Syarat TK-3 tidak terpenuhi karena klaim pada pita P3 ke atas berjumlah nol (syaratnya dua). Syarat TK-2 terpenuhi karena ada satu klaim di pita P2. **Tingkat keluar: TK-2 PANTAU.**

Langkah 10, hitung beban bila tingkat naik. Beban tinjauan untuk klaim yang bersuara pada shift itu: vib 17 tinjauan ([DSS2] bagian 2.2), ssi 0, shk 3, stuck 3, hyd 19, bit_wear tidak masuk daftar [DSS2] bagian 2.2 karena tidak punya kepala L1. Total beban baris adalah 42 baris per shift, sedangkan anggaran waktu [DSS2] bagian 5 adalah 30 menit. Karena tingkat keluar TK-2, tidak ada baris antrean yang dibuat pada siklus ini.

Hasil dewan bengkel: S sama dengan 0,25 dibagi 1,50 sama dengan 16,67 persen, satu klaim P3, tetapi hanya satu engine sehingga kuorum hadir tidak terpenuhi. Menurut tabel 6.3, tingkat dewan bengkel dibatasi TK-2, dan panelnya wajib mencetak lencana "suara tunggal" bersamaan dengan pita P3.

### 7.2 Siklus tingkat jendela, empat contoh yang bisa dibuka kembali

Empat contoh di bawah memakai `contoh_idx_aktif` di [JSON], yang berisi lima indeks aktif pertama per kepala. Aturan bacanya: bila indeks pertama sebuah kepala lebih besar dari jendela yang diperiksa, kepala itu padam pada jendela tersebut, karena daftarnya terurut menaik. Bila jendela yang diperiksa ada di dalam daftar, kepala itu menyala. Bila jendela lebih besar dari indeks terakhir yang tercatat, keadaannya tidak dapat dipastikan dari berkas ini.

Contoh 1, `hyd` indeks 0, konflik K-3. `rule_display` mulai 0 (menyala), `persistence` mulai 20 (padam), `hybrid` mulai 20 (padam).

```
K = (1,00 x 1 + 0,80 x 0 + 1,50 x 0) / 3,30 = 0,3030
batas atas 0,6100 tidak mengikat
pita P2 ; suara V-1 lemah ; konflik K-3 aktif
efek: tingkat klaim dibatasi TK-2, dua pembacaan ditampilkan (H-2)
```

Contoh 2, `stuck` indeks 0, konflik K-4. `persistence` mulai 0 (menyala), `rule_display` mulai 8 (padam), hibrida kembar dengan rule (padam, dan bobotnya dideduplikasi).

```
K = (1,00 x 0 + 0,40 x 1) / 1,40 = 0,2857
pita P2 ; suara V-1 lemah ; aturan K-4 membatasi klaim di P2
arti: status konfirmasi masih menyala dari jendela sebelumnya, tetapi aturan operasional sudah padam
```

Contoh 3, `shk` indeks 20, sepakat penuh. `rule_display` menyala (mulai 20), `persistence` menyala (mulai 20), hibrida kembar dengan rule, `rf_lowo` bisu.

```
K = (1,00 x 1 + 0,40 x 1) / 1,40 = 1,0000
dipotong batas atas 0,5188
pita P3 ; suara V-1 ; tanpa konflik
```

Contoh 3 adalah bukti bahwa pita P3 bisa dicapai di dalam satu mesin pada jendela nyata, dan bahwa potongan batas atas bekerja: skor mentah 1,0000 tampil sebagai 0,5188.

Contoh 4, `vib` indeks 429. `rule_display` menyala (429 ada di daftar), hibrida menyala (daftar sama), `rf_lowo` padam (indeks pertama 517), `persistence` tidak dapat dipastikan (indeks pertamanya 382 sampai 386, dan 429 di luar lima indeks yang tercatat).

```
K batas bawah (persistence padam) = (1,00 + 1,00 + 0) / 2,65 = 0,7547
K batas atas (persistence menyala) = (1,00 + 0,40 + 1,00 + 0) / 2,65 = 0,9057
keduanya dipotong batas atas 0,4950 -> pita P3 pada kedua kemungkinan
```

Contoh 4 memberi hasil yang tidak bergantung pada satu-satunya nilai yang tidak diketahui, karena potongan batas atas mengikat pada kedua ujung. Ini cara yang sah memakai data yang ada tanpa menebak nilai yang hilang, dan pola ini dipakai sebagai uji di bagian 11.

### 7.3 Sensitivitas bobot: dua versi, satu hasil

| Klaim | K versi A | K versi B | Pita A | Pita B | Bobot A | Bobot B |
|---|---:|---:|---|---|---:|---:|
| vib | 0,3519 | 0,3810 | P2 | P2 | 1,65 | 2,05 |
| ssi | 0,0009 | 0,0015 | P1 | P1 | 0,40 | 0,80 |
| shk | 0,0153 | 0,0206 | P1 | P1 | 1,40 | 1,80 |
| stuck K-i | 0,0782 | 0,0871 | P1 | P1 | 1,40 | 1,80 |
| stuck K-ii | 0,0012 | 0,0012 | P1 | P1 | 0,75 | 0,75 |
| hyd K-i | 0,0762 | 0,0762 | P1 | P1 | 3,30 | 3,30 |
| bit_wear K-1 | 0,1032 | 0,1032 | P1 | P1 | 0,25 | 0,80 |
| tool_wear K-i | 0,1659 | 0,1659 | P1 | P1 | 1,25 | 1,25 |
| tool_wear K-ii | 0,6013 | 0,6013 | P3 | P3 | 0,25 | 0,25 |

Keluaran pembanding, ditempel apa adanya:

```
DEWAN_BENGKEL_A S=0.1667 (16.67%) dari 1.50
DEWAN_BENGKEL_B S=0.1667 (16.67%) dari 1.50
DEWAN_RIG_A S=0.1803 (18.03%) dari 9.15
DEWAN_RIG_B S=0.1814 (18.14%) dari 11.30
```

Bacaan: tidak satu pun pita berubah antara dua versi bobot, dan dukungan berbobot bergeser dari 18,03 menjadi 18,14 persen. Tingkat keluar tetap TK-2 kerena pemicunya adalah adanya klaim P2, bukan ambang S. Dengan begitu, temuan silang di bagian 4.2 tidak mengubah keputusan, dan versi bobot mana pun yang akhirnya dipilih pemilik produk akan menghasilkan tingkat yang sama pada segmen ini.

### 7.4 Angka yang harus berubah agar tingkat naik

Bagian ini menjawab pertanyaan yang paling sering muncul saat membaca hasil TK-2: apa yang kurang. Jawabannya bukan pendapat, melainkan aritmetika pada bobot yang sudah ada.

Syarat TK-3 ada empat, dan yang gagal hari ini hanya satu: jumlah klaim pada pita P3 ke atas. Hari ini nol, syaratnya dua. Bila klaim kedua muncul, syarat S 0,40 juga harus diperiksa, dan di sinilah hasilnya menarik:

| Kombinasi klaim pada P3 ke atas | Bobot dukung | S terhadap 9,0525 | S 0,40 terpenuhi |
|---|---:|---:|---|
| vib dan stuck K-i | 3,05 | 33,69 persen | belum |
| vib dan shk | 3,05 | 33,69 persen | belum |
| vib dan hyd K-i | 4,95 | 54,68 persen | ya |
| vib, shk, dan stuck K-i | 4,45 | 49,16 persen | ya |

Artinya, dua klaim P3 tidak otomatis menghasilkan TK-3: komposisinya harus memuat klaim berbobot besar. Ini konsekuensi langsung dari pembobotan, dan lebih jujur dinyatakan sebagai tabel daripada sebagai janji "dua sinyal cukup".

Untuk TK-4, syarat tambahannya adalah satu klaim pada pita P4. Hanya `hyd` K-i yang batas atasnya 0,6100, jadi satu-satunya jalur hari ini adalah:

```
hyd K-i mencapai K_tampil 0,60 ke atas pada shift itu
S pada shift itu 0,60 ke atas (contoh: hyd 3,2025 + vib 1,65 + stuck K-i 1,40 = 6,2525 / 9,0525 = 69,08 persen)
FAR terukur 6 ke bawah pada populasi yang sama (K-7 harus selesai lebih dulu)
lead terukur pada klaim itu (hyd.hybrid sudah punya lead 8,0 menit, [JSON] baris 813)
beban tinjauan shift itu 30 menit ke bawah
```

Tiga bilangan di baris kedua sama dengan 69,08 persen, dan itu bukan ramalan: ia hanya menunjukkan bahwa kombinasi bobot yang ada sekarang membuat TK-4 bisa dicapai tanpa mengubah ambang, asalkan tiga klaim itu benar-benar berada di pita atasnya pada shift yang sama. Yang belum ada adalah data per shift untuk membuktikannya (bagian 12 butir S-1).

## 8. Spesifikasi lima fitur

Lima fitur, masing-masing dengan tiga belas butir wajib dari kartu, tidak diringkas. Kode fitur induk di katalog disebut supaya tidak ada fitur baru yang lahir tanpa rujukan: SWARM-01 memperluas KEP-08 ([KAT] baris 673), SWARM-02 memperluas KEP-01 ([KAT] baris 217), SWARM-03 belum punya rumah di katalog dan diusulkan masuk rumpun kepercayaan, SWARM-04 belum punya rumah dan diusulkan sebagai lampiran protokol, SWARM-05 memperluas LIN-01 ([KAT] baris 2071).

### 8.1 SWARM-01 Panel suara sembilan klaim per dewan

**ID dan nama fitur.** SWARM-01 Panel suara klaim per dewan. Memperluas KEP-08 Panel ketidaksepakatan antar head, dengan satuan yang naik dari kepala ke klaim.

**Tujuan.** Menyelesaikan masalah satu label gabungan yang membuat pembaca tidak tahu siapa yang mendukung dan siapa yang menolak, serta berapa berat masing-masing. Untuk insinyur pengeboran yang harus memutuskan apakah satu klaim layak masuk antrean, dan untuk penilai model yang harus memeriksa apakah dukungan datang dari bukti atau dari bobot administratif.

**Menggambarkan apa.** Komposisi suara, bukan tingkat bahaya. Batang dukung yang memanjang berarti makin banyak bobot bukti yang menyala, bukan makin dekat kegagalan. Batang tolak yang memanjang pada klaim dengan banyak kepala bisu berarti kanal masukan tidak tersedia, bukan kondisi aman. Bila bentang antara dukung dan abstain melebar, artinya cakupan bukti menyusut, dan itu bukan perbaikan.

**Pengguna dan momen pakai.** Insinyur pengeboran, setiap kali membuka satu klaim dari daftar pantau atau antrean, dua sampai empat kali per shift. Pengawas pengeboran saat menanyakan mengapa satu klaim tidak masuk antrean padahal ada suara yang menyala, sekali sampai dua kali per shift. Penilai model saat menyiapkan bab evaluasi, sekali per kampanye.

**Masukan.** [JSON] `engines[].heads[]`: `engine`, `head`, `klaim`, `tier`, `layer`, `layer` untuk lapisan, `n_windows`, `n_aktif`, `frac_aktif`, `metrik_segmen.precision`, `metrik_segmen.recall`, `metrik_segmen.far_segmen`, `badge_far`, `batas_pemakaian`. Satuan: hitungan jendela dan pecahan 0 sampai 1 untuk `frac_aktif`, FAR dalam FP per 24 jam negatif untuk enam engine dan FP per menit untuk `tool_wear`. Rentang nilai: `frac_aktif` 0 sampai 0,6503 pada segmen ini, FAR 0 sampai 496,092. Cara memperoleh: dibaca dari berkas dengan `jq`, tidak dihitung ulang, dan konvensi `n_aktif = tp + fp` diperiksa lebih dulu (24 kepala, 0 ketidakcocokan, bagian 2.2).

**Algoritma.** Lima langkah, semuanya deterministik. (1) Kelompokkan kepala per klaim dengan kunci `engine` ditambah `klaim`. (2) Deduplikasi: dua kepala dalam satu klaim dengan tanda tangan `frac_aktif`, `tp`, `fp`, `n_aktif` identik dihitung satu suara, dan kepala yang dibuang dicatat namanya (aturan K-1, bagian 4.3). (3) Tandai kepala dengan `n_aktif` 0 sebagai bisu dan beri kode AB-5 (aturan K-2). (4) Hitung `K_klaim = jumlah(w_h x s_h) / jumlah(w_h)` dengan `s_h` sama dengan 1 bila kepala menyala dan 0 bila padam; pada tingkat segmen, `s_h` diisi `frac_aktif` dan nilainya diberi label "derajat segmen". (5) Potong dengan `K_max` kelas dari [DSS1] bagian 3.4, petakan ke pita P1 sampai P5 dengan batas 0,20, 0,40, 0,60, 0,80 dari [DSS1] bagian 4.1, lalu tetapkan suara V-1, V-2, atau V-3 (bagian 4.1). Parameter: bobot `w_h` dari [DSS1] bagian 3.2, tanpa ambang bebas baru. Alasan memilih penjumlahan berbobot dan bukan rata-rata sederhana: tanpa bobot, tiga kepala bisu ssi akan berbobot sama dengan kepala rule yang menyala, dan itu sudah terbukti salah di bagian 4.4.

**Workflow.** (1) Muat [JSON]. (2) Periksa `n_aktif = tp + fp` untuk semua kepala bermetrik, hentikan bila ada satu ketidakcocokan. (3) Kelompokkan per klaim. (4) Buang kepala kembar, catat nama yang dibuang. (5) Tandai kepala bisu dengan AB-5. (6) Hitung `K_klaim`, potong dengan `K_max`, petakan ke pita. (7) Tetapkan suara per klaim. (8) Susun panel per dewan, urut bobot menurun. (9) Tampilkan panel pada halaman dewan dan pada setiap kartu klaim.

**Keluaran.** Dua bentuk data. Pertama, satu baris per klaim berisi `engine`, `klaim`, `K_klaim`, `K_max`, `K_tampil`, `pita`, `suara`, `bobot`, `jumlah_kepala_bersuara`, `jumlah_kepala_bisu`, `kode_abstain`. Kedua, satu ringkasan per dewan berisi total bobot, bobot dukung, dukung berbobot S, kuorum hadir, cakupan bobot, dan tingkat. Satuan: pecahan 0 sampai 1 untuk keyakinan dan bobot tak bersatuan, persen untuk S. Arti tiap nilai: `K_tampil` 0,20 ke atas berarti klaim bersuara dukung, di bawah 0,20 berarti tolak dengan alasan, dan ketiadaan angka berarti abstain dengan kode. Pada segmen ini keluarannya sembilan baris dewan rig dan dua baris dewan bengkel, sudah ditempel di bagian 7.1.

**Saran penyajian.** Batang bertumpuk horizontal per klaim, satu baris per klaim, diurut bobot menurun, dengan tiga segmen: dukung, tolak, abstain. Angka bobot dicetak di dalam segmen, dan jumlah kepala bersuara dicetak di ujung baris. Alasan: pembaca membandingkan panjang dan posisi, bukan luas atau sudut, dan perbandingan antar baris terbaca tanpa legenda. Tata letak contoh dalam teks:

```
Dewan rig, segmen F-14, 6 dari 7 engine hadir, cakupan bobot 100 persen
hyd K-i      [========== tolak 3,30 ==========] 3 kepala, pita P1
vib          [== dukung 1,65 ==][== tolak 1,00 ==] 3 kepala, pita P2
shk          [===== tolak 1,40 =====] 2 kepala, rf bisu, pita P1
stuck K-i    [===== tolak 1,40 =====] 2 kepala, pita P1
stuck K-ii   [== tolak 0,75 ==] 3 kepala, pita P1
ssi          [= tolak 0,40 =] 1 kepala, 3 kepala bisu, pita P1
bit_wear K-1 [= tolak 0,25 =] 1 kepala, pita P1
hyd K-ii     [-- abstain AB-1 --] menunggu kampanye K-ii
bit_wear K-2 [-- abstain AB-1 --] menunggu pra-registrasi
                                    S = 18,23 persen (batas dominasi aktif) -> TK-2 PANTAU
```

**Dasar riset penyajian.** [VR] bagian 5.5 menyatakan visual lazim untuk keluaran konsensus adalah batang setuju, tidak setuju, dan abstain per pernyataan, dengan kalimat inti dari LV10: setelah kelompok opini muncul, yang dicari adalah pernyataan yang sama-sama diterima atau ditolak. [VR] bagian 5.4 dan LV15 menolak peringkasan menjadi satu label karena penjelasan yang tidak sepakat akan terbaca seolah sepakat. [VR] bagian 5.8 dan LV7 menyatakan panjang dan posisi 2D mengalahkan luas dan sudut untuk informasi kuantitatif, dan itu alasan menolak donat dan gauge.

**Status bukti.** Sudah dihitung dari data nyata untuk sebelas klaim: bobot, `K_segmen`, `K_tampil`, pita, dan suara berasal dari [JSON] dengan perintah di bagian 2.3, dan keluarannya ditempel di bagian 7.1. Yang masih rancangan: pemakaian per jendela dan per shift, karena deret per menit belum diekspor.

**Salah tafsir yang harus dicegah.** Pertama, membaca batang tolak panjang sebagai "kondisi aman"; batang itu juga bisa berarti kanal tidak tersedia, dan jumlah kepala bisu wajib tercetak. Kedua, membaca `K_tampil` yang tertahan di 0,4950 sebagai skor mentah; itu batas atas bukti kelas, dan nilainya harus selalu ditemani label batas. Ketiga, menjumlahkan bobot dewan rig dan dewan bengkel menjadi satu angka; satuannya berbeda. Keempat, membaca S 18,23 persen sebagai peluang kegagalan; ia adalah pangsa bobot yang mendukung, tanpa satuan peluang.

**Cara menguji.** Uji 1, jalankan perintah bagian 2.3 dan pastikan sembilan baris klaim dewan rig keluar dengan bobot total 9,15. Uji 2, buang aturan deduplikasi pada data sintetis berisi dua kepala identik, lalu pastikan bobot klaim naik sebesar bobot kepala kembar; ini membuktikan deduplikasi bekerja. Uji 3, isi `n_aktif` 0 pada kepala rule ssi dan pastikan suaranya berubah menjadi AB-5, bukan V-2. Uji 4, periksa bahwa tidak ada baris dengan suara V-1 yang pitanya P1.

### 8.2 SWARM-02 Tangga empat tingkat dan syarat naik

**ID dan nama fitur.** SWARM-02 Tangga tingkat keputusan dengan syarat naik yang tercetak. Memperluas KEP-01 Papan vonis per kelas kerusakan ([KAT] baris 217).

**Tujuan.** Menyelesaikan masalah pembaca yang melihat satu label tingkat lalu menebak apa yang kurang untuk naik. Untuk insinyur pengeboran dan pengawas yang perlu tahu apakah diamnya alat berarti tenang atau berarti bukti belum cukup.

**Menggambarkan apa.** Kedudukan satu siklus pada empat tingkat, dan satu syarat yang belum terpenuhi. Naik satu tingkat berarti satu syarat angka terpenuhi, bukan kondisi rig memburuk dengan sendirinya. Turun satu tingkat karena konflik atau data kurang berarti alat menahan diri, bukan kondisi membaik.

**Pengguna dan momen pakai.** Insinyur pengeboran di awal shift saat memutuskan apa yang dibaca lebih dulu, sekali per shift. Pengawas pengeboran saat menerima eskalasi, setiap kali eskalasi terjadi. Auditor internal saat memeriksa apakah satu eskalasi sah, sekali per periode audit.

**Masukan.** Keluaran SWARM-01 ditambah angka kuorum dari SWARM-03, beban tinjauan dari [DSS2] bagian 2.2, dan medan `badge_far` serta `lead_menit` dari [JSON]. Satuan: tingkat tanpa satuan, dukungan berbobot dalam persen, beban dalam menit per shift, FAR dalam FP per 24 jam negatif. Rentang: S 0 sampai 100 persen, beban 0 sampai nilai anggaran 30 menit, FAR 0 sampai 496,092. Cara memperoleh: dihitung pada langkah 7 sampai 10 bagian 7.1, bukan dibaca langsung.

**Algoritma.** Urutan pemeriksaan, berhenti pada tingkat pertama yang gagal. (1) Bila tidak ada klaim 0,20 ke atas, TK-1. (2) Bila ada klaim P2 atau S 0,20 ke atas, TK-2, lalu periksa syarat TK-3. (3) TK-3 bila kuorum hadir 4 dari 7 dan cakupan bobot 0,50 ke atas dan klaim P3 ke atas minimal dua dan S 0,40 ke atas dan beban 30 menit ke bawah. (4) TK-4 bila semua syarat TK-3 dan ada klaim P4 dan S 0,60 ke atas dan FAR terukur 6 ke bawah pada populasi yang sama dan lead terukur dan tidak ada konflik K-3 pada klaim penentu. (5) Terapkan rem H-2 sampai H-5 dan batas dominasi 35 persen sebelum menetapkan tingkat akhir. Parameter: 0,20, 0,40, 0,60 dari [DSS1] bagian 4.1, 4 dari 7 dan 0,50 dari bagian 5.2, 30 menit dari [DSS2] bagian 5, 6 per 24 jam dari [PM1] baris 138. Alasan memilih tangga berurutan dan bukan skor kontinu: keputusan yang diambil bersifat diskret (masuk antrean atau tidak), dan syarat yang tercetak membuat penolakan bisa diperiksa.

**Workflow.** (1) Ambil keluaran SWARM-01. (2) Susun daftar syarat tiap tingkat dengan nilai sekarang dan nilai ambang. (3) Jalankan pemeriksaan berurutan. (4) Terapkan rem H-2 sampai H-5. (5) Tetapkan tingkat. (6) Cetak tingkat, syarat yang gagal, dan satu angka yang harus berubah. (7) Simpan hasil ke log keputusan (LIN-01). (8) Tampilkan tangga pada kepala halaman dewan.

**Keluaran.** Satu objek per siklus: `tingkat`, `nama`, `syarat_lulus` (daftar berpasangan nilai sekarang dan ambang), `syarat_gagal` (satu butir), `rem_aktif` (daftar kode H), `pemutus`, `batas_waktu`. Tanpa satuan kecuali angka pendukungnya. Arti: TK-1 tanpa tindakan, TK-2 daftar pantau, TK-3 antrean tinjauan satu shift, TK-4 eskalasi satu jam. Pada segmen ini keluarannya TK-2 PANTAU dengan syarat gagal "klaim P3 ke atas 0 dari 2" dan rem aktif tidak ada (bagian 7.1).

**Saran penyajian.** Tangga horizontal empat simpul dengan simpul aktif ditandai, dan di bawahnya satu baris teks berisi syarat yang gagal beserta angkanya. Bukan warna saja: setiap simpul membawa label teks TK-1 sampai TK-4 dan namanya. Alasan: tingkat bersifat ordinal, dan pembaca perlu tahu jarak ke tingkat berikutnya, bukan hanya posisi sekarang. Tata letak contoh dalam teks:

```
[TK-1 TENANG] -- [TK-2 PANTAU] -- [TK-3 TINJAU] -- [TK-4 ESKALASI]
                     ^ aktif
gagal : klaim pita P3 ke atas = 0, syarat 2
lulus : kuorum hadir 6/7, cakupan bobot 1,00, S 18,23 persen, beban 42 baris (tidak dipakai pada TK-2)
```

**Dasar riset penyajian.** [VR] bagian 0 butir 2 menetapkan bahwa yang menentukan pilihan visual adalah pertanyaan yang harus dijawab pembaca, bukan estetika, dengan LV13 dan LV6 sebagai sumbernya. Tabel A di [VR] bagian 3 menerapkan aturan itu per jenis keluaran: baris 1 untuk skor keyakinan memilih titik kuantil, dan baris 4 untuk ketidaksepakatan model memilih panel per item. Keduanya bukan pilihan bebas, melainkan turunan dari pertanyaan pembacanya. Pertanyaan di sini adalah "seberapa jauh dari tindakan", jadi bentuknya posisi pada skala berurut, bukan luas atau warna tunggal. [VR] bagian 6 melarang gauge dan cakram untuk besaran kuantitatif karena luas dan sudut tidak diproses cepat (LV7). Untuk larangan warna tanpa label, KEP-03 ([KAT] baris 365) sudah menetapkan badge wajib bertulisan, dan aturan yang sama dipakai di sini.

**Status bukti.** Sudah dihitung dari data nyata untuk segmen F-14: tingkat TK-2 dengan seluruh angka syaratnya (bagian 7.1). Untuk siklus per shift, syaratnya sudah lengkap tetapi datanya belum ada (bagian 12 butir S-1), sehingga yang tampil hari ini adalah tangga pada tingkat segmen.

**Salah tafsir yang harus dicegah.** Pertama, membaca TK-2 sebagai "aman"; TK-2 berarti ada satu klaim di pita P2 yang belum cukup untuk antrean. Kedua, membaca angka 0,40 pada syarat S sebagai peluang; itu pangsa bobot. Ketiga, mengira tingkat bisa naik karena satu engine sangat yakin; batas dominasi 35 persen dan syarat dua klaim mencegahnya. Keempat, membaca rem H-4 (FAR tinggi) sebagai penurunan risiko; FAR tinggi berarti beban tinjauan tinggi ([DSS2] bagian 2.3).

**Cara menguji.** Uji 1, jalankan siklus segmen dan pastikan tingkat keluar TK-2 dengan syarat gagal "0 dari 2" pada klaim P3. Uji 2, ubah pita `vib` dan `stuck` K-i menjadi P3 pada salinan data. Syarat dua klaim P3 menjadi terpenuhi, tetapi S tetap 33,69 persen karena 3,05 dibagi 9,0525, masih di bawah 0,40, sehingga hasilnya tetap TK-2 (tabel bagian 7.4 baris pertama). Ini membuktikan syarat S bekerja dan bukan sekadar syarat jumlah. Uji 3, aktifkan konflik K-3 pada klaim penentu dan pastikan tingkat turun ke TK-2 walaupun syarat lain terpenuhi. Uji 4, periksa bahwa tidak ada satu pun tingkat yang menghasilkan `tindakan_otomatis` bernilai benar.

### 8.3 SWARM-03 Meter kuorum dan cakupan bobot

**ID dan nama fitur.** SWARM-03 Meter kuorum kehadiran dan cakupan bobot. Fitur baru, diusulkan masuk rumpun kepercayaan bersama KEP-03 dan KEP-05.

**Tujuan.** Menyelesaikan masalah "kuorum terpenuhi" yang dinyatakan tanpa angka, sehingga pembaca sukar membedakan dewan yang lengkap dari dewan yang tinggal dua anggota. Untuk penilai model dan pengawas yang perlu tahu apakah satu tingkat dihitung dari mayoritas atau dari minoritas suara.

**Menggambarkan apa.** Kehadiran bukti, bukan mutu bukti. Naiknya cakupan bobot berarti makin banyak klaim yang benar-benar dinilai, bukan makin banyak yang menyala. Turunnya kehadiran di bawah empat engine berarti tingkat tidak boleh naik, sekalipun ada klaim yang menyala kuat.

**Pengguna dan momen pakai.** Penilai model saat memeriksa satu siklus yang hasilnya mengejutkan, sekali per kampanye. Pengawas pengeboran saat menerima eskalasi TK-4, setiap kali eskalasi. Auditor saat menguji apakah laporan tingkat bisa direproduksi, sekali per periode audit.

**Masukan.** Keluaran SWARM-01 (suara per klaim dan bobot per klaim), daftar engine dari [JSON] `engines[].engine`, dan bobot klaim dari bagian 4.5. Satuan: jumlah engine (bilangan bulat 0 sampai 7), pecahan 0 sampai 1 untuk cakupan. Rentang: kehadiran 0 sampai 6 pada segmen ini, cakupan 0 sampai 1. Cara memperoleh: hitung langsung, bukan dibaca.

**Algoritma.** (1) Hitung `Q_hadir` sebagai jumlah engine yang punya minimal satu klaim bersuara V-1 atau V-2. (2) Hitung `W_total` sebagai jumlah bobot semua klaim dewan, termasuk klaim abstain yang berbobot lebih dari nol. (3) Hitung `W_suara` sebagai jumlah bobot klaim yang bersuara. (4) `C_bobot = W_suara / W_total`. (5) Bandingkan dengan ambang 4 dari 7 dan 0,50. (6) Bila cakupan di bawah 0,50, terbitkan rem H-3 dan batasi tingkat di TK-2. Parameter: ambang 4 dan 0,50 dari bagian 5.2. Alasan dua meter dan bukan satu: satu angka kuorum bisa dipenuhi dengan banyak klaim kecil, sementara cakupan mengukur berat bukti yang hadir, dan keduanya perlu dilihat bersama.

**Workflow.** (1) Ambil daftar klaim dan bobot dari SWARM-01. (2) Tandai klaim bersuara. (3) Hitung dua meter. (4) Bandingkan dengan ambang. (5) Kirim hasil ke SWARM-02 sebagai masukan. (6) Tampilkan meter di panel dewan, di bawah panel suara.

**Keluaran.** `Q_hadir` (bilangan bulat), `Q_ambang` (4), `C_bobot` (pecahan), `C_ambang` (0,50), `status_kuorum` (terpenuhi atau tidak), `daftar_absen` (nama engine yang tidak bersuara dan alasannya). Pada segmen ini: 6 dari 7, cakupan 1,00, status terpenuhi, daftar absen berisi `tool_wear` dengan alasan domain terpisah.

**Saran penyajian.** Satu batang horizontal 0 sampai 100 persen untuk cakupan, dengan garis ambang di 50 persen, ditambah tujuh titik kehadiran di bawahnya, masing-masing berlabel nama engine dan berwarna menurut status hadir, abstain, atau di luar dewan. Satu sumbu saja, tanpa sumbu kedua. Tata letak contoh dalam teks:

```
cakupan bobot  [####################################] 100 persen   (ambang 50)
kehadiran      vib *  ssi *  shk *  stuck *  hyd *  bit_wear *  tool_wear (dewan bengkel)
```

**Dasar riset penyajian.** [VR] bagian 6 butir 1 melarang dua sumbu Y pada satu grafik dan menyarankan panel bersusun dengan sumbu x sama, dengan LV8 sebagai sumber. Meter tunggal dengan satu ambang mengikuti anjuran yang sama. [VR] bagian 5.8 dan LV7 menyatakan posisi dan panjang adalah kanal yang paling akurat untuk besaran kuantitatif, sehingga batang dipilih daripada donat atau cincin.

**Status bukti.** Sudah dihitung dari data nyata: 6 dari 7 dan cakupan 1,00 pada segmen F-14 (bagian 7.1). Yang masih rancangan: pemakaian per shift dan riwayat kehadiran antar shift.

**Salah tafsir yang harus dicegah.** Pertama, membaca cakupan 100 persen sebagai semua klaim yakin; cakupan hanya berarti semua klaim punya bobot, dan sembilan dari sebelas klaim justru menolak. Kedua, membaca kehadiran 6 dari 7 sebagai hampir lengkap padahal satu engine dipisah karena satuannya berbeda, bukan karena absen. Ketiga, mengira ambang 50 persen bisa diturunkan bila hasilnya kurang memuaskan; ambang adalah keputusan protokol, bukan parameter yang disetel per pembacaan.

**Cara menguji.** Uji 1, jalankan pada segmen dan pastikan 6 dari 7 serta cakupan 1,00. Uji 2, setel bobot `hyd` K-ii menjadi 0,5 pada salinan data dan pastikan cakupan turun menjadi 9,15 dibagi 9,65 sama dengan 0,948, masih di atas ambang, dan status tetap terpenuhi. Uji 3, setel lima klaim menjadi abstain dan pastikan cakupan turun di bawah 0,50 serta tingkat dibatasi TK-2 dengan rem H-3 aktif.

### 8.4 SWARM-04 Diagram alur siklus protokol

**ID dan nama fitur.** SWARM-04 Diagram alur siklus protokol, satu halaman statis. Fitur baru, diusulkan sebagai lampiran protokol dan bukan bagian riwayat keputusan.

**Tujuan.** Menyelesaikan masalah protokol yang hanya hidup di dokumen dan belum dapat diperiksa pembaca di layar. Untuk auditor dan insinyur baru yang perlu melihat urutan pemeriksaan dan letak setiap rem sebelum memakai alat.

**Menggambarkan apa.** Urutan keputusan, bukan kejadian. Setiap simpul adalah pemeriksaan, setiap panah adalah arah, dan setiap gerbang adalah syarat angka. Naiknya jumlah simpul yang dilewati berarti satu siklus makin didukung bukti; berhentinya siklus di simpul tertentu menunjukkan syarat mana yang gagal.

**Pengguna dan momen pakai.** Auditor internal saat memeriksa apakah satu tingkat dihitung menurut protokol, sekali per periode audit. Insinyur baru saat pertama kali memakai alat, sekali di awal penugasan. Penilai model saat memetakan keluaran mana yang masuk akal untuk satu klaim, sekali per kampanye.

**Masukan.** Tidak ada masukan data. Diagram ini menggambarkan protokol bagian 5 dan bagian 6, dengan angka ambang yang sama. Yang diperiksa: enam simpul, tujuh aturan konflik, lima rem, dan urutan pemeriksaan.

**Algoritma.** Penyusunan diagram bukan hitungan, jadi yang ditetapkan adalah daftar simpul dan gerbangnya. Simpul 1, muat dan periksa konvensi. Simpul 2, susun klaim dan bobot. Simpul 3, hitung `K_klaim` dan potong batas atas. Simpul 4, tetapkan suara. Simpul 5, jumlahkan dukungan dan periksa kuorum. Simpul 6, tetapkan tingkat dan terbitkan syarat gagal. Gerbang di antara simpul 3 dan 4 adalah aturan K-1, K-2, K-4; gerbang di antara simpul 5 dan 6 adalah aturan K-3, K-5, K-6, K-7 dan rem H-2 sampai H-5. Alasan memilih alur dan bukan tabel: yang dibaca adalah urutan, dan kesalahan urutan adalah kesalahan yang paling mahal di protokol ini (misalnya memotong batas atas setelah menjumlahkan dukungan akan membesarkan S).

**Workflow.** (1) Ambil protokol versi terakhir dari bagian 5 dan 6. (2) Susun enam simpul dan tandai gerbangnya. (3) Cetak angka ambang pada setiap gerbang. (4) Tautkan setiap simpul ke fitur yang mengerjakannya: simpul 1 sampai 4 ke SWARM-01, simpul 5 ke SWARM-03, simpul 6 ke SWARM-02 dan SWARM-05. (5) Simpan sebagai satu halaman statis. (6) Periksa ulang setiap kali protokol berubah, dan beri tanggal versi yang digambarkan.

**Keluaran.** Satu gambar alur enam simpul dengan angka ambang, tanpa data. Arti: posisi simpul menunjukkan urutan, bukan waktu; angka pada gerbang menunjukkan syarat, bukan hasil. Nomor versi dan tanggal wajib tercetak, supaya diagram lama tidak dipakai untuk protokol baru.

**Saran penyajian.** Diagram alur vertikal enam simpul, tiap simpul satu kotak berisi nama pemeriksaan dan keluarannya, tiap panah diberi label gerbang bila ada. Lebar satu kolom, tinggi kira-kira satu layar, tanpa warna kecuali satu aksen pada simpul yang sedang dijelaskan. Tata letak contoh dalam teks:

```
[1 muat + periksa konvensi]  ->  24 kepala, 0 mismatch
            |
[2 susun klaim + bobot]      ->  9 klaim rig, 9,15 ; 2 klaim bengkel, 1,50
            |
[3 K_klaim + batas atas]     ->  gerbang K-1 K-2 K-4
            |
[4 suara V-1 V-2 V-3]        ->  pita P1..P5
            |
[5 dukungan + kuorum]        ->  gerbang K-3 K-5 K-6 K-7, rem H-2..H-5
            |
[6 tingkat + syarat gagal]   ->  TK-1..TK-4, pemutus, batas waktu
```

**Dasar riset penyajian.** Batas penting yang harus disebut: [KAT] baris 2097 melarang diagram alir untuk riwayat keputusan di LIN-01 dan meminta tabel, karena pembaca mencari satu baris tertentu dan memeriksa urutan waktu (LV4, LV14). Larangan itu berlaku pada riwayat, bukan pada protokol. Karena itu SWARM-04 hanya menggambarkan satu siklus yang sama untuk semua kejadian dan tidak pernah merender data, sementara semua riwayat tetap di tabel LIN-01 dan buku SWARM-05. Untuk pilihan bentuknya sendiri, [VR] bagian 3 Tabel A baris 10 memakai linimasa vertikal berurut waktu untuk linimasa keputusan (LV16, LV11), dan bentuk alur vertikal di sini meminjam kerangka visual yang sama dengan isi yang berbeda. Ini pilihan desain yang dinyatakan terbuka, bukan klaim bahwa literatur menetapkan diagram alur untuk protokol.

**Status bukti.** Rancangan. Diagram ini belum digambar, dan yang ada baru daftar simpul beserta gerbangnya. Isinya berasal dari protokol yang sudah dihitung, tetapi bentuk gambarnya belum dibuat.

**Salah tafsir yang harus dicegah.** Pertama, membaca urutan simpul sebagai urutan waktu kejadian; ini urutan pemeriksaan pada satu siklus. Kedua, memakai diagram ini sebagai bukti bahwa siklus berjalan; bukti ada di keluaran perintah bagian 2.3 dan 7. Ketiga, memakai versi diagram lama setelah protokol berubah; nomor versi wajib tampil.

**Cara menguji.** Uji 1, hitung jumlah simpul pada gambar dan pastikan enam, sesuai daftar. Uji 2, periksa setiap angka pada gerbang terhadap bagian 5.1 dan 5.2, dan pastikan tidak ada angka yang tidak muncul di dokumen induk. Uji 3, periksa bahwa gambar tidak memuat satu pun data kejadian; bila ada, gambar itu melanggar batas LIN-01 dan harus dipindah ke tabel.

### 8.5 SWARM-05 Buku konflik dan jadwal turunnya manusia

**ID dan nama fitur.** SWARM-05 Buku konflik dan jadwal turunnya manusia. Memperluas LIN-01 Log keputusan human-in-loop ([KAT] baris 2071).

**Tujuan.** Menyelesaikan masalah konflik yang tercatat sebagai catatan bebas sehingga belum dapat dihitung dan belum punya tenggat. Untuk pengawas pengeboran yang harus tahu konflik mana yang menunggu keputusan dan sudah berapa lama, dan untuk auditor yang memeriksa apakah rem dipakai sebagaimana mestinya.

**Menggambarkan apa.** Beban keputusan manusia, bukan kondisi rig. Bertambahnya baris berarti makin banyak konflik atau data kurang yang menunggu, dan itu beban, bukan bahaya. Umur baris yang memanjang berarti tenggat terlewat, dan itu masalah proses, bukan masalah model.

**Pengguna dan momen pakai.** Pengawas pengeboran di awal dan akhir shift, dua kali per shift. Insinyur pengeboran saat membuka satu baris konflik, setiap kali konflik muncul. Auditor internal sekali per periode audit untuk memeriksa tenggat.

**Masukan.** Keluaran SWARM-01 dan SWARM-02 (klaim, pita, tingkat, rem aktif), daftar aturan K-1 sampai K-7 dan rem H-1 sampai H-5, serta stempel waktu siklus. Medan yang dipakai dari [JSON]: `contoh_idx_aktif` untuk membuktikan konflik pada jendela tertentu, `metrik_segmen` untuk angka pembanding, dan `badge_far` untuk kasus K-7. Satuan: waktu dalam jam, umur dalam jam, bobot tanpa satuan. Rentang: umur 0 sampai 8 jam untuk TK-3 dan 0 sampai 1 jam untuk TK-4. Cara memperoleh: dihitung saat siklus berjalan, bukan dibaca.

**Algoritma.** (1) Untuk setiap siklus dengan tingkat TK-2 ke atas, periksa apakah ada aturan konflik atau rem yang aktif. (2) Bila ada, buat satu baris dengan kode aturan, klaim, jendela bukti, tingkat sebelum rem, tingkat sesudah rem, pemutus, dan tenggat. (3) Hitung umur baris sebagai selisih waktu sekarang dengan waktu siklus. (4) Urutkan baris menurut tenggat naik, lalu umur turun. (5) Baris yang umurnya melewati tenggat ditandai terlambat dan dihitung dalam laporan mingguan. Parameter: tenggat 8 jam untuk TK-3 dan 1 jam untuk TK-4 (bagian 5.4). Alasan bentuk tabel dan bukan diagram: pembaca mencari satu baris dan memeriksa tenggatnya, dan itu tugas tabel menurut LV4 dan LV14.

**Workflow.** (1) Jalankan siklus SWARM-01 sampai SWARM-02. (2) Kumpulkan aturan dan rem yang aktif. (3) Buat baris konflik, satu per aturan per klaim. (4) Isi pemutus dan tenggat menurut tingkat. (5) Tampilkan tabel terurut tenggat. (6) Setelah manusia memutuskan, tutup baris dengan keputusan dan alasannya. (7) Hitung tingkat penyelesaian tepat waktu per shift.

**Keluaran.** Tabel dengan sepuluh kolom: waktu siklus, klaim, pita, tingkat sebelum rem, aturan atau rem, tingkat sesudah rem, bukti (jendela atau angka), pemutus, tenggat, umur. Satuan: jam untuk waktu dan umur, tanpa satuan untuk bobot. Arti: umur di bawah tenggat berarti masih dalam kendali, di atas tenggat berarti terlambat, dan tingkat sesudah rem yang lebih rendah dari sebelumnya berarti rem bekerja. Pada segmen ini tidak ada baris yang lahir, karena tingkat keluar TK-2 tanpa rem aktif (bagian 7.1), dan itu sendiri merupakan hasil yang harus tercetak sebagai "buku kosong dengan alasan".

**Saran penyajian.** Tabel terurut tenggat dengan kolom umur dan status, satu baris per konflik, kolom pertama berisi pengenal yang terbaca manusia (nama klaim dan pita, bukan nomor otomatis). Baris terlambat ditandai teks, bukan warna saja. Tata letak contoh dalam teks:

```
waktu    klaim     pita  sebelum  aturan  sesudah  bukti                 pemutus      tenggat  umur
08:12    hyd K-i   P2    TK-3     K-3     TK-2     indeks 0: rule on,    insinyur     16:12    0,3 jam
                                                    persistence off                pengeboran
08:12    shk       P3    TK-3     H-4     TK-2     FAR 6,618 per 24 jam  pengawas     16:12    0,3 jam
```

**Dasar riset penyajian.** [VR] bagian 5.3 menyatakan tabel terurut dengan kolom umur lebih informatif daripada satu angka terbuka, dengan kalimat inti LV14: sebaran umur lebih penting daripada satu hitungan terbuka, dan bucket umur dicontohkan 0 sampai 2 hari, 3 sampai 7 hari, 8 sampai 15 hari, lebih dari 30 hari. Untuk sisi tabel, LV4 menyatakan kolom pertama sebaiknya pengenal yang terbaca manusia, bukan ID otomatis. [KAT] baris 2097 juga meminta tabel, bukan diagram alir, untuk riwayat keputusan.

**Status bukti.** Sebagian sudah dihitung: aturan dan rem yang aktif pada segmen ini sudah diperiksa (tidak ada), dan bukti jendela untuk K-3 dan K-4 sudah dapat dibuka dari `contoh_idx_aktif` (bagian 7.2). Yang masih rancangan: skema pencatatan umur dan tenggat, karena belum ada tabel log keputusan yang menyimpan waktu siklus.

**Salah tafsir yang harus dicegah.** Pertama, membaca buku kosong sebagai "tidak ada masalah"; buku kosong bisa berarti tidak ada rem yang aktif, dan alasan itu harus tercetak. Kedua, membaca umur panjang sebagai kelalaian orang; umur panjang bisa berarti tenggat tidak pernah ditetapkan, dan itu masalah skema. Ketiga, membaca tingkat sesudah rem lebih rendah sebagai penurunan risiko; rem menahan keputusan, bukan menurunkan bahaya. Keempat, menjumlahkan baris konflik dari dua dewan menjadi satu beban; satuannya beda domain.

**Cara menguji.** Uji 1, jalankan siklus segmen dan pastikan buku kosong dengan alasan "tidak ada rem aktif pada TK-2". Uji 2, paksa konflik K-3 pada `hyd` indeks 0 dan pastikan satu baris lahir dengan tenggat 8 jam dan tingkat sesudah rem TK-2. Uji 3, geser waktu siklus 9 jam ke belakang dan pastikan baris yang sama berstatus terlambat. Uji 4, periksa bahwa kolom pertama tidak berisi nomor otomatis.

## 9. Saran penyajian dan dasar risetnya

### 9.1 Ringkasan pilihan visual per fitur

| Fitur | Bentuk visual | Alasan satu baris | Sumber |
|---|---|---|---|
| SWARM-01 | Batang bertumpuk horizontal per klaim, urut bobot | Membandingkan komposisi dukung, tolak, abstain pada banyak klaim sekaligus | LV10 lewat [VR] bagian 5.5; LV15 lewat [VR] bagian 5.4; LV7 lewat [VR] bagian 5.8 |
| SWARM-02 | Tangga empat simpul plus teks syarat gagal | Pertanyaannya jarak ke tindakan, jadi bentuknya posisi pada skala berurut | LV13 dan LV6 lewat [VR] bagian 3 Tabel A baris 1 |
| SWARM-03 | Satu batang cakupan dengan garis ambang, tujuh titik kehadiran | Dua besaran berbeda skala, jadi dipisah menjadi panel bersusun satu sumbu | LV8 lewat [VR] bagian 6 butir 1; LV7 lewat [VR] bagian 5.8 |
| SWARM-04 | Alur vertikal enam simpul dengan gerbang berlabel | Yang dibaca urutan pemeriksaan, dan kesalahan urutan paling mahal | Pilihan desain, batas LIN-01 dari [KAT] baris 2097; bentuk linimasa dari LV16 dan LV11 lewat [VR] bagian 5.10 |
| SWARM-05 | Tabel terurut tenggat dengan kolom umur | Pembaca mencari satu baris dan memeriksa tenggatnya | LV4 dan LV14 lewat [VR] bagian 5.3; [KAT] baris 2097 |

### 9.2 Visual yang ditolak untuk keluaran ini

| Visual | Alasan ditolak | Sumber |
|---|---|---|
| Donat atau cincin untuk komposisi suara | Sudut dan luas tidak diproses secepat panjang dan posisi, dan sembilan klaim tidak muat dalam satu cincin | LV7 lewat [VR] bagian 6 |
| Gauge atau dial untuk S | Besaran kuantitatif tidak boleh dibaca dari sudut | LV7 lewat [VR] bagian 6 |
| Satu angka gabungan "skor dewan" | Menyatukan tujuh engine menjadi satu keyakinan dilarang [DSS1] bagian 3.5, dan menyembunyikan ketidaksepakatan dilarang LV15 | [DSS1], [VR] bagian 5.4 |
| Dua sumbu Y pada panel dukungan dan beban | Skala kedua sewenang-wenang dan mudah salah baca | LV8 lewat [VR] bagian 6 |
| Diagram alir untuk riwayat keputusan | Pembaca mencari baris tertentu, bukan alur | [KAT] baris 2097, LV4, LV14 |
| Warna merah tanpa label untuk TK-4 | Warna tanpa teks tidak terbaca oleh sebagian pembaca, dan [KAT] baris 203 sampai 206 melarang warna merah tanpa label manusia-peninjau | [KAT] baris 203 sampai 206 |

### 9.3 Keputusan yang menutup satu butir terbuka riset visualisasi

[VR] bagian 8 mencatat satu keputusan pemilik produk yang belum diambil: konsensus dihitung dari putusan kepala, atau dari suara manusia. Butir itu berbunyi bahwa bila memilih jalur putusan kepala, data yang dibutuhkan sudah ada di keluaran engine, sedangkan jalur suara manusia memerlukan kanal pengumpulan pendapat baru.

Berkas ini memilih jalur putusan kepala dan klaim. Tiga alasan yang bisa diperiksa:

1. Data jalur itu sudah ada hari ini: [JSON] memuat 27 kepala dengan tier, lapisan, dan metrik, dan bobotnya sudah ditetapkan [DSS1] bagian 3.2. Jalur suara manusia belum punya satu berkas pun.
2. Kerangka wajib butir 1 menetapkan manusia sebagai pemutus, bukan sebagai pemberi suara. Menjadikan manusia pemberi suara akan mengubah alat ini menjadi jajak pendapat, dan itu bukan yang diminta kartu.
3. Jalur suara manusia sudah punya rumah lain di LIN-01, yaitu log keputusan. Di sana suara manusia dicatat sebagai keputusan atas satu peringatan, bukan sebagai suara sejajar dengan mesin.

Konsekuensi yang harus dicatat: konsensus jenis ini mengukur kesepakatan antar mesin, dan tidak mengukur kesepakatan antar orang. Bila kelak dibutuhkan konsensus lintas disiplin (misalnya geologi, pemboran, dan operasi), itu fitur baru di rumpun kepercayaan dengan kanal pengumpulan sendiri, dan tidak boleh menumpang pada panel SWARM-01.

## 10. Salah tafsir yang harus dicegah

| # | Salah tafsir | Kenapa salah | Yang harus tercetak |
|---:|---|---|---|
| 1 | "ssi menolak dengan yakin" | Tiga dari empat kepalanya bisu, dan kanal CRPM tidak tersedia pada 96,57 persen jendela | Label "sebagian bisu 3 dari 4 kepala" dan kode AB-5 |
| 2 | "S 18,23 persen berarti peluang kegagalan 18 persen" | S adalah pangsa bobot, bukan peluang terkalibrasi; tidak ada satuan peluang | Teks "pangsa bobot dukung", tanpa tanda persen peluang |
| 3 | "TK-2 berarti aman" | TK-2 berarti ada klaim P2 yang belum cukup untuk antrean | Nama tingkat dan syarat yang gagal |
| 4 | "Dua klaim P3 cukup untuk TK-3" | Butuh S 0,40 juga, dan dua klaim ringan hanya menghasilkan 33,69 persen | Tabel kombinasi bagian 7.4 |
| 5 | "Kepala hibrida adalah bukti kedua" | Untuk empat pasangan, hibrida identik dengan rule | Nama kepala yang dideduplikasi |
| 6 | "FAR 4,10 berarti klaim lolos gate" | Angka itu dari populasi lintas fold, sedangkan segmen ini 16,611 | Dua angka dengan label populasi (K-7) |
| 7 | "Nilai 0,4950 adalah skor mentah" | Itu batas atas bukti kelas vib, bukan skor | Label "dipotong batas atas" berdampingan |
| 8 | "Bobot dewan bengkel bisa dijumlahkan dengan rig" | Satuannya beda: jendela 1 detik lawan 60 detik, FAR per menit lawan per 24 jam | Dua dewan terpisah, tanpa total gabungan |
| 9 | "Buku konflik kosong berarti tidak ada masalah" | Kosong bisa berarti tidak ada rem yang aktif | Alasan kosong wajib tercetak |
| 10 | "Tingkat bisa dinaikkan dengan menurunkan ambang" | Ambang adalah keputusan protokol | Nomor versi protokol pada setiap panel |

## 11. Cara menguji seluruh keluaran

| # | Uji | Cara | Hasil yang diharapkan |
|---:|---|---|---|
| 1 | Konvensi hitungan | Perintah bagian 2.2 | 24 kepala OK, 0 mismatch |
| 2 | Jumlah engine dan kepala | Perintah bagian 2.2 | 7 engine, 27 kepala, lapisan 5 11 9 2 |
| 3 | Bobot dewan rig | Perintah bagian 2.3 | 9,15 versi A dan 11,30 versi B |
| 4 | Deduplikasi | Bandingkan bobot vib dengan dan tanpa aturan K-1 | Selisih tepat 1,00, yaitu bobot hibrida |
| 5 | Kepala bisu | Periksa empat kepala dengan `n_aktif` 0 | Semua memakai AB-5, tidak satu pun V-2 |
| 6 | Siklus segmen | Langkah 7 sampai 9 bagian 7.1 | S 18,23 persen dan tingkat TK-2 |
| 7 | Konflik K-3 | `hyd` indeks 0 | K 0,3030, pita P2, tingkat dibatasi TK-2 |
| 8 | Konflik K-4 | `stuck` indeks 0 | K 0,2857, pita P2 |
| 9 | Sepakat penuh dan potongan | `shk` indeks 20 | K mentah 1,0000 menjadi 0,5188, pita P3 |
| 10 | Kasus nilai hilang | `vib` indeks 429 | Kedua kemungkinan menghasilkan P3, jadi hasil tidak bergantung tebakan |
| 11 | Batas dominasi | Bagi 3,30 dengan 9,15 | 36,07 persen, melewati 35 persen, dan S berubah dari 18,03 ke 18,23 |
| 12 | Slot alarm otomatis | Baca [JSON] baris 1414, [PIPE] baris 300, dan asersi [PIPE] baris 738 | Ketiganya bernilai 0, dan asersinya lolos |
| 13 | Perilaku tanpa data | Setel semua klaim abstain | Tingkat TK-1 atau TK-2 dengan rem H-3, tanpa galat |

## 12. Syarat yang dibutuhkan agar tingkat di atas TK-2 bisa dipakai

| Kode | Yang belum ada | Syarat agar bisa dikerjakan | Pemilik |
|---|---|---|---|
| S-1 | Deret per menit per kepala, satu berkas dengan kolom engine, kepala, indeks menit, status, skor | Ekspor deret dari pipeline I1 dengan stempel waktu yang sama untuk semua engine, minimal kolom waktu, engine, head, status, skor | Integration Engineer |
| S-2 | Skema log keputusan untuk umur dan tenggat | Sepakati kolom waktu siklus, tingkat sebelum dan sesudah rem, pemutus, tenggat, keputusan, alasan | Product owner bersama pengawas |
| S-3 | Rekonsiliasi dua angka FAR pada `hyd` K-i | Satu paragraf keputusan: populasi mana yang dipakai untuk gate, dan angka mana yang tampil sebagai beban | Pemilik data evaluasi |
| S-4 | Keputusan bobot `persistence` 0,40 atau 0,80 | Satu baris keputusan pada [DSS1] bagian 3.2, lalu perbarui tabel bobot di berkas ini | Pemilik arsitektur |
| S-5 | Peta kode fitur SWARM-03 dan SWARM-04 di katalog | Sisipkan dua kode ke rumpun kepercayaan, dengan nomor baris saran penyajian | Penulis katalog |
| S-6 | Kalibrasi per well untuk klaim yang akan dipakai di TK-3 | Kalibrasi ambang lokal per sumur sesuai D-A4 [PM1] baris 129, lalu ulangi siklus | Algorithm Engineer |
| S-7 | Datun beban tinjauan per shift untuk klaim baru | Perluas [DSS2] bagian 2.2 dengan klaim yang belum punya kepala L1, termasuk bit_wear | Penulis antrean |

## 13. Yang belum diverifikasi di dokumen ini

1. Perhitungan pada tingkat segmen memakai `frac_aktif` sebagai pengganti `s_h` per jendela. Itu pendekatan yang dinyatakan terbuka, bukan hasil hitung per jendela. Akibatnya `K_segmen` tidak identik dengan `K_tampil` yang akan keluar pada satu jendela tertentu.
2. `K_max` per klaim dipinjam dari [DSS1] bagian 3.4, dan dua baris di sana memakai batas atas pinjaman dari baris kelas (stuck K-ii dan tool_wear K-ii). Bila batas itu dipisah per klaim, angka di bagian 5.3 bisa bergeser.
3. Bobot `canary_3rms` pada tingkat segmen memakai `frac_aktif` 0,6013, sedangkan [DSS1] bagian 3.1 menormalkan canary sebagai `min(1, z/3)`. Kedua bacaan tidak identik, dan bagian 7.1 menyebutkan bahwa yang dipakai adalah `frac_aktif`.
4. Angka FAR 4,10 pada `badge_far` `hyd.hybrid` dikutip dari [JSON], tetapi populasi sembilan fold yang disebut di medan itu tidak diperiksa ulang pada sesi ini. Yang diperiksa hanya bahwa medan itu ada dan bahwa `metrik_segmen` memuat 16,611 pada segmen F-14.
5. Pemakaian per shift belum dihitung karena tidak ada deret per menit. Semua angka beban di bagian 7.1 dikutip dari [DSS2] bagian 2.2, bukan dihitung ulang dari [JSON].
6. Tabel keputusan pada bagian 5.4 (pemutus dan batas waktu) adalah usulan protokol, bukan kebijakan yang sudah berlaku di lapangan. Sumbernya hanya [KAT] LIN-01 untuk kolom yang dicatat, dan batas waktu 1 jam untuk TK-4 adalah usulan berkas ini.
7. Kutipan [JSON] baris 1758 dan 1415 memuat tanda pisah panjang. Di berkas ini keduanya ditulis dengan koma. Isi kalimatnya tidak berubah, tetapi kutipan huruf demi huruf tidak dipertahankan.
8. Tidak ada model atau engine yang dijalankan pada sesi ini. Seluruh angka berasal dari berkas keluaran yang sudah ada, ditambah perhitungan `jq` dan `awk`.

## 14. Bukti pemeriksaan berkas ini sendiri

Bagian ini menutup rujukan "bagian 14" yang dipakai bagian 1 dan bagian 2.1. Semua keluaran di bawah adalah keluaran nyata pada sesi ini, ditempel apa adanya.

### 14.1 Ukuran berkas yang dibuka

```
$ stat -c '%s %n' scratch/v9_i1/v9_i1_RESULTS.json code/v9_i1_pipeline.py \
      planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md \
      docs/V9_PM1_ARCHITECTURE.md planning/03_SKOR_KEYAKINAN.md \
      planning/04_ANTREAN_TINJAUAN.md planning/05_KETIDAKSEPAKATAN.md
57555 scratch/v9_i1/v9_i1_RESULTS.json
44359 code/v9_i1_pipeline.py
166662 planning/01_KATALOG_FITUR.md
32141 planning/02_RISET_VISUALISASI.md
50456 docs/V9_PM1_ARCHITECTURE.md
66698 planning/03_SKOR_KEYAKINAN.md
95168 planning/04_ANTREAN_TINJAUAN.md
87228 planning/05_KETIDAKSEPAKATAN.md

$ wc -l scratch/v9_i1/v9_i1_RESULTS.json code/v9_i1_pipeline.py \
        planning/01_KATALOG_FITUR.md planning/02_RISET_VISUALISASI.md \
        docs/V9_PM1_ARCHITECTURE.md planning/03_SKOR_KEYAKINAN.md \
        planning/04_ANTREAN_TINJAUAN.md planning/05*.md
1758 scratch/v9_i1/v9_i1_RESULTS.json
 861 code/v9_i1_pipeline.py
2780 planning/01_KATALOG_FITUR.md
 335 planning/02_RISET_VISUALISASI.md
 528 docs/V9_PM1_ARCHITECTURE.md
1060 planning/03_SKOR_KEYAKINAN.md
1428 planning/04_ANTREAN_TINJAUAN.md
1247 planning/05_KETIDAKSEPAKATAN.md
```

Delapan angka byte dan delapan angka baris di tabel bagian 2.1 cocok dengan keluaran di atas, satu per satu.

### 14.2 Jumlah engine, kepala, dan sebaran lapisan

```
$ jq -r '.engines[] | "\(.engine) \(.heads|length)"' scratch/v9_i1/v9_i1_RESULTS.json \
  | awk '{print; h+=$2; e++} END{print "engines="e" heads="h}'
vib 4
ssi 4
shk 4
stuck 6
hyd 4
bit_wear 2
tool_wear 3
engines=7 heads=27

$ jq -r '[.engines[].heads[].layer] | group_by(.) | .[] | "\(.[0]) \(length)"' scratch/v9_i1/v9_i1_RESULTS.json
L0 5
L1 11
L2 9
L3 2

$ jq -r '[.engines[] | .engine as $e | .heads[] | "\($e)|\(.klaim // "NULL")"] | unique | length' scratch/v9_i1/v9_i1_RESULTS.json
11
```

Lima ditambah sebelas ditambah sembilan ditambah dua sama dengan dua puluh tujuh. Angka sebelas adalah jumlah pasangan engine dan kelas, dan tiga engine (`vib`, `ssi`, `shk`) memakai kelas kosong karena hanya punya satu kelas.

### 14.3 Konvensi `n_aktif = tp + fp`

```
$ jq -r '.engines[] | .engine as $e | .heads[] | select(.metrik_segmen != null)
       | [.n_aktif, (.metrik_segmen.tp + .metrik_segmen.fp),
          (if .n_aktif == (.metrik_segmen.tp + .metrik_segmen.fp) then "OK" else "MISMATCH" end)] | @tsv' \
  scratch/v9_i1/v9_i1_RESULTS.json | awk -F'\t' '{c[$3]++} END{for(k in c) print k"="c[k]}'
OK=24
```

Dua puluh empat kepala bermetrik, nol ketidakcocokan. Tiga kepala tidak masuk hitungan ini karena `metrik_segmen` bernilai kosong, yaitu `hyd.k2_tidak_tersedia`, `bit_wear.k2_onset_belum` (keduanya jendela nol), dan `tool_wear.canary_3rms` yang hanya punya ringkasan dan tidak punya label.

### 14.4 Pemeriksaan gaya dan kelengkapan

Ukuran dan jumlah baris berkas ini dilaporkan pada komentar penyelesaian kartu, bukan ditulis di dalam berkas, karena menulis angkanya ke dalam berkas mengubah angkanya sendiri. Yang diperiksa di dalam berkas adalah hal yang tidak berubah oleh penyuntingan isi:

```
$ F=planning/06_SWARM_KONSENSUS.md
$ grep -oP '[\x{2014}\x{2013}]' $F | wc -l
0
$ grep -oicE 'tidak[ ]bisa' $F
0
$ grep -oicE 'tidak[ ]mungkin' $F
0
$ grep -oicE 'terbat[a]s' $F
0
$ grep -c '^|' $F
221
$ awk '/^\|/{if(!t){t=1;n++}} !/^\|/{t=0} END{print n+0}' $F
28
$ find planning -maxdepth 1 -type f ! -name '*.md' | wc -l
0
```

Pola ditulis dengan kelas karakter, misalnya `terbat[a]s`, justru supaya perintah pemeriksa tidak memasukkan kata larangannya sendiri ke dalam berkas. Tanpa itu, pemeriksa menjadi hitungan palsu: kata yang dicari ikut muncul sebagai pola dan hasilnya tidak lagi nol.

Bacaan: dua ratus dua puluh satu baris berpipa dalam dua puluh delapan tabel, nol tanda pisah panjang, nol tanda pisah pendek, nol dari tiga kata larangan kerangka butir 6, dan nol berkas bukan markdown di `planning/`.

### 14.5 Yang tidak dijalankan

Tidak ada model, engine, atau pipeline yang dijalankan. Tidak ada berkas baru selain berkas ini. Program pada bagian 2.3 hanya membaca [JSON] dan mencetak ke layar; ia tidak menulis berkas apa pun. Karena itu seluruh angka di berkas ini dapat diperiksa ulang tanpa menjalankan ulang pelatihan, dan sekaligus berarti berkas ini tidak membuktikan bahwa engine bekerja pada data baru.



