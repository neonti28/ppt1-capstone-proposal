# V7-D1a — CEK DATA TUBULAR UNTUK SOLUSI R&D (192 file WITSML tubular XML)

Task: `t_5f46ecdc` [Pembaca 01] · Board: capstone-v7-solve · Tanggal: 2026-10-11 (WIB)
Spesifikasi cek: komentar kartu (Master V7-M1, `docs/V7_M1_DELEGASI.md` §2.1) — bit, stabilizer, rating motor.
Solusi dilayani: **S-A3** (LF3 differential sticking `F = μ·A·ΔP`), **S-B1/S-E1** (fitur pemisah shk/ssi/vib), **S-F1/S-D3** (identitas bit untuk kelas keausan).

> **Riset pendahuluan: `verification-mandatory`** — semua angka berasal dari skrip recount mandiri di workspace (`recount_tubular.py`, `followup_checks.py`, `bit_extra_checks.py`, `stab_blade.py`, `dir_coverage.py`, `raw_print_join.py`), BUKAN salinan angka D0. Recount independen: 192 file / 1.392 komponen / 62 tipe — COCOK dengan D0 §1/§4. Klaim D0 "rating motor 0/192" diuji ulang dengan grep sendiri (§3). Ketiadaan dibuktikan dengan ls per direktori, bukan asumsi (§5).
> **Riset pendahuluan: `scientific-critical-thinking`** — klaim "data ada" dipisahkan dari "klayakan": keberadaan kolom ≠ fitur siap pakai; tiap item diberi tes pembeda (mis. `posAxialWellbore` ternyata 0 → posisi aksial harus diturunkan, bukan diklaim langsung). Coverage lintas-sumur dihitung per fold, bukan dirata-rata (temuan coverage bit_wear §1.2).

Metode: parse ElementTree XML asli (namespace `http://www.witsml.org/schemas/1series`), sentinel WITSML `-999.25` dibuang ke null, semua jalur `data/volve/witsml_raw/*/*/tubular/*.xml`.

---

## 0. BUKTI FILE DIBUKA (acceptance a)

**Recount penuh:** `recount_tubular.py` → `[COUNT] tubular xml files = 192`, `parsed OK = 1392 components; parse_fail = 0`, `distinct typeTubularComp = 62`, `distinct nameWellbore = 16`.

**File dicetak utuh (raw):** `Norway-Statoil-NO 15_$47$_9-F-1 C/2/tubular/22.xml` (17.465 bytes, assembly `15/9-F-1 C_32RGUI47`, `nameWellbore = NO 15/9-F-1 C`, 19 komponen drilling). Elemen kunci yang terlihat langsung di raw:

```
<tubularComponent uid="321RGUI47"><typeTubularComp>bit PDC fixed cutter</typeTubularComp><sequence>1</sequence>
<od uom="m">0.444500000000649</od><len uom="m">0.5</len> … <vendor>Hughes Christensen</vendor>
<nameTag uid="…"><name>7902062</name><numberingScheme>serial number</numberingScheme></nameTag>  (×11)
<bitRecord uid="0.4445…"><diaBit uom="m">0.444500000000649</diaBit><typeBit>PDC</typeBit>
  <condInitDull>unknown</condInitDull><condFinalDull>unknown</condFinalDull></bitRecord>
<nozzle uid="72RGUI47"><diaNozzle uom="m">0.0095250000000381</diaNozzle><typeNozzle>normal</typeNozzle></nozzle> (×10)
```

Juga terlihat: `<stabilizer><shapeBlade>spiral</shapeBlade><typeBlade>unknown</typeBlade></stabilizer` pada komponen stabilizer/LWD.

---

## 1. TABEL UTAMA: solusi R&D | data needed | status | bukti | peluang proses

| # | Solusi | Data needed (dari domain TUBULAR) | Status | Bukti (kolom + baris non-null + path) | Peluang proses |
|---|---|---|---|---|---|
| 1a | **S-F1/S-D3** — identitas bit (tipe, ukuran) sebagai konteks kelas `bit_wear` | Komponen tipe bit: `typeTubularComp`, `od`, `len`, `diaBit`, `typeBit` | **ADA SETELAH DIOLAH** (butuh join + normalisasi nama wellbore; coverage fold terbatas — lihat §1.2) | **43** komponen bit-family di **10** `nameWellbore` (39 bit asli: PDC 24, insert roller cone 11, mill tooth roller cone 4; +4 `bit hole opener`). Non-null: `od` 43/43, `len` 43/43, `diaBit` 39/43 (4 hole opener tanpa bitRecord valid), `typeBit` 39/43. `diaBit == od` 39/39 (redundan). Path: semua `witsml_raw/*/tubular/*.xml` (daftar file per wellbore §1.1) | Join via field XML `nameWellbore` (16 nilai; folder ≠ wellbore — folder `F-1 C` berisi wellbore F-1 A/B/C/F-1). Normalisasi: `NO 15/9-F-14` ↔ label USROP `N-SH_F-14d` (kolom `well` di `USROP_labeled.csv` berisi nama file, perlu mapping). 40/43 bit berada di `sequence=1` (posisi dasar) → konteks "bit pada assembly ini" valid |
| 1b | **S-F1/S-D3** — pelengkap: nomor seri bit (identitas fisik lintas-run) | `bitRecord/nameTag/name` + `numberingScheme=serial number` | **ADA SETELAH DIOLAH** | **39** komponen bit membawa nameTag serial; **26 nilai serial unik**; serial berulang lintas file (top: `5221270` muncul di 80 nameTag, `7902062` 36×, `731825` 32×) | Satu bit fisik terpakai di banyak assembly/run → rantai pemakaian bit bisa direkonstruksi (kandidat fitur "akumulasi jam bit" untuk S-F1). Wajib dedup nameTag berulang per file sebelum dipakai |
| 1c | **S-F1/S-D3** — pelengkap: nozzle (JIT hydraulics) | `nozzle/diaNozzle`, `typeNozzle` | **ADA SETELAH DIOLAH** | **39/39** bit punya ≥1 elemen nozzle; contoh 10 nozzle pada file raw §0 (dia 9,5–12,7 mm) | Jumlah × diameter nozzle → total flow area; konteks hidrolik untuk filter "low_ROP karena nozzle" vs keausan (relevan S-C2/S-F1) |
| 1d | **S-F1/S-D3** — ANTI-KLAIM: grade dull bit | `condInitDull`/`condFinalDull` | **TIDAK ADA (isi `unknown`)** | Dari 39 bit: **38** pasang (`unknown`,`unknown`); **1** (`unknown`,`WT`) | Jangan berharap IADC dull-grade dari tubular — hanya 1 baris terisi |
| 2a | **S-B1/S-E1** — stabilizer (od, length, posisi axial) → fitur jarak stabilizer (prediktor stick-slip/whirl) | `typeTubularComp` stabilizer + `od` + `len` + urutan axial | **ADA SETELAH DIOLAH** (od/len langsung; posisi axial harus DITURUNKAN — `posAxialWellbore` kosong) | **75** komponen stabilizer (`stabilizer string` 66 + `stabilizer near bit` 9) di 12 `nameWellbore`. Non-null: `od` **75/75**, `len` **75/75**. **`posAxialWellbore` = 0/1392** (berlaku untuk SEMUA komponen — tidak ada satu pun file yang mengisinya; grep `posAxialWellbore`: 0 file). Sub-elemen blade: 125 `<stabilizer>` — `shapeBlade` spiral 41 / unknown 84; `typeBlade` integral 8 / unknown 117 | Posisi aksial = kumulatif `len` berurutan `sequence` dari bit (seq=1) ke atas. Feasibilitas diuji: **15 assembly** punya ≥2 stabilizer DENGAN rantai `len` lengkap → **30 pasang jarak stab-to-stab** bisa dihitung. Contoh hasil: `15/9-F-1_6RGUI47` 5 stab di [19.3, 21.0, 52.9, 54.1, 93.4] m dari bit → gap [1.7, 31.9, 1.2, 39.3] m. Assembly tanpa rantai len lengkap → posisi tidak dapat (dilaporkan, jangan diimprovisasi) |
| 2b | **S-B1/S-E1** — coverage stabilizer untuk 4 wellbore parse-baru (F-10/F-4/F-12/F-15) | jumlah stabilizer per wellbore target | **SEBAGIAN** | F-10: **0 komponen** (tidak ada file tubular sama sekali — §5); F-4: **0** stabilizer (hanya 2 drill pipe + 2 tubing); F-12: **4** stabilizer (50 komponen); F-15 C: **2** (51 komponen); F-15 D: **6** (235 komponen) | Fitur jarak stabilizer hanya tersedia untuk F-12 & F-15 dari 4 fold baru — jangan dijanjikan untuk F-10/F-4 |
| 3 | **S-A3 LF3** — differential sticking `F = μ·A·ΔP`: geometri kontak (A = π·d·L) dari drill collar & stabilizer | `drill collar` od/len; `stabilizer` od (gauge); `bit` dia (lubang bor) | **ADA SETELAH DIOLAH** (geometri kontak) · ΔP & μ **DI LUAR domain ini** (butuh tekanan pori dari 07 EDM / mud weight — bukan tugas D1a) | `drill collar`: **79** komponen, od non-null **79/79**, len non-null **79/79**, di 8 wellbore (F-1: 22, F-11: 14, F-11 T2: 13, F-15 D: 13, F-1 C: 6, F-11 B: 6, F-5: 3, F-12: 2). `stabilizer near bit`: 9 (gauge contact). `diaBit` 39 nilai nyata (0,14–0,66 m = ukuran lubang) | A_kontak collar per assembly = Σ π·od·len (collar di dalam lubang terbuka). Ketersediaan per wellbore tidak merata (F-14: 0 collar; F-7: 0 collar) |
| 4 | **S-B1/S-E1/S-A3** — rating motor (`torqueMax`/`Pmax`) — konfirmasi klaim D0 | rating motor tekan | **TIDAK ADA (klaim D0 DIKONFIRMASI)** | Grep mandiri 192 file: `torqueMax` **0**, `Pmax` **0**, `torque` **0**, `rpmMax` **0**, `powerMax` **0**, `revPerGallon` **0**. Yang ada hanya `flowrateMx` di **9** file (19 elemen, semua `/mwdTool/` = rentang operasi MWD, bukan motor). 13 komponen motor (`motor` 6 + `motor steerable` 7), 12 dengan od+len valid (1 sentinel total: `15/9-F-11_5QKUJ48` od=id=len=-999.25) — **hanya geometri, tanpa rating** | Kalau solusi butuh rating motor → sumber lain (DDR/pabrikan/asumsi eksplisit bertanda asumsi). Jangan buka I1/TOB dari jalur ini |

---

## 1. Detail BIT (S-F1/S-D3)

### 1.1 Sebaran per `nameWellbore` (43 bit-family; * = termasuk hole opener)

| nameWellbore | file tubular | bit-family | rincian (typeBit) |
|---|---:|---:|---|
| NO 15/9-F-11 | 8 | 9 | PDC + roller cone |
| NO 15/9-F-11 T2 | 13 | 8 | PDC + roller cone |
| NO 15/9-F-1 | 11 | 7 | PDC |
| NO 15/9-F-11 B | 25 | 5 | PDC + roller cone |
| NO 15/9-F-1 B | 17 | 4 | PDC + 1 hole opener* |
| NO 15/9-F-1 C | 29 | 4 | PDC |
| NO 15/9-F-15 D | 36 | 3 | PDC (12-3/16", 17-1/2", 26") |
| NO 15/9-F-1 A | 3 | 1 | roller cone |
| NO 15/9-F-11 A | 2 | 1 | PDC |
| NO 15/9-F-15 C | 14 | 1 | roller cone 8.5" |
| NO 15/9-F-14 | 6 | **0** | — (assembly fishing/milling: drill pipe, mill casing cutting, casing, packer) |
| NO 15/9-F-5 | 9 | **0** | — (assembly fishing: spear, bullnose, mill taper) |
| NO 15/9-F-12 | 9 | **0** | — |
| NO 15/9-F-4 | 3 | **0** | — (4 komponen saja) |
| NO 15/9-F-7 | 5 | **0** | — |
| NO 15/9-F-9 A | 2 | **0** | — |

### 1.2 TEMUAN KRITIS — coverage bit terhadap fold kampanye `bit_wear`

Fold `bit_wear` V6 = **F-14, F-15, F-15S, F-5** (USROP, kolom `well`: `N-SH_F-14d`, `N-SH-F-15d`, `N-SH_F-15Sd`, `N-SH_F-5d` — StatoilHydro). Pencocokan ke tubular:

| Fold bit_wear | nameWellbore tubular | bit tersedia? |
|---|---|---|
| F-14 (47.645 baris USROP) | NO 15/9-F-14 ada (6 file) | **TIDAK** — 0 komponen bit |
| F-15 (53.041 baris) | F-15 C: 1 bit (roller cone 8.5"); F-15 D: 3 bit PDC | **SEBAGIAN** — ambigu: cabang C/D vs sumur utama, mapping USROP F-15 → cabang mana harus didefenisikan eksplisit sebelum dipakai |
| F-15S (51.708 baris) | **TIDAK ADA** `nameWellbore` mengandung "F-15S" (grep 0 dari 1.392 baris) | **TIDAK** |
| F-5 (18.548 baris) | NO 15/9-F-5 ada (9 file) | **TIDAK** — 0 komponen bit |

**Konsekuensi jujur:** identitas bit dari tubular TIDAK menutupi fold `bit_wear` (cakupan 1 dari 4 fold, itupun ambigu C/D). Fungsi tubular untuk S-F1/S-D3 = **konteks geometri BHA/ukuran lubang & rantai pemakaian bit fisik (serial) di 10 wellbore F-1/F-11/F-15** — BUKAN label/identitas run untuk 4 fold kampanye. Jangan menjual "bit identity per fold" ke Master; yang dijual = fitur konteks di subset sumur + kemungkinan rantai serial.

---

## 2. Detail STABILIZER (S-B1/S-E1)

- 75 komponen (`stabilizer string` 66 + `stabilizer near bit` 9), od & len **75/75 non-null**.
- `posAxialWellbore` **0 dari 1.392 komponen** (grep: 0 file dari 192) → posisi aksial = **turunan** dari `sequence` + kumulatif `len`. Validasi mekanis: 15 assembly punya ≥2 stab + rantai len lengkap → 30 gap bisa dihitung; contoh gap 1,2–39,3 m (masuk rentang fisik stabilizer-spacing wajar).
- Blade: 125 sub-elemen `<stabilizer>` (termasuk pada LWD "Flex sub w/ Stab"): `shapeBlade` spiral 41 / unknown 84; `typeBlade` integral 8 / unknown 117. Informasi blade tipis — jangan jadikan fitur utama.
- Sebaran per wellbore: F-1 21, F-11 T2 13, F-11 8, F-1 C 8, F-15 D 6, F-11 B 6, F-12 4, F-5 3, F-1 B 2, F-15 C 2, F-1 A 1, F-11 A 1. **F-14, F-4, F-7, F-9 A: 0 stabilizer.**

---

## 3. RATING MOTOR — klaim D0 DIKONFIRMASI (bukti grep sendiri)

| Kata kunci | File kena (dari 192) |
|---|---:|
| `torqueMax` | **0** |
| `Pmax` | **0** |
| `torque` | **0** |
| `rpmMax` | **0** |
| `powerMax` | **0** |
| `revPerGallon` | **0** |
| `flowrateMx` | 9 (semua `/mwdTool/` — rentang MWD, bukan rating motor) |

Verdict: **rating motor TIDAK ADA di domain TUBULAR.** 13 komponen motor hanya membawa geometri (12 valid, 1 sentinel total `15/9-F-11_5QKUJ48`). Tidak ada dasar untuk "membuka I1/TOB" dari jalur rating motor.

---

## 4. Peluang PROSES lintas-file (untuk Master analisis relasi)

1. **Join key = field XML `nameWellbore`** (16 nilai), BUKAN path folder. Jebakan terkonfirmasi: folder `Norway-Statoil-NO 15_$47$_9-F-1 C` berisi 4 wellbore berbeda (F-1 A/B/C + F-1); folder `F-11` berisi 4 wellbore; folder `F-15` berisi C + D.
2. **Normalisasi nama wellbore ↔ USROP:** kolom `well` `USROP_labeled.csv` berisi nama file sumber (`N-SH_F-14d` dll.) — mapping ke `NO 15/9-F-XX` harus dibuat eksplisit (termasuk kasus F-15: sumur utama vs cabang C/D/S). Rekonsiliasi ini milik Master/bawahan lain; D1a hanya melaporkan kedua bentuk nama.
3. **Rantai bit serial:** 26 serial unik, beberapa muncul di banyak assembly (`5221270` 80× nameTag) → kandidat join intra-tubular "bit fisik yang sama dipakai berulang" → fitur akumulasi pemakaian. Dedup nameTag kembar per file wajib.
4. **Turunan posisi aksial (stabilizer spacing)** butuh rantai `sequence`+`len` lengkap per assembly (15/45 assembly yang punya stabilizer lolos syarat ≥2 stab + rantai lengkap → 30 gap).
5. **Geometri kontak LF3** = turunan Σ(od·len) collar per assembly; join ke waktu/depth kampanye = via `nameWellbore` + interval run (anchor waktu ada di domain bawahan 02 BHARUN, bukan di sini).
6. **Coverage wellbore parse-baru (F-10/F-4/F-12/F-15):** F-10 = 0 file tubular; F-4 = 4 komponen tanpa bit/stab; F-12 & F-15 = kaya (50/51/235 komponen, 4/2/6 stab). Fitur BHA untuk fold baru hanya mungkin di F-12/F-15.

---

## 5. Bukti ketiadaan (anti-karangan)

- **F-10 tanpa tubular:** `ls witsml_raw/` → direktori `Norway-StatoilHydro-15_$47$_9-F-10` ADA (untuk log), tapi `find … -path "*tubular*" -name "*.xml"` = **0**. Per-direktori (26 well dir): hanya 8 dir Statoil-NO yang punya tubular XML (F-1 C 60, F-11 48, F-15 50, F-5 9, F-12 9, F-14 6, F-7 5, F-4 3, F-9 2 = 192). Semua dir `Norway-StatoilHydro-*` dan `Norway-NA-*` = **0 tubular**.
- **`nameWellbore` mengandung "F-10"** di 1.392 baris = **0**.
- **`nameWellbore` mengandung "F-15S"** = **0**.
- **`posAxialWellbore`**: 0 file dari 192 (grep) DAN 0/1392 komponen terparse (parsing).
- **`torqueMax`/`Pmax`/`torque`/`rpmMax`/`powerMax`/`revPerGallon`**: 0 file (§3).

---

## 6. Rekonsiliasi vs klaim V7-M1/D0 (konfirmasi/koreksi)

| Klaim sumber | Angka klaim | Angka recount (sesi ini) | Verdict |
|---|---|---|---|
| 192 file tubular XML | 192 | 192 | KONFIRMASI |
| 1.392 komponen, 62 tipe | 1.392 / 62 | 1.392 / 62 | KONFIRMASI |
| Rating motor `torqueMax`/`Pmax` = 0/192 | 0 | 0 (grep mandiri) | KONFIRMASI |
| Join via `nameWellbore`, bukan path | — | 16 wellbore; folder menyembunyikan wellbore berbeda | KONFIRMASI (jebakan nyata) |
| Klaim implisit "identitas bit tersedia untuk bit_wear" | implisit tersedia | hanya 1/4 fold (F-15, ambigu); F-14/F-5/F-15S = 0 bit | **KOREKSI** — laporkan coverage apa adanya |

---

## 7. Belum diverifikasi (verification-mandatory #3)

1. Mapping eksplisit well USROP (`N-SH_F-14d`, `N-SH-F-15d`, `N-SH_F-15Sd`) → `nameWellbore` tubular/F-15 cabang mana — butuh sumber di luar domain ini (inventaris Volve / Pembaca 08).
2. Validitas fisik rantai `sequence` sebagai posisi aksial (asumsi seq=1 = dasar bit) — diuji konsistensi mekanis (gap 1,2–39,3 m wajar) tapi tidak divalidasi terhadap gambar BHA/DDR.
3. Reproduksi penuh parser V6 (CSV `scratch/v6_d1a_tubular.csv`) — recount sesi ini independent, angka cocok, tapi file CSV lama tidak dibuka ulang baris per baris.
4. `external/dbx_volume/.../tubular` (192 file copy) — jumlah file identik, isi identik/diverifikasi hanya via hitungan, bukan checksum per file.

**Reproduksi:** skrip di workspace task `t_5f46ecdc`: `recount_tubular.py`, `followup_checks.py`, `dir_coverage.py`, `raw_print_join.py`, `bit_extra_checks.py`, `stab_blade.py` (+ artefak `tubular_recount.csv`, 1.392 baris).
