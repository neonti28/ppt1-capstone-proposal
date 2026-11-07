# W1 · Shell, header, sidebar, layout

Status: selesai, dengan 3 sisa masalah di luar cakupan file (dicatat di bagian 6).
File yang diubah: `production/index.html`, `production/css/styles.css`.
File yang TIDAK disentuh: `js/data.js`, `js/views.js`, `js/app.js` (md5 tetap, lihat bagian 8).

`antislop active: during (session override).` Instruksi kartu memerintahkan membaca dan mematuhi
antislop, antislop-ui, antislop-layoutmobile sebelum mengubah tampilan, sehingga mode `during`.

---

## 1. Metode verifikasi

Browser sungguhan (Chromium via CDP), halaman dibuka sebagai
`file:///mnt/d/Capstone%201(v2)/production/index.html`.

Yang diukur, bukan dikira:
- `document.documentElement.scrollWidth` dan `document.body.scrollWidth` dibanding `window.innerWidth`
  pada 1440x1000, 1200x900, 1024x800, 390x844, 360x780, untuk 10 route.
- Pemindai elemen yang melewati tepi kanan, dengan pengecualian elemen yang induknya punya
  `overflow-x` bukan `visible` (tabel dan `.hscroll` memang boleh scroll sendiri).
- Ruang kosong di dalam `.card-body`: jarak antara anak terakhir dan dasar body, ambang 40px.
- Target sentuh: `getBoundingClientRect()` tiap kontrol shell, ambang 44x44.
- Focus ring: `Input.dispatchKeyEvent` Tab sungguhan, lalu `getComputedStyle().outlineStyle`.
- Kontras: rasio luminansi relatif dihitung di halaman dari warna terhitung, latar ditelusuri
  ke leluhur pertama yang punya `background-color` bukan transparan.
- Konsol: kolektor `error` dan `unhandledrejection` dipasang lewat
  `Page.addScriptToEvaluateOnNewDocument` sebelum skrip halaman berjalan.

---

## 2. Defect ditemukan

| # | Defect | Bukti terukur (sebelum) | Aturan |
|---|---|---|---|
| D1 | Sidebar hanya 7 tautan, bukan 10. `batas`, `kamus`, `alat-bantu` tidak ada di nav, hanya di footer | `document.querySelectorAll('#nav a').length` = 7. `window.VIEWS` = 10 route | Target kartu 2, R-24 |
| D2 | Overflow horizontal body di route `perencanaan` pada 390px. Penyebab: `.card-head .head-right { flex: 0 0 auto }` berisi `.seg` 4 tombol tidak bisa menyusut | `scrollWidth` 465 vs `innerWidth` 390 (lebih 75px). Pelaku: `div.head-right` w=379 right=465, `div#mode-seg.seg` w=379 right=465 | Target kartu 3, R-03 |
| D3 | Kartu dipaksa sama tinggi. `.grid { align-items: stretch }` + `.card-body { flex: 1 1 auto }` menaruh ruang mati di dalam kartu pendek | 20 kartu punya ruang kosong >40px di dalam body. Terburuk: `Tiga sumbu` (kamus) 472px, `Harga pemangkasan` (mesin) 243px, `Layer B: slot kosong` (batas) 221px, `Kalkulator beban` (perencanaan) 205px | Target kartu 4, R-05 |
| D4 | `.hscroll` juga memaksa kartu sama tinggi (flex default `stretch`) | Kartu `Yang tidak dijawab` (beranda, di dalam `.hscroll`) 111px ruang mati | Target kartu 4 |
| D5 | Focus ring hilang pada input. `.search input:focus` dan `.field ...:focus` memakai `outline: none` dengan spesifisitas (0,2,1), menimpa `:focus-visible` global (0,1,0) | Tab ke `#global-search`: `outlineStyle` = `none`, `outlineWidth` = `0px` | Target kartu 5, R-32 |
| D6 | Skip link hanya menggulir, fokus tidak pindah ke konten. `<main id="main">` tidak punya `tabindex` | Setelah Enter pada skip link: `document.activeElement` = `BODY` | Target kartu 5, R-32 |
| D7 | Target sentuh di bawah 44px pada 8 dari 10 kontrol shell terukur saat 390px | `.skip-link` 134x39, `.search input` 162x32, `#help-btn` 32x32, `.foot a` 48x15 / 50x15 / 32x15, `#state-select` 73x24, tombol banner 96x24 | R-03, antislop-layoutmobile |
| D8 | Placeholder pencarian terpotong di 390px | `Cari kartu, sumur, atau angka` = 166px, ruang teks 113px | Target kartu 4 (kualitas tampilan) |
| D9 | Bottom nav tidak menghormati safe area perangkat, `viewport` tanpa `viewport-fit=cover` | `meta[name=viewport]` = `width=device-width, initial-scale=1`. `env(safe-area-inset-bottom)` tidak akan pernah bukan nol | antislop-layoutmobile |
| D10 | Angka badge `Perencanaan` = 12 tidak cocok dengan data mana pun | `D.queue.length` = 10, `D.conflicts` = 12 (milik linimasa), `D.provenance` = 12 (milik bukti). Tidak ada array perencanaan berisi 12 | R-17, R-38 |

Angka badge lain diverifikasi dan cocok, jadi dipertahankan:

| Badge | Nilai | Sumber |
|---|---|---|
| Kepercayaan | 11 | `js/data.js:13` `claims: 11` |
| Perencanaan | 10 | `js/data.js:210` array `queue`, 10 entri (dihitung di browser) |
| Data | 6 | `js/data.js:246` array `channels`, 6 entri |
| Mesin | 7 | `js/data.js:12` `engines: 7` |
| Linimasa | 4 | `js/views.js:778` array `gates`, 4 entri |
| Bukti | 10 | `js/data.js:257` array `docs`, 10 entri |

Setiap badge sekarang membawa `title` dan `aria-label` yang menyebut satuannya, supaya angkanya
tidak lagi angka telanjang tanpa arti (sebelumnya pembaca layar mengucapkan "Kepercayaan11").

---

## 3. Perubahan per file:line

### `index.html`

| Baris akhir | Perubahan | Alasan |
|---|---|---|
| 5 | `viewport` ditambah `viewport-fit=cover` | Agar `env(safe-area-inset-bottom)` berfungsi di perangkat ber-home-indicator |
| 64 | `placeholder="Cari kartu"` + `title="Cari kartu, sumur, atau angka"` | Placeholder lama 166px tidak muat di ruang 113px (390px) dan 83px (360px). Teks lengkap tetap tersedia lewat `title` dan `aria-label` |
| 78, 84, 87, 90, 93 | `aria-label` + `title` berisi satuan angka badge | Angka badge diberi arti, bukan angka telanjang |
| 81 | `<span class="count">12</span>` menjadi `10`, plus `aria-label` dan `title` | D10, sumber `js/data.js:210` |
| 96-104 | Tiga tautan nav baru: `#batas` (ikon `i-alert`), `#kamus` (`i-book`), `#alat-bantu` (`i-wrench`) | D1, target kartu 2. Ikon memakai symbol SVG yang sudah ada, tidak menambah aset |
| 117 | `<main id="main" ... tabindex="-1">` | D6, agar skip link memindahkan fokus, bukan cuma menggulir |

### `css/styles.css`

| Baris akhir | Perubahan | Alasan |
|---|---|---|
| 390 | `.grid` `align-items: stretch` menjadi `start` | D3. Kartu tumbuh sesuai isi, tidak dipaksa setinggi kartu tertinggi |
| 427 | `.card-head` ditambah `flex-wrap: wrap` | D2. Kepala kartu boleh pecah baris alih-alih mendorong konten ke luar layar |
| 431 | `.card-head > div:first-child { min-width: 0; }` | D2. Judul boleh menyusut |
| 448-451 | `.card-head .head-right`: `flex: 0 0 auto` menjadi `0 1 auto`, tambah `min-width: 0`, `max-width: 100%`, `flex-wrap: wrap` | D2. Penyebab utama overflow, sebelumnya tidak boleh menyusut sama sekali |
| 591-593 | `.seg` ditambah `flex-wrap: wrap`, `min-width: 0`, `max-width: 100%` | D2. Empat tombol mode boleh pecah baris |
| 842 | `.hscroll` ditambah `align-items: flex-start` | D4 |
| 216-217 | `.search input:focus` tidak lagi `outline: none`; ditambah `.search input:focus-visible { outline: 2px solid var(--red-bright) }` | D5 |
| 977-981 | `.field input/select/textarea:focus` tidak lagi `outline: none`; ditambah aturan `:focus-visible` dengan outline 2px | D5 |
| 1241-1242 | `.sidebar` mobile: `height: calc(58px + env(safe-area-inset-bottom, 0px))` dan `padding-bottom` env | D9 |
| 1252, 1256, 1258 | `.nav` mobile: `justify-content: flex-start`, `overflow-x: auto`, `scrollbar-width: thin` + scrollbar 3px | 10 tautan tidak muat 390px sebagai baris statis. Nav jadi strip yang bisa digeser, bukan mengecilkan tiap target |
| 1262-1268 | `.skip-link` min-height 44, `.search input` height 44, `.topbar .icon-btn` 44x44 + `flex: 0 0 auto`, `.foot a` min-width 44 + center, `.foot a`/`.foot label` min-height 44, `.foot select` height 44, `.state-banner .btn` height 44 | D7 |
| 1278 | `.nav a` mobile: `flex: 1 1 0` menjadi `0 0 auto` + `min-width: 56px` | D7. Target 56x47, bukan 37px |
| 1285 | `.main` mobile: `padding-bottom: calc(72px + env(safe-area-inset-bottom, 0px))` | D9, konten tidak tertutup nav |

Tidak ada gradien, glow, shadow, pill, emoji, ikon dekoratif, atau elemen visual baru yang
ditambahkan. Perubahan hanya ukuran, pembungkusan, dan aksesibilitas.

---

## 4. Ukuran sebelum dan sesudah

| Ukuran | Sebelum | Sesudah |
|---|---|---|
| `index.html` | 12.208 byte | 13.084 byte |
| `css/styles.css` | 35.945 byte | 37.107 byte |
| Tautan nav | 7 | 10 |
| `scrollWidth` route `perencanaan` @390 | 465 (viewport 390, lebih 75) | 375 |
| Kartu dengan ruang kosong >40px di dalam body | 20 kartu | 0 kartu |
| Ruang kosong terburuk di dalam kartu | 472px (`Tiga sumbu`, kamus) | 0px |
| Kontrol shell di bawah 44px @390 | 8 dari 10 terukur | 0 dari 18 terukur |
| `outlineStyle` input saat Tab | `none` | `solid 2px` `rgb(252, 40, 45)` |
| Fokus setelah skip link | `BODY` | `MAIN#main` |
| Placeholder pencarian @390 | 166px teks di 113px ruang | 55px teks di 113px ruang |
| Topbar / sidebar @1440 | 64px / 212px | 64px / 212px (tidak berubah) |

Catatan `DESIGN.md`: `D:\Download\Magang Halliburton\DESIGN.md:72` menulis
`topbar-height: 70px` dan baris 103 menulis "tinggi sekitar 70px". Kartu ini menetapkan 64px
sebagai nilai yang diadopsi. Kode sudah 64px sejak awal, jadi tidak diubah. Perbedaan ini
dicatat, bukan diperbaiki diam-diam.

---

## 5. Hasil verifikasi

### 5.1 Sepuluh tautan nav mengarah ke route yang benar

`document.querySelectorAll('#nav a').length` = **10**. Semua `href` sama dengan `#` + `data-route`,
dan semua route ada di `window.VIEWS`.

Klik berurutan, hasil `document.querySelector('#view .view.active').id`:

```
beranda      -> view-beranda       mesin      -> view-mesin
kepercayaan  -> view-kepercayaan   linimasa   -> view-linimasa
perencanaan  -> view-perencanaan   bukti      -> view-bukti
data         -> view-data          batas      -> view-batas
kamus        -> view-kamus         alat-bantu -> view-alat-bantu
```

10 dari 10 cocok. Hash ikut berubah sesuai route.

### 5.2 Overflow horizontal

`document.documentElement.scrollWidth` dibanding `window.innerWidth` + 2, semua 10 route:

| Lebar | Route yang overflow |
|---|---|
| 1440x1000 | tidak ada |
| 1200x900 | tidak ada |
| 1024x800 | tidak ada |
| 390x844 | tidak ada |
| 360x780 | tidak ada |

Pemindai elemen melewati tepi kanan (mengabaikan yang induknya punya `overflow-x` sendiri)
pada 390x844 route `perencanaan`: **daftar kosong**.

Tabel dan `.hscroll` tetap scroll sendiri, sesuai izin kartu:
`.table-wrap` pada 390px `clientWidth` 323, `scrollWidth` 756, `overflowX` = `auto`.
Kartu `Antrean lengkap` `right` = 365 dengan `innerWidth` 390, border kanan 1px hadir.

### 5.3 Ruang kosong di dalam kartu

Ambang 40px, 10 route, @1440: **0 kartu**. Rincian per route: beranda 0, kepercayaan 0,
perencanaan 0, data 0, mesin 0, linimasa 0, bukti 0, batas 0, kamus 0, alat-bantu 0.

### 5.4 Target sentuh @390

18 kontrol shell diukur, **tidak ada yang di bawah 44x44**:

```
.skip-link 134x44 | .search input 162x44 | #help-btn 44x44
.foot a 48x44 / 50x44 / 44x44 | #state-select 73x44 | .foot label 65x44
#nav a 56x47 (10 tautan, semua)
```

Nav mobile: `scrollWidth` 595, `clientWidth` 375, tautan terakhir terjangkau setelah digeser
(`lastRight` 371 <= `navRight` 375).

### 5.5 Skip link, focus ring, urutan tab

Urutan Tab dari awal halaman, hasil `document.activeElement`, semua dengan
`outline: solid 2px`:

```
1 skip link  2 #global-search  3 #help-btn  4 beranda  5 kepercayaan  6 perencanaan
7 data  8 mesin  9 linimasa  10 bukti  11 batas  12 kamus  13 alat-bantu  14 tombol konten
```

Skip link: Tab pertama mendarat di "Lewati ke konten", `top` = 12 (terlihat setelah transisi
150ms), Enter memindahkan fokus ke `MAIN#main` dengan hash `#main`, Tab berikutnya langsung ke
tombol pertama di dalam konten (`Periksa`), melewati seluruh nav.

Focus ring input sekarang `solid 2px rgb(252, 40, 45)` (sebelumnya `none`).

### 5.6 Kontras teks shell (WCAG AA)

14 elemen diukur @1440, **14 PASS**, rasio terendah 4,55:1 (ambang 4,5:1 untuk teks normal):

```
.topbar-title h1 19px 14.98 PASS      .nav .count 10px 4.90 PASS
.topbar-title p 10.5px 4.55 PASS      .side-status .k 9.5px 4.79 PASS
.topbar-date span:first-child 11px 9.01 PASS   .side-status .note 10px 4.79 PASS
.topbar-date span:last-child 9.5px 4.55 PASS   .side-version 9px 4.95 PASS
.side-label 9.5px 4.95 PASS           .foot 10px 5.10 PASS
.nav a 12.5px 17.51 PASS              .foot a 10px 10.10 PASS
.search input 12px 13.56 PASS         .brand-text strong 18px 6.16 PASS
```

### 5.7 Konsol

Kolektor error dipasang sebelum skrip halaman. Setelah membuka dan berpindah ke 10 route:
`window.__errs` = `[]`. Tidak ada error dan tidak ada rejection.

### 5.8 Target kartu 1 (header dan sidebar mengikuti referensi)

| Ukuran | Terukur |
|---|---|
| Tinggi topbar @1440 | 64px |
| Lebar sidebar @1440 | 212px |
| Latar topbar | `rgb(22, 31, 45)` = `#161F2D` |
| Latar sidebar | `rgb(14, 23, 35)` = `#0E1723` |
| Latar body | `rgb(12, 19, 33)` = `#0C1321` |
| Barlow Condensed | `document.fonts.check` true, dipakai `h1` topbar dan judul view |
| Inter | `document.fonts.check` true, dipakai body |
| JetBrains Mono | `document.fonts.check` true, dipakai `.mono` dan `.num` |

Ketiga nilai warna cocok dengan `DESIGN.md` baris 10, 11, 12.

### 5.9 Regresi yang diperiksa

- `.card-head` tidak pecah baris tanpa perlu di 1440 dan 1200 (tidak ada kepala kartu >34px).
  Di 1024 ada 3 kepala kartu yang pecah baris (48px dan 64px, route kepercayaan dan mesin).
  Itu disengaja: lebar kartu di 1024 hanya sekitar 258px, dan sebelum perubahan isi kepala kartu
  dipaksa menyusut sampai kata terpanjang. Tidak ada overflow di 1024.
- Lebar `.head-right` di 1440 identik dengan sebelum perubahan (379x30 di perencanaan), jadi
  desktop tidak bergeser.
- `node --check` untuk `js/data.js`, `js/views.js`, `js/app.js`: ketiganya OK. Ketiga file tidak
  diubah, md5 tercatat di bagian 8.

---

## 6. Sisa masalah (di luar cakupan `index.html` dan `css/styles.css`)

1. **Kolom aksi tabel tidak terlihat di 390px tanpa petunjuk geser.** `.table-wrap` memang scroll
   sendiri (clientW 323 vs scrollW 756), jadi ini bukan overflow body. Tapi tidak ada penanda
   bahwa masih ada kolom di kanan, sehingga tombol "Tinjau" tidak ditemukan tanpa menggeser.
   Kelas `.scroll-hint` (`css/styles.css:854`) ada dan dipakai, tetapi hanya untuk baris
   `.hscroll` (`js/views.js:207` dan `js/views.js:293`), tidak untuk `.table-wrap`. Menambah
   petunjuk di tabel menyentuh `js/views.js`, jadi tidak dikerjakan di kartu ini.
2. **Isi statistik perencanaan tidak konsisten.** `js/views.js:405` menampilkan
   "Sisa anggaran 1.240 menit" dengan catatan "240 dikurangi 180 terpakai" (= 60). Ini konten di
   `js/views.js`, bukan shell. Tidak diubah.
3. **Jumlah baris vs badge status.** `js/views.js:411` menampilkan 3 badge (baru, ditinjau,
   ditunda) yang berjumlah 9 dari 10 baris. Baris ke-10 berstatus "Ditutup" dan tidak punya badge.
   Bukan cacat hitung, tetapi badge tidak menjelaskan baris ke-10. Konten `js/views.js`.

Catatan retraksi: pemeriksaan visual otomatis sempat melaporkan tiga hal yang dibatalkan oleh
pengukuran, jadi tidak dimasukkan sebagai defect:
(a) "ada overflow horizontal halaman 10-20px" dibatalkan, `scrollWidth` 375 <= `innerWidth` 390,
    scrollbar yang terlihat di dasar layar adalah scrollbar milik `.nav` (595 vs 375), bukan body;
(b) "border kanan kartu terpotong" dibatalkan, kartu `right` 365 dengan `innerWidth` 390 dan
    `borderRightWidth` 1px;
(c) "teks tumpang tindih di kartu TK-2" dibatalkan, 4 sel `.tk-metrics` tidak bertumpuk
    (`overlaps` = 0, `bannerScrollWidth` 351 = `clientWidth` 351);
(d) klaim awal laporan ini bahwa `.scroll-hint` "belum dipakai satu kali pun" dibatalkan oleh
    `grep`, kelas itu dipakai di `js/views.js:207` dan `js/views.js:293` untuk baris `.hscroll`.
    Yang benar: petunjuk geser belum ada untuk `.table-wrap`.

---

## 7. Delivery Gate (antislop)

Block 1 Hard Gate, semua jawaban "tidak":
- Em dash di `index.html` dan `css/styles.css`: 0 (`grep -c`), R-02 PASS.
- Overflow horizontal mobile: tidak ada di 390 dan 360, R-03 PASS.
- Statistik tanpa sumber: badge nav diverifikasi ke `js/data.js` dan `js/views.js` (bagian 2), R-17 PASS.
- Testimoni fiktif: tidak ada, R-18 PASS.
- Aset tanpa instruksi: tidak ada aset baru, ikon memakai symbol SVG yang sudah ada, R-23 PASS.
- Tautan nav ke halaman tidak ada: 10 dari 10 route ada di `window.VIEWS`, R-24 PASS.
- Kontras di bawah AA: 14 dari 14 PASS, terendah 4,55:1, R-25 PASS.
- Kontrol mati: tidak ada yang ditambahkan; semua tautan dan tombol sudah punya perilaku, R-26 PASS.
- Keadaan kosong/memuat/galat: sudah ada (`body[data-state]`, `#state-banner`), diuji lewat
  `#state-select`, banner tampil 355x70 tanpa overflow, R-27 PASS.
- FAQ generik: tidak ada FAQ di shell, R-28 PASS.
- Tidak bisa keyboard: Tab mencapai 13 elemen shell berurutan dengan outline 2px, R-32 PASS.
- Patch lewat skrip: perubahan ditulis langsung di `index.html` dan `css/styles.css`, R-33 PASS.
- Tema rusak: hanya satu tema gelap yang dikirim, tidak ada toggle, R-34 tidak berlaku.
- Dikirim tanpa dijalankan: dijalankan di browser, 10 route diklik, 0 error konsol, R-35 PASS.
- Klaim keamanan/kinerja palsu: tidak ada, R-36 PASS.
- Dibangun tanpa arah: arah dari `DESIGN.md` Halliburton, R-37 PASS.
- Konten fabrikasi: tidak ada teks baru selain `title` dan `aria-label` yang menyebut satuan angka
  nyata, R-38 PASS.

Block 2 Purpose-Gate: tidak ada teknik baru. Gradien, glow, shadow, radius, badge, ikon tidak
ditambah dan tidak diubah alasannya. PASS.

Block 3 Liveliness: dial tidak diubah oleh kartu ini karena ini perbaikan shell, bukan arah visual
baru. Focal point tiap layar tetap judul view + strip statistik. Aksen tetap merah brand saja.
PASS untuk lingkup perbaikan.

Block 4 Craftsmanship: C-1 sampai C-5 PASS. R-05 PASS (ritme bagian tidak diubah). R-11 PASS
(radius tidak diubah). R-15 PASS (tidak ada CTA baru). R-16 PASS. R-20 PASS. R-21 PASS.
R-29 PASS (palet tidak berubah). R-30 PASS. R-31 PASS.

---

## 8. Bukti di disk

Deliverable ini:
- `/mnt/d/Capstone 1(v2)/production/audit/W1_SHELL.md`
  (ukuran byte dan mtime final file ini dicatat di metadata handoff kanban, karena menulis
  angkanya di dalam file ini akan mengubah angkanya sendiri)

Tangkapan layar:
- `/mnt/d/Capstone 1(v2)/production/audit/W1_1440_beranda.png` 227.563 byte, mtime 2026-11-01 07:39
- `/mnt/d/Capstone 1(v2)/production/audit/W1_1440_perencanaan.png` 218.421 byte, mtime 2026-11-01 07:39
- `/mnt/d/Capstone 1(v2)/production/audit/W1_390_beranda.png` 77.533 byte, mtime 2026-11-01 07:39
- `/mnt/d/Capstone 1(v2)/production/audit/W1_390_perencanaan.png` 67.027 byte, mtime 2026-11-01 07:39

File yang diubah:
- `/mnt/d/Capstone 1(v2)/production/index.html` 13.084 byte, mtime 2026-11-01 07:39
- `/mnt/d/Capstone 1(v2)/production/css/styles.css` 37.107 byte, mtime 2026-11-01 07:39

File yang tidak diubah, md5:
```
8d07190d72dacc0ac61f18a81b488662  js/app.js
abb57cfa2f364abc2d547f9bd8d3be84  js/data.js
8c660e0b7c1084600227fda0236301d0  js/views.js
```
