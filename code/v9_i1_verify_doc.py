#!/usr/bin/env python3
"""V9-I1 — verifikasi dokumen: setiap angka kunci di docs/V9_I1_INTEGRATION.md
harus ada di JSON primer / log (S6: json dulu, dokumen kemudian; dokumen = kutipan).

Cek:
  D1 jumlah head = 27 (klaim dokumen) == JSON
  D2 ringkasan layer L0=5 L1=11 L2=9 L3=2 == JSON
  D3 0 slot alarm + 11 L1 == JSON
  D4 sampel angka metrik segmen (vib rule P/FP/FAR, hyd hybrid P/FP/FAR,
     ssi nodata, bit_wear aktif, tool_wear op fp per alat, AUPRC vib) == JSON
  D5 ukuran JSON + jumlah baris TEST_LOG == yang tertulis di dokumen
  D6 hasil verifikasi = 13 cek SEMUA PASS (file VERIFY.txt)
  D7 dokumen memuat 6 baris "Riset pendahuluan" (skill wajib) + acceptance (a)-(d)
Keluaran: stdout + scratch/v9_i1/v9_i1_VERIFY_DOC.txt
"""
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"
DOC = f"{BASE}/docs/V9_I1_INTEGRATION.md"
RES = f"{BASE}/scratch/v9_i1/v9_i1_RESULTS.json"
LOG = f"{BASE}/scratch/v9_i1/v9_i1_TEST_LOG.txt"
VER = f"{BASE}/scratch/v9_i1/v9_i1_VERIFY.txt"

doc = open(DOC, encoding="utf-8").read()
res = json.load(open(RES))
out = []
fails = 0


def ck(vid, ok, detail):
    global fails
    line = f"[{'PASS' if ok else 'GAGAL'}] {vid}: {detail}"
    out.append(line)
    print(line, flush=True)
    if not ok:
        fails += 1


def head(engine, name):
    for e in res["engines"]:
        if e["engine"] == engine:
            for h in e["heads"]:
                if h["head"] == name:
                    return h
    raise KeyError(f"{engine}/{name}")


n_heads = sum(len(e["heads"]) for e in res["engines"])
ck("D1", n_heads == 27 and "27 head" in doc,
   f"jumlah head JSON = {n_heads}; dokumen menyebut '27 head' = {'27 head' in doc}")

lay = res["decision_layer"]["ringkasan"]
ck("D2", lay == {"L0": 5, "L1": 11, "L2": 9, "L3": 2}
   and "L0 status otomatis   : 5 head" in doc
   and "L1 peringatan L-In-L : 11 head" in doc,
   f"ringkasan layer JSON = {lay}; pola blok ada di dokumen = "
   f"{'L1 peringatan L-In-L : 11 head' in doc}")

ck("D3", res["auto_critical_alarm_slots"] == 0
   and res["decision_layer"]["nperingatan_l1"] == 11
   and "Slot ALARM OTOMATIS  : 0" in doc,
   "slot alarm 0 + 11 peringatan L1 == dokumen")

samples = []
vib_r = head("vib", "rule_display")["metrik_segmen"]
samples.append(("vib rule P/FP/FAR", (0.9444, 30, 49.942),
                (vib_r["precision"], vib_r["fp"], vib_r["far_segmen"])))
hyb = head("hyd", "hybrid_rule_and_persistence")["metrik_segmen"]
samples.append(("hyd hybrid P/FP/FAR", (0.8243, 110, 16.611),
                (hyb["precision"], hyb["fp"], hyb["far_segmen"])))
ssi_r = head("ssi", "rule_display")
samples.append(("ssi n_nodata", 5268, ssi_r["n_nodata"]))
bw = head("bit_wear", "persistence")
samples.append(("bit_wear aktif/n", "4.917/47.645", f"{bw['n_aktif']:,}/{bw['n_windows']:,}"
                .replace(",", ".")))
samples.append(("vib RF AUPRC", 0.9117, head("vib", "rf_lowo")["auprc_segmen"]))
op = head("tool_wear", "op_far_calibrated")["per_alat"]
samples.append(("tool_wear op fp per alat", [1, 3, 1, 3], [r["fp_R01"] for r in op]))
samples.append(("tool_wear op TLead", [25, 36, 24, 20],
                [int(r["TLead_s"]) for r in op]))
bad = [(n, a, b) for n, a, b in samples if a != b]
ck("D4", not bad, f"{len(samples)-len(bad)}/{len(samples)} sampel angka cocok; selisih={bad}")
# angka sampel juga harus tertera di dokumen
str_docs = ["0,9444", "0,8243", "5.268/5.455", "4.917/47.645", "0,9117"]
missing = [s for s in str_docs if s not in doc]
ck("D5", not missing, f"angka sampel tertulis di dokumen; hilang={missing}")

log_lines = sum(1 for _ in open(LOG, encoding="utf-8"))
res_size = os.path.getsize(RES)
ck("D6", f"{log_lines} baris" in doc and f"{res_size:,}".replace(",", ".") in doc,
   f"TEST_LOG = {log_lines} baris, JSON = {res_size} byte (dokumen: "
   f"'{log_lines} baris', '{res_size:,}')")

ver = open(VER, encoding="utf-8").read()
n_pass = ver.count("[PASS]")
ck("D7", "SEMUA PASS" in ver and n_pass == 13,
   f"verifikasi = {n_pass} PASS + 'SEMUA PASS' = {'SEMUA PASS' in ver}")

skills = ["scientific-critical-thinking", "statistical-analysis",
          "verification-mandatory", "what-if-oracle", "consciousness-council",
          "sequentialthinking"]
miss = [s for s in skills if f"Riset pendahuluan: `{s}`" not in doc]
acc = all(x in doc for x in ["(a) prototipe berjalan", "(b) 7 engine terintegrasi",
                             "(c) batas pemakaian dihormati",
                             "(d) keputusan manusia dipertahankan"])
ck("D8", not miss and acc,
   f"6 baris riset pendahuluan (hilang={miss}); acceptance a-d = {acc}")

summary = f"\nTOTAL: {'SEMUA PASS' if fails == 0 else f'{fails} GAGAL'}\n"
out.append(summary.strip())
open(f"{BASE}/scratch/v9_i1/v9_i1_VERIFY_DOC.txt", "w").write("\n".join(out) + "\n")
print(summary)
raise SystemExit(1 if fails else 0)
