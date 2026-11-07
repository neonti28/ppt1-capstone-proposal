import glob, os, re
base='/mnt/d/Capstone 1(v2)'
print('=== exact "lulus bersyarat" (case-insens) ===')
for p in glob.glob(base+'/docs/*.md')+glob.glob(base+'/*.md')+[base+'/CHANGELOG.md']:
    t=open(p,encoding='utf-8',errors='replace').read()
    for m in re.finditer(r'lulus\s+bersyarat', t, re.I):
        ln=t[:m.start()].count('\n')+1
        print(os.path.basename(p), ln, t[max(0,m.start()-40):m.start()+40].replace('\n',' '))
print('=== arsip files present ===')
for p in sorted(glob.glob(base+'/docs/*arsip*')): print(os.path.basename(p))
print('=== all *.v*_arsip* anywhere ===')
for p in sorted(glob.glob(base+'/**/*arsip*', recursive=True)): print(p)
