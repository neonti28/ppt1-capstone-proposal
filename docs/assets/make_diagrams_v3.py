"""Gambar rich picture dan diagram tulang ikan untuk naskah V3.

Isi gambar dibaca langsung dari tabel di PPT1_PROPOSAL_FINAL_V3.md, sehingga
gambar tidak dapat menyimpang dari naskah. Jalankan:

    /home/neonti/.venvs/ppt1_figs/bin/python docs/assets/make_diagrams_v3.py
"""

from __future__ import annotations

import pathlib
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DOK = pathlib.Path(__file__).resolve().parents[1] / "PPT1_PROPOSAL_FINAL_V3.md"
KELUAR = pathlib.Path(__file__).resolve().parent
BARIS = DOK.read_text(encoding="utf-8").split("\n")


def potong(mulai: str, akhir: str) -> list[str]:
    i = next(k for k, x in enumerate(BARIS) if x.startswith(mulai))
    j = next(k for k, x in enumerate(BARIS[i + 1 :], i + 1) if x.startswith(akhir))
    return BARIS[i:j]


def sel(baris: str) -> list[str]:
    return [c.strip() for c in baris.strip().strip("|").split("|")]


# ---------------------------------------------------------------- simpul dan relasi
simpul = []
for x in potong("#### Daftar elemen: simpul", "#### Daftar elemen: relasi"):
    if x.startswith("| S"):
        s = sel(x)
        simpul.append({"id": s[0], "nama": s[1], "jenis": s[2]})

relasi = []
for x in potong("#### Daftar elemen: relasi", "#### Loop umpan balik"):
    if x.startswith("| R"):
        s = sel(x)
        relasi.append({"id": s[0], "teks": s[1], "arah": s[2]})

assert len(simpul) == 12, len(simpul)
assert len(relasi) == 11, len(relasi)

# kolom tata letak menurut jenis simpul
KOLOM = {
    "Fasilitas": 0,
    "Persediaan": 0,
    "Lingkungan": 0,
    "Proses": 1,
    "Objek": 2,
    "Keputusan": 3,
    "Pihak luar": 4,
}
WARNA = {
    "Fasilitas": "#1565c0",
    "Persediaan": "#8d6e63",
    "Lingkungan": "#8d6e63",
    "Proses": "#2e7d32",
    "Objek": "#c62828",
    "Keputusan": "#ef6c00",
    "Pihak luar": "#ef6c00",
}

posisi: dict[str, tuple[float, float]] = {}
for jenis_kolom in range(5):
    anggota = [x for x in simpul if KOLOM.get(x["jenis"], 1) == jenis_kolom]
    jumlah = len(anggota)
    for urut, x in enumerate(anggota):
        y = 9.0 if jumlah == 1 else 9.0 - urut * (7.6 / (jumlah - 1))
        posisi[x["id"]] = (jenis_kolom * 3.0 + 1.70, y)

gambar, sumbu = plt.subplots(figsize=(17.5, 11.5))
sumbu.set_xlim(-0.3, 15.1)
sumbu.set_ylim(0.0, 11.2)
sumbu.axis("off")

urut_relasi = 0
for r in relasi:
    pasang = []
    bagian = [b.strip() for b in r["arah"].split(",")]
    for b in bagian:
        if " ke " in b:
            a, k = b.split(" ke ")
            if a in posisi and k in posisi:
                pasang.append((a, k))
    for (a, k) in pasang:
        urut_relasi += 1
        x1, y1 = posisi[a]
        x2, y2 = posisi[k]
        panah = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.3,
            color="#455a64",
            shrinkA=58,
            shrinkB=58,
            connectionstyle=f"arc3,rad={0.05 + 0.06 * ((urut_relasi - 1) % 4)}",
            zorder=1,
        )
        sumbu.add_patch(panah)
        label = "\n".join(textwrap.wrap(r["id"] + " " + r["teks"], 26))
        f_label = 0.30 + 0.16 * ((urut_relasi - 1) % 4)
        sumbu.text(
            x1 + (x2 - x1) * f_label,
            y1 + (y2 - y1) * f_label,
            label,
            ha="center",
            va="center",
            fontsize=6.0,
            color="#455a64",
            zorder=2,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
        )

for x in simpul:
    xk, yk = posisi[x["id"]]
    sumbu.add_patch(
        FancyBboxPatch(
            (xk - 1.32, yk - 0.55),
            2.64,
            1.10,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            linewidth=1.4,
            edgecolor=WARNA.get(x["jenis"], "#37474f"),
            facecolor=WARNA.get(x["jenis"], "#37474f") + "1f",
            zorder=3,
        )
    )
    sumbu.text(
        xk,
        yk + 0.17,
        x["id"] + " " + x["nama"],
        ha="center",
        va="center",
        fontsize=7.0,
        weight="bold",
        color="#1c1c1c",
        zorder=4,
    )
    sumbu.text(
        xk,
        yk - 0.28,
        x["jenis"],
        ha="center",
        va="center",
        fontsize=6.4,
        style="italic",
        color="#546e7a",
        zorder=4,
    )

# penanda gangguan pada simpul yang bersangkutan
PENANDA = {"S1": "G1", "S6": "G2", "S3": "G3", "S10": "G4"}
for kode, label in PENANDA.items():
    if kode not in posisi:
        continue
    xk, yk = posisi[kode]
    pihak = -1 if kode == "S1" else 1
    sumbu.text(
        xk + pihak * 1.28,
        yk + 0.62,
        label,
        ha="center",
        va="center",
        fontsize=7.5,
        weight="bold",
        color="white",
        zorder=5,
        bbox=dict(boxstyle="circle,pad=0.22", facecolor="#b71c1c", edgecolor="none"),
    )

sumbu.text(
    0.1,
    11.05,
    "Rich Picture: siklus kegagalan BHA sebagai perpindahan tool, data, dan keputusan\n"
    "12 simpul, 11 relasi berarah, 3 loop, 4 penanda gangguan, isi dibaca dari tabel 1.1.4",
    fontsize=11.5,
    weight="bold",
    va="top",
)
gambar.tight_layout()
gambar.savefig(KELUAR / "fig10_rich_picture_v3.png", dpi=190, bbox_inches="tight", facecolor="white")
plt.close(gambar)

# ---------------------------------------------------------------- tulang ikan 6M
CABANG = [
    ("MAN", "atas"),
    ("METHOD", "atas"),
    ("MACHINE", "atas"),
    ("MATERIAL", "bawah"),
    ("MEASUREMENT", "bawah"),
    ("ENVIRONMENT", "bawah"),
]

cabang_data = []
for label, posisi_sisi in CABANG:
    mulai = f"#### {label} ("
    i = next(k for k, x in enumerate(BARIS) if x.startswith(mulai))
    j = next(
        (k for k, x in enumerate(BARIS[i + 1 :], i + 1) if x.startswith("#### ") or x.startswith("### ") or x.startswith("## ")),
        len(BARIS),
    )
    potongan = BARIS[i:j]
    ranting = []
    for x in potongan:
        if x.startswith("| "):
            s = sel(x)
            if len(s) >= 3 and s[0] in {"Mn1", "Mn2", "Mn3", "Mn4", "Me1", "Me2", "Me3", "Me4",
                                        "Ma1", "Ma2", "Ma3", "Ma4", "Mt1", "Mt2", "Mt3", "Mt4",
                                        "Ms1", "Ms2", "Ms3", "Ms4", "En1", "En2", "En3", "En4"}:
                ranting.append(f"{s[0]} {s[1]}")
    assert len(ranting) == 4, (label, ranting)
    cabang_data.append({"label": label, "posisi": posisi_sisi, "ranting": ranting})

assert sum(len(c["ranting"]) for c in cabang_data) == 24

gambar, sumbu = plt.subplots(figsize=(22, 11.6))
sumbu.set_xlim(0, 24)
sumbu.set_ylim(-5.6, 5.6)
sumbu.axis("off")

sumbu.annotate(
    "",
    xy=(18.9, 0),
    xytext=(0.4, 0),
    arrowprops=dict(arrowstyle="-|>,head_width=0.28,head_length=0.7", linewidth=3.2, color="#263238"),
)
sumbu.add_patch(
    FancyBboxPatch(
        (18.9, -1.15),
        3.3,
        2.3,
        boxstyle="round,pad=0.12,rounding_size=0.16",
        linewidth=2.0,
        edgecolor="#b71c1c",
        facecolor="#ffebee",
    )
)
sumbu.text(
    20.55,
    0.0,
    "Kegagalan BHA yang datang\ntanpa peringatan dini,\nmenimbulkan kerugian waktu,\nbiaya, energi, dan keselamatan",
    ha="center",
    va="center",
    fontsize=9,
    weight="bold",
    color="#b71c1c",
)

WARNA_CABANG = {
    "MAN": "#5d4037",
    "MATERIAL": "#5d4037",
    "MACHINE": "#1565c0",
    "MEASUREMENT": "#1565c0",
    "METHOD": "#2e7d32",
    "ENVIRONMENT": "#2e7d32",
}

for urut, c in enumerate(cabang_data):
    atas = c["posisi"] == "atas"
    x_pangkal = 2.5 + urut * 2.35
    arah = 1 if atas else -1
    x_ujung = x_pangkal + 1.05
    y_ujung = arah * 4.3
    warna_cabang = WARNA_CABANG[c["label"]]
    sumbu.plot([x_pangkal, x_ujung], [0, y_ujung], linewidth=2.6, color=warna_cabang)
    sumbu.text(
        x_ujung,
        y_ujung + arah * 0.32,
        c["label"],
        ha="center",
        va="bottom" if atas else "top",
        fontsize=11.5,
        weight="bold",
        color=warna_cabang,
    )
    for k, r in enumerate(c["ranting"]):
        f = (k + 1) / (len(c["ranting"]) + 1)
        xb = x_pangkal + (x_ujung - x_pangkal) * f
        yb = y_ujung * f
        panjang = 1.20
        sumbu.plot([xb, xb + panjang], [yb, yb + arah * 0.42], linewidth=1.1, color="#546e7a")
        teks = "\n".join(textwrap.wrap(r, 26))
        sumbu.text(
            xb + panjang + 0.06,
            yb + arah * 0.42,
            teks,
            ha="left",
            va="center",
            fontsize=5.4,
            color="#263238" if atas else "#37474f",
            zorder=5,
            bbox=dict(boxstyle="round,pad=0.10", facecolor="white", edgecolor="none", alpha=0.92),
        )

sumbu.text(
    0.2,
    5.45,
    "Gambar 3: diagram tulang ikan 6M, 6 cabang dan 24 ranting\n"
    "Isi ranting dibaca dari tabel 1.2.3, efek menyatakan kegagalan BHA dan kerugiannya",
    fontsize=11,
    weight="bold",
    va="top",
)
gambar.tight_layout()
gambar.savefig(KELUAR / "fig11_fishbone_v3.png", dpi=190, bbox_inches="tight", facecolor="white")
plt.close(gambar)

print("selesai: fig10_rich_picture_v3.png dan fig11_fishbone_v3.png")
print("simpul:", len(simpul), "relasi:", len(relasi), "cabang:", len(cabang_data))
print("ranting:", sum(len(c["ranting"]) for c in cabang_data))
