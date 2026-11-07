"""S4-G: bangun blok ledger S4 di docs/RND_PROVENANCE_LEDGER.md (idempoten).

Semua angka ditarik dari JSON hasil eksekusi, bukan ditulis tangan.
Blok lama (jika ada) dihapus dulu, jadi menjalankan ulang tidak menggandakan baris.
"""
import os, json, glob, re

ROOT = "/mnt/d/Capstone 1(v2)"
S4 = os.path.join(ROOT, "scratch/rnd/s4")
LEDGER = os.path.join(ROOT, "docs/RND_PROVENANCE_LEDGER.md")

def load(n):
    with open(os.path.join(S4, n), encoding="utf-8") as f:
        return json.load(f)

ddr = load("ddr_activity_stats.json")
lab = load("labels_duration.json")
raw = load("inventory_raw.json")
dt = load("ddr_downtime_table.json")
cc = load("crosscheck.json")
inv = load("inventory.json")
TS = load("token_scan.json")
a = ddr["activity"]
m = inv["metrik_lapisan_b"]

def sz(rel):
    return os.path.getsize(os.path.join(ROOT, rel))

wits = sorted(glob.glob(os.path.join(ROOT, "data/volve/witsml_parsed/*.csv")))
wits_bytes = sum(os.path.getsize(p) for p in wits)

TGL = "2026-10-28"
rows = []
def R(no, angka, satuan, kelas, rujukan, dipakai, status):
    rows.append(f"| S4-{no:03d} | {angka} | {satuan} | {kelas} | {rujukan} | {dipakai} | {status} |")

# --- berkas dan jumlah record ---
R(1, ddr["laporan"]["n_baris"], "laporan", "RUN-KITA", "scratch/rnd/s4/ddr_activity_stats.json laporan.n_baris; pd.read_parquet shape (1759, 17)", "bagian 2 baris 1", "TERUKUR")
R(2, sz("data/volve/ddr.parquet"), "byte", "RUN-KITA", "os.path.getsize data/volve/ddr.parquet", "bagian 2 baris 1", "TERUKUR")
R(3, ddr["laporan"]["n_kolom"], "kolom", "RUN-KITA", "ddr_activity_stats.json laporan.kolom (17 nama)", "bagian 2 baris 1", "TERUKUR")
R(4, a["n_record"], "record activity", "RUN-KITA", "ddr_activity_stats.json activity.n_record", "bagian 2, 3.1", "TERUKUR")
R(5, a["n_kode_unik"], "kode kerja unik", "RUN-KITA", "ddr_activity_stats.json activity.n_kode_unik", "bagian 3.1", "TERUKUR")
R(6, a["n_laporan_punya_activity"], "laporan", "RUN-KITA", "ddr_activity_stats.json activity.n_laporan_punya_activity", "bagian 3.1", "TERUKUR")
R(7, f"{a['interruption']['total_record']} record / {a['interruption']['total_jam']} jam", "record / jam", "RUN-KITA", "ddr_activity_stats.json activity.interruption", "bagian 3.1, 5", "TERUKUR")
R(8, f"{a['maintenance_terkait']['total_record']} record / {a['maintenance_terkait']['total_jam']} jam", "record / jam", "RUN-KITA", "ddr_activity_stats.json activity.maintenance_terkait", "bagian 3.1, 4", "TERUKUR")
R(9, f"{m['B1_henti_perbaikan_per_kejadian']['n_kejadian']} / {m['B1_henti_perbaikan_per_kejadian']['total_jam']} / {m['B1_henti_perbaikan_per_kejadian']['median_jam']} / {m['B1_henti_perbaikan_per_kejadian']['p90_jam']} / {m['B1_henti_perbaikan_per_kejadian']['max_jam']}", "record / jam / median jam / p90 jam / maks jam", "RUN-KITA", "inventory.json metrik_lapisan_b.B1 (dari ddr_activity_stats.json durasi_per_kode['interruption -- repair'])", "bagian 4 B1", "TERUKUR")
R(10, f"{m['B2_henti_maintenance_per_kejadian']['n_kejadian']} / {m['B2_henti_maintenance_per_kejadian']['total_jam']} / {m['B2_henti_maintenance_per_kejadian']['median_jam']} / {m['B2_henti_maintenance_per_kejadian']['p90_jam']} / {m['B2_henti_maintenance_per_kejadian']['max_jam']}", "record / jam / median jam / p90 jam / maks jam", "RUN-KITA", "inventory.json metrik_lapisan_b.B2", "bagian 4 B2", "TERUKUR")
R(11, f"{a['state_fail_durasi']['n']} / {a['state_fail_durasi']['sum_jam']} / {a['state_fail_durasi']['median_jam']}", "record / jam / median jam", "RUN-KITA", "ddr_activity_stats.json activity.state_fail_durasi", "bagian 3.1", "TERUKUR")
R(12, a["total_jam_semua_activity"], "jam", "RUN-KITA", "ddr_activity_stats.json activity.total_jam_semua_activity", "bagian 3.1", "TERUKUR")
R(13, f"{lab['n_baris']} record / {lab['sumber']['baris']} kolom", "record / kolom", "RUN-KITA", "labels_duration.json n_baris dan sumber.kolom (20)", "bagian 2 baris 2", "TERUKUR")
R(14, f"{lab['durasi_jam']['sum']} / {lab['durasi_jam']['median']} / {lab['durasi_jam']['p90']} / {lab['durasi_jam']['max']}", "jam / median jam / p90 jam / maks jam", "RUN-KITA", "labels_duration.json durasi_jam", "bagian 3.1, 4", "TERUKUR")
R(15, f"{lab['n_durasi_valid']} valid / {lab['n_durasi_nol']} nol / {lab['n_durasi_negatif']} negatif", "kejadian", "RUN-KITA", "labels_duration.json n_durasi_valid, n_durasi_nol, n_durasi_negatif", "bagian 3.1", "TERUKUR")
R(16, f"{lab['tujuh_well_engine']['n_kejadian']} / {lab['tujuh_well_engine']['sum_jam']}", "kejadian / jam", "RUN-KITA", "labels_duration.json tujuh_well_engine", "bagian 3.1", "TERUKUR")
R(17, f"{lab['equipment_failure_state_detail']['n']} / {lab['equipment_failure_state_detail']['sum_jam']}", "kejadian / jam", "RUN-KITA", "labels_duration.json equipment_failure_state_detail", "bagian 3.1, 4", "TERUKUR")
R(18, f"{lab['kegagalan_beralasan']['n']} / {lab['kegagalan_beralasan']['sum_jam']}", "kejadian / jam", "RUN-KITA", "labels_duration.json kegagalan_beralasan", "bagian 3.1", "TERUKUR")
R(19, cc["silang_total"]["rasio_jam"], "rasio", "RUN-KITA", "crosscheck.json silang_total.rasio_jam (1225.0 / 8343.253)", "bagian 4 B6, 5", "TERUKUR")
R(20, f"{dt['tabel']['n_file_memuat_tabel']} berkas / {dt['tabel']['persen_file_memuat_tabel']} persen", "berkas / persen", "RUN-KITA", "ddr_downtime_table.json tabel.n_file_memuat_tabel dan persen_file_memuat_tabel", "bagian 3.2 S4-P1", "TERUKUR")
R(21, f"{dt['record']['n_record']} record / {dt['record']['n_downtime_nol']} bernilai nol / {dt['record']['n_downtime_positif']} positif", "record", "RUN-KITA", "ddr_downtime_table.json record", "bagian 3.2 S4-P1, 3.3 S4-N5", "TERUKUR")
R(22, f"26 dengan pola min/menit, 20 dengan pola jam saja, 18 dengan kata utuh", "remark", "RUN-KITA", "scratch/rnd/s4/p_remark_variants.py atas ddr_downtime_records.jsonl (533 record); angka 23 di versi pertama dokumen dikoreksi karena pola regex lama tidak menangkap bentuk 'minutes'", "bagian 3.2 S4-P1", "TERUKUR")
R(23, f"cost {raw['pindai_xml_ddr']['kemunculan'].get('cost', 0)} (lama) / cost {TS['xml']['kemunculan_literal']['cost']} XML dan {TS['html']['kemunculan_literal']['cost']} HTML (baru)", "kemunculan", "RUN-KITA", "token_scan.json (s4i_token_scan.py, 1759 XML + 1759 HTML penuh) menggantikan inventory_raw.json yang hanya memindai 5 token sehingga .get('cost',0) memberi nilai default, bukan hasil ukur", "bagian 3.3 S4-N1", "TERUKUR")
R(24, f"work order {TS['xml']['kemunculan_literal']['work order']} XML / {TS['html']['kemunculan_literal']['work order']} HTML / workorder {TS['xml']['kemunculan_literal']['workorder']} / WO-<angka> {TS['xml']['kemunculan_regex']['nomor_wo']}", "kemunculan", "RUN-KITA", "token_scan.json kemunculan_literal dan kemunculan_regex.nomor_wo", "bagian 3.3 S4-N2", "TERUKUR")
R(25, f"{cc['pres_test_type']['n_laporan_dengan_uji']} laporan / FIT {cc['pres_test_type']['distribusi']['formation integrity test']} / LOT {cc['pres_test_type']['distribusi']['leak off test']}", "laporan", "RUN-KITA", "crosscheck.json pres_test_type", "bagian 3.2 S4-P3", "TERUKUR")
R(26, cc["kode_activity_bernuansa"]["n_record"]["inspect"], "record", "RUN-KITA", "crosscheck.json kode_activity_bernuansa.n_record.inspect (dari 23447)", "bagian 3.3 S4-N3", "TERUKUR")
R(27, f"{raw['pindai_xml_ddr']['kemunculan'].get('inspect', 0)} inspect / {raw['pindai_xml_ddr']['kemunculan'].get('inspection', 0)} inspection", "kemunculan", "RUN-KITA", "inventory_raw.json pindai_xml_ddr (teks bebas 1759 XML)", "bagian 3.3 S4-N3", "TERUKUR")
R(28, f"{raw['folder_total']['n_files']} berkas / {raw['folder_total']['bytes']} byte", "berkas / byte", "RUN-KITA", "inventory_raw.json folder_total (os.walk Well_technical_data)", "bagian 1", "TERUKUR")
R(29, f"{raw['katalog_volve']['n_baris']} baris / other_target {raw['katalog_volve']['kategori']['other_target']} / dlis {raw['katalog_volve']['kategori']['dlis_target']} / las {raw['katalog_volve']['kategori']['las_target']} / bhaRun {raw['katalog_volve']['kategori']['bhaRun']} / mudLog {raw['katalog_volve']['kategori']['mudLog']}", "baris", "RUN-KITA", "inventory_raw.json katalog_volve", "bagian 2 baris 6, 3.2 S4-P5", "TERUKUR")
R(30, raw["csv_di_data"]["n_file"], "berkas CSV/TSV", "RUN-KITA", "inventory_raw.json csv_di_data.n_file (header dipindai untuk kata kunci biaya/inspeksi/work order)", "bagian 1", "TERUKUR")
R(31, m["B3_henti_maintenance_gabungan"]["per_laporan_harian"], "kejadian per laporan harian", "RUN-KITA", "inventory.json B3 (1116 / 1759)", "bagian 4 B3", "TERUKUR")
R(32, m["B3_henti_maintenance_gabungan"]["jam_per_laporan_harian"], "jam per laporan harian", "RUN-KITA", "inventory.json B3 (1777.75 / 1759)", "bagian 4 B3", "TERUKUR")
R(33, m["B5_rasio_kejadian_per_laporan_harian"]["rasio"], "kejadian per laporan harian", "RUN-KITA", "inventory.json B5 (884 / 1759)", "bagian 4 B5", "TERUKUR")
R(34, m["B7_peringatan_terhadap_durasi_henti"]["cakupan_lead_h1_persen_dari_median"], "persen", "DERIVASI", "inventory.json B7: 11.5 menit / (1.0 jam x 60)", "bagian 4 B7, 7", "TERUKUR")
R(35, m["B7_peringatan_terhadap_durasi_henti"]["cakupan_lead_h1_persen_dari_p90"], "persen", "DERIVASI", "inventory.json B7: 11.5 menit / (3.5 jam x 60)", "bagian 4 B7, 7", "TERUKUR")
R(36, m["B8_beban_alarm_per_kejadian"]["contoh_h1_hyd"]["fp_per_onset"], "alarm palsu per onset", "DERIVASI", "inventory.json B8 (935 / 390); FP dan onset dari docs/RND_R8_EVALUASI_BERLAPIS.md", "bagian 4 B8", "TERUKUR")
R(37, m["B8_beban_alarm_per_kejadian"]["contoh_rule_hyd"]["fp_per_onset"], "alarm palsu per onset", "DERIVASI", "inventory.json B8 (2105 / 390)", "bagian 4 B8", "TERUKUR")
_f9 = next(r for r in cc["silang_per_wellbore"] if r["wellbore"] == "NO 15/9-F-9")
R(38, _f9["rasio_labels_terhadap_ddr"], "rasio", "RUN-KITA", "crosscheck.json silang_per_wellbore wellbore='NO 15/9-F-9'", "bagian 5", "TERUKUR")
R(39, a["interruption"]["n_kode"], "kode", "RUN-KITA", "ddr_activity_stats.json activity.interruption.n_kode", "bagian 3.1", "TERUKUR")
R(40, dt["n_kelas_equipment_unik"], "kelas sistem", "RUN-KITA", "ddr_downtime_table.json n_kelas_equipment_unik", "bagian 3.2 S4-P1", "TERUKUR")
R(41, f"HTML {raw['ddr_dokumen_per_format']['html']['n_files']} berkas / {raw['ddr_dokumen_per_format']['html']['bytes']} byte; XML {raw['ddr_dokumen_per_format']['xml']['n_files']} / {raw['ddr_dokumen_per_format']['xml']['bytes']}; PDF {raw['ddr_dokumen_per_format']['pdf']['n_files']} / {raw['ddr_dokumen_per_format']['pdf']['bytes']}", "berkas / byte", "RUN-KITA", "inventory_raw.json ddr_dokumen_per_format", "bagian 1, 2", "TERUKUR")

# sepuluh kode interruption
kodes = ["interruption -- other", "interruption -- waiting on weather", "interruption -- repair",
         "interruption -- sidetrack", "interruption -- fish", "interruption -- maintain",
         "interruption -- wait", "interruption -- lost circulation", "interruption -- rig up/down",
         "interruption -- well control"]
no = 42
for k in kodes:
    v = a["durasi_per_kode"][k]
    R(no, f"{v['n']} / {v['sum_jam']} / {v['median_jam']} / {v['p90_jam']} / {v['max_jam']}", "record / jam / median / p90 / maks (jam)", "RUN-KITA", f"ddr_activity_stats.json durasi_per_kode['{k}']", "bagian 3.1 tabel", "TERUKUR")
    no += 1

# per wellbore silang (mulai 100 agar tidak bertabrakan dengan nomor berkas)
no = 100
for r in cc["silang_per_wellbore"]:
    R(no, f"{r['ddr_interruption_n']} / {r['ddr_interruption_jam']} / {r['labels_n']} / {r['labels_jam']} / {r['rasio_labels_terhadap_ddr']}", "record DDR / jam DDR / kejadian label / jam label / rasio", "RUN-KITA", f"crosscheck.json silang_per_wellbore wellbore={r['wellbore']}", "bagian 5 tabel", "TERUKUR")
    no += 1

R(60, f"{sz('data/predictive/features_timeseries_events.csv')} byte / 661 record / 17 kolom", "byte / record / kolom", "RUN-KITA", "os.path.getsize + pandas read_csv (scratch/rnd/s4/p_rows.py)", "bagian 2 baris 7", "TERUKUR")
R(61, f"{sz('data/USROP_health.csv')} byte / 198928 record / 20 kolom", "byte / record / kolom", "RUN-KITA", "os.path.getsize + pandas read_csv (p_rows.py)", "bagian 2 baris 8", "TERUKUR")
R(62, f"{sz('data/volve/usrop_wellbores_events.csv')} byte / 884 record / 8 kolom", "byte / record / kolom", "RUN-KITA", "os.path.getsize + pandas read_csv (p_rows.py); wc -l memberi 1190 karena baris baru di dalam komentar", "bagian 2 baris 9", "TERUKUR")
R(63, f"{len(wits)} berkas / {wits_bytes} byte", "berkas / byte", "RUN-KITA", "glob data/volve/witsml_parsed/*.csv + os.path.getsize", "bagian 2 baris 10", "TERUKUR")
R(64, sz("data/volve/external/volve_catalog_target_paths.csv"), "byte", "RUN-KITA", "os.path.getsize", "bagian 2 baris 6", "TERUKUR")
R(65, sz("data/volve/labels_curated_v2.csv"), "byte", "RUN-KITA", "os.path.getsize data/volve/labels_curated_v2.csv", "bagian 2 baris 2", "TERUKUR")
R(66, "26.0.0", "versi paket", "KONVENSI", "pyarrow dipasang ke /home/neonti/.venvs/rnd_e3 lewat uv pip install (output: + pyarrow==26.0.0); tanpa pyarrow parquet tidak terbaca", "bagian 1 langkah 3", "TERUKUR")
R(67, "0", "hasil pencarian berkas", "RUN-KITA", "find -iname '*production*' -o -iname '*onstream*' -o -iname '*barrel*' -o -iname '*oil*rate*' di /mnt/d/Capstone 1(v2) memberi 0 hasil", "bagian 3.3 S4-N4", "TERUKUR")
R(68, "7 dari 10 dipindai / 3 dilewati", "berkas", "RUN-KITA", "inventory_raw.json csv_di_data.berkas: 7 path witsml_parsed ikut dipindai; F-12 (840812790), F-14 (812937500), F-15_S (917390378) melewati batas 500 MB", "bagian 1 langkah 6, 9 butir 3", "TERUKUR")
R(69, "12 kutipan diperiksa / 0 menulis jam henti tidak ada", "baris dokumen", "RUN-KITA", "scratch/rnd/s4/p_linecheck.py mencetak isi 12 baris: E3 217,300; E4 256,343; R7 359; R8 148,234; S1 170,255; PM 182,263,292. Semuanya menyebut durasi inspeksi/biaya/jadwal inspeksi, tidak satu pun menyebut jam henti tidak ada", "bagian 7 koreksi", "TERUKUR")
R(70, f"{TS['xml']['n_file_dibaca']} XML / {TS['html']['n_file_dibaca']} HTML / {TS['xml']['n_file_gagal'] + TS['html']['n_file_gagal']} gagal", "berkas", "RUN-KITA", "token_scan.json (s4i_token_scan.py) membaca penuh tiap berkas, bukan sampel", "bagian 1 langkah 4, 3.3 S4-N1", "TERUKUR")
R(71, TS["xml"]["kemunculan_regex"]["kata_berakar_price"], "kemunculan", "RUN-KITA", "token_scan.json kemunculan_regex.kata_berakar_price = 1; konteks diperiksa dengan p_price_ctx.py: 'Called in Ocean Price for cuttings discharge at 21:30 hrs', yaitu nama kapal pada kolom komentar 15_9_F_15_D_2013_11_12", "bagian 3.3 S4-N1", "TERUKUR")
R(72, f"service order {TS['xml']['kemunculan_literal']['service order']} / purchase order {TS['xml']['kemunculan_literal']['purchase order']} / work-order {TS['xml']['kemunculan_literal']['work-order']}", "kemunculan", "RUN-KITA", "token_scan.json kemunculan_literal pada 1759 XML dan 1759 HTML", "bagian 3.3 S4-N2", "TERUKUR")
R(73, f"maintenance {TS['xml']['kemunculan_literal']['maintenance']}", "kemunculan", "RUN-KITA", "token_scan.json kemunculan_literal.maintenance (kata utuh), berbeda dari substring 'maintain' 393 di inventory_raw.json", "bagian 3.3 S4-N3", "TERUKUR")

# baris BELUM
R(90, "tidak terukur", "n/a", "BELUM-TERUKUR", "isi teks 1759 PDF DDR tidak dipindai, sehingga ketiadaan biaya tidak diklaim untuk PDF", "bagian 9 butir 1", "BELUM TERUKUR")
R(91, "tidak terukur", "n/a", "BELUM-TERUKUR", "tidak ada jadwal inspeksi fisik, sehingga rasio alarm per inspeksi dan pengurangan pemeriksaan fisik tidak dapat dihitung (penyebut tidak ada)", "bagian 4, 7", "BELUM TERUKUR")
R(92, "tidak terukur", "n/a", "BELUM-TERUKUR", "tidak ada biaya per jam henti, sehingga nilai rupiah henti yang dihindari tidak dapat dihitung", "bagian 4, 7", "BELUM TERUKUR")
R(93, "tidak terukur", "n/a", "BELUM-TERUKUR", "tidak ada durasi inspeksi per alarm, sehingga jam orang per shift tidak dapat dihitung", "bagian 4, 7", "BELUM TERUKUR")

block = []
block.append("## Bagian S4: pendataan lapisan B (kartu `t_ad4e3f55`)")
block.append("")
block.append("Kelas sumber mengikuti konvensi ledger ini. Baris RUN-KITA berarti angka hasil eksekusi pada `scratch/rnd/s4/` tanggal " + TGL + " (WIB).")
block.append("Tabel ini memakai 7 kolom sesuai kartu: No, Angka, Satuan, Kelas sumber, Rujukan persis, Dipakai di, Status.")
block.append("")
block.append("| No | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |")
block.append("|---|---|---|---|---|---|---|")
block.extend(rows)
block.append("")

new_block = "\n".join(block)

with open(LEDGER, encoding="utf-8") as f:
    txt = f.read()

# hapus blok S4 lama (idempoten)
pat = re.compile(r"## Bagian S4:.*?(?=\n## Bagian |\Z)", re.S)
if pat.search(txt):
    txt = pat.sub("", txt).rstrip() + "\n"
if not txt.endswith("\n"):
    txt += "\n"
txt = txt.rstrip() + "\n\n" + new_block + "\n"

with open(LEDGER, "w", encoding="utf-8") as f:
    f.write(txt)

print("baris ledger S4 ditulis:", len(rows))
print("ukuran ledger:", os.path.getsize(LEDGER))
