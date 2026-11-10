"""Gambar rich picture dan diagram tulang ikan G1.

Isi gambar dibaca langsung dari tabel di PPT1_PROPOSAL_FINAL_V2.md, sehingga
gambar tidak dapat menyimpang dari naskah. Jalankan:

    /home/neonti/.venvs/ppt1_figs/bin/python docs/assets/make_diagrams.py
"""

from __future__ import annotations

import re
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DOK = pathlib.Path(__file__).resolve().parents[1] / "PPT1_PROPOSAL_FINAL_V2.md"
KELUAR = pathlib.Path(__file__).resolve().parent
TEKS = DOK.read_text(encoding="utf-8")
BARIS = TEKS.split("\n")


def potong(mulai: str, akhir: str) -> list[str]:
    i = next(k for k, x in enumerate(BARIS) if x.startswith(mulai))
    j = next(k for k, x in enumerate(BARIS[i + 1 :], i + 1) if x.startswith(akhir))
    return BARIS[i:j]


def sel(baris: str) -> list[str]:
    return [c.strip() for c in baris.strip().strip("|").split("|")]


# ---------------------------------------------------------------- simpul dan relasi
simpul = []
for x in potong("#### Daftar elemen: simpul", "#### Daftar elemen: relasi"):
    if x.startswith("| N"):
        s = sel(x)
        simpul.append({"id": s[0], "nama": s[1], "jenis": s[2]})

relasi = []
for x in potong("#### Daftar elemen: relasi", "#### "):
    if x.startswith("| R"):
        s = sel(x)
        relasi.append({"id": s[0], "dari": s[1], "ke": s[2], "label": s[3], "jenis": s[4]})

assert len(simpul) == 14, len(simpul)
assert len(relasi) == 13, len(relasi)

# ---------------------------------------------------------------- tata letak kolom
KOLOM = {
    "Lingkungan fisik": 0,
    "Peralatan": 0,
    "Aliran data": 1,
    "Penyimpanan": 1,
    "Proses": 2,
    "Proses baru": 2,
    "Antarmuka": 3,
    "Aktor manusia": 3,
    "Aktor eksternal": 3,
    "Aktor proyek": 4,
    "Dampak": 4,
    "Sumber label": 0,
}
WRANA = {
    "Lingkungan fisik": "#8d6e63",
    "Peralatan": "#8d6e63",
    "Aliran data": "#1565c0",
    "Penyimpanan": "#1565c0",
    "Proses": "#2e7d32",
    "Proses baru": "#2e7d32",
    "Antarmuka": "#6a1b9a",
    "Aktor manusia": "#ef6c00",
    "Aktor eksternal": "#ef6c00",
    "Aktor proyek": "#ef6c00",
    "Dampak": "#c62828",
    "Sumber label": "#8d6e63",
}

posisi: dict[str, tuple[float, float]] = {}
for jenis_kolom in range(5):
    anggota = [x for x in simpul if KOLOM.get(x["jenis"], 2) == jenis_kolom]
    jumlah = len(anggota)
    for urut, x in enumerate(anggota):
        y = 8.8 if jumlah == 1 else 8.8 - urut * (7.6 / (jumlah - 1))
        posisi[x["id"]] = (jenis_kolom * 2.95 + 1.70, y)

import textwrap

gambar, sumbu = plt.subplots(figsize=(17.5, 11.5))
sumbu.set_xlim(-0.3, 15.1)
sumbu.set_ylim(0.0, 9.7)
sumbu.axis("off")

# panah digambar lebih dulu supaya berada di belakang kotak
for r in relasi:
    if r["dari"] not in posisi or r["ke"] not in posisi:
        continue
    x1, y1 = posisi[r["dari"]]
    x2, y2 = posisi[r["ke"]]
    panah = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.3,
        color="#455a64",
        shrinkA=58,
        shrinkB=58,
        connectionstyle="arc3,rad=0.05",
        zorder=1,
    )
    sumbu.add_patch(panah)
    label = "\n".join(textwrap.wrap(r["label"], 26))
    sumbu.text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
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
            edgecolor=WRANA.get(x["jenis"], "#37474f"),
            facecolor=WRANA.get(x["jenis"], "#37474f") + "1f",
            zorder=3,
        )
    )
    sumbu.text(
        xk,
        yk + 0.17,
        x["id"] + " " + x["nama"],
        ha="center",
        va="center",
        fontsize=7.6,
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

sumbu.text(
    0.1,
    9.55,
    "Rich Picture: siklus pengeboran sebagai perpindahan data dan keputusan\n"
    "14 simpul, 13 relasi berarah, isi dibaca dari tabel 1.1.4",
    fontsize=11.5,
    weight="bold",
    va="top",
)
gambar.tight_layout()
gambar.savefig(KELUAR / "fig08_rich_picture.png", dpi=190, bbox_inches="tight", facecolor="white")
plt.close(gambar)

# ---------------------------------------------------------------- tulang ikan
cabang = []
for x in potong("| Cabang | Posisi | Label cabang |", "**Aturan gaya gambar G1.**"):
    if re.match(r"^\| B[1-6] \|", x):
        s = sel(x)
        cabang.append({"kode": s[0], "posisi": s[1], "label": s[2], "ranting": s[3]})
assert len(cabang) == 6, len(cabang)

gambar, sumbu = plt.subplots(figsize=(19, 11))
sumbu.set_xlim(0, 20)
sumbu.set_ylim(-5.6, 5.6)
sumbu.axis("off")

sumbu.annotate(
    "",
    xy=(16.4, 0),
    xytext=(0.4, 0),
    arrowprops=dict(arrowstyle="-|>,head_width=0.28,head_length=0.7", linewidth=3.2, color="#263238"),
)
sumbu.add_patch(
    FancyBboxPatch(
        (16.4, -1.15),
        3.3,
        2.3,
        boxstyle="round,pad=0.12,rounding_size=0.16",
        linewidth=2.0,
        edgecolor="#b71c1c",
        facecolor="#ffebee",
    )
)
sumbu.text(
    18.05,
    0.0,
    "Peringatan dini kegagalan BHA\nbelum dapat dioperasikan\nsebagai alarm",
    ha="center",
    va="center",
    fontsize=10,
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

for urut, c in enumerate(cabang):
    atas = "atas" in c["posisi"]
    x_pangkal = 3.0 + urut * 2.05
    arah = 1 if atas else -1
    x_ujung = x_pangkal - 1.0 * arah * 0
    x_ujung = x_pangkal + 1.05
    y_ujung = arah * 4.3
    label_bersih = c["label"].replace("**", "")
    warna_cabang = WARNA_CABANG.get(label_bersih.split()[0], "#455a64")
    sumbu.plot([x_pangkal, x_ujung], [0, y_ujung], linewidth=2.6, color=warna_cabang)
    sumbu.text(
        x_ujung,
        y_ujung + arah * 0.32,
        label_bersih,
        ha="center",
        va="bottom" if atas else "top",
        fontsize=11.5,
        weight="bold",
        color=warna_cabang,
    )
    ranting = [r.strip() for r in c["ranting"].split(";") if r.strip()]
    for k, r in enumerate(ranting):
        f = (k + 1) / (len(ranting) + 1)
        xb = x_pangkal + (x_ujung - x_pangkal) * f
        yb = y_ujung * f
        panjang = 1.45 if atas else 1.45
        # aturan gaya gambar G1 butir 1: ranting yang belum diukur digambar putus-putus
        belum_diukur = bool(re.match(r"^(Me4|Ma3)\b", r))
        sumbu.plot(
            [xb, xb + panjang],
            [yb, yb + arah * 0.42],
            linewidth=1.1,
            color="#546e7a",
            linestyle="--" if belum_diukur else "-",
        )
        teks = r if len(r) <= 40 else r[:38].rstrip() + "..."
        sumbu.text(
            xb + panjang + 0.08,
            yb + arah * 0.42,
            teks,
            ha="left",
            va="center",
            fontsize=6.0,
            color="#263238" if atas else "#37474f",
        )

sumbu.text(
    0.2,
    5.45,
    "Gambar G1: diagram tulang ikan 6M, 6 cabang dan 27 ranting\n"
    "Garis putus-putus menandai ranting yang belum diukur, dibaca dari tabel 1.2.6",
    fontsize=11,
    weight="bold",
    va="top",
)
gambar.tight_layout()
gambar.savefig(KELUAR / "fig09_fishbone_g1.png", dpi=190, bbox_inches="tight", facecolor="white")
plt.close(gambar)

print("selesai: fig08_rich_picture.png dan fig09_fishbone_g1.png")
print("simpul:", len(simpul), "relasi:", len(relasi), "cabang:", len(cabang))
print("ranting:", sum(len([r for r in c["ranting"].split(";") if r.strip()]) for c in cabang))
