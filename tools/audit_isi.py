"""Gerbang audit isi: tidak ada berkas masuk dokumen tanpa putusan auditor.

Berkas yang wajib diaudit dicatat di tools/audit_isi.json beserta sidik jari
sha256 keadaan yang diaudit. Bila isi berkas berubah, sidik jari tidak cocok
dan gerbang menolak commit sampai audit baru dicatat.

Pakai:
    python3 tools/audit_isi.py catat docs/PPT1_PROPOSAL_FINAL_V3.md \
        --putusan LAYAK --auditor "pembaca independen" --bukti "temuan ..."
    python3 tools/audit_isi.py periksa
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

AKAR = Path(__file__).resolve().parent
CATATAN = AKAR / "audit_isi.json"
WAJIB = [
    "docs/PPT1_PROPOSAL_FINAL_V3.md",
    "docs/assets/fig_vsm_v3.png",
    "docs/assets/vsm_v3.map.json",
]
PUTUSAN_SAH = {"LAYAK", "SAMPAH"}


def sidik(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def muat() -> dict:
    if CATATAN.exists():
        return json.loads(CATATAN.read_text(encoding="utf-8"))
    return {"berkas": {}}


def simpan(data: dict) -> None:
    CATATAN.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def catat(args) -> int:
    putusan = args.putusan.upper()
    if putusan not in PUTUSAN_SAH:
        print(f"putusan tidak sah: {args.putusan}", file=sys.stderr)
        return 2
    path = Path(args.path)
    if not path.exists():
        print(f"berkas tidak ada: {path}", file=sys.stderr)
        return 2
    data = muat()
    data["berkas"][args.path] = {
        "sha256": sidik(path),
        "putusan": putusan,
        "auditor": args.auditor,
        "bukti": args.bukti,
    }
    simpan(data)
    print(f"CATAT {args.path} putusan {putusan} oleh {args.auditor}")
    return 0


def periksa() -> int:
    data = muat()
    gagal = []
    for path in WAJIB:
        berkas = Path(path)
        entri = data["berkas"].get(path)
        if not berkas.exists():
            gagal.append(f"{path}: berkas tidak ada")
            continue
        if entri is None:
            gagal.append(f"{path}: belum pernah diaudit")
            continue
        if entri["sha256"] != sidik(berkas):
            gagal.append(f"{path}: isi berubah setelah audit, audit lama tidak berlaku")
            continue
        if entri["putusan"] != "LAYAK":
            gagal.append(f"{path}: putusan auditor {entri['putusan']}")
            continue
        print(f"  {path}: LAYAK oleh {entri['auditor']}")
    if gagal:
        for baris in gagal:
            print(f"  TIDAK LAYAK {baris}")
        print("GERBANG: isi belum lulus audit, commit ditolak")
        return 1
    print("GERBANG: seluruh isi lulus audit")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="perintah", required=True)
    c = sub.add_parser("catat")
    c.add_argument("path")
    c.add_argument("--putusan", required=True)
    c.add_argument("--auditor", required=True)
    c.add_argument("--bukti", required=True)
    c.set_defaults(fungsi=catat)
    p = sub.add_parser("periksa")
    p.set_defaults(fungsi=lambda _: periksa())
    args = parser.parse_args()
    return args.fungsi(args)


if __name__ == "__main__":
    sys.exit(main())
