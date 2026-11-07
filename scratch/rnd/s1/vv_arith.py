vals = {
 "rasio_baris_per_kalender": 32.256/3.5302,
 "rentang_FAR_kalender": 8.9132-0.4059,
 "kali_FAR": 8.9132/0.4059,
 "delta_far_rule_minus_H1": 3.5302-6.932,
 "delta_presisi": 0.7789-0.6835,
 "delta_recall": 0.5638-0.7507,
 "delta_onset": 307-219,
 "delta_fp_F14": 215-110,
 "delta_lead": 11.5-6.0,
}
for k,v in vals.items(): print(f"{k:26s} {round(v,4)}")
