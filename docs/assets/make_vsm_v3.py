"""Gambar 4 naskah PPT1: value stream map kondisi saat ini menurut Rother & Shook.

Unsur gambar mengikuti daftar simbol Learning to See (Rother & Shook, 2003):
ikon pemasok dan pelanggan, kotak kendali produksi, kotak ketentuan aliran,
kotak proses dengan kotak data (C/T, C/O, uptime, pelaksana), panah dorong
bergaris, ikon pengiriman beserta frekuensi, aliran informasi manual dengan
frekuensi, ledakan kaizen, serta tangga waktu dengan waktu tunggu sumur di bawah
garis dan penantian di atas garis. Ceklis kesesuaian ada di
scratch/ppt1/ceklis_vsm_standar.json.

Angka dibaca dari docs/assets/vsm_v3.map.json supaya gambar dan tabel 2.1.1
tidak mungkin berbeda. Durasi tersimpan dalam hari kerja 8 jam.

Jalankan:
    ~/.venvs/ppt1_figs/bin/python docs/assets/make_vsm_v3.py
"""

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

AKAR = Path(__file__).resolve().parent
PETA = AKAR / "vsm_v3.map.json"
KELUAR = AKAR / "fig_vsm_v3.png"

JAM_PER_HARI = 8
TINTA = "#1b1b1b"
ABU = "#6b6b6b"
AKSEN = "#8c2f1f"
KERTAS = "#faf7f2"

NAMA_BARIS = {
    "Diagnosis": "1. Diagnosis",
    "Penarikan": "2. Penarikan",
    "Pelepasan dan inspeksi": "3. Pelepasan\ndan inspeksi",
    "Perakitan pengganti": "4. Perakitan\npengganti",
    "Uji fungsi": "5. Uji fungsi",
    "Turun kembali": "6. Turun\nkembali",
    "Reaming dan pemulihan": "7. Reaming\ndan pemulihan",
}


def baca_peta():
    data = json.loads(PETA.read_text(encoding="utf-8"))
    langkah = []
    for tahap in data["stages"]:
        langkah.append(
            {
                "nama": tahap["name"],
                "waktu": tahap["wait"]["days"] * JAM_PER_HARI,
                "pelaksana": ", ".join(tahap.get("actors") or []) or "kru rig",
            }
        )
    return langkah


def kotak(ax, x, y, lebar, tinggi, teks, ukuran=8.0, tebal=1.2, latar="white", siku=False):
    gaya = "square,pad=0.0" if siku else "round,pad=0.02"
    ax.add_patch(FancyBboxPatch((x, y), lebar, tinggi, boxstyle=gaya,
                                linewidth=tebal, edgecolor=TINTA, facecolor=latar, zorder=3))
    ax.text(x + lebar / 2, y + tinggi / 2, teks, ha="center", va="center",
            fontsize=ukuran, color=TINTA, zorder=4, linespacing=1.3)


def ikon_pabrik(ax, x, y, teks, lebar=1.7, tinggi=0.8):
    ax.add_patch(Polygon([[x, y + tinggi], [x + lebar / 2, y + tinggi + 0.3], [x + lebar, y + tinggi]],
                         closed=True, edgecolor=TINTA, facecolor="white", linewidth=1.2, zorder=3))
    ax.add_patch(Rectangle((x, y), lebar, tinggi, edgecolor=TINTA, facecolor="white",
                           linewidth=1.2, zorder=3))
    ax.text(x + lebar / 2, y + tinggi / 2 - 0.05, teks, ha="center", va="center", fontsize=7.0,
            color=TINTA, zorder=4, linespacing=1.25)


def ikon_truk(ax, x, y, skala=1.0):
    ax.add_patch(Rectangle((x, y), 0.5 * skala, 0.26 * skala, edgecolor=TINTA,
                           facecolor="white", linewidth=1.0, zorder=6))
    ax.add_patch(Rectangle((x + 0.5 * skala, y), 0.22 * skala, 0.18 * skala, edgecolor=TINTA,
                           facecolor="white", linewidth=1.0, zorder=6))
    for dx in (0.12, 0.44):
        ax.add_patch(plt.Circle((x + dx * skala, y - 0.03 * skala), 0.06 * skala,
                                edgecolor=TINTA, facecolor="white", linewidth=0.9, zorder=7))


def ledakan(ax, x, y, jari=0.28):
    titik = []
    for i in range(20):
        sudut = math.pi * i / 10
        r = jari if i % 2 == 0 else jari * 0.55
        titik.append((x + r * math.cos(sudut), y + r * math.sin(sudut)))
    ax.add_patch(Polygon(titik, closed=True, edgecolor=AKSEN, facecolor="#fdf3ee",
                         linewidth=1.1, zorder=6))


def panah(ax, x1, y1, x2, y2, warna=TINTA, tebal=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", linewidth=tebal, color=warna,
                                linestyle="solid", shrinkA=0, shrinkB=0, mutation_scale=11),
                zorder=5)


def dorong(ax, x1, x2, y):
    """Panah dorong bergaris menurut Learning to See."""
    ax.plot([x1, x2 - 0.16], [y, y], color=TINTA, linewidth=5.2, solid_capstyle="butt", zorder=4)
    ax.plot([x1, x2 - 0.16], [y, y], color="white", linewidth=2.6, linestyle=(0, (1.4, 1.4)),
            solid_capstyle="butt", zorder=5)
    ax.annotate("", xy=(x2, y), xytext=(x2 - 0.2, y),
                arrowprops=dict(arrowstyle="-|>", linewidth=1.2, color=TINTA,
                                shrinkA=0, shrinkB=0, mutation_scale=12), zorder=6)


def audit_tata(ax, fig) -> list:
    """Pemeriksa mekanis: kumpulkan kotak teks dan tolak bila bertumpuk atau keluar bidang."""
    fig.canvas.draw()
    perender = fig.canvas.get_renderer()
    kotak_teks = []
    for teks in ax.texts:
        if not teks.get_text().strip():
            continue
        k = teks.get_window_extent(perender)
        kotak_teks.append((teks.get_text().replace("\n", " ")[:40], k))
    temuan = []
    for i in range(len(kotak_teks)):
        for j in range(i + 1, len(kotak_teks)):
            a, b = kotak_teks[i][1], kotak_teks[j][1]
            if a.overlaps(b):
                temuan.append(
                    f"tumpang-tindih: '{kotak_teks[i][0]}' dan '{kotak_teks[j][0]}'"
                )
    batas = fig.bbox
    for nama, k in kotak_teks:
        if k.x0 < batas.x0 - 1 or k.x1 > batas.x1 + 1 or k.y0 < batas.y0 - 1 or k.y1 > batas.y1 + 1:
            temuan.append(f"keluar bidang: '{nama}'")
    return temuan


def gambar():
    langkah = baca_peta()
    total = sum(butir["waktu"] for butir in langkah)

    fig, ax = plt.subplots(figsize=(16.4, 8.6), dpi=200)
    ax.set_facecolor(KERTAS)
    fig.patch.set_facecolor(KERTAS)
    ax.set_xlim(0, 17.2)
    ax.set_ylim(0, 10.6)
    ax.axis("off")

    # --- baris puncak: pemasok, kendali produksi, pelanggan
    ikon_pabrik(ax, 0.35, 9.15, "Pangkalan dan\nbengkel servis")
    kotak(ax, 3.1, 9.1, 9.4, 0.95, "Kendali operasi\nkru rig dan engineer pengukuran",
          ukuran=8.2, latar="#efefef")
    ikon_pabrik(ax, 14.9, 9.15, "Klien dan\noperator sumur")

    # --- kotak ketentuan aliran (dipisah dari jalur informasi agar tidak bertumpuk)
    kotak(ax, 0.35, 2.05, 2.85, 1.25,
          "Ketentuan aliran\n1 kejadian kegagalan\nsiklus 36 jam\nspread cost 20.000\nUSD per jam (deepwater)",
          ukuran=6.2, tebal=0.9, latar="#f4f1ea", siku=True)

    # --- aliran informasi manual dengan frekuensi
    panah(ax, 1.7, 9.3, 3.1, 9.45, tebal=0.9)
    ax.text(0.35, 8.99, "First Alert dan\nEquipment Failure Report,\nper kejadian", fontsize=6.0,
            color=AKSEN, ha="left", va="top", linespacing=1.25)
    panah(ax, 12.5, 9.45, 14.9, 9.4, tebal=0.9)
    ax.text(12.62, 9.62, "laporan interupsi layanan, per sumur", fontsize=6.0, color=AKSEN,
            ha="left", va="bottom")

    # --- kotak proses, kotak data, panah dorong
    lebar, tinggi = 1.45, 0.95
    kiri, jarak = 3.35, 1.75
    pusat = []
    for i, butir in enumerate(langkah):
        x = kiri + i * jarak
        pusat.append(x + lebar / 2)
        kotak(ax, x, 5.75, lebar, tinggi, NAMA_BARIS.get(butir["nama"], butir["nama"]),
              ukuran=7.0)
        kotak(ax, x, 4.05, lebar, 1.45,
              f"C/T {butir['waktu']:.0f} jam\nC/O —\nuptime —\n{butir['pelaksana']}",
              ukuran=6.0, tebal=0.9, siku=True)
        ax.plot([x + lebar / 2, x + lebar / 2], [5.5, 5.75], color=TINTA, linewidth=0.9, zorder=2)
        if i < len(langkah) - 1:
            dorong(ax, x + lebar + 0.06, x + jarak - 0.06, 6.22)

    # --- pengiriman tool pengganti dari pangkalan ke perakitan
    ax.plot([1.2, 1.2, pusat[3]], [9.15, 8.15, 8.15], color=TINTA, linewidth=1.2, zorder=2)
    panah(ax, pusat[3], 8.15, pusat[3], 6.7, tebal=1.2)
    ikon_truk(ax, 1.5, 8.2, skala=0.9)
    ax.text(2.65, 8.28, "pengiriman tool pengganti, per kejadian", fontsize=6.0, color=TINTA,
            ha="left", va="center")

    # --- aliran informasi dari kendali ke proses dan kembali
    panah(ax, 4.1, 9.1, pusat[0], 6.7, tebal=0.9)
    ax.text(2.95, 7.1, "keputusan\npenarikan", fontsize=6.0, color=AKSEN, ha="left",
            va="center", linespacing=1.2)
    panah(ax, 8.7, 9.1, pusat[3], 6.7, tebal=0.9)
    ax.text(8.85, 7.2, "permintaan tool pengganti", fontsize=6.0, color=AKSEN, ha="left",
            va="center")
    panah(ax, pusat[6], 6.7, 12.3, 9.1, tebal=0.9)
    ax.text(11.0, 7.4, "laporan harian (DDR)\ndan BHA tally, harian", fontsize=6.0,
            color=AKSEN, ha="center", va="center", linespacing=1.2)

    # --- ledakan kaizen pada dua langkah terlama (di atas kotak Penarikan dan Turun kembali)
    for i, jam in ((1, "11 jam"), (5, "9 jam")):
        ledakan(ax, pusat[i], 6.95)
        ax.text(pusat[i] + 0.33, 6.95, jam, fontsize=6.2, color=AKSEN, ha="left", va="center")

    # --- tangga waktu: waktu tunggu sumur di bawah garis, penantian antarproses di atas
    garis, bawah, atas = 3.55, 0.6, 0.55
    x = 3.35
    for butir in langkah:
        bagian = butir["waktu"] / total * 11.9
        ax.add_patch(Rectangle((x, garis - bawah), bagian, bawah, edgecolor=TINTA,
                               facecolor="#e8d6c8", linewidth=0.9, zorder=3))
        ax.text(x + bagian / 2, garis - bawah / 2, f"{butir['waktu']:.0f}", fontsize=6.8,
                ha="center", va="center", color=TINTA, zorder=4)
        x += bagian
    ax.plot([3.35, x], [garis, garis], color=TINTA, linewidth=1.1, zorder=4)
    ax.text(3.35, garis + 0.33, "penantian antarproses: 0 jam (tidak ada antrean terekam)",
            fontsize=6.4, color=ABU, ha="left", va="center")

    # --- jumlah
    ax.text(3.35, 2.45,
            f"Lead time {total:.0f} jam ({(total / JAM_PER_HARI):.1f} hari kerja)".replace(".", ",")
            + f"    waktu tunggu sumur {total:.0f} jam    waktu nilai tambah 0 jam    efisiensi aliran 0 persen",
            fontsize=8.0, color=TINTA, ha="left", va="center")
    ax.text(3.35, 2.1,
            "C/T pada kotak data adalah waktu langkah di rig; waktu nilai tambah diukur dari kemajuan sumur menurut sudut pandang pelanggan, dan seluruh 36 jam tidak menambah satu meter pun.",
            fontsize=6.8, color=ABU, ha="left", va="center")

    # --- legenda
    ax.plot([3.35, 4.15], [1.35, 1.35], color=TINTA, linewidth=1.2)
    ax.text(4.25, 1.35, "aliran material dan pengiriman", fontsize=6.4, color=TINTA,
            ha="left", va="center")
    ax.plot([6.9, 7.7], [1.35, 1.35], color=AKSEN, linewidth=0.9)
    ax.text(7.8, 1.35, "aliran informasi manual", fontsize=6.4, color=TINTA, ha="left", va="center")
    ax.plot([10.3, 11.1], [1.35, 1.35], color=TINTA, linewidth=5.0, solid_capstyle="butt")
    ax.plot([10.3, 11.1], [1.35, 1.35], color="white", linewidth=2.4, linestyle=(0, (1.4, 1.4)),
            solid_capstyle="butt")
    ax.text(11.2, 1.35, "panah dorong", fontsize=6.4, color=TINTA, ha="left", va="center")
    ledakan(ax, 12.85, 1.35, jari=0.16)
    ax.text(13.05, 1.35, "peluang perbaikan (kaizen)", fontsize=6.4, color=TINTA,
            ha="left", va="center")

    ax.text(3.35, 0.75,
            "Besaran yang tidak tercatat pada kejadian ini dan karena itu ditulis strip, bukan angka: waktu ganti (C/O), "
            "uptime, dan cacah operator per langkah.",
            fontsize=6.6, color=ABU, ha="left", va="center")

    temuan = audit_tata(ax, fig)
    fig.savefig(KELUAR, bbox_inches="tight", facecolor=KERTAS)
    print(f"GAMBAR {KELUAR} | langkah {len(langkah)} | lead {total:.0f} jam | nilai tambah 0 jam")
    if temuan:
        for baris in temuan:
            print(f"  CACAT TATA LETAK {baris}")
        raise SystemExit(1)
    print("TATA LETAK: tidak ada teks bertumpuk atau keluar bidang")


if __name__ == "__main__":
    gambar()
