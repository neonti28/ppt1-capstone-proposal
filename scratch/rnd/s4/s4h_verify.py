"""S4-H: verifikasi silang dokumen lawan ledger dan JSON.

1. Setiap kode S4-xxx yang dikutip di dokumen harus ada di ledger.
2. Tidak boleh ada em-dash sebagai penghubung klausa.
3. Token angka penting di dokumen harus cocok dengan nilai di JSON.
"""
import os, re, json

ROOT = "/mnt/d/Capstone 1(v2)"
DOC = os.path.join(ROOT, "docs/RND_S4_LAYER_B_DATA.md")
LEDGER = os.path.join(ROOT, "docs/RND_PROVENANCE_LEDGER.md")
S4 = os.path.join(ROOT, "scratch/rnd/s4")

doc = open(DOC, encoding="utf-8").read()
led = open(LEDGER, encoding="utf-8").read()

# 1. kode S4 di dokumen vs ledger
ref_doc = set(re.findall(r"S4-[0-9]{3}", doc))
ref_led = set(re.findall(r"^\| (S4-[0-9]{3})", led, flags=re.M))
missing = sorted(ref_doc - ref_led)
print("kode di dokumen:", len(ref_doc), "| kode di ledger:", len(ref_led), "| hilang:", missing)

# 2. em-dash
print("em-dash (U+2014) di dokumen:", doc.count("\u2014"), "| di ledger bagian S4:", led.split("## Bagian S4")[-1].count("\u2014"))

# 3. token angka penting
inv = json.load(open(os.path.join(S4, "inventory.json"), encoding="utf-8"))
lab = json.load(open(os.path.join(S4, "labels_duration.json"), encoding="utf-8"))
ddr = json.load(open(os.path.join(S4, "ddr_activity_stats.json"), encoding="utf-8"))
cc = json.load(open(os.path.join(S4, "crosscheck.json"), encoding="utf-8"))
dt = json.load(open(os.path.join(S4, "ddr_downtime_table.json"), encoding="utf-8"))
raw = json.load(open(os.path.join(S4, "inventory_raw.json"), encoding="utf-8"))
a = ddr["activity"]

def id_fmt(x):
    """format angka gaya Indonesia dengan titik ribuan."""
    s = f"{x:,}".replace(",", ".")
    return s

checks = [
    (id_fmt(ddr["laporan"]["n_baris"]), "1759 laporan"),
    (id_fmt(a["n_record"]), "23447 activity"),
    (f"{a['interruption']['total_jam']:,.3f}".replace(",", "X").replace(".", ",").replace("X", "."), "8343.253 jam interruption"),
    (f"{a['maintenance_terkait']['total_jam']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "1777.75 jam maintenance"),
    (f"{lab['durasi_jam']['sum']:,.1f}".replace(",", "X").replace(".", ",").replace("X", "."), "1225.0 jam label"),
    (str(lab["n_baris"]), "884 kejadian"),
    (str(dt["tabel"]["n_file_memuat_tabel"]), "325 berkas tabel"),
    (str(dt["record"]["n_record"]), "533 record tabel"),
    (id_fmt(cc["pres_test_type"]["distribusi"]["formation integrity test"]), "1072 FIT"),
    (id_fmt(raw["folder_total"]["n_files"]), "5473 berkas"),
    (id_fmt(raw["folder_total"]["bytes"]), "409920771 byte"),
    (id_fmt(raw["katalog_volve"]["n_baris"]), "4035 record katalog"),
    (str(a["n_kode_unik"]), "64 kode"),
    (id_fmt(a["n_laporan_punya_activity"]), "1750 laporan ber-activity"),
    (str(a["state_fail_durasi"]["n"]), "480 state fail"),
    (str(lab["tujuh_well_engine"]["n_kejadian"]), "671 kejadian 7 well"),
    (str(lab["equipment_failure_state_detail"]["n"]), "770 equipment failure"),
    (str(lab["kegagalan_beralasan"]["n"]), "388 kegagalan beralasan"),
    (str(dt["n_kelas_equipment_unik"]), "41 kelas"),
]
bad = []
for tok, label in checks:
    if tok not in doc:
        bad.append((label, tok))
print("token angka tidak ditemukan di dokumen:", bad if bad else "tidak ada")

# angka persen dan rasio
for key, val, label in [
    ("rasio jam berlabel", cc["silang_total"]["rasio_jam"], "0,1468"),
    ("persen file tabel", dt["tabel"]["persen_file_memuat_tabel"], "18,48"),
    ("per laporan harian", inv["metrik_lapisan_b"]["B3_henti_maintenance_gabungan"]["per_laporan_harian"], "0,6345"),
    ("jam per laporan", inv["metrik_lapisan_b"]["B3_henti_maintenance_gabungan"]["jam_per_laporan_harian"], "1,0107"),
    ("B5", inv["metrik_lapisan_b"]["B5_rasio_kejadian_per_laporan_harian"]["rasio"], "0,5026"),
    ("B7 median", inv["metrik_lapisan_b"]["B7_peringatan_terhadap_durasi_henti"]["cakupan_lead_h1_persen_dari_median"], "19,17"),
    ("B7 p90", inv["metrik_lapisan_b"]["B7_peringatan_terhadap_durasi_henti"]["cakupan_lead_h1_persen_dari_p90"], "5,48"),
    ("B8 H1", inv["metrik_lapisan_b"]["B8_beban_alarm_per_kejadian"]["contoh_h1_hyd"]["fp_per_onset"], "2,3974"),
    ("B8 rule", inv["metrik_lapisan_b"]["B8_beban_alarm_per_kejadian"]["contoh_rule_hyd"]["fp_per_onset"], "5,3974"),
]:
    print(f"{key}: json={val} | diharapkan di dokumen={label} | ada={label in doc}")
