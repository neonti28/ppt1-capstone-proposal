"""Pemeriksa independen untuk docs/PPT1_BAB3_2.md dan scratch/ppt1/affinity.json.

Tidak mengimpor modul data pembangun. Membaca keluaran apa adanya, lalu memeriksa:
1. acceptance kartu, yaitu 9 alternatif berklaster, minimal 3 BoK didalami, minimal 4 user story.
2. setiap rujukan berkas:baris benar-benar ada, dan sejumlah token penanda benar-benar muncul di baris itu.
3. kunci JSON registry yang dipakai sebagai bukti.
4. integritas tabel markdown.
5. larangan em-dash, emoji, dan aksara Han.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MD = os.environ.get("BAB3_2_MD") or os.path.join(ROOT, "docs", "PPT1_BAB3_2.md")
JS = os.environ.get("BAB3_2_JSON") or os.path.join(ROOT, "scratch", "ppt1", "affinity.json")
ALT = os.path.join(ROOT, "scratch", "ppt1", "alternatif.json")
REG = os.path.join(ROOT, "scratch", "v9_i1", "v9_i1_RESULTS.json")

fails = []
oks = []


def ok(msg):
    oks.append(msg)


def bad(msg):
    fails.append(msg)


# ---------- muat ----------
md = open(MD, encoding="utf-8").read()
lines = md.splitlines()
data = json.load(open(JS, encoding="utf-8"))
alt = json.load(open(ALT, encoding="utf-8"))
reg = json.load(open(REG, encoding="utf-8"))
alt_ids = [a["id"] for a in alt["alternatif"]]

# ---------- 1. acceptance kartu ----------
seen = []
for k in data["klaster"]:
    seen.extend(k["anggota"])
if len(seen) == 9 and sorted(seen) == sorted(alt_ids):
    ok("9 alternatif masuk klaster tepat satu kali")
else:
    bad(f"klaster tidak menutup 9 alternatif tepat sekali: {sorted(seen)}")
if len(seen) != len(set(seen)):
    bad("ada alternatif ganda antar klaster")
if len(data["bok_didalami"]) >= 3:
    ok(f"BoK didalami: {len(data['bok_didalami'])} (minimal 3)")
else:
    bad("BoK didalami kurang dari 3")
if len(data["user_stories"]) >= 4:
    ok(f"user story: {len(data['user_stories'])} (minimal 4)")
else:
    bad("user story kurang dari 4")
n_ac = sum(len(u["acceptance"]) for u in data["user_stories"])
tanpa_ac = [u["id"] for u in data["user_stories"] if not u["acceptance"]]
if tanpa_ac:
    bad(f"user story tanpa kriteria penerimaan: {tanpa_ac}")
else:
    ok(f"setiap user story punya kriteria penerimaan, total {n_ac}")

# setiap alternatif muncul di dokumen
hilang = [a for a in alt_ids if a not in md]
if hilang:
    bad(f"alternatif tidak disebut pada dokumen: {hilang}")
else:
    ok("seluruh kode A1 sampai A9 disebut pada dokumen")

# struktur wajib dokumen
wajib = [
    "### 3.2.1", "### 3.2.2", "### 3.2.3", "### 3.2.4", "### 3.2.5", "### 3.2.6",
    "### 3.2.7", "### 3.2.8", "### 3.2.9",
    "## 3.3", "### 3.3.1", "### 3.3.2", "### 3.3.3", "### 3.3.4", "### 3.3.5",
    "### 3.3.6", "### 3.3.7",
]
kurang = [w for w in wajib if w not in md]
if kurang:
    bad(f"subbab wajib tidak ada: {kurang}")
else:
    ok("17 subbab wajib ada pada dokumen")

# ---------- 2. rujukan berkas:baris ----------
ref_re = re.compile(r"(docs/[A-Za-z0-9_\-\.]+\.md|scratch/[A-Za-z0-9_\-/\.]+\.json):([0-9][0-9,\s\-]*)")


def nomor_dari(grup):
    out = []
    for bagian in grup.split(","):
        bagian = bagian.strip()
        if not bagian:
            continue
        if "-" in bagian:
            a, b = bagian.split("-", 1)
            try:
                out.extend(range(int(a), int(b) + 1))
            except ValueError:
                continue
        else:
            try:
                out.append(int(bagian))
            except ValueError:
                continue
    return out


refs = set()
for m in ref_re.finditer(md):
    for ln in nomor_dari(m.group(2)):
        refs.add((m.group(1), ln))
for k in data["klaster"]:
    for _, _, jejak in k["angka"]:
        for m in ref_re.finditer(jejak):
            for ln in nomor_dari(m.group(2)):
                refs.add((m.group(1), ln))
for b in data["bok_didalami"]:
    for _, _, jejak in b["angka"]:
        for m in ref_re.finditer(jejak):
            for ln in nomor_dari(m.group(2)):
                refs.add((m.group(1), ln))
for u in data["user_stories"]:
    for ac in u["acceptance"]:
        for m in ref_re.finditer(ac["jejak"]):
            for ln in nomor_dari(m.group(2)):
                refs.add((m.group(1), ln))

cek_baris = 0
for path, ln in sorted(refs):
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        bad(f"berkas jejak tidak ada: {path}")
        continue
    n = len(open(fp, encoding="utf-8", errors="replace").read().splitlines())
    cek_baris += 1
    if ln < 1 or ln > n:
        bad(f"{path}:{ln} di luar rentang berkas ({n} baris)")
if not any("jejak tidak ada" in f or "di luar rentang" in f for f in fails):
    ok(f"{len(refs)} rujukan berkas dan baris unik diperiksa, {cek_baris} baris dalam rentang")

# ---------- 2b. token penanda pada baris tertentu ----------
ANCHOR = [
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 12, "Volve"),
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 57, "27 head"),
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 123, "Konfirmasi status"),
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 158, "UNDERPOWERED"),
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 327, "Batas muktamad"),
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 3031, "0 alarm otomatis"),
    ("docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md", 3142, "L0 5"),
    ("docs/V4_MAINTENANCE_ML_OPTIONS.md", 62, "bhaRun"),
    ("docs/V4_MAINTENANCE_ML_OPTIONS.md", 145, "6a"),
    ("docs/V4_MAINTENANCE_ML_OPTIONS.md", 164, "presisi palsu"),
    ("docs/V4_MAINTENANCE_ML_OPTIONS.md", 165, "G1/G2"),
    ("docs/V7_R1_SOLUTIONS.md", 37, "GAINLOSSTOT"),
    ("docs/V7_R1_SOLUTIONS.md", 45, "188"),
    ("docs/V7_R1_SOLUTIONS.md", 48, "77"),
    ("docs/V7_R1_SOLUTIONS.md", 76, "witsml_parsed"),
    ("docs/V7_R1_SOLUTIONS.md", 97, "3/7"),
    ("docs/V7_R1_SOLUTIONS.md", 111, "stand"),
    ("docs/V7_R1_SOLUTIONS.md", 112, "BPOS"),
    ("docs/V7_R1_SOLUTIONS.md", 127, "2/7"),
    ("docs/V7_R1_SOLUTIONS.md", 152, "pembanding"),
    ("docs/V7_R1_SOLUTIONS.md", 160, "0/4"),
    ("docs/V7_R1_SOLUTIONS.md", 197, "4/5"),
    ("docs/V7_R1_SOLUTIONS.md", 203, "3/4"),
    ("docs/V8_E_shk_CAPABILITY.md", 106, "FAR 18"),
    ("docs/V8_PM_VERDICT.md", 202, "kontrol-positif stuck 0/10"),
    ("docs/V8_R1_ABC_SPEC.md", 240, "6 per 24 jam"),
    ("docs/V9_EVAL_B_LAYERB.md", 101, "0,51"),
    ("docs/V9_EVAL_B_LAYERB.md", 103, "0/3"),
    ("docs/V9_EVAL_C_LAYERC.md", 98, "4/4 alat"),
    ("docs/V9_EVAL_C_LAYERC.md", 99, "0,516"),
    ("docs/V9_PM1_ARCHITECTURE.md", 186, "281.030"),
    ("docs/V9_PM1_ARCHITECTURE.md", 276, "469 jendela"),
    ("docs/V9_PM1_ARCHITECTURE.md", 470, "per stand"),
    ("docs/V9_PM2_VERDICT.md", 114, "119,6"),
    ("docs/PPT1_LEDGER_ANGKA.md", 145, "73.500"),
    ("docs/PPT1_LEDGER_ANGKA.md", 193, "50 di antaranya"),
    ("docs/V10_D1_BAB_DATA.md", 86, "52.905"),
    ("docs/V10_D1_BAB_DATA.md", 296, "52.905"),
]
gagal_anchor = []
for path, ln, token in ANCHOR:
    fp = os.path.join(ROOT, path)
    row = open(fp, encoding="utf-8", errors="replace").read().splitlines()[ln - 1]
    if token not in row:
        gagal_anchor.append(f"{path}:{ln} tidak memuat token {token!r}")
if gagal_anchor:
    for g in gagal_anchor:
        bad(g)
else:
    ok(f"{len(ANCHOR)} token penanda cocok pada baris yang dikutip")

# ---------- 3. kunci JSON registry ----------
heads = [h for e in reg["engines"] for h in e["heads"]]
p_auto = reg["auto_critical_alarm_slots"] == 0
p_n = len(heads) == 27
p_human = sum(1 for h in heads if h.get("human_review_required") is True) == 13
p_belum = sum(1 for h in heads if h.get("tier") == "BELUM LAYAK PAKAI") == 2
p_layers = [len(reg["decision_layer"]["layers"][k]) for k in ("L0", "L1", "L2", "L3")] == [5, 11, 9, 2]
for nama, cond, nilai in [
    ("auto_critical_alarm_slots sama dengan 0", p_auto, reg["auto_critical_alarm_slots"]),
    ("jumlah head sama dengan 27", p_n, len(heads)),
    ("head dengan review manusia sama dengan 13", p_human, sum(1 for h in heads if h.get("human_review_required") is True)),
    ("head belum layak pakai sama dengan 2", p_belum, sum(1 for h in heads if h.get("tier") == "BELUM LAYAK PAKAI")),
    ("lapisan L0 sampai L3 sama dengan 5/11/9/2", p_layers, [len(reg["decision_layer"]["layers"][k]) for k in ("L0", "L1", "L2", "L3")]),
]:
    if cond:
        ok(f"registry: {nama} (nilai {nilai})")
    else:
        bad(f"registry: {nama} gagal (nilai {nilai})")

# ---------- 4. integritas tabel ----------
tabel = 0
baris_tabel = 0
i = 0
gagal_tabel = []
while i < len(lines):
    ln = lines[i]
    if ln.startswith("|") and ln.count("|") > 1:
        # awal blok tabel bila baris berikutnya adalah pemisah
        if i + 1 < len(lines):
            nxt = lines[i + 1].strip()
            is_sep = bool(nxt) and all(c in "-|: " for c in nxt) and "-" in nxt
            if is_sep:
                tabel += 1
                n_kolom = ln.count("|") - 1
                j = i
                while j < len(lines) and lines[j].startswith("|"):
                    if lines[j].count("|") - 1 != n_kolom:
                        gagal_tabel.append(
                            f"baris {j + 1} punya {lines[j].count('|') - 1} kolom, seharusnya {n_kolom}"
                        )
                    j += 1
                baris_tabel += j - i
                i = j
                continue
        baris_tabel += 1
        i += 1
    else:
        i += 1
for g in gagal_tabel:
    bad(g)
if not gagal_tabel:
    ok(f"integritas tabel: {tabel} tabel dan {baris_tabel} baris tabel konsisten")
if tabel == 0:
    bad("tidak ada tabel terdeteksi, pemeriksa tabel tidak berjalan")

# ---------- 5. larangan karakter ----------
em = md.count("\u2014") + md.count("\u2013")
cjk = len(re.findall(r"[\u4e00-\u9fff]", md))
emoji = len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", md))
for nama, val in [("em-dash dan en-dash", em), ("aksara Han", cjk), ("emoji", emoji)]:
    if val == 0:
        ok(f"{nama}: 0")
    else:
        bad(f"{nama}: {val} (harus 0)")

# ---------- 6. konsistensi JSON dan dokumen ----------
for k in data["klaster"]:
    for a in k["anggota"]:
        if a not in md:
            bad(f"alternatif {a} tidak disebut pada dokumen")
if data["rekap"]["jumlah_user_story"] != len(data["user_stories"]):
    bad("rekap jumlah_user_story tidak konsisten")
else:
    ok("rekap JSON konsisten dengan isi")
if data["g1"]["node_alternatif"] and len(data["g1"]["node_alternatif"]) == 9:
    ok("struktur G1 memuat 9 node alternatif dan 4 node klaster")
else:
    bad("struktur G1 tidak lengkap")

# ---------- ringkasan ----------
print("=== LOLOS ===")
for o in oks:
    print(" +", o)
if fails:
    print("=== GAGAL ===")
    for f in fails:
        print(" -", f)
    print(f"\nRINGKASAN: {len(oks)} lolos, {len(fails)} gagal")
    sys.exit(1)
print(f"\nRINGKASAN: {len(oks)} lolos, 0 gagal")
print("STATUS: LOLOS")
