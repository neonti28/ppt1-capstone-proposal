# V1 · Auditor independen

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
11. Header dan sidebar mengadopsi `D:\Download\Magang Halliburton\DESIGN.md`, tetapi tombol dan card mengikuti riset `planning/DESIGN.md`, bukan copy mentah.
12. Ada pola judul di luar card lalu deretan card horizontal yang bisa digeser, minimal pada "Daftar Kerusakan".
13. Setiap view disusun bertahap: layout dulu, lalu isi card. Tidak ada view yang hanya berisi satu card raksasa atau card kosong.

## Input tambahan
Baca juga `production/audit/R1_SOFTWARE.md` dan `production/audit/R2_SCI.md` bila sudah tersedia.

## Deliverable
Tulis `production/audit/V1_VERDICT.md`:
- Ringkasan verdict: LULUS / LULUS BERSYARAT / PERLU PERBAIKAN.
- Tabel defect: ID, tingkat (P0/P1/P2), file:line, bukti, dampak, saran perbaikan.
- Daftar hal yang belum dicek.
- Jangan mengedit file selain laporan ini.

KERANGKA WAJIB (sama untuk semua kartu):
- Bahasa keluaran: Indonesia, langsung, tanpa basa-basi.
- File md lama di docs/ dan planning/ tetap valid dan otoritatif. Jangan menulis ulang, meregenerasi, atau mengganti 16 file planning. Ambil isi dari sana.
- Referensi visual: `D:\Download\Magang Halliburton\DESIGN.md` untuk header, sidebar, palet, dan tipografi. Tombol serta pola card disesuaikan dengan riset di `planning/DESIGN.md`, bukan copy mentah.
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

