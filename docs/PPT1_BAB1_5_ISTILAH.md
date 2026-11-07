# BAB I 1.5: ISTILAH DAN PENAMAAN

Bagian ini menetapkan istilah yang dipakai di seluruh proposal, karena tiga kata berbeda sering tertukar: apa yang dideteksi, alat yang mendeteksinya, dan metode yang dipakai. Penetapan ini bukan soal gaya bahasa, melainkan soal menghindari salah baca pada angka dan pada klaim.

## 1.5.1 Mode kegagalan

**Mode kegagalan adalah bentuk atau cara kerja suatu sistem bisa gagal**, bukan alat dan bukan metode. Istilah ini sama dengan *failure mode* pada analisis keandalan (FMECA), yang sudah dipakai pada Bab II.

Penjelasan untuk pembaca non-teknis: sepeda motor bisa rusak dengan beberapa cara berbeda, misalnya ban bocor, rantai lepas, atau aki soak. Keempatnya adalah "mode" kerusakan. Tiap mode punya tanda, penanganan, dan biaya yang berbeda. Kalimat "motor saya rusak" tidak cukup untuk bertindak, karena yang harus diketahui adalah bentuk kerusakannya. Hal yang sama berlaku pada rangkaian pengeboran.

Tujuh mode kegagalan yang menjadi sasaran rancangan ini:

| Kode | Mode kegagalan | Penjelasan sederhana | Tanda fisis yang dipakai |
|---|---|---|---|
| `vib` | Getaran rangkaian bor | Rangkaian bergetar dan membentur dinding lubang, sehingga peralatan aus lebih cepat | Kanal status getaran dan risiko hentakan MWD |
| `ssi` | Stick-slip | Putaran bor tersendat: berputar, tertahan, lalu terlepas berulang | Kanal putaran dan torsi permukaan |
| `shk` | Hentakan (*shock*) | Beban kejut berulang pada rangkaian, seperti palu memukul berulang | Kanal risiko hentakan MWD |
| `stuck` | Pipa terjepit | Rangkaian tidak dapat naik atau turun karena terjepit dinding lubang | Kanal status pipa terjepit dan riwayat tarikan |
| `hyd` | Masalah hidraulik sumur | Tekanan dan laju alir tidak sesuai rancangan, berisiko masuknya fluida formasi atau hilangnya lumpur | Tekanan standpipe dan laju alir |
| `bit_wear` | Keausan mata bor | Mata bor kehilangan ketajaman, laju penembusan menurun | Energi spesifik mekanis |
| `tool_wear` | Keausan peralatan | Peralatan permukaan dan bengkel turun kinerja dan perlu perawatan | Riwayat pemakaian alat dan pengukuran bengkel |

Dua mode terakhir berada pada domain berbeda: `bit_wear` pada rangkaian lubang bawah, `tool_wear` pada peralatan permukaan dan bengkel. Karena itu waktu terdepannya tidak boleh dijumlahkan, seperti dinyatakan pada bagian 1.4.

## 1.5.2 Detektor

**Detektor adalah pelaksana yang menghasilkan peringatan untuk satu mode kegagalan.** Satu detektor bisa berupa aturan ambang, pembanding jendela sebelumnya (*persistence*), gabungan keduanya, atau model yang dilatih. Istilah ini dipakai ketika yang dibicarakan adalah barang yang berjalan dan menghasilkan keluaran, misalnya "detektor pipa terjepit memperoleh presisi 0,92".

## 1.5.3 Head

**Head adalah satu varian metode yang dievaluasi di dalam satu mode.** Tujuh mode memiliki 27 head pada registry, contohnya `rule`, `persistence_event`, dan `hybrid_rule_and_persistence`. Head dipakai ketika yang dibicarakan adalah slot evaluasi yang punya angka sendiri (presisi, recall, laju alarm palsu), bukan mode dan bukan alat utuh.

## 1.5.4 Engine

**Kata engine dipakai hanya untuk mesin atau algoritma**, misalnya *engine* pencarian hyperparameter otomatis (H2O AutoML), *rule engine*, atau *engine* pembelajaran mesin. Kata ini tidak dipakai lagi untuk menyebut mode kegagalan.

Draf sebelum revisi ini memakai kata "engine" untuk menyebut mode kegagalan (`engine vib`, `engine ssi`), sehingga satu kata menunjuk dua hal sekaligus dan maknanya bergantung konteks. Pada versi ini seluruh penyebutan mode memakai kata "mode", dan penyebutan pelaksana memakai kata "detektor".

## 1.5.5 Ringkasan pemakaian

| Istilah | Arti | Contoh pemakaian yang benar | Contoh pemakaian yang salah |
|---|---|---|---|
| Mode kegagalan | Bentuk kegagalan yang dideteksi | "tujuh mode kegagalan", "mode getaran" | "engine getaran" |
| Detektor | Pelaksana yang menghasilkan peringatan | "detektor pipa terjepit memberi presisi 0,92" | "mode pipa terjepit memberi presisi", karena mode tidak memberi angka |
| Head | Satu varian metode dalam satu mode | "27 head, 13 di antaranya wajib tinjauan manusia" | "27 mode" |
| Engine | Mesin atau algoritma | "engine pencarian otomatis H2O" | "engine vib" |

## 1.5.6 Konsekuensi pada penamaan berkas dan kunci data

Kunci data yang sudah terlanjur memakai kata `engine` tidak diubah agar hasil yang
tersimpan tetap dapat ditelusuri apa adanya, misalnya larik `engines[]` pada berkas
hasil eksekusi detektor. Di dalam naskah, kunci itu hanya dikutip sebagai nama berkas,
sedangkan konsepnya ditulis sebagai mode deteksi dan head seperti pada 1.5.5.

