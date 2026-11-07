"""R2: berapa iterasi Monte Carlo yang memberi CI stabil?

Dua pertanyaan nyata yang dijawab dengan run, bukan tebakan:

A. MC nonparametrik (bootstrap) untuk CI proporsi/FAR pada data nyata kita
   (stuck K-ii: n=95.925 baris, 389 positif; hyd K-i hybrid: n=10.401, 865 positif).
   Ukuran: standar error dari batas CI 95% (persentil 2,5% dan 97,5%) diukur
   sebagai simpangan baku antar-seed, untuk N iterasi bertingkat.
   Kriteria stabil: SE batas CI <= 0,005 FAR absolut (0,5 FP/24 jam) DAN <= 1% lebar CI.

B. MC paramterik untuk uji sensitivitas ambang: FAR = FP/24 jam = f(tau).
   Di sini yang diukur adalah galat baku rerata FAR akibat jumlah iterasi
   simulasi Poisson/binomial. Kriteria: galat baku relatif <= 1%.

Semua angka ditulis ke scratch/rnd_r2/mc_result.json. Tidak memakai numpy:
bootstrap disampling dengan random.Random(seed) agar reproducible.
"""
import json
import math
import random
import statistics
import time

OUT = "/mnt/d/Capstone 1(v2)/scratch/rnd_r2/mc_result.json"
RES = {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "runs": {}}

# ---------------- A. Bootstrap CI untuk FAR pada data nyata ----------------
# Populasi diambil dari hasil pipeline V9-I1 (JSON primer):
#   stuck K-ii rf/glob: n=95.925, neg=95.536, fp=40  -> FAR 0,603 FP/24jam
#   hyd K-i hybrid    : n=10.401, neg=9.536, fp=110  -> FAR 16,611 FP/24jam
# FAR didefinisikan FP per 24 jam negatif (jendela 60 dtk) => FAR = fp/neg * 1440.
CASES = {
    "stuck_k2_rf": {"neg": 95536, "fp": 40, "far_json": 0.603},
    "hyd_ki_hybrid": {"neg": 9536, "fp": 110, "far_json": 16.611},
}

ITER_GRID = [200, 500, 1000, 2000, 5000, 10000]
SEEDS = [11, 22, 33, 44, 55]


def far_boot(neg, fp, n_iter, seed):
    """Bootstrap nonparametrik: resample n=neg+fp label biner, hitung FAR."""
    rng = random.Random(seed)
    total = neg + fp
    p = fp / total
    out = []
    for _ in range(n_iter):
        if hasattr(rng, "binomialvariate"):
            k = rng.binomialvariate(total, p)
        else:
            k = sum(1 for _ in range(total) if rng.random() < p)
        f = k / max(1, (total - k)) * 1440.0
        out.append(f)
    out.sort()
    lo = out[int(0.025 * (n_iter - 1))]
    hi = out[int(0.975 * (n_iter - 1))]
    return lo, hi


for name, c in CASES.items():
    neg, fp = c["neg"], c["fp"]
    rows = []
    print(f"\n=== {name}: neg={neg} fp={fp} (FAR JSON {c['far_json']}) ===")
    for n_iter in ITER_GRID:
        los, his, widths = [], [], []
        for s in SEEDS:
            lo, hi = far_boot(neg, fp, n_iter, s)
            los.append(lo); his.append(hi); widths.append(hi - lo)
        se_lo = statistics.pstdev(los)
        se_hi = statistics.pstdev(his)
        se_w = statistics.pstdev(widths)
        mean_w = statistics.mean(widths)
        rows.append({"n_iter": n_iter, "se_lo": se_lo, "se_hi": se_hi,
                     "mean_width": mean_w, "se_width": se_w,
                     "se_rel_pct_of_width": 100 * se_w / mean_w if mean_w else None,
                     "ci_lo_range": [min(los), max(los)], "ci_hi_range": [min(his), max(his)]})
        print(f"  N={n_iter:6d} SE(lo)={se_lo:8.4f} SE(hi)={se_hi:8.4f} lebar={mean_w:8.4f} SE(lebar)={se_w:7.4f} ({100*se_w/mean_w:5.2f}% lebar)")
    RES["runs"][name] = {"neg": neg, "fp": fp, "grid": rows}

# ---------------- B. Simulasi ambang: FAR = f(tau) ----------------
# Model operasional: pada jendela 1 menit, FP per jendela = q(tau); FAR = q*1440.
# Simulasi Poisson: hitung galat baku relatif rerata FAR untuk N iterasi.
TAUS = {"q=0.0035 (stuck far 0.6)": 0.603 / 1440, "q=0.0115 (hyd far 16.6)": 16.611 / 1440,
        "q=0.0416 (shk far 6.6 per 24jam neg)": 6.618 / 1440}
RES["threshold_sim"] = {}
print("\n=== Simulasi Poisson: galat baku relatif rerata FAR ===")
for label, q in TAUS.items():
    rows = []
    for n_iter in ITER_GRID:
        far_means = []
        for s in SEEDS[:3]:
            rng = random.Random(1000 + s)
            acc = 0
            for _ in range(n_iter):
                # jumlah FP per 1440 menit ~ Poisson(q*1440)
                lam = q * 1440
                # Poisson via Knuth (lam kecil -> cepat)
                L = math.exp(-lam)
                k, prod = 0, rng.random()
                while prod > L:
                    k += 1
                    prod *= rng.random()
                acc += k
            far_means.append(acc / n_iter)
        m = statistics.mean(far_means)
        sd = statistics.pstdev(far_means)
        rel = 100 * sd / m if m else None
        rows.append({"n_iter": n_iter, "mean_far": m, "sd": sd, "rel_sd_pct": rel})
        print(f"  {label:42s} N={n_iter:6d} FAR_mean={m:8.4f} sd={sd:7.4f} rel_sd={rel:6.2f}%")
    RES["threshold_sim"][label] = {"q": q, "grid": rows}

json.dump(RES, open(OUT, "w"), indent=1)
print("\nSaved", OUT)
