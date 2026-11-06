# PROTOKOL RISET TIM — WAJIB (Neonti, 2026-10-06)

> Perintah operator: **"tim wajib pakai skill sci riset — R&D riset, ML Engineer skill ML; kalau ada masalah JANGAN langsung perbaiki: RISET SOLUSI DULU, baru perbaiki. Biar gak ngawur."**

## Aturan 1 — Riset dulu, perbaiki kemudian

Untuk SETIAP masalah/gagal/hasil aneh, urutan wajib:

```
MASALAH → RISET (baca skill sci + literature + diskusi hipotesis)
        → TULIS opsi solusi + bukti pendukung (di komentar kartu / dokumen)
        → PILIH opsi berbasis bukti (bukan tebakan pertama)
        → PERBAIKI / eksekusi
        → VERIFIKASI hasil
```

Dilarang: gagal → patch langsung → harap berhasil. Patch tanpa riset = "ngawur".
(Ini AMENDEMEN aturan `mem_muv4v0p1` — "gagal langsung perbaiki" tetap berlaku untuk
gangguan teknis mekanis/infrastruktur, TETAPI untuk masalah METODE/STATISTIK/ML/RISET:
riset dulu. Yang dimaksud user di sini: jangan asal perbaiki tanpa paham akar masalah.)

## Aturan 2 — Skill sci per tim (WAJIB dipakai, `skill_view(name=...)`)

| Tim | Skill wajib | Untuk apa |
|---|---|---|
| **R&D** | `literature-review`, `paper-lookup`, `research-lookup`, `scientific-critical-thinking`, `hypothesis-generation` | Kajian solusi, cari metode SOTA (mis. cara orang deteksi BHA failure dari time-series), bedah kelayakan metode sebelum dipakai |
| **ML Engineer** | `scikit-learn`, `statistical-analysis`, `experimental-design`, `statistical-power`, `shap` | Desain kampanye, pemilihan model/uji statistik, power analysis (apakah 467 pos cukup!), interpretasi fitur |
| **ML Auditor** | `scientific-critical-thinking`, `statistical-analysis`, `peer-review` | Audit klaim, grade bukti, cek metodologi |
| **Data QA / Data Eng** | `exploratory-data-analysis`, `uncertainty-and-units`, `polars` | Profil data, missingness/leakage audit, sanity check satuan |
| **PM** | `what-if-oracle`, `scientific-critical-thinking`, `consciousness-council` | Skenario verdict, uji asumsi gate, deliberasi keputusan |
| **Penulis / Bab** | `scientific-writing`, `markdown-mermaid-writing` | Laporan + diagram |

Skill lengkap kategori `sci` = 107 skill (`skills_list(category='sci')`). Tidak harus
semuanya — paling tidak 1 skill riset dari daftar timnya WAJIB dirujuk & disebut di
output (nama skill + poin yang dipakai), supaya bisa diaudit penggunaannya.

## Aturan 3 — Bukti pemakaian

Di setiap deliverable/dokumen/verdict, cantumkan baris:
`Riset pendahuluan: <nama_skill> — <1 baris poin yang dipakai>`
Kalau tidak ada riset pendahuluan → dianggap belum layak dikerjakan.

## Aturan 4 — Gate & angka TIDAK boleh berubah setelah hasil diketahui

Pra-registrasi tetap wajib untuk kampanye ML (seperti T2-e/T2-f). Riset = memahami
masalah & memilih metode SEBELUM eksekusi, bukan mengubah target SESUDAH melihat hasil.
