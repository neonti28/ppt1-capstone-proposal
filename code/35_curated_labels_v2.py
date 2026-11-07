"""
35_curated_labels_v2.py — T8: kolom outcome + component + audit 100 uncertain.

Rerunnable, deterministik:
  python3 code/35_curated_labels_v2.py   # exit 0

Output:
  data/volve/labels_curated_v2.csv        (884 baris, 16 kolom lama utuh + 4 kolom baru)
  data/volve/uncertain_audit_100.csv      (sampel seed 20261001, terisi status+bukti)
  docs/V2_LABEL_AUDIT_UNCERTAIN.md        (audit 100/100 baris berbukti)
  data/volve/labels_curated_v2_log.json   (log eksekusi)
"""
import pandas as pd, re, random, json, sys
from pathlib import Path

BASE = Path("/mnt/d/Capstone 1")
IN_CSV = BASE / "data/volve/labels_curated.csv"
OUT_CSV = BASE / "data/volve/labels_curated_v2.csv"
AUDIT_CSV = BASE / "data/volve/uncertain_audit_100.csv"
AUDIT_MD = BASE / "docs/V2_LABEL_AUDIT_UNCERTAIN.md"
LOG_JSON = BASE / "data/volve/labels_curated_v2_log.json"

# ---------- 0. AUDIT VERDICTS (hasil audit manual 100 baris, seed 20261001) ----------
# status : keeps_uncertain (label dipertahankan) | suggest_no | suggest_yes
#          -> suggestion TIDAK diterapkan ke CSV; hanya didokumentasikan (PM decision).
# reason : thin_narrative | out_of_range | ambiguous
# quote  : kutipan VERBATIM dari comments_full baris bersangkutan (divalidasi di bawah).
VERDICTS_JSON = r'''{
"1": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Checked box on intermediate joint no. 4 threads ok.", "note": "51 char, rutinitas cek ulir, tanpa konteks kegagalan atau komponen."},
"2": {"status": "suggest_no", "reason": "out_of_range", "quote": "Changed burst disk in turbine cooling system", "note": "Turbine cooling = topside, di luar cakupan BHA."},
"3": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "took survey with bit at 3293m", "note": "Bit disebut tapi kegiatan trip/survey rutin, tanpa bukti kegagalan."},
"4": {"status": "suggest_no", "reason": "out_of_range", "quote": "Build sacffolding in moonpool for installing shackles on riser.", "note": "Pekerjaan scaffolding moonpool, permukaan."},
"5": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Made up Vetco jet sub. RIH with jet sub and located across BOP.", "note": "Jet sub disebut, operasi casing rutin di BOP, tanpa kegagalan."},
"6": {"status": "suggest_no", "reason": "out_of_range", "quote": "Had problems with bolts on deadline anchor spooler drum.", "note": "Spooler drum = peralatan lantai rig."},
"7": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Held tool box talk and removed the HTS rollers.", "note": "47 char; identitas HTS rollers tidak dijelaskan narasi."},
"8": {"status": "suggest_no", "reason": "out_of_range", "quote": "Found air lock in suction line to mud pumps.", "note": "Mud pump = peralatan permukaan."},
"9": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "picked up the back up Adjustment Sub Setting Tool", "note": "Tool setting casing + HWDP, dicampur; narasi tak menyebut kegagalan BHA."},
"10": {"status": "suggest_no", "reason": "out_of_range", "quote": "Meanwhile layed out and measured 9 5/8\" csg on cantilever.", "note": "Penanganan casing di cantilever, permukaan."},
"11": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "RIH with jet/flush tool from surface to 140 m.", "note": "46 char, satu kalimat rutin, tanpa hasil."},
"12": {"status": "suggest_no", "reason": "out_of_range", "quote": "Welded 1,5\" hex socket onto 1\" drive interface on j-gun.", "note": "Perf gun wireline; bukan komponen BHA."},
"13": {"status": "suggest_no", "reason": "out_of_range", "quote": "picked up and made up Screen Hanger", "note": "Screen hanger = peralatan completion, bukan BHA."},
"14": {"status": "suggest_no", "reason": "out_of_range", "quote": "Landed 10 3/4\" casing hanger in slips", "note": "Casing hanger = wellhead/completion, bukan BHA."},
"15": {"status": "suggest_no", "reason": "out_of_range", "quote": "Polished WH area from datum at 138,9 m to 139,3 m", "note": "Persiapan permukaan wellhead, bukan downhole."},
"16": {"status": "suggest_yes", "reason": "ambiguous", "quote": "Removed radioactive source from BHA.", "note": "Aksi maintenance pada BHA eksplisit; tanpa bukti adverse sehingga tidak dijadikan yes otomatis."},
"17": {"status": "suggest_no", "reason": "out_of_range", "quote": "Removed leaking hose from skidding unit, installed new hose and pressure tested same.", "note": "Hose skidding unit = peralatan permukaan."},
"18": {"status": "suggest_no", "reason": "out_of_range", "quote": "POOH from 500 m with perforation string on WL.", "note": "Toolstring wireline, bukan BHA."},
"19": {"status": "suggest_no", "reason": "out_of_range", "quote": "Changed casing tong dies.", "note": "Casing tong = peralatan lantai rig."},
"20": {"status": "suggest_no", "reason": "out_of_range", "quote": "POOH with bowl protector RT, broke and laid out same.", "note": "Bowl protector rotary table, permukaan."},
"21": {"status": "suggest_no", "reason": "out_of_range", "quote": "Removed PS-21 slips and installed masterbushings.", "note": "Slips/master bushing = peralatan rotary table."},
"22": {"status": "suggest_no", "reason": "out_of_range", "quote": "Isolated and de-isolated TDS.", "note": "Top drive = peralatan permukaan."},
"23": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Observed 30 MT continuos drag after release.", "note": "Observasi drag string; komponen dan lokasi kegagalan tidak disebut."},
"24": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Troubleshot on interlock system for mudbucket.", "note": "Intertlock mudbucket permukaan, tapi narasi juga menyebut drill string."},
"25": {"status": "suggest_no", "reason": "out_of_range", "quote": "Changed casing tong dies and clamps.", "note": "Casing tong = permukaan."},
"26": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "P/U and M/U tool string.", "note": "24 char; tool string tidak diidentifikasi (WL atau drill)."},
"27": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Held tool box talk with crew", "note": "28 char, hanya toolbox talk, tanpa objek."},
"28": {"status": "suggest_no", "reason": "out_of_range", "quote": "Changed o-ring and reinstalled alignement cylinder in top drive.", "note": "Perbaikan top drive, permukaan."},
"29": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Held toolbox talk for continued casing running.", "note": "47 char, rapat perencanaan tanpa tindakan/kegagalan."},
"30": {"status": "suggest_no", "reason": "out_of_range", "quote": "POOH with WL toolstring.", "note": "Toolstring wireline, bukan BHA."},
"31": {"status": "suggest_no", "reason": "out_of_range", "quote": "Removed 10 3/4\" BX elevator and installed DP elevator.", "note": "Elevator = peralatan lantai rig."},
"32": {"status": "suggest_no", "reason": "out_of_range", "quote": "Bled off 22 bar pressure on casing. R/D side entry assembly.", "note": "Side entry assembly = perakitan wireline permukaan."},
"33": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Applied 50 bars inside string to verify setting tool integrity.", "note": "Uji setting tool via drill string; setting tool casing, identitas belum pasti BHA."},
"34": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "L/D ME-plug RT", "note": "14 char, singkatan tanpa penjelasan."},
"35": {"status": "suggest_no", "reason": "out_of_range", "quote": "Picked up bowl protector RT and made up to stand of 5 1/2\" DP.", "note": "Penanganan pipa di floor; bukan peristiwa downhole."},
"36": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Meanwhile continued to check for possible leaking valves.", "note": "Valve bocor tidak dilokasi (surface atau downhole)."},
"37": {"status": "suggest_no", "reason": "out_of_range", "quote": "Had to pull 128 MT overpull to free casing", "note": "String casing tersangkut, bukan BHA."},
"38": {"status": "suggest_no", "reason": "out_of_range", "quote": "filled riser/lubricator with 250 ltrs of 100% MEG using cmt unit", "note": "Isi lubricator/riser = persiapan permukaan."},
"39": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "RIH to 938 m. Increased rate to 1100 lpm and washed from 938 m to 940 m.", "note": "Operasi washing downhole tanpa penyebutan komponen."},
"40": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Held toolbox talk prior to laying out DP single (innerstring).", "note": "Rapat perencanaan; tanpa tindakan atau kegagalan."},
"41": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Laid down Powerdrive. Picked up back-up Powerdrive. Made up 12 1/4\" bit.", "note": "Komponen BHA eksplisit tapi kegiatan ganti perkakas rutin, tanpa kegagalan."},
"42": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "pulled 171/2\" BHA into shoe at 195 m", "note": "BHA disebut, tapi perbaikan utama adalah kebocoran hidraulik ROV permukaan."},
"43": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Made up and RIH with 12 1/4\" BHA to 107 m MD.", "note": "45 char, trik rutin dengan BHA, tanpa kegagalan."},
"44": {"status": "suggest_no", "reason": "out_of_range", "quote": "Closed SV & HMV and inflow tested same.", "note": "SV/HMV = valve permukaan/wellhead."},
"45": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Worked string up and down as per Drill-Quip instructions.", "note": "Aktivitas string terkait setting tool casing; kegagalan tidak diidentifikasi."},
"46": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Checked line up and troubleshot loss of pressure.", "note": "49 char, kehilangan tekanan tanpa lokasi peralatan."},
"47": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Performed operational checks and tested tools", "note": "45 char, generik tanpa objek spesifik."},
"48": {"status": "suggest_no", "reason": "out_of_range", "quote": "Greased and operated valves on kill manifold and in moonpool.", "note": "Kill manifold/cement unit = permukaan."},
"49": {"status": "suggest_no", "reason": "out_of_range", "quote": "L/U landing collar/float joint.", "note": "Landing collar/float joint = perkakas cementing casing, bukan BHA."},
"50": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Secured area. Evaluated situation. Performed TOFS.", "note": "Generik, tanpa objek atau hasil."},
"51": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Had oil leak in TDS. Reamed back on std and RB in derrick to have 17 1/2\" bit inside shoe at 195 m.", "note": "Kebocoran TDS permukaan bercampur posisi bit downhole; sinyal campuran."},
"52": {"status": "suggest_no", "reason": "out_of_range", "quote": "CAN (climbers) secured upper part of fwd PRS to derrick beam", "note": "PRS/derrick = struktur permukaan."},
"53": {"status": "suggest_no", "reason": "out_of_range", "quote": "Installed diverter and master bushing.", "note": "Diverter/master bushing = peralatan lantai rig."},
"54": {"status": "suggest_no", "reason": "out_of_range", "quote": "Inflow tested HMV with SIWHP 5 bar for 10 min.", "note": "HMV valve permukaan; pemeriksaan tool string wireline sekunder."},
"55": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "RIH with isolation test tool from surface to 139 m. Landed and set tool as per GE Vetco instructions.", "note": "Test tool downhole, identitas komponen tidak jelas, tanpa kegagalan."},
"56": {"status": "suggest_no", "reason": "out_of_range", "quote": "Function tested Weatherford auto stabber.", "note": "Auto stabber = peralatan floor permukaan."},
"57": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Unable to start RIH with BHA #1 due to power shut down on WL winch.", "note": "BHA disebut tetapi penyebabnya kegagalan daya winch permukaan."},
"58": {"status": "suggest_no", "reason": "out_of_range", "quote": "Performed TBT for pulling tubing bonnet and running surface riser.", "note": "Tubing bonnet/surface riser = completion permukaan."},
"59": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Attempted to release adjustable sub tool several times. No success.", "note": "Kegagalan pada sub tool; lokasi downhole tidak dinyatakan, tidak di BHA."},
"60": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Inspected seal assembly, found vertical marks on the seal OD.", "note": "Seal assembly tidak diidentifikasi; lokasi tidak disebut."},
"61": {"status": "suggest_no", "reason": "out_of_range", "quote": "Lowered tubing bonnet to XMT deck utilising TDS.", "note": "XMT deck = completion permukaan."},
"62": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Attempted to pressure tested well to 34 bar against Timelock plug and diverter packer.", "note": "Tes tekanan terhadap plug/packer (downhole) tapi hasil bercampur, interupsi di 32 bar."},
"63": {"status": "suggest_no", "reason": "out_of_range", "quote": "Removed inserts in elevators and checked activating pin.", "note": "Elevator = peralatan lantai rig."},
"64": {"status": "suggest_no", "reason": "out_of_range", "quote": "Disconnected slings from riser and R/U to lift diverter", "note": "Rigging surface riser/diverter."},
"65": {"status": "suggest_no", "reason": "out_of_range", "quote": "Electrican opened ex-panel and re-sat level sensor.", "note": "Panel listrik/sensor permukaan."},
"66": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Removed hose and circ. sub from string.", "note": "Circ sub dari string (downhole) bercampur uji kelly hose permukaan."},
"67": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Performed TBT for pulling diverter.", "note": "35 char, toolbox talk tanpa tindakan detail."},
"68": {"status": "suggest_no", "reason": "out_of_range", "quote": "Installed lifting equipment onto riser. Removed scaffolding in moonpool.", "note": "Peralatan angkat/scaffolding permukaan."},
"69": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Meanwhile reamed on stand and downlinked powerdrive.", "note": "PRS permukaan bercampur aksi downlink powerdrive downhole."},
"70": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "POOH with BHA#1 from 3348 m to surface.", "note": "BHA disebut, POOH rutin; verifikasi log dilakukan wireline."},
"71": {"status": "suggest_no", "reason": "out_of_range", "quote": "Held toolbox talk prior to POOH with 10 3/4\" tie-back casing.", "note": "Tie-back casing = completion; narasi hanya rapat perencanaan."},
"72": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Flow checked well, well static.", "note": "31 char, pemeriksaan umum tanpa komponen."},
"73": {"status": "suggest_no", "reason": "out_of_range", "quote": "Could not rack back 5 1/2\" HWDP due to finger on FWD PRS not working.", "note": "Kegagalan finger PRS = peralatan permukaan."},
"74": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Made up spear to HWDP and RIH and engaged the spear in the 10 3/4\" casing.", "note": "Fishing spear pada string; kegiatan terkait casing, tidak jelas BHA."},
"75": {"status": "suggest_no", "reason": "out_of_range", "quote": "set liner hanger and held for 3mins.", "note": "Liner hanger/packer = completion, bukan BHA."},
"76": {"status": "suggest_no", "reason": "out_of_range", "quote": "Function tested fwd PRS.", "note": "PRS = peralatan permukaan."},
"77": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "No movement observed on hanger at Tensioner deck. Wrong indications.", "note": "Kegagalan setting tool casing (hanger), bukan komponen BHA; belum cukup bukti."},
"78": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Made up 7\" liner in stands and racked back in derrick.", "note": "Reciprocate drill string bercampur penanganan liner di derrick."},
"79": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Changed out damaged breakband.", "note": "30 char; breakband tidak diidentifikasi."},
"80": {"status": "suggest_no", "reason": "out_of_range", "quote": "P/U back up casing tong from deck.", "note": "Casing tong = peralatan permukaan."},
"81": {"status": "suggest_no", "reason": "out_of_range", "quote": "POOH with perforation string on WL from 4200 m.", "note": "Toolstring wireline, bukan BHA."},
"82": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Held toolbox talk for running 10 3/4\" casing stands.", "note": "Rapat perencanaan, tanpa tindakan atau kegagalan."},
"83": {"status": "suggest_no", "reason": "out_of_range", "quote": "Changed casing tong dies.", "note": "Casing tong = peralatan permukaan."},
"84": {"status": "suggest_no", "reason": "out_of_range", "quote": "Meanwhile cleaned BOP, installed rubber skirts in wellhead module", "note": "Pembersihan BOP/module wellhead = permukaan/subsea package, bukan BHA."},
"85": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Pressure tested well to 35 bar against Timelock plug and tubing bonnet.", "note": "Tes integritas sumur dengan plug/tubing bonnet; hasil baik tapi bukan peristiwa BHA."},
"86": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "M/U TDS and down linked the LWD tools.", "note": "TDS permukaan bercampur downlink LWD (komponen BHA), tanpa kegagalan."},
"87": {"status": "suggest_no", "reason": "out_of_range", "quote": "M/U lubricator at QST. Pressure tested lubricator to 275 bar.", "note": "Lubricator = perakitan permukaan."},
"88": {"status": "suggest_no", "reason": "out_of_range", "quote": "Picked up new space out pup and back up 10 3/4\" surface hanger and made up same.", "note": "Surface hanger = wellhead casing, bukan BHA."},
"89": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Powered up WL tractor and continued RIH with BHA #2 to perforate interval #1", "note": "BHA #2 disebut tetapi kegiatan perforasi wireline, tanpa kegagalan."},
"90": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Meanwhile held tool box talk prior to L/O BHA.", "note": "Rapat perencanaan; BHA hanya objek rencana, tanpa tindakan/kegagalan."},
"91": {"status": "suggest_no", "reason": "out_of_range", "quote": "Released tubing bonnet from wellhead ustilising slings in TDS bails.", "note": "Tubing bonnet/wellhead = completion permukaan."},
"92": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "M/U side entry assy.", "note": "20 char; side entry assembly wireline tanpa konteks lebih lanjut."},
"93": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "RIH with 12 1/4\" drilling BHA on 5 1/2\" DP from 606 m to 1697 m MD.", "note": "BHA eksplisit tetapi trik rutin, tanpa kegagalan."},
"94": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Re-dressed test tool.", "note": "21 char, tool tidak diidentifikasi."},
"95": {"status": "keeps_uncertain", "reason": "thin_narrative", "quote": "Awaited instructions for releasing PADPRT.", "note": "Menunggu instruksi; tanpa tindakan atau lokasi peristiwa."},
"96": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "confirmed threads damaged on joint and in collar on float joint pup.", "note": "Kerusakan ulir nyata, tapi identitas float joint pup tidak pasti bagian BHA."},
"97": {"status": "keeps_uncertain", "reason": "ambiguous", "quote": "Pulled out DP single with adjustable sub actuation tool and laid out same.", "note": "Penanganan floor bercampur tool actuation casing; tidak jelas BHA."},
"98": {"status": "suggest_no", "reason": "out_of_range", "quote": "Electrican opened ex-panel and re-sat main switch.", "note": "Panel listrik permukaan."},
"99": {"status": "suggest_no", "reason": "out_of_range", "quote": "Unable to proceed with WL operation due to ongoing 5-yearly work on tension cylinders in moonpool.", "note": "Hambatan akibat pekerjaan cylinder permukaan di moonpool."},
"100": {"status": "suggest_no", "reason": "out_of_range", "quote": "Checked firing head, crimped wire observed.", "note": "Firing head wireline = persiapan permukaan."}
}'''
AUDIT_VERDICTS = json.loads(VERDICTS_JSON)

# ---------- 1. LOAD ----------
df = pd.read_csv(IN_CSV)
print(f"Loaded {len(df)} rows, {df.shape[1]} cols")
assert len(df) == 884, f"Expected 884 rows, got {len(df)}"
orig_bha = df['bha_relevant'].value_counts().to_dict()
orig_cols = list(df.columns)
print("Original bha_relevant:", orig_bha)
assert orig_bha == {'uncertain': 571, 'no': 263, 'yes': 50}, f"Input counts drifted: {orig_bha}"

df['cf'] = df['comments_full'].fillna('').str.strip()

# ---------- 2. OUTCOME PATTERNS ----------
# deterministic patterns from narrative; multiple can match
OUT_PATTERNS = {
    'repaired':       r'\brepaired?\b|\brectifi\w+|\bfixed\b|\brefurbished\b',
    'replaced':       r'\breplaced?\b|\breplacing\b|change(d|s)?\s+out\b|change(d|s)?\s+over\b',
    'resumed':        r'\bresumed?\b|re[- ]?started\b|back to (normal|operation)|operations?\s+resumed',
    'tested_ok':      r'tested?\s+(ok|good|satisfactory|success)|functioned\s+(ok|good|success)|no\s+faults?\b|\bpassed\b|\bpasses\b',
    'fished':         r'\bfished\b|\bovershot\b|junk\s+(basket|jar)|fishing\s+(tool|overshot)',
    'jarred':         r'\bjarred\b|\bjarring\b',
    'aborted':        r'\baborted?\b|terminated\b',
    'no_action':      r'\bno\s+(action|further action)\b|\bnot\s+(required|needed)\b',
    'deferred':       r'\bdeferred?\b|postpon\w+|scheduled\s+for',
    'downtime':       r'\bdowntime\b|\bwaiting\s+time\b|\bstandby\b|non[- ]?productive|\bNPT\b',
    'monitored':      r'\bmonitor\w+\b|\bobserved\b|\bkeep\s+(on|watch)\b',
    'tightened':      r'\btighten\w+|re[- ]?tight\w+',
    'installed':      r'\binstalled?\b|\bfitted\b|\bmounted\b|\brassembled\b',
    'removed':        r'\bremoved?\b|\bpulled?\b|\bwithdrawn\b',
    'made_up':        r'\bmade\s+up\b',
}

def extract_outcomes(text):
    """Return list of outcome labels found in text."""
    t = text.lower()
    hits = []
    for label, pat in OUT_PATTERNS.items():
        if re.search(pat, t):
            hits.append(label)
    return hits

def outcome_to_string(hits):
    if not hits:
        return ""
    seen, ordered = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h)
            ordered.append(h)
    return "|".join(ordered)

def outcome_reason(text):
    """Human-readable reason for empty outcome."""
    t = text.lower()
    if not t.strip():
        return "no_narrative"
    if len(t) < 50:
        return "narrative_too_short"
    if any(w in t for w in ["rih", "pooh", "tripping", "drilling", "casing", "cement", "survey", "circulating", "connection"]):
        if not any(w in t for w in ["problem", "fail", "stuck", "repair", "trouble", "issue"]):
            return "routine_operations_no_outcome_stated"
    return "no_outcome_keywords_found"

# ---------- 3. COMPONENT (BHA) PATTERNS ----------
COMP_PATTERNS = {
    'bit':            r'\bbit\b',
    'shoe':           r'\bshoe\b',
    'stabilizer':     r'stabilis\w+|stabiliz\w+',
    'centralizer':    r'centralis\w+|centraliz\w+',
    'mwd_lwd':        r'\bMWD\b|\bLWD\b|xceed|powerdrive|ecoscope|gyro\b|GR\b|sonic',
    'ubho':           r'\bUBHO\b',
    'nmxdc':          r'\bNMDC\b|non.?magnetic',
    'drill_collar':   r'drill\s?collar|\bDC\b(?!\w)',
    'drill_string':   r'drill\s?string|drillstring|HWDP|heavy weight drill',
    'motor':          r'mud\s?motor|mudmotor',
    'jar':            r'\bjars?\b|jarred|jarring',
    'reamer':         r'\breamer\b',
    'sub':            r'\bsub\b|\bsubs\b|crossover|\bXO\b|pup\s?joint',
    'bha_word':       r'\bBHA\b',
    'packer':         r'packer',
    'liner':          r'liner',
    'screen':         r'\bscreen\b',
    'casing':         r'\bcasing\b',
    'tubing':         r'\btubing\b',
    'fishing_tool':   r'overshot|fishing\s+(tool|overshot|BHA)|junk\s+(basket|jar)|fishing jar',
    'perf_gun':       r'\bguns?\b|perforat\w+|PGGT',
    'toolstring':     r'tool\s?string|toolstring',
    'tractor':        r'\btractor\b',
    'wlp':            r'\bwlp\b|wireline',
}

def extract_components(text):
    t = text.lower()
    hits = []
    for label, pat in COMP_PATTERNS.items():
        if re.search(pat, t):
            hits.append(label)
    return hits

def component_to_string(hits):
    if not hits:
        return ""
    seen, ordered = set(), []
    for h in hits:
        if h not in seen:
            seen.add(h)
            ordered.append(h)
    return "|".join(ordered)

def component_reason(text):
    t = text.lower()
    if not t.strip():
        return "no_narrative"
    if len(t) < 30:
        return "narrative_too_short"
    surface_only = any(w in t for w in ["prs", "tds", "tongs", "elevator", "slips", "drawworks", "mud pump", "floor", "derrick", "catwalk", "bop", "choke", "manifold"])
    downhole_hint = any(w in t for w in ["bit", "bha", "drill", "mwd", "lwd", "jar", "stuck", "fishing", "hole", "formation", "md ", "depth"])
    if surface_only and not downhole_hint:
        return "surface_equipment_only"
    return "no_bha_component_keywords"

# ---------- 4. APPLY EXTRACTION ----------
print("Extracting outcomes...")
df['outcome'] = df['cf'].apply(lambda t: outcome_to_string(extract_outcomes(t)))
df['outcome_reason'] = df.apply(lambda r: outcome_reason(r['cf']) if not r['outcome'] else "", axis=1)

print("Extracting components...")
df['component'] = df['cf'].apply(lambda t: component_to_string(extract_components(t)))
df['component_reason'] = df.apply(lambda r: component_reason(r['cf']) if not r['component'] else "", axis=1)

# --- ACCEPTANCE (a): setiap nilai non-kosong outcome/component diturunkan ulang dari narasi baris itu sendiri
n_out = int((df['outcome'] != '').sum())
n_comp = int((df['component'] != '').sum())
bad = 0
for idx, r in df.iterrows():
    for col, getter in (('outcome', extract_outcomes), ('component', extract_components)):
        val = r[col]
        if not val:
            continue
        rederv = outcome_to_string(getter(r['cf'])) if col == 'outcome' else component_to_string(getter(r['cf']))
        if rederv != val:
            bad += 1
            print("RE-DERIVE MISMATCH", col, r['event_id'], val, rederv)
assert bad == 0, f"{bad} nilai tidak bisa diturunkan ulang dari narasi"
print(f"Acceptance (a) OK: outcome={n_out}, component={n_comp}, re-derive 0 mismatch dari comments_full")

print("\n=== OUTCOME STATS ===")
print(f"Rows with outcome: {n_out} / rows without: {884 - n_out}")
for k in OUT_PATTERNS:
    cnt = df['outcome'].apply(lambda v, k=k: k in v.split('|') if v else False).sum()
    if cnt:
        print(f"  {k}: {cnt}")
print("\n=== COMPONENT STATS ===")
print(f"Rows with component: {n_comp} / rows without: {884 - n_comp}")
for k in COMP_PATTERNS:
    cnt = df['component'].apply(lambda v, k=k: k in v.split('|') if v else False).sum()
    if cnt:
        print(f"  {k}: {cnt}")

# ---------- 5. AUDIT 100 UNCERTAIN (seed 20261001) + VERDICTS ----------
random.seed(20261001)
unc_idx = df[df['bha_relevant'] == 'uncertain'].index.tolist()
print(f"\nUncertain pool: {len(unc_idx)}")
audit_idx = random.sample(unc_idx, 100)
audit_rows = []
for i, idx in enumerate(audit_idx):
    r = df.loc[idx]
    aid = str(i + 1)
    v = AUDIT_VERDICTS[aid]
    nar_norm = re.sub(r'\s+', ' ', str(r['comments_full'] or '')).strip()
    q_norm = re.sub(r'\s+', ' ', v['quote']).strip()
    assert q_norm in nar_norm, f"audit_id={aid} quote bukan kutipan verbatim narasi: {v['quote']!r}"
    assert v['status'] in {'keeps_uncertain', 'suggest_no', 'suggest_yes'}
    assert v['reason'] in {'thin_narrative', 'out_of_range', 'ambiguous'}
    audit_rows.append({
        'audit_id': int(aid),
        'event_id': int(r['event_id']),
        'wellbore': r['wellbore'],
        'event_date': r['event_date'],
        'source_code': r['source_code'],
        'state_detail': r['state_detail'],
        'category': r['category'],
        'bha_relevant': r['bha_relevant'],
        'narrative': r['comments_full'],
        'narrative_len': len(r['cf']),
        'outcome_extracted': r['outcome'],
        'outcome_reason': r['outcome_reason'],
        'component_extracted': r['component'],
        'component_reason': r['component_reason'],
        'status': v['status'],                 # keeps_uncertain | suggest_no | suggest_yes (TIDAK diterapkan)
        'uncertainty_reason': v['reason'],      # thin_narrative | out_of_range | ambiguous
        'bha_evidence_quote': v['quote'],       # verbatim dari comments_full
        'notes': v['note'],
    })
audit_df = pd.DataFrame(audit_rows)
assert len(audit_df) == 100
assert audit_df['bha_evidence_quote'].map(bool).all()
assert (audit_df['bha_relevant'] == 'uncertain').all()
audit_df.to_csv(AUDIT_CSV, index=False, encoding='utf-8')
print(f"Audit CSV: {AUDIT_CSV} (100 baris, semua terisi)")

# ---------- 6. WRITE V2 CSV ----------
new_cols = ['outcome', 'outcome_reason', 'component', 'component_reason']
out_df = df.drop(columns=['cf'])
final_cols = orig_cols + new_cols
out_df = out_df[final_cols]
out_df.to_csv(OUT_CSV, index=False, encoding='utf-8')
print(f"\nWritten v2: {OUT_CSV} ({len(out_df)} rows, {out_df.shape[1]} cols)")

# ACCEPTANCE (c)+(d): 884 baris, kolom lama identik sel demi sel, angka bha sama
assert len(out_df) == 884, "Row count changed!"
new_bha = out_df['bha_relevant'].value_counts().to_dict()
assert new_bha == orig_bha, f"bha_relevant changed! old={orig_bha} new={new_bha}"
src = pd.read_csv(IN_CSV)
cell_diff = 0
for c in orig_cols:
    a = src[c].fillna('__NA__').astype(str)
    b = out_df[c].fillna('__NA__').astype(str)
    cell_diff += int((a != b).sum())
assert cell_diff == 0, f"{cell_diff} sel kolom lama berubah"
print(f"Acceptance (c)(d) OK: 884 baris, 0 sel kolom lama berubah, bha {new_bha}")

# ---------- 7. AUDIT MARKDOWN (100/100 baris berbukti) ----------
import collections
status_ct = collections.Counter(audit_df['status'])
reason_ct = collections.Counter(audit_df['uncertainty_reason'])

md = []
md.append("# V2 Label Audit — 100 Baris `uncertain` (berbukti)")
md.append("")
md.append("**Script:** `code/35_curated_labels_v2.py` (rerunnable, seed **20261001**)")
md.append(f"**Sumber sampel:** `data/volve/labels_curated.csv` (884 baris; pool `uncertain` = {len(unc_idx)})")
md.append("**Tabel audit lengkap:** `data/volve/uncertain_audit_100.csv` (100 baris, semua kolom terisi)")
md.append("")
md.append("## 1. Metode")
md.append("")
md.append("1. `random.seed(20261001)` + `random.sample(pool_uncertain, 100)` — sampel acak reproducible.")
md.append("2. Setiap baris dibaca narasinya (`comments_full`) utuh, lalu diberi:")
md.append("   - `status` — hasil audit atas label `uncertain`;")
md.append("   - `uncertainty_reason` — klasifikasi kenapa baris tetap/semestinya `uncertain`;")
md.append("   - `bha_evidence_quote` — kutipan **verbatim** dari narasi baris itu (divalidasi script: substring ketat, 0 kegagalan);")
md.append("   - `notes` — alasan singkat.")
md.append("3. **Tidak ada label yang diubah.** `bha_relevant` tetap yes 50 / no 263 / uncertain 571. Saran perubahan (`suggest_no` / `suggest_yes`) hanya didokumentasikan di sini sebagai rekomendasi PM — tidak diterapkan ke CSV.")
md.append("")
md.append("## 2. Definisi")
md.append("")
md.append("`status`:")
md.append("")
md.append("| status | arti |")
md.append("|---|---|")
md.append("| `keeps_uncertain` | Narasi tidak cukup untuk memutuskan; label `uncertain` dipertahankan. |")
md.append("| `suggest_no` | Narasi menunjukkan peristiwa di luar cakupan BHA; *kandidat* `no` — **belum diterapkan**. |")
md.append("| `suggest_yes` | Narasi menyebut BHA eksplisit dengan tindakan; *kandidat* `yes` — **belum diterapkan**. |")
md.append("")
md.append("`uncertainty_reason`:")
md.append("")
md.append("| alasan | arti |")
md.append("|---|---|")
md.append("| `thin_narrative` | Narasi terlalu pendek/generik (rapat, satu kalimat rutin, singkatan tanpa konteks). |")
md.append("| `out_of_range` | Peristiwa jelas di luar BHA (permukaan, wellhead/completion, wireline, penanganan casing/floor). |")
md.append("| `ambiguous` | Sinyal campuran: ada unsur downhole/BHA tetapi tidak ada bukti kegagalan atau identitas komponen tidak pasti. |")
md.append("")
md.append("## 3. Ringkasan")
md.append("")
md.append("| status | count |")
md.append("|---|---:|")
for k in ['keeps_uncertain', 'suggest_no', 'suggest_yes']:
    md.append(f"| {k} | {status_ct.get(k, 0)} |")
md.append(f"| **total** | **{sum(status_ct.values())}** |")
md.append("")
md.append("| uncertainty_reason | count |")
md.append("|---|---:|")
for k in ['thin_narrative', 'out_of_range', 'ambiguous']:
    md.append(f"| {k} | {reason_ct.get(k, 0)} |")
md.append(f"| **total** | **{sum(reason_ct.values())}** |")
md.append("")
md.append("Interpretasi: dari 100 sampel, 50 baris (`out_of_range`) secara jelas di luar cakupan BHA, "
          "20 baris (`thin_narrative`) kekurangan narasi untuk diputuskan, dan 30 baris (`ambiguous`) "
          "benar-benar campuran. Ini konsisten dengan keputusan PM: 64,6% `uncertain` adalah fakta jujur, "
          "dan penurunannya hanya boleh berbasis bukti per baris — bukan dipaksa.")
md.append("")
md.append("## 4. Audit per baris (100/100)")
md.append("")
for _, ar in audit_df.iterrows():
    md.append(f"### audit_id={ar['audit_id']} · event_id={ar['event_id']} · {ar['wellbore']} · {ar['event_date']}")
    md.append("")
    md.append(f"- source_code: `{ar['source_code']}` · state_detail: `{ar['state_detail']}` · category: `{ar['category']}` · bha_relevant: `{ar['bha_relevant']}`")
    md.append(f"- outcome: `{ar['outcome_extracted']}` {('(kosong: ' + ar['outcome_reason'] + ')') if not ar['outcome_extracted'] else ''}")
    md.append(f"- component: `{ar['component_extracted']}` {('(kosong: ' + ar['component_reason'] + ')') if not ar['component_extracted'] else ''}")
    md.append(f"- **status**: `{ar['status']}` · **uncertainty_reason**: `{ar['uncertainty_reason']}`")
    md.append(f"- **bukti (kutipan verbatim narasi, {ar['narrative_len']} char)**: > {ar['bha_evidence_quote']}")
    md.append(f"- catatan: {ar['notes']}")
    md.append("")

md.append("## 5. Acceptance yang diverifikasi script")
md.append("")
md.append(f"- (a) kolom `outcome`/`component` ada; {n_out} + {n_comp} nilai non-kosong semuanya diturunkan ulang dari `comments_full` barisnya sendiri (0 mismatch).")
md.append("- (b) 100/100 baris `uncertain` teraudit: `status`, `uncertainty_reason`, `bha_evidence_quote` (verbatim), `notes` — 0 kolom kosong.")
md.append("- (c) jumlah baris tetap 884.")
md.append("- (d) angka lama tidak berubah: yes 50 / no 263 / uncertain 571; 0 sel dari 16 kolom lama berubah.")
md.append("- (e) dokumen ini bebas klaim terlarang `08_TODO` §10 (dicek script).")
md.append("")

doc_text = "\n".join(md)
FORBIDDEN = [
    "0,955", "0.955", "accuracy 0,955",
    "external validation",
    "sistem deployed Halliburton",
    "A1/A2/C2", "A1, A2, C2",
    "membuktikan predictive maintenance",
    "training/competence",
]
hits = [f for f in FORBIDDEN if f.lower() in doc_text.lower()]
assert not hits, f"Klaim terlarang terdeteksi di doc: {hits}"
AUDIT_MD.write_text(doc_text, encoding='utf-8')
print(f"Audit MD: {AUDIT_MD} ({len(doc_text)} bytes, 100 baris)")
print("Acceptance (b)(e) OK: 100/100 terisi verbatim, 0 klaim terlarang")

# ---------- 8. LOG ----------
log = {
    'script': '35_curated_labels_v2.py',
    'timestamp': pd.Timestamp.now().isoformat(),
    'input_rows': 884,
    'output_rows': int(len(out_df)),
    'output_cols': int(out_df.shape[1]),
    'original_bha_counts': orig_bha,
    'new_bha_counts': new_bha,
    'old_column_cell_diffs': cell_diff,
    'outcome_rows_with_value': n_out,
    'component_rows_with_value': n_comp,
    'rederive_mismatch': bad,
    'audit_sample_size': 100,
    'audit_seed': 20261001,
    'audit_status_counts': dict(status_ct),
    'audit_reason_counts': dict(reason_ct),
    'audit_quotes_verified': 100,
    'forbidden_claims_hits': len(hits),
    'exit_code': 0,
}
LOG_JSON.write_text(json.dumps(log, indent=2), encoding='utf-8')
print("Log written.")
print("DONE - exit 0")
sys.exit(0)
