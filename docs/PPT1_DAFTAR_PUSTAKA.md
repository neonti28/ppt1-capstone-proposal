# DAFTAR PUSTAKA DAN LANDASAN KEPUTUSAN DESAIN

Berkas ini mencatat setiap keputusan desain yang punya dasar pustaka, beserta status
kekuatan buktinya. Tujuannya agar pada sidang tidak ada klaim yang berdiri tanpa rujukan,
dan agar pembaca bisa membedakan mana yang berasal dari publikasi peer-review, mana dari
standar, dan mana dari sumber industri yang tidak melalui peer-review.

## A. Peta keputusan ke rujukan

| Keputusan dalam proposal | Rujukan | Isi yang dipakai | Status bukti |
|---|---|---|---|
| NPT layak dijadikan titik masalah ekonomi | [1] | 279 sumur offshore, 69 rig jackup: 37.866 jam NPT = 8,7% dari 434.076,5 jam operasi; severity US$9.760 per jam NPT; total anggaran US$4,24 miliar | Peer-review (Springer, jurnal akses terbuka) |
| Rentang tarif rig dipakai sebagai batas atas ASUMSI | [1] | Day rate drillship ultra-deepwater US$300.000–1.000.000 per hari | Peer-review, dikutip dari laporan pasar rig |
| Stuck pipe dipilih sebagai mode prioritas | [2] | Stuck pipe ≥25% dari NPT pengeboran; tingkat keberhasilan penanganan turun tajam setelah 4 jam | Sumber industri (glosarium teknis), bukan peer-review |
| Masalah stabilitas lubang sebagai mode tersendiri | [2] | Stabilitas lubang ≈10% NPT, rata-rata US$2 juta per sumur di Laut Utara | Sumber industri, angka spesifik perlu verifikasi lanjut |
| Getaran sebagai penyebab kegagalan BHA | [2] | 20–30% kegagalan alat lubang bawah disebabkan getaran | Sumber industri |
| Urgensi penurunan waktu deteksi | [2] | Rata-rata rig offshore mengalami ≈27 hari downtime tak terencana per tahun, ≈US$38 juta (Kimberlite) | Sumber industri, angka pihak ketiga |
| Kenapa dashboard, bukan laporan periodik | [3] | DSS di ruang kendali menurunkan beban kognitif dan menaikkan performa, tetapi menurunkan situation awareness karena ketergantungan berlebih | Peer-review (MDPI Processes) |
| Kenapa desain advisory, 0 alarm otomatis | [3] | Risiko over-reliance: operator percaya penuh pada sistem dan berhenti memantau; trust adalah faktor kritis adopsi | Peer-review (MDPI Processes) |
| Batas jumlah metrik per layar | [4] | Batasi tampilan ke 6–8 metrik kunci; organisasi dengan dashboard KPI terstruktur 3,4 kali lebih cepat mengenali aset bermasalah kronis | Sumber industri (konsultan), bukan peer-review |
| Risiko alarm flood bila alarm ditambah | [5] | EPRI: alarm flood (>10 alarm per 10 menit) terjadi pada >70% pembangkit fosil saat transien; tata kelola alarm mengikuti ISA 18.2 | Sumber industri, bukan peer-review |
| Kerangka FMECA dan perhitungan RPN | [6] | Definisi, perencanaan, dan pelaporan FMEA/FMECA; varian criticality memakai severity dan bobot kepentingan | Standar internasional (IEC) |
| Tahapan proyek berhenti di State the Problem dan Investigate | [7] | Tujuh aktivitas SIMILAR: State, Investigate, Model, Integrate, Launch, Assess, Re-evaluate | Peer-review (jurnal sistem engineering) |
| Pemilihan solusi dengan TOPSIS | [8] | Metode MADM berbasis jarak ke solusi ideal positif dan negatif | Buku teks rujukan utama (Springer, 1981) |
| Peta alur nilai dan pemborosan waktu tunggu | [9] | Value stream mapping: memetakan aliran nilai dan mengidentifikasi muda | Buku kerja standar industri (Shingo Award 1999) |
| Sumber data dan lisensi | [10] | ≈40.000 berkas, produksi 2008–2016, Equinor Open Data Licence, tanpa registrasi | Sumber primer pemilik data |

## B. Catatan kejujuran atas dua rujukan kunci

Dua rujukan paling menentukan argumen "kenapa dashboard" adalah [3] dan [2]. Keduanya
dipakai dengan pembatasan berikut:

1. **[3] tidak mendukung klaim bahwa dashboard menurunkan NPT.** Yang dibuktikan adalah
   pengaruhnya pada performa operator dan beban kognitif di lingkungan simulasi ruang
   kendali proses kimia, bukan di rig. Karena itu proposal ini memakai [3] hanya untuk
   membenarkan bentuk antarmuka dan pembatasan otomatisasi, bukan untuk mengklaim
   penghematan.
2. **[2] dan [4] dan [5] adalah halaman industri, bukan publikasi peer-review.** Angkanya
   dipakai sebagai rentang indikatif dan selalu diberi label ASUMSI di Lampiran D.
   Satu-satunya angka ekonomi yang berstatus peer-review adalah US$9.760 per jam NPT
   dari [1].

## C. Daftar pustaka

[1] Risk-based budgeting: quantifying Non-Productive Time (NPT) offshore drilling
    financial risk. *Journal of Engineering and Applied Science* (Springer Nature).
    https://doi.org/10.1186/s44147-026-01049-9

[2] GA Drilling. Non-Productive Time (NPT). Glosarium teknis.
    https://www.gadrilling.com/glossary/non-productive-time-npt

[3] Enhancing Control Room Operator Decision Making. *Processes*, 12(2), 328. MDPI.
    https://doi.org/10.3390/pr12020328

[4] Oxand. Predictive Maintenance Dashboards: Which Views Actually Drive Better
    Decisions? https://oxand.com/en/blog/predictive-maintenance-dashboards-drive-better-decisions

[5] iFactory. Control Room Modernization: AI Dashboards & Alarm Management.
    https://ifactoryapp.com/blog/power-plant-control-room-ai-dashboards-alarm-hmi

[6] International Electrotechnical Commission. (2018). *IEC 60812:2018 Failure modes
    and effects analysis (FMEA and FMECA)* (3rd ed.). Geneva: IEC.

[7] Bahill, A. T., & Gissing, B. (1998). Re-evaluating systems engineering concepts
    using systems thinking. *IEEE Transactions on Systems, Man, and Cybernetics,
    Part C*, 28(4), 516–527.

[8] Hwang, C.-L., & Yoon, K. (1981). *Multiple Attribute Decision Making: Methods and
    Applications*. Lecture Notes in Economics and Mathematical Systems, Vol. 186.
    Berlin: Springer-Verlag.

[9] Rother, M., & Shook, J. (1999). *Learning to See: Value Stream Mapping to Add Value
    and Eliminate Muda*. Cambridge, MA: Lean Enterprise Institute.

[10] Equinor. (2018). Volve field data set. Equinor Open Data Licence.
     https://www.equinor.com/energy/volve-data-sharing

## D. Rujukan yang sengaja tidak dipakai

Beberapa sumber ditemukan tetapi tidak dimasukkan karena tidak dapat diverifikasi
kelengkapannya (misalnya makalah yang hanya tersedia sebagai pratinjau, atau situs yang
tidak mencantumkan penulis dan tahun). Kebijakan ini dipegang agar daftar pustaka hanya
berisi entri yang bisa ditelusuri pembaca, meskipun jumlahnya lebih sedikit.
