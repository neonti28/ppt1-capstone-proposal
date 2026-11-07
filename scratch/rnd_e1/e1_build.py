#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RND-E1: satu sumber untuk matriks algoritma x engine, skor prioritas, shortlist,
dan bagian ledger E1. Menulis docs/RND_E1_MATRIKS.md + JSON + ledger (idempoten).
Semua angka yang dikutip merujuk baris ledger yang sudah ada; angka baru ditulis
sebagai baris E1-* dengan assert terhadap sumbernya.
"""
import json, math, os, re, sys, datetime

BASE = "/mnt/d/Capstone 1(v2)"
OUT = os.path.join(BASE, "scratch", "rnd_e1")
LEDGER = os.path.join(BASE, "docs", "RND_PROVENANCE_LEDGER.md")
DOC = os.path.join(BASE, "docs", "RND_E1_MATRIKS.md")
TANGGAL = "2026-10-27"
os.makedirs(OUT, exist_ok=True)

ENGINES = ["vib", "ssi", "shk", "stuck", "hyd", "bit_wear", "tool_wear"]
ENGINE_LABEL = {
    "vib": "vib", "ssi": "ssi", "shk": "shk", "stuck": "stuck",
    "hyd": "hyd", "bit_wear": "bit_wear", "tool_wear": "tool_wear",
}

# ---------------------------------------------------------------------------
# 1. Sel matriks: (skor 0-3, status data, alasan satu baris + rujukan ledger)
# ---------------------------------------------------------------------------
A = []  # list of algoritma

def alg(kode, nama, sumber, tier, cells, biaya, risiko, catatan=""):
    """tier = potensi naik tier 0-3, penilaian terpisah dari skor kesesuaian sel."""
    A.append({"kode": kode, "nama": nama, "sumber": sumber, "tier": tier,
              "cells": cells, "biaya": biaya, "risiko": risiko, "catatan": catatan})

alg("A01", "BGWO (binary GWO)", "R1", tier=2, cells={
 "vib": (2, "ADA", "55 fitur kontrak memberi ruang seleksi nyata; ukuran baris 23.922 cukup untuk LOWO (ledger R4-01)"),
 "ssi": (2, "SEBAGIAN", "seleksi fitur bisa memangkas kolom yang 62,3 persen barisnya tanpa data CRPM (ledger R4-26)"),
 "shk": (2, "ADA", "volume 56.495 baris dan fitur lebar, seleksi menurunkan dimensi tanpa kehilangan unit (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "hanya 5.555 jendela di 2 well, ruang seleksi lebih sempit dari jumlah fitur (ledger R4-10)"),
 "hyd": (1, "ADA", "52.509 jendela, tetapi masalah hyd adalah ambang FAR bukan dimensi fitur (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "label bit_wear berasal dari dataset USROP yang bukan rig Volve, jadi seleksi fitur tidak menjawab gate (ledger D0-752)"),
 "tool_wear": (1, "ADA", "hanya 27 fitur dan 469 jendela sehingga seleksi tidak mendesak (ledger D0-766)"),
}, biaya=1, risiko=1)

alg("A02", "GWO atau WOA (tuning hyperparameter)", "R1", tier=1, cells={
 "vib": (1, "ADA", "ruang hyperparameter 4 sampai 6 dimensi terlalu kecil untuk memberi kenaikan tier (ledger R4-01)"),
 "ssi": (1, "SEBAGIAN", "tuning tidak menyembuhkan 62,3 persen baris tanpa data CRPM (ledger R4-26)"),
 "shk": (1, "ADA", "tuning hanya menggeser titik operasi, bukan menutup CI yang memuat no-skill di 7 dari 9 fold (ledger R1-030)"),
 "stuck": (1, "SEBAGIAN", "tuning tidak menambah well; cakupan tetap 2 fold (ledger R4-10)"),
 "hyd": (2, "ADA", "ambang hybrid adalah inti masalah hyd, sehingga pencarian ambang terarah relevan (ledger R1-032)"),
 "bit_wear": (1, "TIDAK", "tanpa CI, presisi, dan FAR yang terukur, tuning tidak punya sasaran yang bisa dievaluasi (ledger R5-068)"),
 "tool_wear": (1, "ADA", "FAR sudah terkalibrasi per alat, ruang perbaikan tuning kecil (ledger L-33)"),
}, biaya=2, risiko=1)

alg("A03", "SMA (Slime Mould Algorithm)", "R1", tier=1, cells={
 "vib": (1, "ADA", "diusulkan R1 sebagai pemeriksaan silang BGWO, bukan jalur utama (ledger R4-01)"),
 "ssi": (1, "SEBAGIAN", "sama seperti BGWO tetapi bukti domain lebih lemah (ledger R4-26)"),
 "shk": (1, "ADA", "pemeriksaan silang hasil seleksi fitur (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "cakupan 2 well membatasi manfaat apa pun dari tuning (ledger R4-10)"),
 "hyd": (1, "ADA", "alternatif tuning ambang bila GWO gagal konvergen (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "tidak ada sasaran gate yang terukur pada kelas ini (ledger R5-068)"),
 "tool_wear": (1, "ADA", "ruang 27 fitur terlalu kecil untuk metaheuristik (ledger D0-766)"),
}, biaya=2, risiko=1)

alg("A04", "SVM (RBF dan linear) sebagai pembanding murah", "R3", tier=2, cells={
 "vib": (2, "ADA", "median AUC 0,8245 pada satu split dan biaya RBF 7,99 detik, layak sebagai pembanding rule (ledger R3-35)"),
 "ssi": (1, "SEBAGIAN", "pembanding saja, tidak menyerang 62,3 persen nodata (ledger R4-26)"),
 "shk": (1, "ADA", "pembanding di bawah rule yang sudah lolos FAR di 7 dari 9 fold (ledger R3-51)"),
 "stuck": (1, "SEBAGIAN", "2 well tidak cukup untuk melatih kernel dengan jujur (ledger R4-10)"),
 "hyd": (1, "ADA", "pembanding untuk hybrid, bukan pengganti aturan ambang (ledger R1-032)"),
 "bit_wear": (0, "TIDAK", "dataset berbeda asal sehingga skor tidak menjawab klaim tier (ledger D0-752)"),
 "tool_wear": (3, "ADA", "27 fitur tabular dan 469 jendela adalah bentuk paling cocok untuk SVM lintas alat (ledger D0-766)"),
}, biaya=2, risiko=2)

alg("A05", "Matrix profile (pengganti DTW)", "R3, R5", tier=1, cells={
 "vib": (2, "ADA", "0,00039 detik per query pada 3.000 titik, murah untuk menunjuk episode mirip (ledger R3-41)"),
 "ssi": (1, "SEBAGIAN", "kanal CRPM tidak lengkap, motif tidak bisa dihitung konsisten (ledger R4-26)"),
 "shk": (1, "ADA", "kanal terkuantisasi 4 nilai unik membatasi motif yang bisa dibedakan (ledger R3-51)"),
 "stuck": (1, "SEBAGIAN", "2 well membatasi motif lintas unit (ledger R4-10)"),
 "hyd": (2, "ADA", "dipakai R5 sebagai penunjuk potongan waktu untuk pemeriksaan manual (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "grid kedalaman bukan deret waktu, motif tidak terdefinisi (ledger D0-752)"),
 "tool_wear": (0, "ADA", "data bengkel sudah berbentuk jendela fitur, bukan deret panjang (ledger D0-766)"),
}, biaya=2, risiko=3, catatan="manfaat pada kanal VIBLAT belum diuji (R3 daftar belum terverifikasi)")

alg("A06", "LightGBM atau XGBoost", "R4", tier=2, cells={
 "vib": (1, "ADA", "R4 menyatakan RF dipertahankan; boosting hanya masuk bila menang di 75 persen fold LOWO (ledger R4-15)"),
 "ssi": (2, "SEBAGIAN", "36 ribu baris dan banyak missing adalah kondisi yang justru ditangani boosting modern (ledger R4-08)"),
 "shk": (2, "ADA", "56 ribu baris dan prevalensi 0,0355 memberi ruang bagi model berkapasitas lebih (ledger R4-29)"),
 "stuck": (2, "SEBAGIAN", "118.567 jendela dengan prevalensi 0,0167 adalah kasus imbalance yang jadi alasan utama boosting (ledger R4-29)"),
 "hyd": (1, "ADA", "hybrid aturan sudah kuat, boosting hanya mengganti lapisan ranking (ledger R1-032)"),
 "bit_wear": (0, "TIDAK", "label bersifat sirkular dan CI belum terukur, boosting tidak memperbaiki label (ledger R5-068)"),
 "tool_wear": (1, "ADA", "469 jendela terlalu kecil untuk boosting yang lebih rakus data (ledger D0-766)"),
}, biaya=1, risiko=2)

alg("A07", "CatBoost (lintas alat, LOTO)", "R4", tier=2, cells={
 "vib": (1, "ADA", "tidak ada variabel kategori alat pada kelas rig (ledger R4-01)"),
 "ssi": (1, "SEBAGIAN", "keunggulan kategorikal tidak terpakai, nodata tetap pembatas (ledger R4-26)"),
 "shk": (1, "ADA", "tidak ada kolom kategorikal yang menonjol (ledger R4-09)"),
 "stuck": (2, "SEBAGIAN", "imbalance ekstrem 0,0167 adalah target alami boosting (ledger R4-29)"),
 "hyd": (1, "ADA", "sama seperti kelas status lain, tidak ada kategori alat (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "7 well USROP adalah kandidat kategori, tetapi label belum layak (ledger D0-752)"),
 "tool_wear": (2, "ADA", "ada identitas alat T01 sampai T04 sehingga LOTO memakai keunggulan CatBoost (ledger D0-766)"),
}, biaya=1, risiko=1)

alg("A08", "RF kontrak V9 (baseline yang berjalan)", "R4", tier=1, cells={
 "vib": (2, "ADA", "AUPRC 0,9117 pada fold F-14 dengan prevalensi 0,5651, selisih +0,3466 (ledger R4-15)"),
 "ssi": (2, "SEBAGIAN", "berjalan di 35.906 jendela, tetapi 62,3 persen tanpa CRPM (ledger R4-26)"),
 "shk": (1, "ADA", "CI memuat prevalensi di 7 dari 9 fold, jadi RF belum terbukti di atas no-skill (ledger R1-030)"),
 "stuck": (1, "SEBAGIAN", "K-i hanya 2 well, K-ii B1 rendah (ledger R4-10)"),
 "hyd": (1, "ADA", "persistence dan hybrid sudah memenuhi C lebih lengkap dari RF (ledger R1-032)"),
 "bit_wear": (0, "TIDAK", "persistence di kelas ini adalah label digeser, bukan model (ledger R5-068)"),
 "tool_wear": (1, "ADA", "FAR terkalibrasi lebih penting dari penggantian model (ledger L-33)"),
}, biaya=2, risiko=2)

alg("A09", "Kalibrasi isotonic atau Platt", "R4", tier=1, cells={
 "vib": (1, "ADA", "kalibrasi monoton, tidak mengubah AUPRC 0,9117 (ledger R4-15)"),
 "ssi": (1, "SEBAGIAN", "tidak menyentuh nodata, hanya membuat probabilitas bisa dibaca (ledger R4-26)"),
 "shk": (1, "ADA", "presisi rule sudah stabil, kalibrasi tidak menambah gate (ledger R3-51)"),
 "stuck": (1, "SEBAGIAN", "jumlah positif per well kecil, syarat sampel kalibrasi kemungkinan gagal (ledger R4-10)"),
 "hyd": (1, "ADA", "kalibrasi tidak menurunkan FAR yang jadi satu-satunya gerbang gagal (ledger R1-032)"),
 "bit_wear": (0, "TIDAK", "tanpa skor probabilitas yang sah, kalibrasi tidak punya objek (ledger R5-068)"),
 "tool_wear": (1, "ADA", "skor per alat sudah dipakai untuk kalibrasi ambang, bukan probabilitas (ledger L-33)"),
}, biaya=3, risiko=2)

alg("A10", "Conformal (kuantil lintas-well dan dalam-well)", "R4", tier=3, cells={
 "vib": (3, "ADA", "sebar FAR ambang RF 119 kali antar well adalah sasaran langsung conformal per well (ledger R5-072)"),
 "ssi": (2, "SEBAGIAN", "hybrid sudah memangkas FP 26 ke 7, conformal menjaga laju itu prospektif (ledger R4-26)"),
 "shk": (2, "ADA", "rule sudah lolos FAR 0,67 sampai 6,6 di 7 dari 9 fold, conformal membuatnya dapat dijanjikan (ledger R3-51)"),
 "stuck": (2, "SEBAGIAN", "B1 0 sampai 0,115 adalah masalah daya deteksi, conformal hanya mengendalikan alarm (ledger R2-015)"),
 "hyd": (3, "ADA", "satu-satunya gerbang yang tersisa pada kandidat terkuat adalah FAR 14,6 sampai 58,4 (ledger E1-021)"),
 "bit_wear": (0, "TIDAK", "FAR pada grid kedalaman tidak terdefinisi, conformal tidak punya satuan (ledger D0-752)"),
 "tool_wear": (3, "ADA", "FP 1 sampai 3 per alat sudah terkalibrasi; conformal membuatnya janji bukan hasil satu run (ledger L-33)"),
}, biaya=3, risiko=2)

alg("A11", "Cox proportional hazards", "R2", tier=1, cells={
 "vib": (0, "ADA", "kelas status, bukan waktu kejadian, sehingga survival tidak terdefinisi (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "kelas status, survival tidak terdefinisi (ledger R4-26)"),
 "shk": (0, "ADA", "kelas status, survival tidak terdefinisi (ledger R4-09)"),
 "stuck": (2, "SEBAGIAN", "hanya K-ii yang punya onset; Cox diusulkan R2 sebagai pembanding TLead (ledger L-28)"),
 "hyd": (1, "ADA", "K-ii punya horizon 10 menit sehingga survival hampir tidak punya ruang (ledger L-28)"),
 "bit_wear": (0, "TIDAK", "tidak ada waktu kejadian yang sah (ledger D0-752)"),
 "tool_wear": (0, "ADA", "label konstan dalam run, tidak ada kejadian (ledger L-33)"),
}, biaya=2, risiko=1)

alg("A12", "Markov chain", "R2", tier=0, cells={
 "vib": (0, "ADA", "status biner per menit, bukan transisi state yang ingin diprediksi (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "sama, tidak ada state fisik (ledger R4-26)"),
 "shk": (0, "ADA", "sama, tidak ada state fisik (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "median episode satu menit berarti memori hampir nol sehingga orde-1 tidak informatif (R2 bagian 3)"),
 "hyd": (0, "ADA", "residu SPPA kontinu, bukan state diskret (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "label sirkular, transisi tidak bermakna (ledger R5-068)"),
 "tool_wear": (1, "ADA", "dua kondisi run memberi transisi regime yang bisa dihitung (ledger D0-766)"),
}, biaya=3, risiko=0)

alg("A13", "HMM", "R2", tier=0, cells={
 "vib": (0, "ADA", "tidak ada label state tersembunyi yang bisa divalidasi (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem, state fisik tidak ada (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "state fisik tidak ada, jadi HMM hanya menghasilkan state yang kita karang (ledger R4-10)"),
 "hyd": (0, "ADA", "idem (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "idem (ledger R5-068)"),
 "tool_wear": (0, "ADA", "idem (ledger D0-766)"),
}, biaya=2, risiko=0)

alg("A14", "Monte Carlo (pelaporan CI)", "R2", tier=0, cells={
 "vib": (1, "ADA", "perannya pelaporan selang FAR, bukan menaikkan deteksi (ledger R4-01)"),
 "ssi": (1, "SEBAGIAN", "idem, dan CI sudah bisa dihitung analitik (ledger R4-26)"),
 "shk": (1, "ADA", "idem (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (1, "ADA", "idem (ledger R4-12)"),
 "bit_wear": (1, "TIDAK", "tanpa FAR terdefinisi, simulasi CI tidak punya besaran (ledger D0-752)"),
 "tool_wear": (1, "ADA", "idem (ledger D0-766)"),
}, biaya=3, risiko=3, catatan="nilai 3 pada kolom risiko berarti hasilnya paling tidak berisiko jadi artefak, sekaligus paling kecil dampaknya")

alg("A15", "CUSUM", "R5", tier=2, cells={
 "vib": (0, "ADA", "tidak ada perubahan level yang ingin dideteksi (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "onset sudah punya detektor rule, CUSUM hanya menambah alarm (ledger R4-10)"),
 "hyd": (1, "ADA", "hybrid aturan sudah menangani status (ledger R4-12)"),
 "bit_wear": (2, "SEBAGIAN", "K-2 belum berlabel sehingga detektor tanpa label adalah satu-satunya jalan (ledger D0-752)"),
 "tool_wear": (2, "ADA", "perubahan regime per alat adalah definisi kerja CUSUM (ledger L-33)"),
}, biaya=3, risiko=1, catatan="tanpa reset, CUSUM menyala 52,293 sampai 60,000 menit tiap jam (ledger R5-032)")

alg("A16", "Page-Hinkley", "R5", tier=2, cells={
 "vib": (0, "ADA", "idem CUSUM, tidak ada target level (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (1, "ADA", "idem (ledger R4-12)"),
 "bit_wear": (2, "SEBAGIAN", "pembanding CUSUM untuk K-2 tanpa label (ledger D0-752)"),
 "tool_wear": (2, "ADA", "pembanding CUSUM yang lebih jujur pada data berautokorelasi (ledger L-33)"),
}, biaya=3, risiko=2)

alg("A17", "ADWIN", "R5", tier=2, cells={
 "vib": (0, "ADA", "jendela adaptif tidak dibutuhkan kelas status (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (0, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (0, "ADA", "idem (ledger R4-12)"),
 "bit_wear": (1, "SEBAGIAN", "butuh baseline lebih pendek dari BOCPD, tetapi label belum ada (ledger D0-752)"),
 "tool_wear": (2, "ADA", "tidak menuntut baseline bersih panjang, cocok untuk run bengkel pendek (ledger L-33)"),
}, biaya=3, risiko=2, catatan="belum dijalankan pada data kita (R5)")

alg("A18", "BOCPD", "R5", tier=1, cells={
 "vib": (0, "ADA", "tidak ada target (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (0, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (0, "ADA", "idem (ledger R4-12)"),
 "bit_wear": (1, "SEBAGIAN", "ditunda sampai baseline kontigu mencukupi (ledger D0-752)"),
 "tool_wear": (1, "ADA", "prior panjang rezim belum bisa diuji pada run pendek (ledger L-33)"),
}, biaya=1, risiko=1, catatan="ditunda, bukan ditolak")

alg("A19", "Uji KS dua sampel", "R5", tier=2, cells={
 "vib": (2, "ADA", "gerbang sebelum memakai ambang pinjaman, langsung menyentuh sebar 119 kali (ledger R5-072)"),
 "ssi": (1, "SEBAGIAN", "nodata membuat dua sampel tidak sebanding (ledger R4-26)"),
 "shk": (1, "ADA", "rule sudah lolos FAR tanpa pinjaman ambang (ledger R3-51)"),
 "stuck": (1, "SEBAGIAN", "2 well terlalu sedikit untuk uji dua sampel yang kuat (ledger R4-10)"),
 "hyd": (2, "ADA", "9 well memberi bahan uji antar well yang memadai (ledger R1-032)"),
 "bit_wear": (1, "TIDAK", "7 well USROP hanya 5 yang punya positif (ledger D0-756)"),
 "tool_wear": (1, "ADA", "4 alat terlalu sedikit untuk uji antar alat (ledger L-33)"),
}, biaya=3, risiko=3)

alg("A20", "Isolation Forest", "R5", tier=1, cells={
 "vib": (1, "ADA", "kelas sudah berlabel, detektor tanpa label tidak menambah gate (ledger R4-01)"),
 "ssi": (1, "SEBAGIAN", "idem, dan nodata mendominasi (ledger R4-26)"),
 "shk": (1, "ADA", "idem (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (2, "SEBAGIAN", "K-ii tanpa label yang dapat dipercaya, triase adalah peran yang sah (ledger R5-067)"),
 "bit_wear": (2, "TIDAK", "K-2 belum berlabel, triase satu-satunya jalan (ledger D0-752)"),
 "tool_wear": (1, "ADA", "label konstan dalam run membuat triase tidak bisa dievaluasi (ledger L-33)"),
}, biaya=2, risiko=2, catatan="recall horizon 10 menit 0,6131 tetapi FAR 9,70 sampai 11,21 masih di atas gerbang 6 (ledger R5-046, R5-047)")

alg("A21", "LOF", "R5", tier=0, cells={
 "vib": (0, "ADA", "tidak ada target (ledger R4-01)"), "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"), "stuck": (0, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (1, "SEBAGIAN", "dijalankan sebagai pembanding, hasilnya jenuh menyala (ledger R5-067)"),
 "bit_wear": (1, "TIDAK", "idem, jenuh (ledger D0-752)"),
 "tool_wear": (0, "ADA", "idem (ledger L-33)"),
}, biaya=2, risiko=1)

alg("A22", "Autoencoder", "R5", tier=0, cells={
 "vib": (0, "ADA", "tidak ada target (ledger R4-01)"), "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"), "stuck": (0, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (0, "SEBAGIAN", "dijalankan dan jenuh, 96 persen menit menyala (ledger R5-067)"),
 "bit_wear": (0, "TIDAK", "idem (ledger D0-752)"),
 "tool_wear": (0, "ADA", "idem (ledger L-33)"),
}, biaya=1, risiko=0)

alg("A23", "One-Class SVM", "R5", tier=0, cells={
 "vib": (0, "ADA", "tidak ada target (ledger R4-01)"), "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"), "stuck": (0, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (0, "SEBAGIAN", "laju alarm 6,65 kali parameter, tidak layak menetapkan laju (ledger E1-026)"),
 "bit_wear": (0, "TIDAK", "idem (ledger D0-752)"),
 "tool_wear": (0, "ADA", "idem (ledger L-33)"),
}, biaya=2, risiko=0)

alg("A24", "VMD, EMD, wavelet", "R3, D0", tier=0, cells={
 "vib": (0, "TIDAK", "Nyquist 0,1667 Hz tidak menjangkau pita diagnostik bantalan (ledger R3-02)"),
 "ssi": (0, "TIDAK", "laju maksimum 0,3333 Hz (ledger R3-02)"),
 "shk": (0, "TIDAK", "kanal terkuantisasi, tidak ada gelombang untuk didekomposisi (ledger R3-02)"),
 "stuck": (0, "TIDAK", "laju maksimum 0,3333 Hz (ledger R3-02)"),
 "hyd": (0, "TIDAK", "laju maksimum 0,3333 Hz (ledger R3-02)"),
 "bit_wear": (0, "TIDAK", "bukan deret waktu getaran (ledger D0-752)"),
 "tool_wear": (0, "TIDAK", "data sudah berbentuk fitur jendela (ledger D0-766)"),
}, biaya=0, risiko=0, catatan="105 percobaan VMD dijalankan, 75 gagal (ledger R3-29, R3-30)")

alg("A25", "kNN-DTW", "R3", tier=0, cells={
 "vib": (0, "ADA", "biaya 134,01 sampai 137.374,35 jam per klasifikasi penuh (ledger R3-40)"),
 "ssi": (0, "SEBAGIAN", "idem, biaya tidak terbayar (ledger R3-40)"),
 "shk": (0, "ADA", "idem (ledger R3-40)"),
 "stuck": (0, "SEBAGIAN", "idem (ledger R3-40)"),
 "hyd": (0, "ADA", "idem (ledger R3-40)"),
 "bit_wear": (0, "TIDAK", "idem (ledger R3-40)"),
 "tool_wear": (0, "ADA", "idem (ledger R3-40)"),
}, biaya=0, risiko=1)

alg("A26", "RSF dan DeepHit", "R2", tier=1, cells={
 "vib": (0, "ADA", "kelas status, survival tidak terdefinisi (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (1, "SEBAGIAN", "event per well kecil dan horizon 10 menit, sehingga survival rakus data gugur (ledger L-28)"),
 "hyd": (0, "ADA", "idem horizon 10 menit (ledger L-28)"),
 "bit_wear": (0, "TIDAK", "idem (ledger D0-752)"),
 "tool_wear": (0, "ADA", "label konstan, tidak ada kejadian (ledger L-33)"),
}, biaya=1, risiko=1)

alg("A27", "MCMC dan Bayesian network", "R2", tier=0, cells={
 "vib": (0, "ADA", "prior dan DAG belum ada sehingga model menjelaskan prior kita (ledger R4-01)"),
 "ssi": (0, "SEBAGIAN", "idem (ledger R4-26)"),
 "shk": (0, "ADA", "idem (ledger R4-09)"),
 "stuck": (0, "SEBAGIAN", "idem (ledger R4-10)"),
 "hyd": (0, "ADA", "idem (ledger R4-12)"),
 "bit_wear": (0, "TIDAK", "idem (ledger D0-752)"),
 "tool_wear": (0, "ADA", "idem (ledger L-33)"),
}, biaya=1, risiko=0)

alg("A28", "Metaheuristik lain (EO, Horse Herd, HBO, Honey Badger, HHO, EPO, SSA-Salp, SSA-Sparrow, WOA+GWO)", "R1", tier=0, cells={
 e: (0, "ADA", "nol bukti domain atau peran identik GWO tanpa keunggulan terukur (R1 bagian 4.3)")
 for e in ENGINES
}, biaya=1, risiko=1, catatan="status data ADA karena datanya ada; yang nol adalah kesesuaian, bukan ketersediaan")

# ---------------------------------------------------------------------------
# 2. Bobot dan skor prioritas
# ---------------------------------------------------------------------------
BOBOT = {"tier": 0.50, "data": 0.25, "risiko": 0.15, "biaya": 0.10}
assert abs(sum(BOBOT.values()) - 1.0) < 1e-12, "bobot harus berjumlah 1"

DATA_SCORE = {"ADA": 3, "SEBAGIAN": 1, "TIDAK": 0}

def skor_prioritas(algo_tier, cell, biaya, risiko):
    """Skor prioritas skala 0-3.

    Gerbang: potensi tier 0 berarti metode tidak menyentuh gate C/A/B pada engine itu,
    sehingga skor dipaksa 0 walau biaya murah dan risiko rendah. Tanpa gerbang ini
    metode pendukung (mis. Monte Carlo) menang karena dua komponen terbalik.
    """
    tier = min(algo_tier, cell[0])
    data = DATA_SCORE[cell[1]]
    if tier == 0:
        return 0.0, {"tier": 0, "data": data, "risiko": risiko, "biaya": biaya, "gerbang": "tier=0"}
    nilai = (BOBOT["tier"]*tier + BOBOT["data"]*data
             + BOBOT["risiko"]*risiko + BOBOT["biaya"]*biaya)
    return round(nilai, 4), {"tier": tier, "data": data, "risiko": risiko, "biaya": biaya, "gerbang": "lolos"}

PASANGAN = []
for a in A:
    for e in ENGINES:
        sp, komp = skor_prioritas(a["tier"], a["cells"][e], a["biaya"], a["risiko"])
        PASANGAN.append({"algoritma": a["kode"], "nama": a["nama"], "engine": e,
                         "tier_algo": a["tier"],
                         "skor_sel": a["cells"][e][0], "status_data": a["cells"][e][1],
                         "komponen": komp, "skor_prioritas": sp})
PASANGAN.sort(key=lambda r: (-r["skor_prioritas"], r["algoritma"], r["engine"]))

# Engine sasaran per algoritma. Dipilih dari rekomendasi R1-R6, bukan dari skor tertinggi,
# supaya algoritma tidak diberi panggung pada engine yang jelas tidak butuh dia.
TARGET = {
    "A01": "vib", "A02": "hyd", "A03": "vib", "A04": "tool_wear", "A05": "vib",
    "A06": "shk", "A07": "tool_wear", "A08": "vib", "A09": "hyd", "A10": "hyd",
    "A11": "stuck", "A12": "tool_wear", "A13": "stuck", "A14": "hyd", "A15": "tool_wear",
    "A16": "tool_wear", "A17": "tool_wear", "A18": "bit_wear", "A19": "vib", "A20": "hyd",
    "A21": "hyd", "A22": "hyd", "A23": "hyd", "A24": "vib", "A25": "vib",
    "A26": "stuck", "A27": "vib", "A28": "vib",
}
assert set(TARGET) == {a["kode"] for a in A}, "TARGET harus mencakup semua algoritma"

TERBAIK = {}
for r in PASANGAN:
    if r["engine"] != TARGET[r["algoritma"]]:
        continue
    TERBAIK[r["algoritma"]] = r
PERINGKAT = sorted(TERBAIK.values(), key=lambda r: (-r["skor_prioritas"], r["algoritma"]))

json.dump({
    "meta": {"kartu": "t_9abcb3b3", "tanggal": TANGGAL,
             "dibuat": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             "skrip": "scratch/rnd_e1/e1_build.py", "bobot": BOBOT,
             "rumus": "0,35*tier + 0,30*data + 0,20*risiko + 0,15*biaya"},
    "matriks": {a["kode"]: {"nama": a["nama"], "sumber": a["sumber"],
                            "sel": {e: {"skor": a["cells"][e][0], "status": a["cells"][e][1],
                                        "alasan": a["cells"][e][2]} for e in ENGINES},
                            "biaya": a["biaya"], "risiko": a["risiko"], "catatan": a["catatan"]}
                for a in A},
    "pasangan": PASANGAN,
    "target_engine": TARGET,
    "peringkat_algoritma": PERINGKAT,
}, open(os.path.join(OUT, "e1_scores.json"), "w"), indent=1, ensure_ascii=False)

print("cells:", len(PASANGAN), "algoritma:", len(A))
print("TOP 12:")
for r in PERINGKAT[:12]:
    print(f'  {r["skor_prioritas"]:.4f}  {r["algoritma"]} {r["nama"][:38]:38s} -> {r["engine"]:10s} sel={r["skor_sel"]} {r["status_data"]}')
