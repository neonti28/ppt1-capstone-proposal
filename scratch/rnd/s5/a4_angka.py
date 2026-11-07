#!/usr/bin/env python3
"""Cakupan angka dokumen terhadap ledger dan artefak JSON.

Setiap angka di dokumen (tabel dan prosa) dicari di (a) blok ledger kartu dan
(b) nilai numerik artefak JSON kartu. Angka yang tidak ditemukan di keduanya
disebut ORPHAN dan wajib ditinjau manusia sebelum dianggap cacat.
"""
import json
import pathlib
import re
import sys

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")
LEDGER = BASE / "docs/RND_PROVENANCE_LEDGER.md"
DOC = {
    "S1": "docs/RND_S1_SEED_ROBUSTNESS.md",
    "S2": "docs/RND_S2_HYBRID_VIB_SSI.md",
    "S3": "docs/RND_S3_HYBRID_BITWEAR.md",
    "S4": "docs/RND_S4_LAYER_B_DATA.md",
}
CARD = {"S1": "s1", "S2": "s2", "S3": "s3", "S4": "s4"}

NUM = re.compile(r"(?<![\w.])(\d+(?:[.,]\d+)?)(?![\w])")


def norm(tok):
    t = tok.replace(".", "").replace(",", ".") if re.search(r"\d[,.]\d", tok) else tok
    try:
        return float(t)
    except ValueError:
        return None


def kanon(x):
    """Representasi pembanding: buang nol di belakang, 6 desimal maksimum."""
    if x is None:
        return None
    return ("%.6f" % float(x)).rstrip("0").rstrip(".")


def angka_json(o, keluar):
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        keluar.add(kanon(o))
    elif isinstance(o, str):
        pass
    elif isinstance(o, dict):
        for v in o.values():
            angka_json(v, keluar)
    elif isinstance(o, list):
        for v in o:
            angka_json(v, keluar)


def ledgers():
    t = LEDGER.read_text(encoding="utf-8").splitlines()
    blok, cur, nama = {}, None, None
    for l in t:
        if l.startswith("## Bagian"):
            cur = l
            nama = re.search(r"Bagian (S\d)", l)
            nama = nama.group(1) if nama else None
            if nama:
                blok[nama] = []
            continue
        if cur and nama:
            blok[nama].append(l)
    return {k: "\n".join(v) for k, v in blok.items()}


def main():
    L = ledgers()
    hasil = {}
    for card, rel in DOC.items():
        doc = (BASE / rel).read_text(encoding="utf-8")
        kartu = CARD[card]
        jset = set()
        for p in (BASE / "scratch/rnd" / kartu).glob("*.json*"):
            try:
                if p.suffix == ".jsonl":
                    for line in p.read_text(encoding="utf-8").splitlines():
                        if line.strip():
                            angka_json(json.loads(line), jset)
                else:
                    angka_json(json.loads(p.read_text(encoding="utf-8")), jset)
            except Exception as e:
                print("GAGAL", p.name, e, file=sys.stderr)

        lteks = L.get(card, "")
        lset = {kanon(norm(m.group(1))) for m in NUM.finditer(lteks)}
        lset.discard(None)

        tokens = []
        for i, line in enumerate(doc.splitlines(), 1):
            if line.startswith("#"):
                continue
            for m in NUM.finditer(line):
                v = norm(m.group(1))
                if v is None:
                    continue
                tokens.append((i, m.group(1), kanon(v), line.strip().startswith("|")))

        # buang angka struktural: nomor bagian/tabel dan tahun
        def struktural(tok, v, tabel):
            if v is None:
                return True
            if 1900 <= v <= 2100 and float(v).is_integer():
                return True
            if not tabel and float(v).is_integer() and v <= 40 and len(tok) <= 2:
                return True
            return False

        dipakai = [t for t in tokens if not struktural(t[1], norm(t[1]), t[3])]
        in_led = [t for t in dipakai if t[2] in lset]
        in_js = [t for t in dipakai if t[2] in jset]
        both = [t for t in dipakai if t[2] in lset and t[2] in jset]
        orphan = [t for t in dipakai if t[2] not in lset and t[2] not in jset]
        hasil[card] = dict(
            n_angka=len(dipakai), n_di_ledger=len(in_led), n_di_json=len(in_js),
            n_keduanya=len(both), n_orphan=len(orphan),
            frac_ledger=round(len(in_led) / max(len(dipakai), 1), 4),
            frac_json=round(len(in_js) / max(len(dipakai), 1), 4),
            orphan_unik=sorted({(t[1], t[0]) for t in orphan})[:80],
            contoh_tanpa_ledger=sorted({t[1] for t in dipakai if t[2] not in lset})[:40],
        )
        print("=" * 70)
        print(card, rel)
        print(f"  angka diperiksa {len(dipakai)} | di ledger {len(in_led)} "
              f"({hasil[card]['frac_ledger']:.2%}) | di JSON {len(in_js)} "
              f"({hasil[card]['frac_json']:.2%}) | keduanya {len(both)} | orphan {len(orphan)}")
        print("  contoh angka yang TIDAK ada di ledger:", hasil[card]["contoh_tanpa_ledger"][:25])
        print("  orphan unik (angka, baris):", hasil[card]["orphan_unik"][:25])

    out = BASE / "scratch/rnd/s5/s5_angka_coverage.json"
    out.write_text(json.dumps(hasil, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nWROTE", out)


if __name__ == "__main__":
    main()
