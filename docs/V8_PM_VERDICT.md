# V8-PM — VERDICT AKHIR: apakah peta alat PdM koheren & layak pakai?

**PM:** [PM] V8-PM (t_3b98266a) · **Board:** capstone-v8-capability · **Tanggal:** 2026-10-12 (WIB)
**Kerangka:** penilaian di TINGKAT ALAT PdM (prinsip operator #6) — standar 3 lapisan A/B/C
`docs/V8_R1_ABC_SPEC.md`, BUKAN gate biner V6/V7.
**Sumber:** `docs/V8_R1_ABC_SPEC.md`, 7 profil `docs/V8_E_*_CAPABILITY.md`,
`docs/V8_M1_CAPABILITY_MAP.md`, `docs/V8_A1_CAPABILITY_AUDIT.md`, baseline
`docs/V6_PM_VERDICT.md` / `docs/V7_PM_VERDICT.md`, riwayat sesi (session_search), agentmemory.

> **Riset pendahuluan: `what-if-oracle`** — vonis diuji 5 cabang (Ω/α/Δ/Ψ/Φ) + tripwire
> eksplisit (§6), supaya kesimpulan "koheren" tidak bergantung pada satu asumsi
> (kampanye penguatan berhasil / label valid / dst).
> **Riset pendahuluan: `scientific-critical-thinking`** — klaim "koheren/layak" diberi
> falsifier eksplisit (§5.3); tiap bukti dipisah OBSERVED (grep/read langsung sesi ini)
> vs kutipan A1 vs DERIVED; kontradiksi antar-dokumen diadjudikasi, bukan diabaikan (§2).
> **Riset pendahuluan: `consciousness-council`** — deliberasi 5 arketipe (Empiricist,
> Architect, Pragmatist, Contrarian, Futurist) dengan ketegangan wajib, sintesis §5.
> **Riset pendahuluan: `sequentialthinking`** (sequ-mcp, 3 pikiran, 3/3 sukses) —
> inventaris bukti → verifikasi anti-regresi + hitungan alat → sintesis akhir dgn
> uji falsifier.
> **Riset pendahuluan: `verification-mandatory`** — setiap klaim vonis di bawah punya
> jejak: grep/read_file sesi ini, hitung ulang A1, atau session_search; tanpa itu ditandai
> "belum diverifikasi" (§9).

---

## 0. VONIS (tegas)

**VONIS: KOHEREN dan LAYAK PAKAI — sebagai alat PdM kelas ADVISORY / human-in-loop.**
**BUKAN** sebagai alat alarm otomatis kritis: 0 dari 7 engine memenuhi syarat alarm
otomatis, dan semua evaluator menyatakan itu terus terang.

- Alat punya **tujuh komponen bernilai, semuanya dengan peran + batas pemakaian +
  kekuatan bukti tertulis**; tidak ada komponen dibuang, tidak ada yang diklaim
  melampaui buktinya.
- Fungsi alat minimum PdM **terpenuhi hari ini**: konfirmasi status otomatis (Layer-0,
  rule/persistence terukur), peringatan human-in-loop pada well terkalibrasi (3 engine),
  tren/skor dashboard (5–6 engine), keputusan manusia (Layer-3).
- Gap yang ada (G1–G8, §4) **memblokir EKSPANSI** (alarm otomatis, diagnosis, lead
  >10–30 mnt, generalisasi lintas-wellbore) — **tidak memblokir fungsi dasar alat**.
- Keputusan "layak tren/peringatan TETAPI belum alarm otomatis" = **keputusan wajar,
  bukan kegagalan** (kerangka V8-R1 §4, instruksi operator).

**Confidence: TINGGI** — 0 klaim fabrikasi (A1: 121 klaim dihitung ulang), 0 evaluator
kembali ke gate biner (dicek ulang sesi ini), tier konsisten (0+3+2+2=7), falsifier
diuji dan gugur (§5.3).

---

## (a) KEPUTUSAN AKHIR MENURUT DUA OPSI TUGAS

Tugas menyediakan dua opsi. **Opsi 1 dipilih: PETA ALAT KOHEREN & LAYAK** → ringkasan
alat PdM + langkah eksekusi nyata diserahkan ke operator di §7–§8. Enam patch angka dan
dua pelanggaran skill dicatat sebagai tindak lanjut (§2, §8), bukan sebagai syarat
vonis — tidak ada satupun yang membalikkan tier engine mana pun (dibuktikan §2).

---

## (a') KEPAATIHAN SKILL PER TIM

Kriteria (task V8-PM): baris `Riset pendahuluan` + skill sci + sequ mcp; acuan protokol
`docs/PROTOCOL_RISET_TIM.md` Aturan 2–4 (PM wajib: what-if-oracle, scientific-critical-
thinking, consciousness-council).

| Tim / dokumen | Baris "Riset pendahuluan" | Skill sci (scientific-critical-thinking dll) | Sequ mcp dideklarasikan | Status |
|---|---|---|---|---|
| R&D `V8_R1_ABC_SPEC.md` | ✓ (5 skill) | ✓ | ✓ (5 pikiran, 5/5) | PATUH |
| Evaluator `vib` | ✓ (4 skill) | ✓ | ✓ (5/5) | PATUH |
| Evaluator `ssi` | ✓ (4 skill) | ✓ | ✓ (pikiran 1–5) | PATUH |
| Evaluator `bit_wear` | ✓ (4 skill) | ✓ | ✓ (5/5) | PATUH |
| Evaluator `stuck` | ✓ (4 skill) | ✓ | ✓ (4 pikiran) | PATUH |
| Evaluator `hyd` | ✓ (4 skill) | ✓ | ✓ (5 pikiran) | PATUH |
| Evaluator `shk` | ✓ (3 skill — tanpa baris sequ) | ✓ | ✗ **TIDAK ADA** (grep `sequ` = 0 di dokumen) | **PELANGGARAN #1** |
| Evaluator `tool_wear` | ✓ (4 skill) | ✓ | ✓ (5/5) | PATUH |
| Master `V8_M1_CAPABILITY_MAP.md` | ✓ (4 skill) | ✓ | ✓ (5/5) | PATUH |
| Auditor `V8_A1_CAPABILITY_AUDIT.md` | ✓ (4 skill) | ✓ | ✗ tidak dideklarasikan di dokumen; metadata kartu klaim "digunakan saat diskriminasi — tak diverifikasi di log run" | **PELANGGARAN #2 (catatan)** |
| PM (dokumen ini) | ✓ (5 baris di atas) | ✓ | ✓ (3 pikiran, 3/3 sukses, tool_call sequ-mcp sesi ini) | PATUH |

**Pelanggaran tercatat (2):**
1. **shk** — deklarasi sequ-mcp tidak ada. Ini pelanggaran PROSEDURAL (bukti pemakaian),
   bukan metodologis: angka shk sendiri diverifikasi A1 (termasuk 45/45 sel tabel
   per-well cocok) dan dokumen shk memuat baris riset 3 skill lain.
2. **A1** — sequ diklaim di metadata kartu tapi tidak muncul di dokumen dan tidak ada
   jejak log; diperlakukan sebagai TIDAK TERVERIFIKASI (jangan dikutip sebagai bukti
   pemakaian).

Tidak ada tim yang melewatkan baris `Riset pendahuluan` atau skill sci. Tidak ada
pelanggaran yang mempengaruhi angka hasil.

---

## (b) KONSISTENSI ANGKA ANTAR LAPORAN

### b.1 Selisih yang ADA dan sudah diadjudikasi

A1 menghitung ulang 121 klaim numerik unik + 45 sel tabel shk dari artefak JSON primer:
**114 terverifikasi, 0 karangan, 6 selisih nyata**. Keenamnya **saya verifikasi ulang
langsung ada di dokumen sumber** (grep sesi ini, baris persis):

| # | Klaim dokumen | Angka benar (hitung ulang A1) | Lokasi | Dampak ke vonis |
|---|---|---|---|---|
| 1 | hyd: "CI persistence vs RF tidak tumpang tindih **6/7 fold**" | **5/7** (F-5 juga overlap) | hyd baris 63/179; **diwarisi M1 baris 54/65** | nol — keunggulan persistence tetap (ΔB<0 7/7) |
| 2 | shk: "persistence > RF di **4/9 fold**" | **5/9** (+ F-15_S) | shk baris 41 | nol — justru melemahkan klaim shk |
| 3 | shk: "FAR≤1 dgn recall>0 **TIDAK tercapai di fold mana pun / 0 dari 9 fold**" | **1 titik**: F-14 tau0,30 → FAR 0,69/24j, recall **0,92%** (tidak operasional) | shk baris 61/112; **diwarisi M1 baris 55/169** | nol — "BELUM alarm otomatis" tetap benar |
| 4 | stuck: "FAR semua engine **9,9–185** / 25–185" | **9,9–1.440** (E3_RF LOWO F-14→F-9_A = 1.440/24j; ada di tabel & verdict dokumen sendiri) | stuck baris 31/206 (M1 baris 53 BENAR) | nol — malah memperkuat "BELUM alarm" |
| 5 | tool_wear: T_lead median E1 "**30 dtk**" | **24,5 dtk** (nilai 20,24,25,36) | tw baris 102/106/162 | nol — tetap detik, tetap LAYAK tren |
| 6 | tool_wear: T_lead median E2 "**47,5 dtk**" | **47,0 dtk** | tw baris 101/133/162 | nol (slip 0,5 dtk) |

Catatan A5 yang saya konfirmasi: "RF ≥ persistence B1 di 9/9 fold" benar sebagai "≥",
tapi 4 di antaranya tie (3× 0–0, 1× 0,071) — "ML menambah nilai" ketat hanya **4/9**;
klaim M1 "nilai tambah ML terukur" untuk onset shk perlu anotasi tie ini.

**Adjudikasi:** untuk seluruh vonis ini dipakai **angka hitung ulang A1** (bukan kutipan
dokumen bila berbeda). Ke-6 selisih = kekeliruan penyajian (median, rentang, jumlah
fold, tumpang-tindih CI) — **tidak satu pun membalikkan tier/kemampuan engine apa
pun**. Patch ke dokumen sumber = langkah eksekusi §8.1.

### b.2 Cek silang konsistensi TAMBAHAN (dilakukan sesi ini)

- Tier M1: 0 + 3 + 2 + 2 = **7 ✓**; "5/7 punya jalur peringatan" = 3 terbukti + 2
  bersyarat **✓**; 0 engine dobel, 0 engine hilang **✓**.
- M1 "shk 4 titik FAR≤6, P 0,18–0,55" = shk baris 108 **cocok ✓**.
- M1 stuck "9,9–1.440" = angka benar; dokumen stuck yang salah di ringkasan (kontradiksi
  INTERNAL dokumen stuck: ringkasan 9,9–185 vs tabel sendiri 1.440) **✓ terkonfirmasi**.
- Tabel per-well shk (M1 vs dokumen shk): 45/45 sel cocok (A1) **✓**.
- Selisih antar-dokumen yang TIDAK ditemukan: tidak ada angka yang muncul dengan dua
  nilai berbeda di dua tempat selain keenam butir di atas.

### b.3 Riwayat kegagalan (session_search — wajib)

- Kartu evaluator **shk pernah `blocked`** (2026-10-11) — di-unblock dan selesai;
  dokumennya lolos audit angka.
- Kartu **Auditor A1 crash 2× (pid mati) sebelum menulis dokumen** — didorong menulis
  temuan yang sudah ada (80 angka: 73 PASS, 6 FAIL, 1 tidak-bisa) lalu diskriminasi
  satu-satu; hasil akhir = dokumen A1 lengkap. Ini **kegagalan infrastruktur, bukan
  metodologi** — angka tetap berasal dari artefak JSON yang sama.
- Tidak ada kegagalan run yang menghasilkan angka hilang/tidak terverifikasi di
  dokumen akhir.

---

## (c) VERIFIKASI: anti-regresi gate biner + batas pemakaian + baseline relevan

| Cek | Hasil | Bukti |
|---|---|---|
| Ada evaluator kembali ke gate biner (LULUS/GAGAL sebagai vonis)? | **TIDAK ADA (0/7)** | grep `LULUS\|GAGAL` di 7 profil = hanya penafian eksplisit ("BUKAN vonis LULUS/GAGAL" — hyd baris 5, stuck baris 5, shk "Baris status (bukan LULUS/GAGAL)" baris 124) atau rujukan FAKTA gate V6 sebagai konteks (vib baris 28/31/53; ssi baris 9). A1 §6: 0 temuan; praktik benar: ssi G1 4/5 + G2 5/5 tercapai TETAPI tetap "BELUM LAYAK alarm" krn B4/FAR/C3 belum |
| Semua engine punya batas pemakaian ("BELUM untuk…")? | **7/7** | bagian "LAYAK untuk X, BELUM untuk Y" ada di tiap profil (vib baris 121–122, ssi baris 115–117, bit_wear baris 164, stuck §5 baris 184–213, hyd §5 baris 174–191, shk baris 105–111, tool_wear baris 130–145) |
| Baseline relevan per tugas (bukan universal)? | **7/7** | A1 §7; tiap profil mendeklarasikan baseline sendiri (canary/persistence/prevalence-random/rule absolut sesuai kelas) |
| Gate V6 digeser? | **TIDAK** | R1 §5: G1/G2 dipindah jadi syarat ambang-atas "TERBUKTI prediksi kuat", tidak dihapus/dilunakkan; ambang baru (B1 50/80%, FAR 1/6) = desain pra-reg yang boleh disetel sekali sebelum run |

---

## (c') PERBANDINGAN DENGAN BASELINE V6/V7 (kerangka biner)

Baseline terverifikasi dari `V6_PM_VERDICT.md` baris 131: **LULUS penuh = 2 (vib, ssi);
4 kelas GAGAL (stuck, shk, hyd, tool_wear); bit_wear = layak bersyarat** — status
conditional bahkan hilang dari narasi ringkas "2 LULUS + 4 GAGAL".

| Dimensi | V6/V7 (biner) | V8 (kemampuan) |
|---|---|---|
| Output per engine | 1 bit (LULUS/GAGAL) | ~10 dimensi: jenis tugas · lapisan A/B/C · LAYAK-untuk · BELUM-untuk · kekuatan bukti · tier pemakaian |
| Informasi yang hilang | bit_wear "bersyarat"; alasan kegagalan; kelayakan non-alarm | semuanya tercatat |
| Jujur tentang alarm | tidak ada konsep FAR/lead-time | 0/7 alarm dinyatakan eksplisit + syarat kenaikan tier |
| Baseline | 1 universal (G2 canary) | relevan per tugas (6 jenis baseline) |
| Hasil hitungan | "2 lolos" | 3 peringatan terbukti + 2 bersyarat + 2 tren + 7/7 berperan |

**Kesimpulan: V8 menghasilkan gambaran LEBIH KAYA dan LEBIH JUJUR** — setiap "kekalahan"
V6 berubah menjadi kemampuan-terbatas yang bisa dipakai + tahu persis syarat
meningkatkannya. Tidak ada informasi V6 yang hilang di V8.

---

## (d) HITUNGAN KEBERHASILAN ALAT PdM (prinsip operator #6)

Dihitung per ENGINE (7 unit), tier = kemampuan tertinggi TERBUKTI hari ini
(sumber: M1 §d, diverifikasi ulang 0+3+2+2=7):

| Tier alat | Jumlah | Engine |
|---|---|---|
| **LAYAK alarm otomatis kritis** | **0 / 7** | — (syarat R1 §4: FAR≤1/24j dgn recall>0 + B1≥80% + C2/C3 — belum ada yang terpenuhi; shk titik terdekat recall 0,92%) |
| **LAYAK peringatan human-in-loop (terbukti)** | **3 / 7** | **shk** (lead 2–9 mnt, well terkalibrasi lokal) · **stuck** (triage manual, sumur mirip F-10; E1 P 0,457, lead 10 mnt) · **hyd K-ii** (indikasi dini lead 7 mnt, label UNDERPOWERED wajib tampil) |
| **LAYAK peringatan BERSYARAT (menunggu ukur FAR/B4)** | **2 / 7** | **vib** (syarat: FAR_t + B4 di kampanye F-4/F-10/F-15) · **ssi** (syarat: FAR diukur; label keyakinan wajib) |
| **Tier tertinggi = tren/skor/indikasi saja** | **2 / 7** | **bit_wear K-1** (persistence status 0,679–0,984 = konfirmasi terukur terbaik; RF screening) · **tool_wear** (skor LOTO lintas-alat + detektor perubahan-regime) |
| **Punya peran dalam alat** | **7 / 7** | tidak ada engine dibuang atau dilabeli "gagal/buang" |

**Ringkas:** 0 alarm otomatis · 3 peringatan operasional terbukti · 5/7 punya jalur
peringatan (3+2) · 7/7 layak setidaknya konfirmasi-status/tren/indikasi pada batasnya.
Yang membatasi 0-alarm = bukti B & FAR **belum diukur** (vib, ssi, bit_wear) atau
**sudah terukur dan di atas ambang** (shk, stuck, hyd, tool_wear) — **bukan ketiadaan
sinyal A**.

### Gap (dari M1 §e — diverifikasi tetap relevan untuk vonis)

| # | Gap | Menghalangi? |
|---|---|---|
| G1 | Diagnosis/akar-masalah = 0 engine (EDM BLOCKED, ordinal shk belum, semantik STUCK_RT belum) | menghalangi **luas** alat, tidak fungsi dasar |
| G2 | Alarm otomatis FAR≤1/24j dgn recall>0 = 0/7 | menghalangi **klaim alarm** — sudah jujur tidak diklaim |
| G3 | B3 pengurangan pemeriksaan: shk NEGATIF (−0,11…−53,75), lain belum terukur (butuh data beban-kerja rig — tidak ada di Volve) | menghalangi **klaim efisiensi inspeksi** |
| G4 | Peringatan >10–30 mnt = semua horizon ≤10 mnt | menghalangi **lead panjang** (bit-change/well-control berjam-jam) |
| G5 | Generalisasi lintas-wellbore (hyd K-ii 1 wellbore; stuck F-12 belum; vib F-4/F-10/F-15 belum diparse; shk F-10/F-12 lift ≈1) | menghalangi **pemakaian di well baru tanpa kalibrasi** |
| G6 | C3 toleransi dropout sensor: baru tool_wear + shk | menghalangi **klaim robustness sensor** utk 5 engine |
| G7 | Validitas label lintas-well (kontrol-positif stuck 0/10; hyd label proxy; severity-mix beda) | mengancam **kuadran onset** — sudah dianotasi sbg bukti rendah-sedang |
| G8 | Onset bit_wear K-2 = nol angka (kandidat 481/329) | menghalangi **peringatan-dini bit** |

**Tidak ada gap yang menghalangi alat berfungsi di kelas yang diklaimnya**
(advisory/human-in-loop, well terkalibrasi, horizon ≤10 menit).

---

## (e) DELIBERASI DAWAR (consciousness-council) — 5 anggota

❓ **Empiricist** — *Position:* vonis "koheren" didukung bukti, asal skopnya jujur.
*Reasoning:* 121 klaim dihitung ulang, 0 fabrikasi; 7/7 baseline per-tugas; tier
konsisten; 0 evaluator klaim alarm tanpa bukti. Angka "0 alarm" justru data terkuat
yang dimiliki peta ini. *Key risk:* 6 selisih penyajian belum di-patch — mengutip M1
apa adanya akan mengulangi angka salah ke laporan Bab II. *Insight:* kekuatan bukti
terendah ada di label (G7), bukan di model.

🏛 **Architect** — *Position:* struktur alat jelas 4 lapis, satu grid 60 detik.
*Reasoning:* L0 (rule/persistence) → L1 (peringatan human-in-loop) → L2 (tren) → L3
(manusia); kalibrasi lokal per well di setiap lapis. Arsitektur tidak punya komponen
menggantung — semua 7 engine punya slot. *Key risk:* onset-layer punya 4 head terpisah
dengan grid bersama; kalau semantik label (G7) salah, yang rusak head prediktor, bukan
infrastruktur. *Insight:* hybrid = infrastruktur bersama, bukan bobot bersama (M1 §b.3)
— itu yang membuat peta koheren meski tiap engine berbeda kualitas.

🚦 **Pragmatist** — *Position:* layak pakai SEKARANG untuk 3 well terkalibrasi, jangan
tunggu sempurna. *Reasoning:* operator butuh konfirmasi status + triage hari ini; L0
sudah jalan tanpa ML; L1 shk/stuck/hyd bisa dipasang dengan badge beban-kerja. *Key
risk:* kampanye penguatan (parse VIBLAT, S-E1, K-2) bisa tidak pernah jalan → alat
stagnan di 3 peringatan. *Insight:* langkah eksekusi termurah dulu — patch 6 angka (jam
kerja, nol data baru) sebelum kampanye data.

🌀 **Contrarian** — *Position:* "koheren" bisa jadi ilusi kohesi naratif. *Reasoning:*
M1 menulis koherensi tapi mewarisi 2 kesalahan angka; shk satu-satunya yang benar-benar
menghitung B3 dan hasilnya NEGATIF — kalau B3 negatif juga di kelas lain, nilai
"pengurangan pemeriksaan" alat bisa nol. *Key risk:* G3 butuh data yang tidak ada di
Volve → klaim nilai PdM bisa tinggal "layak lihat layar". *Insight:* vonis harus
dibaca sebagai "koheren dalam scope advisory" — tanpa kalimat itu, vonis overclaim.
(Claw ini sudah dipenuhi: vonis §0 menyebut skop eksplisit.)

🔭 **Futurist** — *Position:* nilai jangka panjang = platform kalibrasi, bukan model.
*Reasoning:* semua bukti menunjukkan ambang tidak transfer lintas well → alat yang
benar adalah alat yang belajar kalibrasi per well dengan cepat; 7 engine adalah
modul-nya. *Key risk:* tanpa G4 (lead >30 mnt), alat tidak pernah sampai ke keputusan
bit-change/POOH — nilai bisnis terbesar. *Insight:* tripwire M1 (FAR≤1 terukur, K-2
jalan, kontrol-positif disinkron) = daftar yang tepat untuk menaikkan tier.

**SINTESIS:**
- **Konvergensi (5/5):** peta koheren & layak dipakai di kelas advisory; angka jujur;
  0-alarm bukan kegagalan.
- **Ketegangan inti:** "layak pakai" vs "belum ada alarm otomatis" — keduanya benar pada
  lapisan berbeda; resolusi = skop eksplisit dalam vonis.
- **Blind spot:** keberhasilan alat bergantung **kalibrasi lokal per well** — alat hari-ini
  hanya layak utk well terkalibrasi; ini batas pemakaian yang harus tampil di UI alat.
- **Confidence: TINGGI** (konvergensi kuat; ketegangan ter-resolusi dengan bukti).
- **Satu pertanyaan untuk dipegang:** berapa FAR aktual di well BUKAN tempat kalibrasi —
  karena di sanalah "peringatan" berubah jadi "gangguan".

---

## (f) STRESS-TEST VONIS (what-if-oracle) — 5 cabang

| Cabang | Bobot | Skenario | Konsekuensi terhadap vonis | Tripwire |
|---|---|---|---|---|
| **Ω Best 15%** | — | Kampanye penguatan jalan (VIBLAT F-4/F-10/F-15, S-E1 11 fold, K-2 bit_wear) → FAR+B4 tercetak | vib/ssi naik penuh ke LAYER-1; vonis TETAP koheren, tier peringatan naik 3→5 | FAR≤1 terukur per kelas |
| **α Likely 45%** (prioritas aksi 61,8%) | — | Alat live sebagai L0 + L2 + L1-terbatas (shk/stuck/hyd per-well) | **VONIS BERLAKU apa adanya** — koheren di scope advisory | pemasangan L1 di 1 well terkalibrasi |
| **Δ Worst 20%** | — | FAR/B tak pernah terukur (kampanye batal) | alat tetap koheren di L0+L2+L1 3-engine — batas jujur, bukan kegagalan | kampanye penguatan tidak jalan 30 hari |
| **Ψ Wildcard 10%** | — | Label semantik salah lintas-well (STUCK_RT 0–3, severity-mix, hyd proxy) | onset layer salah sasaran → vonis turun jadi "koheren HANYA di L0/L2" | kontrol-positif stuck 0/10 (sudah ada) disinkronkan |
| **Φ Contrarian 10%** | — | Ternyata persistence/rule sudah cukup utk nilai PdM | ML hanya dipertahankan shk/stuck/hyd-onset; arsitektur & vonis tetap sama | ΔB vs persistence per kelas |

Vonis tidak bergantung pada satu asumsi: di 4 dari 5 cabang vonis **tetap koheren**
(skop bisa menyempit pada cabang Ψ). Prioritas aksi mengikuti bobot α (61,8%).

---

## (g) RINGKASAN ALAT PdM (diserahkan ke operator)

**Alat: "PdM Advisory V8" — satu grid 60 detik, empat lapis keluaran, kalibrasi lokal
per wellbore.**

```
LAYER-0  KONFIRMASI STATUS (otomatis, tanpa ML)                [TERBUKTI]
  rule VIBLAT ≥32,17 · rule SSI≥1 · rule display shock ·
  persistence: hyd P 0,615–0,793 · bit_wear 0,679–0,984 ·
  stuck 0,787 (V6) · vib-status
  → indikator status di layar rig. KONFIRMASI keadaan, bukan alarm PdM.

LAYER-1  PERINGATAN HUMAN-IN-LOOP (butuh konfirmasi operator)  [3 TERBUKTI + 2 BERSYARAT]
  terbukti: shk-RF (lead 2–9 mnt, well terkalibrasi; badge FAR) ·
            stuck E1-triage (sumur mirip F-10; P 0,457; lead 10 mnt) ·
            hyd K-ii (F-9A; lead 7 mnt; label UNDERPOWERED tampil)
  bersyarat (masuk setelah ukur FAR/B4): vib · ssi
  → notifikasi + label keyakinan + badge beban-kerja (FAR terukur per fold)

LAYER-2  TREN / SKOR (dashboard, tanpa notifikasi)             [5–6 ENGINE]
  vib-RF · ssi-RF · bit_wear (persistence+RF screening) ·
  tool_wear LOTO-score · stuck E3 ranking · hyd persistence trend

LAYER-3  KEPUTUSAN MANUSIA                                    [SEMUA KELAS]
  alat menyarankan, manusia memutuskan.

ALARM OTOMATIS KRITIS: 0 slot hari ini (0/7 engine) — syarat R1 §4 belum tercapai.
```

**Batas pemakaian yang WAJIB tampil di alat:** hanya well terkalibrasi lokal · horizon
≤10 menit · tanpa klaim diagnosis (G1) · tanpa klaim pengurangan inspeksi (G3) ·
tool_wear = domain bengkel, terpisah · FAR ditampilkan pada skala aslinya.

**Kekuatan bukti agregat:** A kuat di 4 kelas (vib/ssi/hyd/shk), sedang di 2
(bit_wear/tool_wear), rendah-sedang di stuck; B terukur penuh hanya shk/stuck/hyd;
C4 (transparansi ketidakpastian) terpenuhi 7/7; angka bebas fabrikasi (A1).

---

## (h) LANGKAH EKSEKUSI NYATA (urut, termurah dulu)

1. **Patch 6 selisih angka (0 data baru, jam kerja):**
   - hyd baris 63/179 + M1 baris 54/65: "CI non-tumpang 6/7" → "5/7 (F-5 & F-9 overlap)".
   - shk baris 41: "4/9 (F-7, F-14, F-10, F-12)" → "5/9 (+ F-15_S)".
   - shk baris 61/112 + M1 baris 55/169: "TIDAK tercapai / 0 dari 9 fold" → "1 titik
     dari seluruh grid: F-14 tau0,30 FAR 0,69/24j, recall 0,92% — tidak operasional".
   - shk baris 83/107 + M1: "RF≥persistence 9/9 → ML menambah nilai" → tambah "4 fold
     tie; menambah nilai ketat di 4/9".
   - stuck baris 31/206: "9,9–185 / 25–185" → "9,9–1.440 (E3_RF LOWO 1.440/24j)".
   - tool_wear baris 102/106/133/162: median E1 30 → 24,5 dtk; E2 47,5 → 47,0 dtk.
   - Catat di tiap dokumen bahwa angka dikoreksi per V8-A1.
2. **Pasang LAYER-1 di 3 engine terbukti** pada 1 well terkalibrasi (shk/stuck/hyd),
   dengan badge FAR + label keyakinan + beban-kerja; log setiap notifikasi vs kejadian
   nyata (membangun B3/G3 dari data riil).
3. **Kampanye penguatan ukur B & FAR** (syarat naik tier vib/ssi → peringatan penuh):
   parse VIBLAT F-4/F-10/F-15 · re-run S-E1 ssi 11 fold · pra-reg K-2 bit_wear
   (onset 481/329, nol parse = termurah).
4. **Sinkronkan validitas label (G7):** kontrol-positif stuck dengan zona waktu benar ·
   dokumentasi semantik STUCK_RT 0–3 lintas-well · ordinal shk (S-B3) · parse
   GAINLOSSTOT F-1C/F-11 untuk hyd K-ii.
5. **Uji C3 dropout** (paket murah, tanpa data baru) di vib/ssi/bit_wear/hyd/stuck.
6. **Kalibrasi-per-well sebagai prosedur baku:** ambang selalu dihitung di train lokal
   (bukti: shk 0 alarm lintas-well, stuck q95 jenuh, hyd FAR meledak 26–300×).
7. **Dokumen operasional alat** = tabel M1 §a + batas pemakaian (§g) — dipakai apa
   adanya untuk laporan Bab II; JANGAN klaim "deteksi dini otomatis" di dokumen mana pun
   sebelum syarat R1 §4 (FAR≤1/24j + B1≥80% + C2/C3) terpenuhi.

---

## (i) BATAS vonis ini (verification-mandatory #3)

- Vonis menilai **koherensi & kelayakan alat dari dokumen + hitung ulang A1**; tidak
  mengeksekusi ulang model (re-run = ranah evaluator berikutnya).
- Angka V6 yang dikutip di dalam dokumen sumber = kutipan yang sudah melalui audit
  V5_A1/V7 + reproduksi evaluator; tidak dihitung ulang di sesi ini.
- Kelayakan "advisory" berlaku untuk **well terkalibrasi pada data Volve**; transfer ke
  rig/well lain belum diuji (G5) — vonis tidak mengklaim sebaliknya.
- Pelanggaran skill shk/A1 dicatat sebagai temuan prosedural; jika operator menilai
  pemakaian sequ-mcp wajib diverifikasi, dua dokumen itu perlu deklarasi ulang dengan
  jejak log — bukan hal yang mengubah angka.

## Sumber (dibaca langsung sesi ini via read_file/terminal)

`docs/V8_R1_ABC_SPEC.md` (413 baris) · `docs/V8_M1_CAPABILITY_MAP.md` (229) ·
`docs/V8_A1_CAPABILITY_AUDIT.md` (118) · 7 × `docs/V8_E_*_CAPABILITY.md` (grep +
cuplikan kunci; angka utama melalui A1) · `docs/V6_PM_VERDICT.md` baris 131 ·
`docs/PROTOCOL_RISET_TIM.md` Aturan 2–4 · session_search (riwayat kegagalan shk/A1) ·
grep lintas-dokumen (LULUS/GAGAL, BELUM, sequ, selisih #1–#6).
