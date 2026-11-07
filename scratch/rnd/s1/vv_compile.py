import py_compile
for f in ("code/rnd_hybrid_harness.py","code/rnd_s1_run.py","code/rnd_s1_ledger.py",
          "code/rnd_s1_dokumen.py","code/rnd_s1_hluas.py","code/rnd_s1_hcheck.py"):
    py_compile.compile(f, doraise=True)
    print("compile OK:", f)
