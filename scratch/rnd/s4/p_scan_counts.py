import json
d = json.load(open('/mnt/d/Capstone 1(v2)/scratch/rnd/s4/inventory_raw.json', encoding='utf-8'))
for k in ('pindai_xml_ddr', 'pindai_html_ddr'):
    print(k, {kk: vv for kk, vv in d[k].items() if not isinstance(vv, (dict, list))})
    print('  kemunculan:', d[k]['kemunculan'])
