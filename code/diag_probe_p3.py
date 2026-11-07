#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe counter anti-leakage: JSON vs arsip vs MD (P3)."""
import json

R = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS.json"
A = "/mnt/d/Capstone 1/docs/V2_ML_BEAT_CANARY_TS_T2D_ARSIP.json"
r = json.load(open(R))
a = json.load(open(A))
print("res.anti_leakage       =", json.dumps(r.get("anti_leakage"))[:400])
print("arsip.anti_leakage     =", json.dumps(a.get("anti_leakage"))[:400])
print("res.anti_leakage_event =", json.dumps(r.get("anti_leakage_event"))[:400])
print("res.koreksi_t2e.P3     =", json.dumps(r["koreksi_t2e"].get("P3"))[:500])
p4 = r["p4_desain_baru"]
print("p4.anti_leakage        =", json.dumps(p4.get("anti_leakage"))[:400])
print("p4.anti_leakage_event  =", json.dumps(p4.get("anti_leakage_event"))[:400])
print("p4.koreksi?            =", "koreksi_t2e" in p4)
