#!/usr/bin/env python3
import re
p = "/mnt/d/Capstone 1(v2)/docs/V11_ML.md"
doc = open(p, encoding="utf-8").read()
print("EM DASH:", doc.count("—"))
for i, m in enumerate(re.finditer("—", doc), 1):
    print(f"{i:2d}. {doc[max(0, m.start()-70):m.start()+50]!r}")
print("\nEN DASH:", doc.count("–"))
for i, m in enumerate(re.finditer("–", doc), 1):
    print(f"{i:2d}. {doc[max(0, m.start()-50):m.start()+35]!r}")
