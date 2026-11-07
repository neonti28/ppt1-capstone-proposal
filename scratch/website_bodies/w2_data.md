# W2 · Data dan provenance

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

