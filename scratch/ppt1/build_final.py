"""Bangun ulang docs/PPT1_PROPOSAL_FINAL.md dari berkas bab.

Urutan baku Bab I sampai Bab IV lalu Daftar Pustaka. Judul bab duplikat dari berkas
lanjutan (tiga berkas Bab III) dibuang supaya dokumen final hanya punya satu H1 per bab.
Preamble diambil dari dokumen final sebelumnya agar catatan revisi tidak hilang.
"""
import pathlib

D = pathlib.Path("/mnt/d/ARCT-9F2/docs")
URUTAN = ["PPT1_BAB1_1.md", "PPT1_BAB1_2.md", "PPT1_BAB1_3.md", "PPT1_BAB1_4.md", "PPT1_BAB2.md",
          "PPT1_BAB3_1.md", "PPT1_BAB3_2.md", "PPT1_BAB3_4_MCDM.md", "PPT1_BAB4.md",
          "PPT1_DAFTAR_PUSTAKA.md"]
TUJUAN = D / "PPT1_PROPOSAL_FINAL.md"


def bangun():
    lama = TUJUAN.read_text()
    preamble = lama[:lama.find("\n---\n")]
    dilihat, bagian = set(), []
    for f in URUTAN:
        baris = (D / f).read_text().strip().split("\n")
        if baris and baris[0].startswith("# "):
            if baris[0] in dilihat:
                baris = baris[1:]
                while baris and not baris[0].strip():
                    baris = baris[1:]
            else:
                dilihat.add(baris[0])
        bagian.append("\n".join(baris))
    teks = preamble.rstrip() + "\n\n---\n\n" + "\n\n---\n\n".join(bagian) + "\n"
    TUJUAN.write_text(teks)
    return teks


if __name__ == "__main__":
    t = bangun()
    h1 = [l for l in t.split("\n") if l.startswith("# ")]
    print("byte:", len(t.encode()), "| H1:", len(h1))
    for l in h1:
        print("  ", l)
