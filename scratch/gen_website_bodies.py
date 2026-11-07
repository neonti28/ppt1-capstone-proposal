from pathlib import Path

OUT = Path("/mnt/d/Capstone 1(v2)/scratch/website_bodies")
OUT.mkdir(parents=True, exist_ok=True)

KERANGKA = """KERANGKA WAJIB (sama untuk semua kartu):
- Bahasa keluaran: Indonesia, langsung, tanpa basa-basi.
- File md lama di docs/ dan planning/ tetap valid dan otoritatif. Jangan menulis ulang, meregenerasi, atau mengganti 16 file planning. Ambil isi dari sana.
- Referensi visual: `D:\\Download\\Magang Halliburton\\DESIGN.md` untuk header, sidebar, palet, dan tipografi. Tombol serta pola card disesuaikan dengan riset di `planning/DESIGN.md`, bukan copy mentah.
- Satu folder output: `/mnt/d/Capstone 1(v2)/production/`. Tidak boleh membuat website di folder lain.
- Urutan desain: kerangka layout dan susunan card dulu, baru isi tiap card maksimal. Tidak boleh ada card kosong atau ruang kosong yang tidak proporsional.
- Jika satu card tidak muat dalam satu layar, gunakan scroll horizontal atau vertikal di dalam card. Contoh pola: judul di luar card, misalnya "Daftar Kerusakan", lalu deretan card kerusakan disusun horizontal dan digeser ke kiri kanan.
- Baca skill antislop, antislop-ui, antislop-layoutmobile sebelum mengubah tampilan. Patuhi: tanpa gradien neon atau ungu, tanpa bento grid, tanpa glow halaman, tanpa shadow di semua kartu, tanpa pill di semua elemen, tanpa emoji dekoratif, tanpa logo/testimoni/delta palsu, tanpa gauge/donut/radar/dual-Y.
- Setiap angka yang ditulis atau diubah harus punya sumber file:line di docs/ atau planning/ atau scratch JSON. Kalau tidak ada sumber, tulis "BELUM KUTIP" dan jangan tampilkan sebagai fakta.
- Dilarang mengarang output, angka, path, status, atau klaim selesai. Verifikasi dengan tool output nyata.
- Jangan mengubah model atau provider. Jangan menyentuh board lain.
- Jangan memakai em dash sebagai penghubung klausa. Gunakan koma, titik dua, atau konjungsi.
- Sebelum selesai: jalankan `node --check` untuk setiap JS yang diubah, lalu tulis ringkasan bukti.
- Deliverable harus benar-benar ada di disk. Sertakan path absolut, ukuran byte, dan mtime.
"""

BODIES = {}

BODIES["w1_shell.md"] = f"""# W1 · Shell, header, sidebar, layout

Kamu adalah pekerja visual untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki shell website: `index.html` dan `css/styles.css` saja.
Jangan mengubah `js/data.js`, `js/views.js`, atau `js/app.js`.

## Target
1. Header dan sidebar mengikuti referensi `D:\\Download\\Magang Halliburton\\DESIGN.md` yang sudah diadopsi: topbar 64px, sidebar 212px, palet gelap Halliburton, Barlow Condensed untuk judul, Inter untuk body, JetBrains Mono untuk angka.
2. Tombol dan pola card tidak boleh copy mentah dari Halliburton. Sesuaikan dengan riset di `planning/DESIGN.md`: radius 4/6/8/10 sesuai peran, tinggi tombol konsisten, tidak semua elemen jadi pill.
3. Semua 10 tautan navigasi ada dan mengarah ke route yang benar: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.
4. Tidak ada overflow horizontal pada body di 1440px dan 390px. Tabel dan `.hscroll` boleh scroll sendiri, bukan body.
5. Tidak ada kartu kosong atau ruang kosong tidak proporsional. Jika satu kartu butuh tinggi, biarkan tumbuh; jangan memaksa semua kartu sama tinggi sampai isi terpotong.
6. Layout disusun bertahap: shell, grid, lalu card. Setiap card harus punya ruang untuk judul, isi, dan foot. Jangan menaruh card tanpa isi.
7. Jika satu card tidak muat satu layar, sediakan scroll di dalam card atau `.hscroll`, bukan memaksa mengecilkan teks.
8. Skip link, focus ring, dan urutan tab tetap benar.
9. Jangan menambah dekorasi yang tidak membawa informasi.

## Cara verifikasi
- Baca `index.html` dan `css/styles.css` penuh sebelum mengubah.
- Cek 10 href di sidebar dan `id` view yang dirujuk.
- Jika browser tool tersedia: buka `file:///mnt/d/Capstone%201(v2)/production/index.html`, ukur 1440x1000 dan 390x844, cari `document.body.scrollWidth > innerWidth + 2`, dan ambil screenshot.
- Jika browser tidak tersedia, lakukan pemeriksaan statis dan tulis keterbatasan itu di laporan.

## Deliverable
Tulis `production/audit/W1_SHELL.md` berisi: defect ditemukan, perubahan per file:line, ukuran sebelum/sesudah, hasil verifikasi, dan sisa masalah.
Jangan klaim "selesai" tanpa output verifikasi.

{KERANGKA}
"""

BODIES["w2_data.md"] = f"""# W2 · Data dan provenance

Kamu adalah pekerja data untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki `js/data.js` saja. Jangan mengubah `index.html`, `css/styles.css`, `js/views.js`, atau `js/app.js`.

## Sumber otoritatif
- `planning/04_ANTREAN_TINJAUAN.md` bagian 6.2: tabel 10 baris antrean, K_tampil, pita, menit, alasan, aksi.
- `planning/06_SWARM_KONSENSUS.md` bagian ringkasan per klaim: K_seg, cap, vote, bobot.
- `docs/RND_S6_PM_WAVE2.md`: bukti hyd H1p.
- `docs/RND_S2_ML_WAVE2.md` dan `docs/RND_S3_*` bila ada: bukti vib, ssi, bit_wear.
- `docs/RND_PROVENANCE_LEDGER.md`: ledger rujukan.

## Target
1. `focus` tepat 3 kartu: hyd K-i, vib, shk. Nilainya harus sama dengan `04` bagian 6.2: hyd 0,6100 P4 3 kepala 20 jendela lead 8,0 menit; vib 0,4950 P3 3 kepala 429 jendela tanpa lead; shk 0,5188 P3 3 kepala 20 jendela tanpa lead.
2. `queue` tepat 10 baris dari `04` bagian 6.2, bukan 12 baris rekaan. Tidak boleh ada nama sumur rekaan seperti F-15, F-12, F-10, F-9, F-7, atau Bengkel. Semua baris memakai `well: "F-14"` sebagai segmen, karena `04` menyatakan nama sumur per baris tidak tersedia.
3. `age` per baris tidak tersedia di `04`; gunakan `"—"` dan jangan mengarang umur jam. `minutes` harus 6,4,4,4,4,2,2,2,2,0 sesuai tabel.
4. `damages` tepat 11 kelas. Untuk kelas yang ada di `04`, `k` dan `pita` harus memakai K_tampil dan pita dari `04`, bukan K_seg dari `06`. `vote` dan `weight` tetap dari `06` dan harus diberi label sumber di komentar.
5. Hapus atau tandai `BELUM KUTIP` setiap angka yang tidak bisa dilacak. Jangan mempertahankan angka 0,58, 0,47, 0,51, atau 0,35 yang tidak ada di sumber.
6. Tambahkan komentar provenance di atas setiap blok: file sumber dan bagian.

## Verifikasi wajib
- `node --check js/data.js`.
- Hitung `focus.length === 3`, `queue.length === 10`, `damages.length === 11`.
- `rg -n 'F-15|F-12|F-10|F-9|F-7|Bengkel|0,58|0,47|0,51|0,35' js/data.js` dan jelaskan setiap sisa hit.
- Tulis `production/audit/W2_DATA.md` dengan tabel angka sebelum/sesudah dan sumber file:line.

{KERANGKA}
"""

BODIES["w3_views.md"] = f"""# W3 · Isi sepuluh tampilan

Kamu adalah pekerja konten untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki `js/views.js` saja. Jangan mengubah `js/data.js`, `js/app.js`, `index.html`, atau `css/styles.css`.

## Target
1. Sepuluh view harus terisi maksimal, bukan kerangka: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.
2. Setiap kartu harus punya judul, sub, isi, dan foot yang informatif. Tidak boleh ada kartu dengan body kosong atau teks kurang dari 40 karakter.
3. Gunakan data dari `window.DATA`, bukan angka hardcoded baru. Hitungan baris memakai `D.queue.length` dan `countBy(...)`.
4. Label antrean harus "Segmen", bukan "Sumur". Label keyakinan harus "K_tampil", bukan "K_segmen".
5. Jangan tampilkan nama sumur rekaan di antrean. Jika data tidak ada, tulis "belum dihitung" atau "BELUM KUTIP".
6. Semua angka yang tampil harus bisa dilacak ke `data.js` dan sumbernya. Jika ragu, tandai `BELUM KUTIP`.
7. Jangan memakai em dash sebagai penghubung klausa. Gunakan koma, titik dua, atau konjungsi.
8. Isi disusun bertahap: pertama kerangka card per view, lalu isi card satu per satu sampai penuh. Jangan mengisi satu card sampai penuh sementara card lain kosong.
9. Pola "Daftar Kerusakan": judul bagian di luar card, lalu deretan card kerusakan disusun horizontal di dalam `.hscroll`, bisa digeser kiri kanan. Setiap card punya nama, pita, K_tampil, bukti singkat, dan batas.
10. Jika isi satu card panjang, gunakan scroll vertikal di dalam card atau tabel yang bisa digeser. Jangan memotong teks sampai tidak terbaca.
11. Ruang kosong boleh ada asal proporsional. Jangan memaksa card pendek menjadi tinggi hanya untuk menyamakan baris.

## Verifikasi wajib
- `node --check js/views.js`.
- `rg -n '12 baris|K_segmen|"Sumur"|TODO|TBD|FIXME' js/views.js` harus bersih atau setiap sisa dijelaskan.
- Pastikan `window.VIEWS` berisi 10 kunci.
- Tulis `production/audit/W3_VIEWS.md` berisi daftar view, jumlah kartu, dan defect yang diperbaiki.

{KERANGKA}
"""

BODIES["w4_app.md"] = f"""# W4 · Interaksi, router, aksesibilitas

Kamu adalah pekerja interaksi untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki `js/app.js` saja. Jangan mengubah `js/data.js`, `js/views.js`, `index.html`, atau `css/styles.css`.

## Target
1. Router hash menangani 10 route: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.
2. Navigasi aktif tersinkron dengan hash. Judul topbar berubah sesuai route.
3. Modal: buka/tutup, Escape, focus trap Tab, dan kembalikan fokus ke pemicu.
4. Pencarian global: alias hyd, vib, shk, ssi, stuck, bit_wear, tool_wear, tk. Tekan "/" fokus ke search.
5. Tidak ada error console saat memuat 10 route.
6. Tombol dengan ikon harus punya nama aksesibel. SVG dekoratif harus `aria-hidden`.
7. Jangan menambah dependensi eksternal.

## Verifikasi wajib
- `node --check js/app.js`.
- Jika browser tersedia: buka `file:///mnt/d/Capstone%201(v2)/production/index.html`, klik 10 route, buka/tutup modal, uji Escape dan "/", catat error console.
- Jika browser tidak tersedia, lakukan audit statis dan tulis keterbatasan.
- Tulis `production/audit/W4_APP.md` dengan hasil per route dan defect yang diperbaiki.

{KERANGKA}
"""

BODIES["v1_audit.md"] = f"""# V1 · Auditor independen

Kamu adalah auditor independen. Kamu TIDAK boleh mengedit file produksi apa pun.

## Tugas
Audit website di `/mnt/d/Capstone 1(v2)/production/` terhadap permintaan operator dan aturan antislop. Baca file, jalankan verifikasi, dan tulis temuan. Jangan memperbaiki.

## Checklist
1. 10 route dapat dibuka dan menampilkan konten, bukan halaman kosong.
2. Header 64px dan sidebar 212px konsisten; tidak ada overflow body di 1440px dan 390px.
3. Tidak ada kartu kosong, teks terpotong, atau ruang kosong tidak proporsional.
4. Kontras teks minimal 4.5:1 untuk teks normal dan 3:1 untuk teks besar.
5. Tidak ada emoji dekoratif, gradien neon/ungu, bento grid, glow halaman, shadow di semua kartu, gauge/donut/radar/dual-Y.
6. Antrean memakai "Segmen", bukan "Sumur"; keyakinan memakai "K_tampil"; 10 baris; tidak ada nama sumur rekaan.
7. Angka kunci bisa dilacak ke `data.js` dan sumber di `docs/` atau `planning/`. Uji minimal 10 angka dengan grep.
8. Tidak ada `TODO`, `TBD`, `FIXME`, atau teks placeholder.
9. Tidak ada em dash sebagai penghubung klausa di teks yang tampil.
10. Tidak ada klaim "siap produksi" tanpa bukti.
11. Header dan sidebar mengadopsi `D:\\Download\\Magang Halliburton\\DESIGN.md`, tetapi tombol dan card mengikuti riset `planning/DESIGN.md`, bukan copy mentah.
12. Ada pola judul di luar card lalu deretan card horizontal yang bisa digeser, minimal pada "Daftar Kerusakan".
13. Setiap view disusun bertahap: layout dulu, lalu isi card. Tidak ada view yang hanya berisi satu card raksasa atau card kosong.

## Deliverable
Tulis `production/audit/V1_VERDICT.md`:
- Ringkasan verdict: LULUS / LULUS BERSYARAT / PERLU PERBAIKAN.
- Tabel defect: ID, tingkat (P0/P1/P2), file:line, bukti, dampak, saran perbaikan.
- Daftar hal yang belum dicek.
- Jangan mengedit file selain laporan ini.

{KERANGKA}
"""

BODIES["s1_final.md"] = f"""# S1 · Integrasi dan verdict akhir

Kamu adalah integrator terakhir. Kamu boleh mengedit semua file di `/mnt/d/Capstone 1(v2)/production/`, tetapi hanya untuk menutup defect dari `production/audit/V1_VERDICT.md`.

## Tugas
1. Baca `production/audit/V1_VERDICT.md`, `W1_SHELL.md`, `W2_DATA.md`, `W3_VIEWS.md`, dan `W4_APP.md`.
2. Tutup semua defect P0 dan P1. Untuk P2, perbaiki bila murah; jika tidak, catat alasan.
3. Jangan mengubah `docs/` atau `planning/`.
4. Jalankan verifikasi akhir: `node --check` untuk 3 file JS, buka 10 route, cek 1440px dan 390px, cek kontras, cek antrean 10 baris dan label "Segmen"/"K_tampil".
5. Cek khusus desain: header dan sidebar mengadopsi referensi Halliburton, tombol tidak copy mentah, ada pola card horizontal "Daftar Kerusakan", tidak ada card kosong, dan setiap view disusun layout dulu baru isi.
6. Tulis `production/REVIEW.md` berisi: verdict akhir, defect yang ditutup, bukti perbaikan, sisa masalah, dan daftar yang belum dicek.

## Aturan
- Jangan menutup defect dengan menghapus fitur atau mengosongkan kartu.
- Jangan mengarang hasil browser. Jika browser tidak tersedia, tulis keterbatasan.
- Jangan menyebut "siap produksi" jika masih ada P0/P1 terbuka.

{KERANGKA}
"""

for name, body in BODIES.items():
    (OUT / name).write_text(body, encoding="utf-8")
    print(name, len(body.encode("utf-8")))
