---
version: 0.3.0-alpha
name: Situs Keputusan Pemeliharaan Sumur
description: Dashboard pendukung keputusan berwarna gelap navy-black dengan aksen crimson. Setiap angka model tampil bersama pita keyakinan, batas kelas, dan badge FAR. Bentuk visual dipilih dari jenis data, bukan dari kisi kartu.
reference_canvas: 1536x1024
mobile_canvas: 375
theme: dark
colors:
  # Permukaan (diambil dari rujukan)
  bg-app: "#0C1321"
  bg-app-alt: "#0E1522"
  bg-sidebar: "#0E1723"
  bg-topbar: "#161F2D"
  bg-panel: "#111A29"
  bg-panel-alt: "#131E2B"
  bg-panel-inner: "#0F1824"
  bg-input: "#1D2739"
  bg-table-head: "#202B3A"
  border-panel: "#283342"
  border-subtle: "#192433"
  border-input: "#2F3D4C"
  grid-line: "#1E2838"
  # Merah brand (hanya aksen dan elemen interaktif utama)
  brand-red: "#E81725"
  brand-red-dark: "#A6091E"
  brand-red-deep: "#730516"
  red-bright: "#FC282D"
  red-soft: "#F0475C"
  red-tint-bg: "#5F1521"
  # Pita keyakinan P1 sampai P5. Selalu ditemani teks dan tekstur, tidak pernah warna saja.
  band-p1: "#3A4656"
  band-p2: "#6E7989"
  band-p3: "#FBB632"
  band-p4: "#F0475C"
  band-p5: "#E2142E"
  # Abstain: abu berpola garis miring, bukan merah
  abstain-fill: "#2A3442"
  abstain-stripe: "#3A4656"
  # Provenance angka (tiga warna label)
  prov-ok: "#30C97B"
  prov-note: "#FBB632"
  prov-block: "#AEB7C0"
  # Status kesiapan fitur
  ready-now: "#23B67C"
  ready-partial: "#FBB632"
  ready-draft: "#7C8797"
  # Teks
  text-primary: "#F1F4F5"
  text-secondary: "#B7C0CC"
  text-muted: "#7C8797"
  text-link: "#F0475C"
  # Grafik netral
  bar-neutral: "#6E7989"
  line-reference: "#E6EAF0"
  line-series-a: "#E2142E"
  line-series-b: "#B7C0CC"
  heat-low: "#16212F"
  heat-high: "#E2142E"
typography:
  font-family-display: "Barlow Condensed, Oswald, Arial Narrow, sans-serif"
  font-family-ui: "Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
  font-family-mono: "JetBrains Mono, Consolas, monospace"
  page-title: { size: 26px, weight: 800, tracking: 0.04em, transform: uppercase, family: display }
  page-question: { size: 15px, weight: 500, color: text-secondary }
  panel-title: { size: 15px, weight: 600 }
  stat-value: { size: 26px, weight: 600, numeric: tabular }
  stat-label: { size: 12px, weight: 400 }
  body: { size: 13px, weight: 400 }
  table-cell: { size: 12px, weight: 400, numeric: tabular }
  table-head: { size: 11px, weight: 500, color: text-muted }
  caption: { size: 11px, weight: 400 }
  axis: { size: 10px, weight: 400 }
  badge: { size: 10px, weight: 700, tracking: 0.06em, transform: uppercase }
  provenance-ref: { size: 10px, weight: 400, family: mono }
rounded:
  panel: 8px
  button: 6px
  badge: 4px
  input: 6px
  full: 9999px
spacing:
  base: 4px
  panel-padding: 14px
  grid-gap: 12px
  sidebar-width: 212px
  topbar-height: 64px
  footer-height: 40px
  row-height-table: 28px
grid:
  columns: 12
  breakpoints: { desktop: 1280px, tablet: 768px, mobile: 375px }
---

# Overview

Situs ini membantu insinyur pengeboran, supervisor, auditor, dan dosen penguji menjawab satu pertanyaan per halaman tentang klaim kerusakan alat bor: apa yang perlu dilihat, boleh dipercaya sejauh mana, dan apa yang dikerjakan shift ini. Sistem ini pendukung keputusan, bukan sistem alarm. Slot alarm otomatis bernilai 0 dan keputusan akhir selalu manusia, jadi tidak ada halaman notifikasi dan tidak ada tombol yang bertindak sendiri.

Nuansa visual mengikuti rujukan: industrial, gelap, presisi, satu aksen crimson, kepadatan informasi tinggi. Yang berubah adalah cara memilih bentuk. Rujukan memakai kisi kartu tetap, gauge, dan donat. Situs ini memilih bentuk dari jenis datanya (bagian "Pemilihan visual"), dan membuang bentuk yang terbukti menyesatkan untuk data ini (bagian "Penyimpangan dari rujukan").

Sumber isi: 48 fitur di katalog, enam rumpun (KEP, MNT, DAT, CMP, LIN, INS), sepuluh halaman PG-00 sampai PG-09, lima pita keyakinan P1 sampai P5, lima kode abstain AB-1 sampai AB-5, empat tingkat dewan TK-1 sampai TK-4. Angka pada dokumen ini adalah contoh dari berkas proyek. Implementasi wajib mengambil nilai dari data, bukan menyalin angka contoh.

# Prinsip yang mengikat desain

1. **Satu halaman, satu pertanyaan.** Judul halaman ditulis sebagai pertanyaan pembaca, misalnya "Boleh saya percaya angka ini, dan sejauh mana". Tidak ada halaman "semua angka".
2. **Angka tidak tampil sendirian.** Angka model selalu bersama pita keyakinan, batas kelas, dan badge FAR di blok yang sama.
3. **Bentuk mengikuti pertanyaan data.** Perbandingan besaran memakai panjang dan posisi. Urutan waktu memakai garis. Dua kategori silang memakai matriks. Daftar yang harus dibaca tepat memakai tabel.
4. **Kekurangan data adalah keadaan tampilan.** Data yang belum ada tampil sebagai label bertekstur dengan alasan dan pemilik data, bukan nol dan bukan area kosong.
5. **Warna tidak pernah membawa makna sendirian.** Setiap warna status selalu ditemani teks, dan pita ditemani tekstur. Layar harus tetap terbaca dalam skala abu.
6. **Tidak ada ruang kosong tanpa fungsi.** Aturan pengisian ada di bagian Layout.

# Penyimpangan dari rujukan

| Elemen rujukan | Diganti dengan | Alasan |
|---|---|---|
| Gauge ring "Model Confidence 92%" | Batang mendatar 0 sampai 1 dengan garis batas kelas, persen sebagai teks di ujung batang | Sudut dan luas bukan kanal cepat untuk besaran. Panjang dan posisi lebih akurat |
| Donut "Equipment Health" dan "Work Order Status" | Batang tersegmen horizontal bersumbu 0 sampai 100 persen, dengan jumlah di tiap segmen | Donat menyulitkan perbandingan antar segmen. Batang tersegmen menjaga total dan urutan |
| Satu angka besar sebagai pahlawan KPI | Sel stat dengan angka, satuan, selang atau pita, dan umur data | Angka tunggal tanpa sebaran terbaca sebagai kepastian |
| Warna hijau, kuning, merah sebagai Healthy, Monitor, High Risk | Pita P1 sampai P5 dengan label, dan abstain berpola abu | Keyakinan bukti bukan peluang kerusakan. Merah tanpa label peninjau manusia dilarang |
| Peta dunia aset | Tidak dipakai. Diganti matriks sumur lawan kanal atau berkas | Data proyek tidak berbasis lokasi geografis |
| Kartu KPI berderet seragam | Strip stat berpemisah garis tipis, bukan kartu | Kartu seragam memaksa isi berbeda ke ukuran sama dan menyisakan ruang kosong |
| Pill "HIGH RISK" | Lencana pita dengan nama pita ("Keyakinan kuat") | Istilah "risiko" dan "prioritas" untuk pita dilarang di layar |

Elemen rujukan yang dipertahankan: palet navy-black, aksen crimson, tipografi condensed untuk judul, radius 8px, border 1px, tabel rapat, dropdown kecil, sidebar kiri, topbar, dan footer tipis.

# Layout

## Kerangka global

| Zona | Isi |
|---|---|
| Topbar 64px | Wordmark situs di blok merah bersisi miring, judul "Situs Keputusan Pemeliharaan Sumur", tanggal potong data, kolom cari klaim, tombol bantuan |
| Sidebar 212px | Tujuh butir: Beranda, Kepercayaan, Perencanaan, Data, Mesin, Linimasa, Bukti. Aktif ditandai bar kiri 3px `red-bright` |
| Konten | Grid 12 kolom, jarak 12px, padding luar 14px |
| Footer 40px | Dua penanda tetap: "nol slot alarm otomatis" dan "keputusan akhir manusia". Tautan Kamus dan Batas data |

Halaman PG-06 Alat bantu, PG-08 Batas data, dan PG-09 Kamus dicapai dari kaki halaman dan tautan di dalam blok. Tidak ada butir menu kedelapan.

Logo: slot generik. Wordmark pihak ketiga tidak dipakai kecuali ada izin pemilik merek.

## Primitif tata letak

Bentuk wadah dipilih dari jenis isinya. Kartu bukan wadah bawaan.

| Primitif | Dipakai untuk | Ciri |
|---|---|---|
| **Strip stat** | 3 sampai 6 angka ringkas yang sejajar | Satu panel lebar penuh, sel dipisah garis vertikal tipis. Tiap sel: label, angka, satuan, penjelas pendek |
| **Panel grafik** | Satu grafik dengan sumbu dan legenda | Judul, kontrol di kanan atas, grafik mengisi sisa tinggi |
| **Tabel** | Daftar yang dibaca tepat, diurutkan, atau dicari | Header `bg-table-head`, baris 28px, kolom pertama berisi pengenal terbaca manusia, bukan ID otomatis |
| **Matriks** | Dua dimensi kategori, misalnya head lawan head atau sumur lawan kanal | Sel berisi angka dan warna, tidak warna saja |
| **Kartu entitas** | Satu klaim, satu kepala, satu sumur. Objek diskret yang punya badge sendiri | Hanya dipakai bila yang ditampilkan adalah sebuah benda, bukan sebuah angka |
| **Linimasa vertikal** | Urutan keputusan dan dokumen | Kolom waktu, aktor, keputusan, akibat |
| **Banner kondisi** | Satu baris keadaan sistem di puncak halaman | Tinggi satu baris, berisi tingkat dewan, kuorum, cakupan |

## Aturan pengisian ruang

1. Setiap baris grid wajib berjumlah 12 kolom. Blok disusun dengan lebar mengikuti isinya: tabel 8 sampai 12 kolom, grafik 4 sampai 8 kolom, strip stat 12 kolom, matriks sesuai jumlah kolom datanya.
2. Dalam satu baris, tinggi semua blok disamakan dengan menggabungkan blok yang kepadatannya mirip. Bila tinggi tidak sama, blok yang lebih pendek diisi catatan metode atau legenda yang memang diperlukan, bukan dibiarkan kosong.
3. Satu blok yang isinya tipis (kurang dari 3 baris data) digabung ke blok tetangga sebagai sub-bagian, bukan diberi panel sendiri.
4. Tidak ada panel yang hanya berisi satu angka besar. Angka tunggal masuk strip stat.
5. Kartu entitas tidak boleh dipaksa seragam tinggi bila isinya berbeda. Gunakan tata letak masonry dengan lebar kolom tetap dan tinggi menyesuaikan isi.
6. Tabel panjang tidak menggulir tanpa ujung. Tampilkan sepuluh baris pertama dan penghitung baris tunda.
7. Keadaan kosong tampil sebagai kalimat berarti ("tidak ada baris pada pita P2 ke atas, 5.455 jendela tenang"), bukan panel kosong.

## Responsif

Desktop 1280px memakai 12 kolom. Tablet 768px memakai 6 kolom. Ponsel 375px satu kolom: sidebar menjadi bar bawah, tabel menjadi daftar baris dengan kolom utama di atas, matriks menggulir horizontal di dalam wadahnya sendiri, strip stat menjadi dua kolom. Halaman tidak boleh menggulir ke samping.

# Pemilihan visual

Tabel ini adalah aturan utama. Bila data baru muncul, tentukan bentuknya dari tabel ini sebelum merancang panel.

| Jenis data | Bentuk | Yang dihindari | Alasan |
|---|---|---|---|
| Keyakinan satu klaim | Batang mendatar 0 sampai 1, garis batas kelas, persen di ujung batang | Gauge, donat, angka besar tunggal | Panjang dan posisi adalah kanal terbaik untuk besaran |
| Sebaran hasil yang mungkin | Titik kuantil (quantile dotplot), 20 titik yang bisa dihitung | Kurva density tanpa penjelasan | Pembaca menghitung titik untuk mendapat peluang. Variasi taksiran lebih kecil |
| Kalibrasi skor | Reliability diagram: titik per bin, garis diagonal acuan, jumlah sampel per bin sebagai strip batang di bawahnya | Skor tunggal seperti Brier | Skor tunggal mencampur kalibrasi, daya pisah, dan keacakan |
| Presisi lawan recall antar komposisi head | Scatter plot: tiap komposisi satu titik, selang sebagai garis di titik | Grafik batang dua seri | Dua ukuran saling menukar. Scatter menunjukkan pertukaran itu |
| Perbandingan model lawan baseline per fold | Tabel dengan dumbbell kecil sebaris: dua titik, selisih, vonis menang atau kalah | Batang ganda tanpa selisih | Jumlah fold kecil, jadi nilai tepat harus terbaca |
| Sebaran metrik antar fold atau sumur | Dot plot per fold bila n kecil, histogram atau density bila n besar, lebar bin dicoba lebih dari satu | Histogram satu lebar bin | Bentuk histogram bergantung lebar bin |
| Antrean kerja | Tabel terurut dengan kolom umur dan status, plus strip batang tersegmen untuk pita umur (0 sampai 15, 16 sampai 60, 61 sampai 120, di atas 120 menit) | Satu angka backlog, papan kanban sebagai tampilan utama | Sebaran umur lebih informatif dari jumlah terbuka |
| Beban tinjauan per shift | Batang mendatar per klaim, penanda p50 dan p95, garis vertikal kapasitas anggaran | Menjumlahkan rule dan hibrida | Setiap alarm hibrida juga alarm rule, jadi dihitung dua kali |
| Jam henti per sebab | Diagram Pareto: batang urut menurun plus garis persen kumulatif | Pie chart | Tujuannya memusatkan perhatian pada sebab terbesar |
| Tren keausan, getaran, MTBF | Garis dengan satu satuan di sumbu Y, sumbu waktu eksplisit, penanda kejadian | Dua sumbu Y, sumbu terpotong | Dua sumbu menyulitkan membaca dua seri sekaligus |
| Dua satuan harus berdampingan | Panel bersusun dengan sumbu X sama, atau keduanya diindeks ke 100 di awal | Dua sumbu Y | Lihat baris di atas |
| Kesepakatan antar head | Matriks head lawan head, angka di dalam sel, tombol "mentah" dan "ternormalisasi per baris" | Heatmap tanpa angka | Normalisasi diperlukan saat kelas tidak seimbang |
| Peta kalah-menang per kelas | Matriks kelas lawan pasangan model, sel berisi vonis dan selang | Radar | Sudut antar sumbu tidak sebanding |
| Kelengkapan kanal per sumur | Matriks sumur lawan kanal, sel berisi ikon status dan fraksi | Satu persen kelengkapan rata-rata | Rata-rata menyembunyikan kanal yang absen |
| Antrean parse (3.906 dari 7.150) | Batang progres tunggal, tersegmen: selesai dan belum | Donat | Sama dengan donat lain |
| Drift antar sumur | Heatmap sumur lawan kanal dengan angka selisih | Skor drift satu angka | Drift bersifat per kanal |
| Tingkat dewan TK-1 sampai TK-4 | Tangga empat anak tangga, yang aktif disorot, tiap anak tangga memuat syarat dan batas waktu | Lampu lalu lintas | TK bukan alarm |
| Kuorum dan cakupan bobot | Dua batang terpisah dengan garis ambang masing-masing | Satu skor gabungan | Dua angka mengukur hal berbeda |
| Batas dominasi satu klaim | Batang mendatar pangsa bobot, garis ambang 35 persen, penanda "sebelum" dan "sesudah" pemotongan | Pie chart | Pemotongan harus terlihat sebagai jarak |
| Posisi kelas pada tingkat kesiapan | Tangga tiga tingkat per kelas dengan penanda posisi dan daftar syarat naik | Skor tunggal armada | Kelas tidak sebanding |
| Urutan keputusan | Linimasa vertikal: waktu, aktor, keputusan, akibat | Diagram alir | Riwayat dibaca sebagai urutan waktu |
| Daftar angka dengan asal | Tabel rujukan: angka, nilai, satuan, berkas, baris, status TERUKUR atau TURUNAN, tanggal uji | Angka tanpa rujukan | Setiap angka harus bisa ditelusuri |

# Aturan tooltip dan penjelasan data

Setiap angka, badge, sumbu, dan istilah bertanda punya penjelasan yang bisa dibuka. Penjelasan harus menambah informasi, bukan mengulang apa yang sudah terlihat di layar.

## Larangan

1. Tooltip tidak boleh mengulang label dan nilai. Bila layar menulis "Keyakinan 98%", tooltip yang berbunyi "Keyakinan 98%" dihapus.
2. Tooltip tidak boleh berupa paragraf. Maksimum tiga baris berlabel, tiap baris satu kalimat.
3. Tooltip tidak boleh memuat kata kosong seperti "menampilkan data", "menunjukkan nilai".

## Format tiga baris

| Baris | Menjawab | Contoh isi |
|---|---|---|
| **Arti** | Apa yang diukur, dan apa yang tidak | Menggambarkan seberapa kuat bukti mendukung klaim ini pada jendela ini. Bukan peluang kerusakan |
| **Cara dihitung** | Bagaimana angka diperoleh, dengan satuan dan rujukan | Skor kepala yang dinilai digabung, lalu dipotong batas atas bukti kelas. Rumus: 03_SKOR_KEYAKINAN bagian 3 |
| **Cara membaca** | Arah baik atau buruk, ambang, atau jebakan tafsir | Makin besar makin kuat buktinya. Turun mendadak ke abstain berarti data hilang, bukan kondisi membaik |

Baris keempat opsional hanya bila ada batas data: **Batas**, misalnya "ECE belum diukur, jadi kurva ini rancangan".

## Contoh lengkap

Layar menampilkan: `hyd K-i  P4  61%`.

Tooltip pada "61%":

- **Arti:** Seberapa kuat bukti mendukung klaim kerusakan hidrolik pada jendela ini. Bukan peluang kerusakan.
- **Cara dihitung:** Skor tiga kepala yang dinilai digabung, lalu dipotong batas atas bukti kelas hyd K-i (0,61).
- **Cara membaca:** Makin besar makin kuat. Angka ini tertahan batas kelas, jadi menambah kepala yang menyala tidak menaikkannya.

Tooltip pada badge FAR "4,10 per 24 jam":

- **Arti:** Jumlah peringatan palsu yang dihasilkan komposisi ini dalam satu hari kalender.
- **Cara dihitung:** Alarm tanpa kejadian nyata dibagi jumlah hari kalender pada data uji. Satuan per 24 jam, bukan per menit.
- **Cara membaca:** Jangan dibandingkan dengan angka per menit atau per shift tanpa konversi.

## Kapan tooltip dipasang

| Elemen | Tooltip |
|---|---|
| Angka model (keyakinan, FAR, lead, ECE, recall) | Wajib, tiga baris |
| Badge dan lencana (pita, abstain, bisu, kembar, provenance) | Wajib. Isinya: syarat terpicu dan akibat pada tampilan |
| Header kolom tabel dan sumbu grafik | Wajib bila satuan atau cara hitung tidak jelas dari label |
| Sel matriks | Muncul saat diarahkan: dua nama yang dibandingkan, angka mentah, jumlah sampel |
| Titik pada grafik garis | Nilai tepat, waktu, dan penanda kejadian terdekat. Tanpa arti, karena arti ada di judul panel |
| Istilah di teks | Tautan ke Kamus (PG-09), bukan tooltip panjang |

Tooltip dapat dibuka dengan fokus keyboard, bukan hanya hover. Di ponsel dibuka dengan ketuk dan ditutup dengan ketuk di luar.

# Komponen

## Lencana pita keyakinan

Bentuk persegi panjang radius 4px berisi kode pita dan nama. Teks selalu ada. Tekstur berbeda per pita agar terbaca dalam skala abu.

| Pita | Rentang | Nama | Warna | Tekstur | Perilaku kartu |
|---|---|---|---|---|---|
| P1 | 0,00 sampai 0,19 | Tidak ada indikasi | `band-p1` | polos | Angka disembunyikan. Hanya nama pita dan jumlah kepala |
| P2 | 0,20 sampai 0,39 | Indikasi lemah | `band-p2` | titik jarang | Persen kecil, redup, alasan batas atas dibuka, tanpa tombol tindakan |
| P3 | 0,40 sampai 0,59 | Perlu tinjauan | `band-p3` | garis tipis | Persen sedang, badge FAR di sampingnya, tombol "Periksa" |
| P4 | 0,60 sampai 0,79 | Keyakinan kuat | `band-p4` | garis tebal | Persen besar, komponen S_A, S_B, S_C terbuka, tombol "Antrean kerja" dengan konfirmasi operator |
| P5 | 0,80 sampai 1,00 | Keyakinan tinggi | `band-p5` | kotak solid | Persen besar, label "syarat alarm terpenuhi", tombol "Eskalasi ke supervisor" |

Kartu L2 (tier TREN) hanya boleh menampilkan P1 sampai P3. Kartu L3 hanya boleh menampilkan abstain.

## Kartu keyakinan (kartu entitas)

Tiga zona dalam satu kartu:

1. Baris judul: nama klaim, jendela waktu, lencana pita.
2. Baris bukti: batang 0 sampai 1 dengan garis batas kelas dan persen di ujung, jumlah kepala dinilai, badge kalibrasi, badge FAR berikut satuan.
3. Baris alasan: S_A, S_B, S_C, lead dalam menit, tanggal rujukan batas kelas.

Urutan kartu: pita tertinggi dulu, lalu lead terkecil, lalu jendela terbaru. Kartu abstain di bawah dengan penanda "menunggu data".

## Kartu abstain

Abu `abstain-fill` dengan garis miring `abstain-stripe`. Angka diganti tanda pisah pendek. Teks alasan wajib. Tidak pernah merah. Tidak pernah masuk antrean kerja.

| Kode | Nama | Teks yang tampil |
|---|---|---|
| AB-1 | Tanpa kepala berskor | "Tidak dinilai: belum ada kepala berskor" dan daftar kepala menunggu |
| AB-2 | Data sensor kurang | "Tidak dinilai: kanal absen pada X persen jendela" dan tautan kartu kesiapan kanal |
| AB-3 | Skor jendela belum diekspor | "Tidak dinilai: skor jendela belum diekspor" dan pita ringkasan yang ada |
| AB-4 | Klaim lapis L3 | "Tidak dinilai menurut desain" dan alasan dari lapisan |
| AB-5 | Kepala bisu | Lencana "bisu", bukan penolakan |

## Lencana provenance

Tiga warna pada setiap angka yang bisa dikutip: hijau `prov-ok` boleh dikutip, kuning `prov-note` boleh dikutip dengan catatan metode, abu `prov-block` belum boleh dikutip. Angka bertanda abu tampil tanpa tombol salin rujukan.

## Badge FAR

Selalu berisi angka dan satuan tertulis ("4,10 per 24 jam kalender"). Bila satuan berbeda antar kepala, label satuan beda ditampilkan dan angka tidak dijumlahkan.

## Tangga tingkat dewan

Empat anak tangga: TK-1 TENANG, TK-2 PANTAU, TK-3 TINJAU, TK-4 ESKALASI. Yang aktif disorot dengan bar kiri `red-bright`. Tiap anak tangga menyebut syarat angka, pemutus manusia, dan batas waktu (TK-3 satu shift 8 jam, TK-4 satu jam). Tangga ini bukan alarm dan tidak mengirim pesan.

## Tabel antrean

Sembilan kolom terlihat: nomor, klaim, jendela, kepala, keyakinan, pita, umur, menit, aksi. FAR, lead, dan selang tampil di panel detail saat satu baris dibuka. Kolom keyakinan berisi batang mini ditambah persen, bukan persen saja. Aksi dengan dua tombol: "Tutup baris" (menulis log keputusan dan menghentikan umur) dan "Tunda" (wajib alasan).

## Dropdown, tombol, input

Dropdown tinggi 26px, radius 4px, latar `bg-input`, border `border-input`. Tombol primer: gradien horizontal `brand-red` ke `brand-red-dark`, tinggi 36px, radius 6px. Tombol sekunder: latar `bg-input`, border `border-input`. Tombol tindakan tidak dirender pada pita P1 dan P2.

## Ikon

Outline 1.5px, ujung membulat, 20px untuk navigasi, 24px untuk panel. Warna putih atau abu terang.

# Isi tiap halaman

Kolom "Bentuk" menetapkan visual. Kolom "Penjelasan" memuat isi tooltip dalam format Arti, Cara dihitung, Cara membaca yang diringkas.

## PG-00 Beranda hari ini

Pertanyaan: "Apa yang perlu saya lihat sekarang, dan seberapa kuat buktinya?"

| Blok | Bentuk | Isi | Penjelasan (ringkas) |
|---|---|---|---|
| Banner tingkat dewan | Banner kondisi, satu baris | TK aktif, dukungan berbobot (contoh 18,23 persen), kuorum (contoh 6 dari 7 engine), cakupan bobot, waktu hitung | TK-2 berarti bahan pantau, bukan antrean kerja. Dukungan dihitung setelah batas dominasi 35 persen |
| Tiga kartu fokus | Kartu entitas, maksimal tiga, masonry | Klaim, jendela, lencana pita, batang keyakinan, jumlah kepala, FAR, lead, umur | Keyakinan bukti, bukan peluang rusak. Tertahan batas kelas bila ada |
| Ringkasan beban shift | Strip stat 4 sel | Perkiraan baris per shift (contoh 40,15), p50, p95, sisa anggaran menit | Mengukur beban tinjauan, bukan risiko. Setelah deduplikasi rule dan hibrida |
| Antrean ringkas | Tabel 5 baris | Baris teratas dengan umur dan menit, tautan "Buka antrean shift" | Umur berhenti bertambah saat baris ditutup |
| Keadaan data | Baris lencana abstain | Jumlah klaim abstain, kode, alasan terpendek | Abstain berarti data masukan kurang, bukan kondisi rig membaik |
| Penanda tetap | Label tetap di kaki | Nol slot alarm otomatis, keputusan akhir manusia | Keputusan desain, bukan kegagalan |
| Kaki bukti | Teks kecil mono | Tanggal potong data, versi katalog, tautan PG-07 | |

Susunan baris: banner (12 kolom), tiga kartu fokus (12 kolom, masonry), strip stat (12 kolom), lalu antrean ringkas (8 kolom) berdampingan dengan keadaan data dan kaki bukti (4 kolom). Aksi utama: "Buka antrean shift" dan "Catat keputusan".

Keadaan tenang: banner TK-1, kartu fokus diganti satu kalimat "jendela tenang, tidak ada baris antrean baru" beserta jumlah jendela tenang.

## PG-01 Kepercayaan

Pertanyaan: "Boleh saya percaya angka ini, dan sejauh mana?"

| Blok | Bentuk | Isi | Penjelasan (ringkas) |
|---|---|---|---|
| Ringkasan papan vonis | Strip stat 6 sel | 27 kepala, 5 L0, 11 L1, 9 L2, 2 L3, 0 slot alarm otomatis | Lapis menunjukkan kesiapan pakai kepala, bukan mutu model |
| Papan vonis | Kartu entitas, 11 kartu urutan tetap | Nama kelas, tugas satu kalimat, lencana tier, dua sampai empat angka penopang, syarat menggantung, tanggal potong | Tier menilai kesiapan pakai. Dilarang dijumlahkan antar kelas |
| Kartu keyakinan | Kartu entitas | Lihat komponen Kartu keyakinan | Lihat contoh tooltip di atas |
| Batang keyakinan lawan batas kelas | Panel grafik, batang mendatar | Satu batang per klaim, garis batas kelas (contoh vib 0,4950, bit_wear 0,2525, hyd K-i 0,6100) | Batas kelas adalah plafon bukti. Sinyal kuat tetap tertahan bila bukti kelas tipis |
| Sebaran skor | Titik kuantil, 20 titik | Sebaran hasil pada jendela yang sama dengan angka keyakinan | Satu titik mewakili sekitar lima persen kemungkinan |
| Badge beban alarm | Badge pada kartu | Alarm per 24 jam kalender, satuan tertulis | Per 24 jam kalender, bukan per menit |
| Panel ketidaksepakatan | Panel per kejadian: putusan tiap kepala sejajar | Putusan tiap kepala pada jendela sama, daftar pasangan kembar | Perbedaan putusan adalah informasi, bukan gangguan |
| Kurva kalibrasi | Reliability diagram per engine | Titik per bin, diagonal acuan, jumlah bin, strip jumlah sampel | Penyimpangan dari diagonal berarti skor tidak boleh dibaca sebagai frekuensi. Label "rancangan" selama ECE belum diukur |
| Papan dua pembacaan | Tabel dua kolom (literal, ketat) plus kolom selisih dan sebab | Satu klaim, dua pembacaan | Selisih menunjukkan seberapa bergantung angka pada cara membaca |
| Gerbang provenance | Lencana tiga warna | Pada setiap angka | Lihat komponen provenance |
| Banner bit_wear | Banner kondisi tetap | Satu kalimat: label keausan bit adalah indeks mekanika, bukan observasi keausan | |
| Slot nilai lapisan B | Lima slot berlabel pemilik data | Tarif biaya henti yang belum diisi | Slot kosong adalah permintaan data, bukan angka nol |

## PG-02 Perencanaan maintenance

Pertanyaan: "Apa yang saya kerjakan shift ini, dan berapa menit tersedia?"

| Blok | Bentuk | Isi | Penjelasan (ringkas) |
|---|---|---|---|
| Banner anggaran | Strip stat 4 sel | Anggaran menit, terlayani, ditunda, total menit tunda | Jumlah tunda wajib tampil, bukan catatan kaki |
| Tabel antrean | Tabel 9 kolom | Lihat komponen Tabel antrean | Panjang daftar mengukur beban, bukan bahaya |
| Pita umur | Batang tersegmen satu baris | Empat pita umur per shift | Umur lebih informatif dari jumlah terbuka |
| Beban per shift per klaim | Batang mendatar dengan penanda p50, p95, garis anggaran | Lambda per klaim (contoh vib 16,647, hyd rule 18,523, hyd hibrida 5,537, shk 2,206, stuck 2,774) | Dihitung setelah deduplikasi. Beban vib yang benar 17, bukan 34 |
| Urutan berlapis dan neraca penundaan | Tabel kecil dua bagian | Empat lapis urutan, jatah minimum per klaim, baris tunda, menit kekurangan | Jatah minimum mencegah satu engine mengisi seluruh anggaran |
| Pareto jam henti | Panel grafik Pareto | Dari 39.397,986 jam tercatat: equipment failure 2.739,667, interruption other 2.680,917, waiting on weather 1.925,5, stuck equipment 212,0, circulation loss 195,0 | Garis kumulatif menunjukkan berapa sebab yang menanggung sebagian besar jam henti |
| Kalkulator pemeriksaan | Panel input dengan hasil langsung | Pemeriksaan manual yang dihemat per titik operasi, biaya waktu per pemeriksaan | Hasil memakai biaya waktu yang diisi pengguna |
| Sakelar titik operasi | Segmented control dua atau empat pilihan | Konsekuensi tiap titik operasi sudah dihitung | Bukan tombol global. Tiap pilihan memperlihatkan harga: alarm turun, presisi naik, recall turun |

Tiga keadaan antrean: kosong (kalimat dan jumlah jendela tenang), panjang (sepuluh baris pertama dan penghitung tunda), keyakinan rendah (baris redup tanpa tombol).

Susunan baris: banner 12 kolom; tabel antrean 8 kolom berdampingan dengan pita umur dan beban per klaim 4 kolom; Pareto 6 kolom berdampingan dengan kalkulator dan sakelar 6 kolom.

## PG-03 Kualitas data

Pertanyaan: "Apakah data yang menopang angka ini ada dan layak dipakai?"

| Blok | Bentuk | Isi | Penjelasan (ringkas) |
|---|---|---|---|
| Antrean parse | Strip stat 3 sel plus batang progres tersegmen | 3.906 belum diparse dari 7.150 (54,63 persen), 213 label terbuka | Label gugur belum tentu hilang, sebagian menunggu fold |
| Kartu kesiapan kanal | Matriks sumur lawan kanal, sel: siap, tipis, absen | Satu baris per sumur | Absen karena tidak logging berbeda dari sensor rusak |
| Matriks ketersediaan berkas | Matriks sumur lawan jenis berkas | Sel berisi jumlah dan status unduh | |
| Kartu kelengkapan jendela | Batang tersegmen per jendela | Fraksi kanal hadir pra-event dan vonis layak atau tidak | |
| Kanal tidak logging | Tabel daftar | Kanal absen karena sumur tidak logging, dengan sebab | Ditampilkan sebagai lencana "tidak logging", bukan nol |
| Peta label ke fold | Tabel dengan kolom alur: label, fold, atau alasan gugur | | |
| Pemilih kanal | Tabel dengan batang fill rate dan kolom QC fisik | Vonis pakai, pakai dengan catatan, tolak | Kanal setengah kosong tidak dipakai sebagai bukti fisik |
| Katalog label instrumen | Matriks sumur lawan label, angka jumlah event | | |
| Peta drift | Heatmap sumur lawan kanal | Selisih sebaran antar sumur dan dalam satu sumur | |
| Validitas kedalaman | Tabel dengan lencana valid atau tidak | Apakah fitur tekanan memakai kedalaman vertikal yang benar | |

Aksi: "Minta data" pada baris absen (membuka kartu permintaan data bertanda tangan) dan "Buka bukti kanal" (menuju PG-07).

## PG-04 Perbandingan mesin

Pertanyaan: "Mesin mana yang lebih baik, pada kelas apa, dan dengan harga apa?"

| Blok | Bentuk | Isi | Penjelasan (ringkas) |
|---|---|---|---|
| Balapan model lawan persistence | Tabel dengan dumbbell sebaris | Satu baris per fold, dua nilai, selisih, vonis | Persistence adalah baseline paling sederhana. Menang berarti melampaui tebakan tanpa model |
| Peta kalah-menang per kelas | Matriks kelas lawan pasangan model | Sel berisi vonis dan selang | |
| Panel kesetaraan head hyd | Scatter plot presisi lawan recall | Tiga komposisi head, selang pada titik, rekomendasi di samping | Presisi naik biasanya menukar recall. Titik yang jauh dari garis tukar adalah kandidat |
| Harga pemangkasan | Tabel dua baris dengan panah perubahan | hid: alarm turun 35,79 persen, presisi naik 0,2017, recall turun 0,1052. tool_wear: alarm turun 93,11 persen, recall turun 0,6666 | Recall selalu turun saat memangkas. Angkanya tertulis |
| Matriks kesepakatan komponen | Matriks head lawan head, toggle mentah dan ternormalisasi | Kesepakatan seluruh jendela 92,47 sampai 99,43 persen, pada kelas positif 23,81 persen untuk shk | Kesepakatan seluruh jendela didominasi jendela tenang. Lihat kolom kelas positif |
| Lencana pola konflik | Lencana pada sel dan kartu | Kembar, cakupan sebagian, saling meniadakan, bisu, masing-masing dengan alasan | Kembar tidak dihitung dua bukti. Bisu berarti diam, bukan menolak |
| Peta ketidaksepakatan tingkat klaim | Matriks 7 mesin lawan 11 klaim | Kolom yang paling sering tidak disepakati disorot | |
| Tabel kanal melawan intuisi | Tabel | Kanal yang tidak membantu dan angka pendukung | |
| Rekam jejak per sumur | Batang mendatar | Jumlah kejadian nyata per sumur | Jumlah kejadian adalah batas atas klaim |
| Bukti sirkularitas | Banner peringatan pada panel terkait | Target mekanika rekonstruksi tidak layak jadi bukti | |
| Lembar prasyarat eksperimen | Daftar periksa | Prasyarat sebelum menyimpulkan | |

Aksi: "Buka jendela" pada sel matriks (menampilkan putusan tiap kepala pada jendela sama) dan "Bandingkan komposisi".

## PG-05 Linimasa keputusan

Pertanyaan: "Apa yang diputuskan, kapan, oleh siapa, dan apa akibatnya?"

| Blok | Bentuk | Isi | Penjelasan (ringkas) |
|---|---|---|---|
| Tangga empat tingkat | Tangga TK-1 sampai TK-4 | Syarat, pemutus, batas waktu | Tidak ada tingkat yang mengirim pesan sendiri |
| Panel suara dewan | Matriks kepala lawan klaim, sel: dukung, tolak, abstain berkode | | Abstain berkode AB menjelaskan sebab diam |
| Meter kuorum | Dua batang dengan garis ambang | Kuorum hadir (ambang 4 dari 7) dan cakupan bobot (ambang 0,50) | Dua ukuran terpisah. Lolos satu belum tentu lolos dua |
| Batas dominasi | Batang pangsa bobot dengan garis 35 persen | Contoh pangsa hyd K-i 36,07 persen dipotong | Mencegah satu klaim menentukan tingkat dewan sendirian |
| Log keputusan | Tabel | Waktu, kepala, label tindakan, alasan, penghitung terbuka | Label "abaikan" adalah keputusan operator, bukan penilaian kebenaran model |
| Garis waktu gerbang | Linimasa vertikal | Urutan dokumen vonis, gerbang, perubahan target | |
| Register status dokumen | Tabel dengan lencana berlaku atau digantikan | | |
| Kalender sumber angka | Tabel tanggal uji terakhir dan hasil | | |
| Buku konflik | Tabel K-1 sampai K-7 dan H-1 sampai H-5 | Aturan konflik dan pemicu turunnya manusia | |
| Linimasa tier per kelas | Tangga tiga tingkat per kelas dengan syarat naik | | Tier kepala, pita klaim, dan tingkat dewan adalah tiga sumbu berbeda dengan pemutus berbeda |

Log kosong membedakan "belum ada keputusan tercatat" dari "tidak ada peringatan".

## PG-06 Alat bantu insinyur

Pertanyaan: "Langkah apa yang harus dijalankan sebelum memindahkan ambang atau mengutip angka?"

| Blok | Bentuk | Isi |
|---|---|---|
| Wizard kalibrasi dan uji jalan | Stepper vertikal, satu langkah aktif | Periksa drift, pilih titik operasi, uji jalan, catat hasil |
| Panduan skrip verifikasi | Blok kode dengan salin satu klik dan keluaran yang diharapkan | Prosedur memeriksa satu angka |
| Kartu kelayakan sinyal | Kartu entitas dengan vonis layak atau tidak | Sebelum VMD, EMD, atau wavelet |
| Kartu kanal yang perlu dipasang | Tabel dengan alasan angka dan prioritas | |
| Kartu permintaan data bertanda tangan | Formulir ringkas | Kanal, sumur, alasan angka, pemilik, tanda tangan |
| Daftar periksa mutu angka | Daftar periksa enam butir | Sumber, baris, satuan, selang, tanggal, alat |

## PG-07 Bukti angka

Pertanyaan: "Dari mana angka ini, dan boleh dikutip atau belum?"

| Blok | Bentuk | Isi |
|---|---|---|
| Tabel rujukan angka | Tabel, kolom pertama berisi nama angka terbaca manusia | Angka, nilai, satuan, berkas sumber, baris, status TERUKUR atau TURUNAN, tanggal uji |
| Lencana provenance | Lencana tiga warna | Pada tiap baris tabel |
| Pengunci rujukan dan uji mutasi | Tabel hasil uji dengan lencana lulus atau gagal | Baris rujukan benar berisi angka itu, dan pemeriksa terbukti bisa gagal |
| Papan satuan | Tabel pasangan satuan rawan tertukar | FAR per 24 jam kalender, FP per menit, tinjauan per shift |
| Daftar dokumen belum dibuka | Tabel | 119 dokumen di docs, 69 belum pernah dibuka, ditulis terbuka |
| Kaki berkas | Tabel kecil | Ukuran byte dan jumlah baris tiap berkas masukan |

## PG-08 Batas dan syarat data

Pertanyaan: "Apa yang belum ada, siapa pemiliknya, dan apa syaratnya?"

| Blok | Bentuk | Isi |
|---|---|---|
| Peta kode abstain | Tabel 5 baris | Kode, syarat terpicu, tampilan, satu contoh nyata per kode |
| Peta lapis L3 | Dua kartu entitas | Dua kepala L3, status, alasan tidak dinilai |
| Slot nilai lapisan B | Lima slot berlabel pemilik | Tarif biaya henti |
| Syarat per fitur | Tabel | Sepuluh butir syarat, cacat pemblokir C-01 sampai C-05 |
| Peta pemilik data | Tabel | Pemilik peta sumur, tarif biaya, identitas alat, kanal baru, deret per menit |
| Status per fitur | Batang tersegmen 3 warna | 32 siap sekarang, 15 siap sebagian, 1 rancangan |
| Larangan tampilan | Daftar dengan contoh salah dan benar | Sembilan visual yang dihindari |

## PG-09 Kamus dan kuis angka

Pertanyaan: "Istilah ini artinya apa, dan bagaimana angka ini diuji?"

| Blok | Bentuk | Isi |
|---|---|---|
| Kamus lima belas istilah | Daftar dengan pencarian | Tier kepala, lapisan, pita, kode abstain, tingkat TK, keyakinan bukti, FAR, lead, umur item, cakupan, kuorum, batas dominasi, ECE, kembar, bisu. Tiap entri: arti, cara dihitung, contoh baca benar dan salah |
| Peta tiga sumbu | Tabel 3 baris | Tier kepala, pita klaim, tingkat dewan beserta pemutusnya |
| Contoh baca angka | Dua kolom: dibaca benar, dibaca salah, dengan sebab salah | |
| Daftar istilah terlarang | Tabel istilah dan penggantinya | "Alarm" untuk tingkat dewan, "peluang rusak" untuk keyakinan bukti, "prioritas" untuk pita |
| Kuis dua halaman | Kuis pilihan ganda, sepuluh pertanyaan | Jawaban bisa diperiksa dengan batas tiap angka |

# Keadaan tampilan lintas halaman

Tidak ada halaman galat. Kekurangan data punya penampilan baku.

| Keadaan | Pemicu | Tampilan |
|---|---|---|
| Tenang | Tidak ada klaim di P2 ke atas | Banner TK-1, kalimat jumlah jendela tenang, tanpa tombol tindakan |
| Tanpa kepala berskor | Bobot klaim 0 | Kartu abstain AB-1 |
| Data sensor kurang | n_nodata per n_windows lebih dari 0,50 | Kartu abstain AB-2 dengan persen kanal absen |
| Skor jendela belum diekspor | Hanya ringkasan min, median, maks | Kartu abstain AB-3 dengan pita ringkasan |
| Klaim lapis L3 | Tier BELUM LAYAK PAKAI | Kartu abstain AB-4 tanpa pita |
| Kepala bisu | n_aktif 0 pada segmen | Lencana bisu AB-5 |
| Keyakinan rendah | P1 atau P2 | Kartu redup, tanpa tombol tindakan |
| Beban melebihi anggaran | Terlayani kurang dari masuk | Angka tunda dan menit kekurangan di banner |
| Konflik saling meniadakan | Dua kepala setara berbeda putusan | Dua pembacaan berdampingan, tingkat dibatasi TK-2 |
| Dua angka FAR | Satu kepala membawa dua populasi | Dua angka berdampingan dengan label populasi |
| Log kosong | Belum ada keputusan tercatat | Kalimat pembeda dari "tidak ada peringatan" |
| Angka belum boleh dikutip | Provenance kuning atau abu | Angka tampil dengan lencana, tanpa tombol salin rujukan |

# Warna dan gradien

- Latar utama: gradien vertikal sangat halus `bg-app-alt` ke `bg-app`.
- Merah brand: blok wordmark topbar (gradien 135deg `#9B0219` ke `brand-red-deep`, sisi kanan miring sekitar 15deg), tombol primer (gradien horizontal `brand-red` ke `brand-red-dark`), item sidebar aktif (`red-tint-bg` ke `#85262C` dengan bar kiri `red-bright`).
- Merah pita P4 dan P5 hanya muncul pada lencana dan batang yang berlabel teks.
- Heatmap: skala satu warna dari `heat-low` ke `heat-high`. Angka tetap tertulis di sel.
- Tidak ada gradien ungu, biru neon, atau efek kaca.

# Aturan pemakaian

1. Merah brand hanya untuk aksen utama dan elemen berlabel. Bukan latar besar.
2. Pita P1 sampai P5 dan abstain adalah satu-satunya sistem status keyakinan. Hijau, kuning, abu untuk provenance dan kesiapan fitur tidak boleh dipakai untuk keyakinan.
3. Teks utama putih, sekunder abu terang, pendukung abu muted. Kontras minimal 4.5:1 pada latar panel.
4. Semua panel radius 8px dan border 1px `border-panel`.
5. Angka memakai digit tabular dan satuan tertulis di sebelahnya. Format angka Indonesia: koma desimal, titik ribuan.
6. Persen keyakinan memakai label "keyakinan bukti", bukan "peluang".
7. Tanda pisah panjang dan pendek tidak dipakai di teks layar. Rentang ditulis "sampai".
8. Tombol hanya untuk tindakan manusia. Tidak ada tombol yang mengirim pesan, memicu alarm, atau mengubah ambang tanpa konfirmasi.
9. Setiap grafik: satu satuan per sumbu Y, sumbu batang mulai dari nol, judul menyebut satuan.

# Aksesibilitas

- Uji pada 375px dan skala abu. Pita dan status harus terbaca dari teks dan tekstur.
- Semua tooltip dan kartu terbuka dapat dijangkau keyboard. Fokus terlihat dengan ring 2px `red-soft`.
- Grafik punya tabel data setara yang dapat dibuka. Matriks mempunyai atribut baris dan kolom untuk pembaca layar.
- Jangan mengandalkan animasi. Hormati preferensi gerak berkurang.

# Daftar periksa sebelum merilis halaman

1. Pertanyaan halaman tertulis dan terjawab dalam satu layar pertama.
2. Setiap angka model punya pita, batas kelas, dan badge FAR di blok yang sama.
3. Tidak ada gauge, donat, radar, dua sumbu Y, atau satu angka besar tunggal.
4. Setiap bentuk visual cocok dengan tabel Pemilihan visual.
5. Setiap baris grid berjumlah 12 kolom dan tidak ada panel kosong.
6. Setiap tooltip memuat Arti dan Cara dihitung, dan tidak mengulang label.
7. Keadaan kosong, abstain, dan tenang sudah dirancang.
8. Setiap angka punya rujukan di PG-07 dan lencana provenance.
9. Tidak ada tombol tindakan pada P1, P2, dan abstain.
10. Pemeriksaan 375px dan skala abu lulus.
