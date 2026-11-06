# V11-A_AUDIT: STRUKTUR, KELUHAN (a)-(f), KEPATUHAN EVALUASI USER.TXT, EM-DASH, MD=IPYNB

Task: `t_08261bde` [Auditor umum] · Board: `capstone-v11-vs` · Tanggal: 2026-10-15 (WIB)
Peran: menguji struktur, penutupan keluhan operator, kepatuhan instrumen Evaluasi User.txt,
paket .md = .ipynb, aturan em-dash, dan konsistensi 7 engine / 11 klaim / 27 head.
Identitas kandidat ditulis sebagai "kandidat 1 / kandidat 2" dengan path lengkap (kode opaque);
tidak ada kesimpulan versi baru/lama dan tidak ada perbandingan menang/kalah di dokumen ini
(keputusan akhir = PM-FINAL).

> Riset pendahuluan: `scientific-critical-thinking` - pemisahan data vs interpretasi per poin
> (status TERTUTUP/SEBAGIAN/BELUM berdasarkan seksi, bukan kesan umum); tiap temuan punya
> falsifier (angka yang membuktikan); kekuatan bukti diberi status eksekusi vs kehadiran.
> Riset pendahuluan: `verification-mandatory` - seluruh angka di dokumen ini berasal dari
> eksekusi skrip di sesi ini (bukti mentah di §10); daftar "belum diverifikasi" ditulis eksplisit
> di §9; dua false negative alat ukur (pola case-sensitive) dilaporkan dan diperbaiki (§9).
> Riset pendahuluan: `statistical-analysis` - penilaian mengikuti rubrik terkunci PM-0 (§8)
> dengan bobot tidak diubah; skor kriteria 2 dinyatakan provisional karena ketelusuran 30
> angka = peran AUD-CLAIM, bukan kartu ini; tidak ada rata-rata lintas kampanye.
> Riset pendahuluan: `sequentialthinking` (sequ-mcp, 5 pikiran): inventaris bukti -> rencana
> skrip -> sintesis penilaian per kriteria -> penulisan dokumen.

---

## 0. PETA KANDIDAT (kode opaque)

| Label | Path .md (dicek ulang) | Path .ipynb (pasangan wajib) |
|---|---|---|
| Kandidat 1 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` (352 baris) | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.ipynb` |
| Kandidat 2 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (3.557 baris) | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb` |

---

## 1. TUGAS 1: KELUHAN OPERATOR (a)-(f)

Sumber keluhan verbatim: `docs/V10_PM1_OUTLINE.md` baris 8-11.
Status: TERTUTUP = ada seksi yang benar-benar menjawab; SEBAGIAN = ada tapi tidak lengkap;
BELUM = tidak ada.

### Kandidat 1

| Poin | Status | Bukti seksi / ketiadaan |
|---|---|---|
| (a) daftar 7 hal yang dideteksi | **TERTUTUP** | §1 "tujuh mesin deteksi" (baris 44-46); §8.2 "Tujuh kelas target" (baris 135); §15.1 tabel "Peta Ketujuh Mesin" dengan nama ketujuh (baris 244-252) |
| (b) engine mana yang bekerja & bagaimana caranya | **SEBAGIAN** | "mana yang bekerja": §1 tabel status 0/3/2/2 (baris 50-56) + §15.1 kolom "Tingkat pemakaian terbukti". "Bagaimana caranya": hanya setingkat keluarga metode (§5 baris 84-90, §9.2 baris 151-159); tidak ada mekanisme/mekanika per engine |
| (c) alasan KENAPA tiap engine dipilih (bukti, bukan selera) | **SEBAGIAN** | §12 "Alasan Pemilihan Metode" (baris 198-207) dan kolom Alasan §9.2 (baris 151-159): alasan pada tingkat keputusan metodologis, tanpa bukti angka per engine |
| (d) peran DATA | **SEBAGIAN** | §8.1 kolom "Peran" per sumber data (baris 125-129), §8.2-8.3 (fitur, pembagian data, prapemrosesan); tidak ada bagian tersendiri yang merangkum peran data dalam identifikasi kerusakan |
| (e) labeling ML / statistik / workflow hybrid | **BELUM** | labeling = 1 kalimat anti-sirkularitas (baris 137) tanpa skema per kelas; statistik disebut sebagai nama metode (baris 87, 155) tanpa rumus; hibrida disebut (baris 90, 159) tanpa rumus h(t), tanpa workflow, tanpa angka pemangkasan FP |
| (f) penjelasan TEGAS 7 vs 11 (dan 27 head) | **BELUM** | rekam murni `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md`: "11 klaim" = 0 kemunculan, "27 head" = 0 kemunculan, `4+4+4+6+4+2+3` = 0, `3x1+4x2` = 0 (skrip v11_a_headcheck.py). Hanya angka 7 yang dijelaskan ("tujuh mesin/kelas") |

Rekap kandidat 1: 1 TERTUTUP, 3 SEBAGIAN, 2 BELUM.

### Kandidat 2

Matriks penutupan resmi ada di dokumen kandidat §2.9 (baris 330-339); isi tiap butir diverifikasi
dengan membuka bab yang ditunjuk (bukan matriksnya sendiri):

| Poin | Status | Bukti seksi (dibuka langsung) |
|---|---|---|
| (a) daftar 7 hal yang dideteksi | **TERTUTUP** | Bab 1 §1.1 tabel 7 engine dengan kanal/ambang (baris 195-205); Bab 7 §0.1 (baris 2915); Bab 8 §1 (baris 3200) |
| (b) engine mana yang bekerja & bagaimana caranya | **TERTUTUP** | Bab 7 kerangka + tabel besar 11 klaim (baris 2963); Bab 8 §2 "CARA KERJA ENGINE" (baris 3224); Bab 1 §1.3 daftar 27 head (baris 226-258) |
| (c) alasan KENAPA tiap engine dipilih | **TERTUTUP** | Bab 2 §2.1-§2.7 alasan per engine fisika -> sensor -> metode (baris 510-681); Bab 2 §5 "MENJAWAB KELUHAN OPERATOR (khusus poin (c))" (baris 764) |
| (d) peran DATA | **TERTUTUP** | Bab 3 §3.0 ringkas (baris 896), §3.2 isi/peran/keterbatasan tiap dataset (baris 949), §3.6.1 "(d) Peran data" (baris 1348); Bab 8 §4 (baris 3291) |
| (e) labeling ML / statistik / workflow hybrid | **TERTUTUP** | Bab 4 labeling per kelas + asersi anti-sirkular (baris 1555-1640); Bab 5 rumus statistik per head (baris 1985-2348); Bab 6 §3 rumus & workflow hibrida (baris 2553-2674) |
| (f) penjelasan TEGAS 7 vs 11 (dan 27 head) | **TERTUTUP** | Bab 1 §0 jawaban satu paragraf (baris 169-179), §1 penjelasan tegas + §1.1/§1.2/§1.3 daftar eksak (baris 183-261), §1.4 "mengapa tiga angka" (baris 263-270) |

Rekap kandidat 2: 6 TERTUTUP.

Catatan jujur: matriks §2.9 dan tabel acceptance §5 kandidat 2 adalah klaim dokumen itu sendiri;
yang dinilai di sini adalah pembukaan bab-babnya (baris-baris di atas), bukan matriksnya.

---

## 2. TUGAS 2: KEPATUHAN EVALUASI USER.TXT (POIN a-e)

Sumber: `/mnt/d/Capstone 1(v2)/Evaluasi User.txt` (39 baris); pemetaan butir = V11_PROTOCOL §5.

### Kandidat 1

| Poin | Terpenuhi? | Bukti seksi |
|---|---|---|
| (a) lapisan A/B/C | **YA** | §11.2 ketiga lapisan didefinisikan dan diterapkan per mesin (baris 184-192); §13 pemetaan metrik -> lapisan (baris 209-221); §1 ringkasan hasil per lapisan (baris 46). Catatan: tanpa angka metrik per lapisan di dokumen ini (penilaian angka ada di kartu domain) |
| (b) baseline relevan per tugas, bukan satu universal | **YA (prinsip), SEBAGIAN (implementasi)** | §9.2 baris 153-154 (canary = pembanding wajib per tugas; persistence = pembanding status-quo), §12 baris 204 "Baseline relevan per tugas | Satu baseline universal | ditolak", §13 baris 218. Tidak ada penetapan baseline per tugas secara eksplisit per daftar tugas |
| (c) bedakan jenis tugas (anomali/kondisi/diagnosis/prediksi) | **YA** | §5 baris 92 dan §9.1 baris 147 menyebut keempat jenis tugas; §15.1 kolom "Jenis tugas" per mesin (baris 244-252) memakai label turunan |
| (d) kemampuan + batas + kekuatan bukti, tanpa vonis biner tingkat alat | **YA** | §15.1 kolom "Tingkat pemakaian terbukti" dan "Batas (BELUM untuk)" ketujuh mesin (baris 244-252); §15.3 kejujuran batas + gap bukti (baris 262-264); §11.2 baris 192 menolak vonis tunggal; §16 R1-R7 |
| (e) nilai pada tingkat alat, bukan jumlah model lolos gate | **YA** | §1 baris 56 "Punya peran dalam alat: 7 dari 7"; §15.2 tingkat pemakaian + "0 Tingkat 3" (baris 254-260); §5 baris 92 "tidak semua mesin memerlukan ambang yang identik"; §8.3/§11.1 validitas data & uji temporal tetap dituntut (baris 141, 182) |

### Kandidat 2

| Poin | Terpenuhi? | Bukti seksi |
|---|---|---|
| (a) lapisan A/B/C | **YA** | Bab 7 judul "Hasil A/B/C" (baris 2868); baris 320 metrik per blok: "A (P/R/FAR/AUPRC/lift/CI vs baseline), B (TLead/B1-B4), C (C1-C4)"; Bab 8 §8.1 tiga lapisan penilaian A/B/C (baris 3404); Bab 1 §1.3 tabel tier/lapisan per head (baris 260-261) |
| (b) baseline relevan per tugas, bukan satu universal | **YA** | Bab 1 aturan lintas-bab #4 (baris 364); Bab 6 §4 "BASELINE S9: KENAPA TIAP ENGINE BUTUH BASELINE RELEVAN SENDIRI" (baris 2675); Bab 1 baris 473 mengutip "bukan satu baseline universal (Evaluasi User.txt, prinsip 1-6)" |
| (c) bedakan jenis tugas | **YA** | Bab 1 §1.2 tabel "Jenis tugas" per 11 klaim (baris 209-221): deteksi kondisi, deteksi anomali, prediksi kejadian mendatang, prediksi onset, ranking; Bab 4/5 label & baseline mengikuti jenis tugas |
| (d) kemampuan + batas + kekuatan bukti, tanpa vonis biner tingkat alat | **YA** | Bab 7 §4 "BELUM TERUKUR / BELUM DIVERIFIKASI (dipisah tegas dari gagal)" (baris 3083); baris 2877 "**BUKAN vonis LULUS/GAGAL** ... memenuhi untuk X / belum untuk Y / belum terukur"; Bab 8 §9 batas jujur (baris 3445) |
| (e) nilai pada tingkat alat, bukan jumlah model lolos gate | **YA** | baris 2905 "vonis ditaruh di tingkat alat, bukan 'N model lolos gate'"; Bab 8 §7 hitungan alat 0 alarm + 3 peringatan + 2 bersyarat + 2 tren (baris 3371); Bab 8 §8.1-§8.2 cara membaca peta kemampuan L0-L3 (baris 3399-3444); aturan #2 (baris 362) "nol angka karangan ... yang belum ada ditulis belum terukur, bukan 0, bukan dihapus" |

---

## 3. TUGAS 3: VONIS BINER LULUS/GAGAL & POST-MORTEM (dilarang untuk proposal)

Hitung kata murni dengan pola `\bLULUS\b`, `\bGAGAL\b` pada .md (skrip v11_a_markers.py).

### Kandidat 1
- `LULUS`: **0** kemunculan. `GAGAL`: **0** kemunculan.
- Penolakan vonis biner ditulis eksplisit: §11.2 baris 192 "bukan vonis tunggal lulus/tidak lulus".
- Post-mortem: **tidak ada di badan proposal**; riwayat kegagalan kampanye dipindah ke
  `CHANGELOG.md` (baris 14 "agar proposal terbaca sebagai rencana solusi, bukan post-mortem";
  baris 58 dan 352 menegaskan hal yang sama). Referensi "vonis SAH" di baris 321 adalah kutipan
  dokumen primer [A-1], bukan vonis yang dikeluarkan proposal ini.
- Status: **PATUH** (tanpa vonis biner tingkat mesin; tanpa post-mortem kegagalan).

### Kandidat 2
- `LULUS`: **4** kemunculan (baris 374-376 = tabel acceptance **internal kerangka PM1**:
  AC-1 outline konsisten REGISTRY, AC-2 matriks keluhan, AC-3 delegasi kartu; ini penilaian
  diri dokumen terhadap kelengkapan outline, bukan vonis mesin) dan baris 2877 = penegasan
  negasi ("BUKAN vonis LULUS/GAGAL").
- `GAGAL`: **2** kemunculan: baris 2877 (negasi yang sama) dan baris 671
  "spesifisitas keausan GAGAL karena cp signifikan 8/8 run termasuk 8/8 alat BARU (precision
  run 0,50)" = hasil satu tes spesifisitas dengan angka dan lanjutan batas ("layak sebagai
  gating inspeksi, bukan alarm"), bukan vonis biner tingkat alat.
- Pemakaian lain: baris 1825/3190/3401 memakai "lulus/gagal" dalam kalimat negasi
  ("bukan lulus/gagal", "peta kemampuan tidak berbunyi lulus/gagal").
- Post-mortem: **tidak ada**; proposal berulang kali menyatakan "bukan riwayat kegagalan"
  (baris 366, 877, 1485, 1937, 2430, 3169) dan memindahkan riwayat ke `CHANGELOG.md` (baris 15).
- Status: **PATUH pada inti larangan** (tidak ada vonis biner LULUS/GAGAL untuk mesin/klaim;
  post-mortem tidak diproposal), **CATATAN**: kosakata "LULUS" pada tabel acceptance internal
  PM1 (baris 374-376) membawa nuansa vonis di dalam dokumen proposal; itu penilaian
  kelengkapan outline, bukan penilaian mesin.

---

## 4. TUGAS 4: EM-DASH (U+2014) DAN EN-DASH

Metode: hitung Python `chr(0x2014)`/`chr(0x2013)` per baris pada .md dan pada sel markdown
.ipynb, lalu tiap konteks diperiksa manual (skrip v11_a_emdash.py; JSON:
`/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/emdash_counts.json`).

| Kandidat | em-dash .md | em-dash sel .ipynb | en-dash .md | Pelanggaran penghubung klausa |
|---|---|---|---|---|
| Kandidat 1 | **14** | **14** | 2 (keduanya rentang) | **>= 6** |
| Kandidat 2 | **0** | **0** | 225 | **0** |

Kandidat 1, daftar 14 em-dash dan klasifikasi (baris = nomor baris .md):
- **Penghubung klausa tanpa konjungsi/pemisah (pelanggaran)**: baris 62 (2 buah:
  "Kegagalan BHA -- mencakup ..." dan "... keausan komponen -- menyebabkan NPT"),
  baris 136 ("... slope, last, fraksi) -- 55 fitur dari 11 kanal"), baris 182
  ("pertanyaan bisnis yang benar -- apakah mesin berguna ..."), baris 352 (2 buah:
  "Riwayat pengembangan lengkap -- termasuk ..." dan "... penilaian berturut-turut --
  tercatat pada CHANGELOG.md"). Total = **6 pelanggaran jelas**.
- **Sisanya (8)**: pasangan label istilah baris 9-10 (tabel kontrol dokumen), baris
  188-190 (Lapisan A/B/C), baris 256-258 (Tingkat 1/2/3). Pola "istilah -- definisi"
  ini termasuk gaya penegasan yang dipakai berulang (8 kali) sehingga tidak memenuhi
  syarat "dipakai jarang" pada V11_PROTOCOL §7.3; tetap dicatat sebagai pelanggaran
  gaya, dan skor sudah jatuh pada 4+ pelanggaran.
- Skor 4d kandidat 1 = **0** (4 pelanggaran atau lebih).

Kandidat 2:
- 0 em-dash di .md maupun di sel markdown .ipynb. Skor 4d = **3**.
- En-dash 225: 205 terklasifikasi rentang numerik (mis. baris 74 "baris 74-287",
  AUPRC 0,4405-0,9117), 19 sisanya rentang seksi/label (§1.1-§1.3, (a)-(f), [1]-[27],
  B1-B4, C1-C4) dan 1 sebagai sel tabel kosong (baris 2152 "0,000 | -- |"). **Tidak ada**
  en-dash yang menghubungkan klausa (semua konteks ada di JSON §10).

---

## 5. TUGAS 5: .md VS .ipynb (SETIAP BARIS ISI .md WAJIB ADA DI .ipYNB)

Metode: ekstrak sel markdown .ipynb, normalisasi (rapikan spasi), bandingkan multiset baris
dengan .md (skrip v11_a_parity.py; JSON: `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/md_ipynb_parity.json`).

| Kandidat | Baris substansial .md | Hilang di .ipynb | Selisih bukan substansial |
|---|---|---|---|
| Kandidat 1 | 255 | **0** | 8 baris ekstra di .ipynb = blok arsip VIS ("ARSIP VISUALISASI KAMPANYE LAMA ... bukan bagian narasi proposal") |
| Kandidat 2 | 2.829 | **0 substantif** | 2 baris "hilang" ternyata tergabung jadi 1 baris di .ipynb dengan karakter `\n` literal (baris md 648-649 = kutip `v8_e_shk_02b`; teks identik, hanya dipisah literal backslash-n) + 9 baris ekstra = blok arsip VIS |

Kecocokan kemunculan 30 angka checklist di .md vs sel .ipynb juga dihitung (§7): identik
per kandidat (7/30 dan 30/30 di kedua format).

- Kandidat 1: **lolos cek mekanis** (4c = 4).
- Kandidat 2: isi substantif identik; ada 1 **artefak kosmetik** literal backslash-n pada satu
  sel (baris md 648-649 yang tergabung) sehingga pembaca notebook melihat teks "\n" di tengah
  kalimat. Ini bukan selisih angka/klaim/struktur (syarat 4c), tetapi dicatat sebagai cacat
  tampilan. 4c = 4 dengan catatan artefak.

---

## 6. TUGAS 6: KONSISTENSI 7 ENGINE / 11 KLAIM / 27 HEAD (DENGAN EKSEKUSI)

Primer = REGISTRY `code/v9_i1_pipeline.py` yang **dijalankan** (import modul + baca
`REGISTRY`, `SEED`, `AUTO_CRITICAL_SLOTS`; skrip v11_a_registry.py + v11_a_klaim.py).
Hasil eksekusi (JSON: `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/registry_facts.json`):

- 7 engine: `vib, ssi, shk, stuck, hyd, bit_wear, tool_wear` (7 kunci).
- 11 klaim = 3 engine x 1 klaim (vib, ssi, shk) + 4 engine x 2 klaim (stuck K-i/K-ii,
  hyd K-i/K-ii, bit_wear K-1/K-2, tool_wear K-i/K-ii) = 11. Teks `klaim_tugas` tiap engine
  dibaca langsung (mis. stuck: "K-i: deteksi kondisi blok STUCK_RT; K-ii: prediksi onset
  0->1 (H=10 mnt)").
- 27 head, sebaran `4+4+4+6+4+2+3` (vib 4, ssi 4, shk 4, stuck 6, hyd 4, bit_wear 2,
  tool_wear 3).
- Rekap tier: PERINGATAN-BERPENGAWAS 12, TREN 13, BELUM LAYAK PAKAI 2.
- Rekap lapisan: L0 5, L1 11, L2 9, L3 2. `AUTO_CRITICAL_SLOTS = 0`. `SEED = 42`.
- Ambang di teks REGISTRY: vib `VIBLAT_RT >= 32,17405 ft/s2`; stuck onset `H=10 mnt`;
  hyd K-i `residu SPPA |z|>2` (semua cocok dengan yang dikutip kandidat 2).

### Hasil per kandidat

**Kandidat 1**
- Angka 7: konsisten (§1, §8.2, §15.1 selalu 7 mesin/kelas; §15.2 rekap 3/2/2/0 = 7,
  sejalan dengan rekap tier V8 pada checklist item 29).
- Angka 11 dan 27: **tidak disebut sama sekali** (0 kemunculan; lihat §1). Konsistensi
  antar-angka tidak dapat diuji karena ketidakhadirannya; untuk rubrik ini = ketiadaan
  penjelasan (4b = 0).

**Kandidat 2**
- Tabel 27 head (baris 232-258) dibandingkan baris per baris dengan REGISTRY yang dieksekusi:
  **27 baris, 0 mismatch** (engine, nama head, tier, lapisan semuanya cocok; 0 head REGISTRY
  hilang; skrip v11_a_headcheck.py, JSON `head_table_and_markers.json`).
- Tabel 11 klaim (baris 209-221) cocok dengan teks `klaim_tugas` REGISTRY termasuk status
  jujur klaim #7 (hyd K-ii TIDAK TERSEDIA) dan #9 (bit_wear K-2 BELUM) yang tetap dihitung.
- Rekap tier 12/13/2 (baris 260) dan lapisan 5/11/9/2 + slot alarm 0 (baris 261) **sama
  persis** dengan hasil eksekusi.
- Sebaran `4+4+4+6+4+2+3` (5 kemunculan) dan `3x1+4x2` (5 kemunculan) konsisten di seluruh
  dokumen; "11 klaim" 25 kemunculan, "27 head" 42 kemunculan, "7 engine" 37 kemunculan,
  tanpa angka kontradiktif yang terdeteksi pada pola ini.

**Antar kandidat**: keduanya menyebut 7 kelas kegagalan yang dapat dipetakan 1:1
(getaran lateral=vib, stick-slip=ssi, shock/aksial=shk, stuck pipe, anomali hidraulik=hyd,
keausan bit, keausan mata bor=tool_wear); tidak ada kelas yang bertambah/menghilang.
Perbedaannya: kandidat 2 menyertakan unit 11 klaim dan 27 head beserta rekap tier/lapisan;
kandidat 1 hanya sampai level 7 (lihat §1 poin (f)).

---

## 7. BUKTI TAMBAHAN: KEHADIRAN 30 ANGKA CHECKLIST (V11_PROTOCOL §4)

Metode: pencocokan pola per butir pada .md dan sel .ipynb (skrip v11_a_checklist.py, JSON
`checklist_presence.json`). Kehadiran ≠ kebenaran; ketelusuran nilai ke primer tetap tugas
AUD-CLAIM. Yang **dieksekusi dan cocok** di kartu ini = butir 1-10 (dibandingkan ke REGISTRY
yang dijalankan, §6).

| Kandidat | Kehadiran .md | Kehadiran .ipynb | Item tidak ada |
|---|---|---|---|
| Kandidat 1 | **7/30** | **7/30** | 2, 3, 4, 5, 7, 8, 9, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 30 |
| Kandidat 2 | **30/30** | **30/30** | (tidak ada) |

Item yang ADA pada kandidat 1: 1 (7 engine), 6 (alarm otomatis 0), 10 (seed 42),
11 (USROP 198.928), 15 (55 fitur), 20 (XML 192/161), 29 (rekap 0/3/2/2).

Temuan akurasi dalam cakupan kartu ini (satu-satunya angka kandidat 1 yang diuji ke primer):
angka "**8.474.172 baris**" (kandidat 1 baris 127) **bertentangan dengan primernya sendiri**:
`docs/V3_WITSML_PARSE_REPORT.md` baris 20 berbunyi "Total: 7,080,457 baris time-series,
8 CSV" (dibaca langsung di sesi ini), dan `docs/V11_DATA1.md` baris 82 mencatat seluruh
enumerasi 45 pasangan 8-dari-10 file tidak menghasilkan 8.474.172 (itu juga di luar cakupan
ulang-hit kartu ini, status: diverifikasi parsial: kutipan primer cocok, enumerasi ulang belum
saya jalankan sendiri).

---

## 8. LEMBAR SKOR (RUBRIK PM-0 TERKUNCI; TANPA PERBANDINGAN AKHIR)

Sub-kriteria dan bobot persis V11_PROTOCOL §2. Perbandingan kemenangan = PM-FINAL.

### Kandidat 1 (`.../ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` + `.ipynb`)

| Kriteria | Sub | Skor | Dasar (bukti seksi) |
|---|---|---|---|
| 1. Kedalaman teknis (30) | 1a rumus per engine/head | 0/10 | tidak ada satu pun rumus/definisi operasional di dokumen (baca penuh 352 baris; hanya nama metode) |
| | 1b labeling per kelas + anti-sirkular | 1/7 | 1 kalimat anti-sirkularitas (baris 137), tanpa skema label per kelas |
| | 1c workflow hybrid + interaksi | 1/7 | hibrida disebut (baris 90, 159) tanpa rumus/workflow/mekanisme |
| | 1d bukti per klaim | 3/6 | sitasi internal [A-1..A-13] + angka tier + audit 121 klaim; klaim kemampuan per mesin tanpa angka inline |
| | **Jumlah** | **5/30** | |
| 2. Akurasi (30) | 2a checklist 30 angka | **4/18 (provisional, batas atas = batas bawah)** | kehadiran 7/30; kehadiran maksimum memberi 18 x 7/30 = 4,2; ketelusuran nilai = AUD-CLAIM |
| | 2b angka di luar checklist | 4/6 (provisional) | angka inventaris yang diuji kartu ini: 198.928 (cocok), 192/161 (cocok PM0); 8.474.172 terbukti tidak dapat ditelusuri (§7); mayoritas angka lain belum ditelusuri di kartu ini |
| | 2c nihil angka karangan | 4/6 (provisional) | 1 angka terbukti tidak bersumber (8.474.172) dalam sampel pemeriksaan; angka lain belum penuh diuji |
| | **Jumlah** | **12/30 (provisional)** | |
| 3. Evaluasi User.txt (25) | 3a lapisan A/B/C | 5/6 | ketiga lapisan ada & dipakai konsisten di tingkat desain (§11.2/§13/§15); tanpa angka metrik per lapisan di dokumen |
| | 3b baseline per tugas | 4/5 | prinsip tegas (§9.2/§12/§13); penetapan baseline per tugas tidak didetail |
| | 3c jenis tugas | 4/5 | keempat jenis disebut (§5/§9.1) + kolom jenis tugas §15.1 memakai label turunan |
| | 3d kemampuan+batas+bukti tanpa vonis biner | 6/6 | §15.1 semua 7 mesin punya Tingkat + Batas; §15.3; penolakan vonis eksplisit §11.2; 0 kata LULUS/GAGAL |
| | 3e tingkat alat | 3/3 | sintesis "7 dari 7 punya peran", 3/2/2/0 (§1, §15.2, §19) |
| | **Jumlah** | **22/25** | |
| 4. Struktur (15) | 4a outline | 4/4 | DAFTAR ISI 19 seksi, BAGIAN A/B/C jelas |
| | 4b penjelasan 7/11/27 | 0/4 | 11 klaim & 27 head tidak pernah ada (0 kemunculan) |
| | 4c md = ipynb | 4/4 | 0 baris substansial hilang |
| | 4d em-dash | 0/3 | 14 em-dash, >=6 pelanggaran penghubung klausa |
| | **Jumlah** | **8/15** | |
| **TOTAL** | | **47/100** | (kriteria 2 provisional; 1, 3, 4 final dalam cakupan kartu ini) |

### Kandidat 2 (`.../ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` + `.ipynb`)

| Kriteria | Sub | Skor | Dasar (bukti seksi) |
|---|---|---|---|
| 1. Kedalaman teknis (30) | 1a rumus per engine/head | 9/10 | rumus ada per keluarga: Bab 5 (median/MAD qcut, z E2, SSE change-point + permutation, fisher), Bab 6 (rule per kelas, persistence, h(t) hibrida), Bab 4 (kontrak RF/GB/LR), Bab 2 (sitasi per rumus); verifikasi kebenaran literal per rumus = kartu domain (E_STAT/E_HYB), kartu ini hanya kehadiran + sampel (SSE tool_wear baris 667-668 terbaca benar) |
| | 1b labeling per kelas + anti-sirkular | 6/7 | Bab 4 §1 empat kelas sumber label + §1.1 asersi anti-sirkular runtime; celah minor di luar cakupan penuh kartu ini (tidak diuji ulang di sini) |
| | 1c workflow hybrid + interaksi | 7/7 | Bab 6 §3.1 rumus, §3.2 workflow 4 langkah, §3.3 mekanisme pengaruh antar-komponen, §3.4 degenerasi |
| | 1d bukti per klaim | 5/6 | tiap bab punya seksi "SUMBER ANGKA (traceability)" + seksi verifikasi; beberapa klaim naratif ringkas tanpa angka |
| | **Jumlah** | **27/30** | |
| 2. Akurasi (30) | 2a checklist 30 angka | 6/18 (provisional, batas bawah tereksekusi) | kehadiran 30/30 di md & ipynb; butir 1-10 **cocok 1:1 dengan REGISTRY yang dieksekusi** (18 x 10/30 = 6); butir 11-30 baru kehadiran, ketelusuran nilai = AUD-CLAIM (batas atas 18) |
| | 2b angka di luar checklist | 5/6 (provisional) | slice kartu ini: tabel 27 head + rekap tier/lapisan + ambang REGISTRY cocok 1:1 (0 mismatch); angka lain belum ditelusuri di kartu ini |
| | 2c nihil angka karangan | 6/6 (provisional) | nol angka karangan ditemukan dalam slice pemeriksaan kartu ini; belum penuh |
| | **Jumlah** | **16/30 (provisional, rentang 16-29 menunggu AUD-CLAIM)** | |
| 3. Evaluasi User.txt (25) | 3a lapisan A/B/C | 6/6 | Bab 7 hasil per lapisan + metrik A/B/C per blok (baris 320) + §1.3 tier/lapisan per head |
| | 3b baseline per tugas | 5/5 | Bab 6 §4 baseline relevan per engine + aturan lintas-bab #4 |
| | 3c jenis tugas | 5/5 | Bab 1 §1.2 tabel jenis tugas per 11 klaim, label & baseline mengikuti jenis |
| | 3d kemampuan+batas+bukti tanpa vonis biner | 6/6 | Bab 7 §4 "belum terukur terpisah dari gagal" + baris 2877 penolakan eksplisit; 3 "LULUS" = acceptance outline internal PM1, bukan vonis mesin (§3 dokumen ini) |
| | 3e tingkat alat | 3/3 | Bab 8 §7-§8 hitungan alat + cara membaca L0-L3 + larangan "N model lolos gate" |
| | **Jumlah** | **25/25** | |
| 4. Struktur (15) | 4a outline | 4/4 | 8 bab + DAFTAR ISI + hierarki heading konsisten |
| | 4b penjelasan 7/11/27 | 4/4 | Bab 1 §1 tegas + daftar eksak + rekap; konsisten lintas bab; 27/27 baris tabel head cocok REGISTRY |
| | 4c md = ipynb | 4/4 | 0 baris substansial hilang; 1 artefak literal backslash-n (kosmetik, dicatat) |
| | 4d em-dash | 3/3 | 0 em-dash; 225 en-dash semuanya rentang/sel kosong |
| | **Jumlah** | **15/15** | |
| **TOTAL** | | **83/100** | (kriteria 2 provisional; 1, 3, 4 final dalam cakupan kartu ini) |

Disclosure bias: penilai menyadari pemetaan label path (K1 = path `.v3_arsip`, K2 = path utama)
karena tertulis di badan kartu tugas; penilaian di atas berpatokan pada rubrik tertulis dan
bukti seksi/eksekusi, bukan pada makna kata "arsip" (V11_PROTOCOL §1.2).

---

## 9. BELUM DIVERIFIKASI (eksplisit)

1. Ketelusuran nilai 30 angka checklist ke primer (butir 11-30) untuk kedua kandidat = tugas
   AUD-CLAIM; kartu ini baru membuktikan kehadiran (7/30 dan 30/30) dan kebenaran butir 1-10
   via REGISTRY yang dieksekusi.
2. Enumerasi ulang 45 pasangan 8-dari-10 CSV untuk angka 8.474.172 tidak saya jalankan sendiri;
   yang saya baca langsung adalah `V3_WITSML_PARSE_REPORT.md` baris 20 (7,080,457) dan temuan
   `V11_DATA1.md`.
3. Kebenaran literal seluruh rumus Bab 5/Bab 6 (dibandingkan baris kode modul E_STAT/E_RULE)
   = cakupan kartu domain; kartu ini hanya memastikan kehadiran + 1 sampel (SSE tool_wear).
4. Output execution cell .ipynb tidak dibaca; yang dibandingkan adalah sel markdown.
5. Angka kemampuan per engine (AUPRC, FAR, TLead, fold) tidak diuji ulang di kartu ini.
6. Dua false negative alat ukur yang ditemukan dan diperbaiki selama sesi ini: (i) skrip
   penanda awal memakai pola case-sensitive sehingga "Alasan Pemilihan Metode" kandidat 1
   lolos (diperbaiki dengan re.IGNORECASE pada skrip v11_a_headcheck.py); (ii) skrip
   checklist awal memakai pola "3 peringatan" huruf kecil sehingga butir 29 kandidat 2
   terlewat (diperbaiki; hasil akhir 30/30). Kedua koreksi dilakukan sebelum skor ditulis.
7. Isi `.ipynb` kandidat 2 dipastikan memuat semua baris md, tetapi urutan/sel code tidak
   diverifikasi setara dengan md selain kehadiran angka checklist per format (identik).

---

## 10. BUKTI MENTAH: SKRIP DAN JSON PRIMER

Skrip (workspace `t_08261bde`, semuanya dieksekusi di sesi ini, exit 0):

| Skrip | Fungsi |
|---|---|
| `v11_a_outline.py` | daftar heading kandidat 2 (208 heading); `v11_a_k1heads.py` menghitung heading kandidat 1 = 43 |
| `v11_a_emdash.py` | hitung U+2014/U+2013 md + sel markdown ipynb + konteks tiap baris |
| `v11_a_parity.py` | normalisasi multiset baris md vs ipynb |
| `v11_a_registry.py` | import & jalankan REGISTRY + klasifikasi en-dash |
| `v11_a_klaim.py` | teks `klaim_tugas` per engine + `AUTO_CRITICAL_SLOTS` + `SEED` |
| `v11_a_markers.py` | pemindaian penanda keluhan/Evaluasi/vonis (awal, case-sensitive) |
| `v11_a_headcheck.py` | tabel 27 head vs REGISTRY + marker case-insensitive + pola 7/11/27 |
| `v11_a_checklist.py` | matriks kehadiran 30 angka + klasifikasi en-dash |

JSON primer (tersimpan sebelum penulisan dokumen, S6):
- `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/emdash_counts.json`
- `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/md_ipynb_parity.json`
- `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/registry_facts.json`
- `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/marker_scan.json`
- `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/head_table_and_markers.json`
- `/mnt/d/Capstone 1(v2)/scratch/v11_a_audit/checklist_presence.json`

Dokumen yang dibaca langsung: `docs/V11_PROTOCOL.md` (rubrik, checklist 30 angka, aturan
em-dash/md=ipynb), `Evaluasi User.txt` (39 baris), `docs/V10_PM1_OUTLINE.md` baris 8-11
(keluhan verbatim), kedua kandidat .md (kandidat 1 dibaca penuh 352 baris; kandidat 2 dibaca
selektif per seksi yang diuji), `docs/V3_WITSML_PARSE_REPORT.md` baris 20,
`docs/V11_DATA1.md` baris 82 (pendukung, diberi status).

---

*Selesai V11-A_AUDIT (`t_08261bde`): keluhan (a)-(f) dan Evaluasi a-e dinilai per seksi;
vonis biner & post-mortem diperiksa dengan hitung kata; em-dash 14 (>=6 pelanggaran) vs 0;
parity md=ipynb 0 baris substantif hilang di kedua kandidat; 7/11/27 diverifikasi lewat
REGISTRY yang dieksekusi (tabel 27 head kandidat 2 cocok 27/27); skor per kandidat tanpa
perbandingan akhir.*
