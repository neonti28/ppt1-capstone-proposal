import re
p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_build.py"
s = open(p).read()
TIER = {"A01":2,"A02":1,"A03":1,"A04":2,"A05":1,"A06":2,"A07":2,"A08":1,"A09":1,"A10":3,
        "A11":1,"A12":0,"A13":0,"A14":0,"A15":2,"A16":2,"A17":2,"A18":1,"A19":2,"A20":1,
        "A21":0,"A22":0,"A23":0,"A24":0,"A25":0,"A26":1,"A27":0,"A28":0}
old_sig = '''def alg(kode, nama, sumber, cells, biaya, risiko, catatan=""):
    A.append({"kode": kode, "nama": nama, "sumber": sumber,
              "cells": cells, "biaya": biaya, "risiko": risiko, "catatan": catatan})'''
new_sig = '''def alg(kode, nama, sumber, tier, cells, biaya, risiko, catatan=""):
    """tier = potensi naik tier 0-3, penilaian terpisah dari skor kesesuaian sel."""
    A.append({"kode": kode, "nama": nama, "sumber": sumber, "tier": tier,
              "cells": cells, "biaya": biaya, "risiko": risiko, "catatan": catatan})'''
if old_sig in s:
    s = s.replace(old_sig, new_sig)
for kode, t in TIER.items():
    # form A: alg("Axx", "..", "..", {      -> add tier + cells=
    patA = re.compile(r'(alg\("%s", "[^"]*", "[^"]*")\s*,\s*\{' % kode)
    s, nA = patA.subn(r'\1, tier=%d, cells={' % t, s)
    if nA == 0:
        # form B: already has tier=N, cells={
        patB = re.compile(r'(alg\("%s", "[^"]*", "[^"]*", tier=)\d+(, cells=\{)' % kode)
        s, nB = patB.subn(r'\g<1>%d\g<2>' % t, s)
        assert nB == 1, (kode, nA, nB)
    else:
        assert nA == 1, (kode, nA)
open(p, "w").write(s)
print("patched")
