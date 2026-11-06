# TAKSONOMI VISUALISASI MODEL PREDIKTIF

Disusun 2026-10-29. Basis: scikit-learn Visualizations & Inspection guide, SHAP API,
Interpretable ML Book (Molnar: PDP/ICE/ALE), literatur uncertainty visualization
(Padilla & Kay; Hullman HOP; Wilke Fundamentals of Data Visualization),
lift/gain chart (Univ. of Regina CS831), raincloud (Allen et al. 2021).

Total: 12 kelompok, ~140 teknik/varian, ~60 keluarga plot inti.
Tanda: [W] = wajib/dipakai hampir semua paper model prediktif.

---

## A. DATA & FITUR (sebelum/sesudah model)

1. [W] Histogram
2. [W] KDE / density plot
3. ECDF (empirical CDF)
4. [W] Box plot
5. Violin plot
6. Raincloud plot (violin + box + raw jitter)
7. Strip / swarm / beeswarm plot
8. Ridgeline plot
9. [W] Scatter matrix / pairplot
10. Hexbin (2D density untuk data padat)
11. Kontur 2D density (bivariate KDE)
12. [W] Correlation heatmap
13. Correlation matrix (masked upper triangle)
14. Bar chart kategori / countplot (class imbalance)
15. Mosaic plot (kombinasi 2 variabel kategorik)
16. Missing-value matrix / heatmap (missingno)
17. Target distribution per kelas (density/violin overlay)
18. QQ-plot fitur vs normal
19. Lag scatter plot (autokorelasi fitur waktu)

## B. PERFORMA KLASIFIKASI

20. [W] ROC curve + AUC
21. [W] Precision-Recall curve + AP
22. [W] Confusion matrix (raw + row-normalized)
23. DET curve / EER
24. [W] Lift chart (per desil)
25. Cumulative gain chart / CAP curve
26. KS plot (Kolmogorov-Smirnov separation)
27. [W] Calibration curve / reliability diagram (+ Brier score)
28. Threshold sweep plot (precision, recall, F1 vs cut-off)
29. Cost curve (expected cost vs threshold)
30. Class-wise metrics heatmap
31. Score distribution by class (histogram/KDE 2 kelompok)
32. [W] Decision boundary / decision region (2 fitur)
33. Margin / confidence distribution plot
34. Per-class error bar chart

## C. PERFORMA REGRESI + DIAGNOSTIK ASUMSI

35. [W] Predicted vs actual scatter + garis identitas y=x
36. [W] Residual vs fitted values
37. [W] Residual histogram / QQ-plot residual
38. Scale-Location plot (sqrt|residual| vs fitted)
39. Residual vs leverage
40. Cook's distance / influence plot
41. PredictionErrorDisplay (sklearn)
42. Bland-Altman plot (agreement)
43. Error distribution per bin target
44. ACF residual (autokorelasi sisa)
45. Residual over time (time-order plot)

## D. OPTIMASI & SELEKSI MODEL

46. [W] Learning curve (train vs CV score vs n sampel)
47. [W] Validation curve (skor vs satu hiperparameter)
48. Train/val loss curve per epoch
49. Early-stopping view (loss + best epoch marker)
50. Hyperparameter heatmap 2D
51. Parallel coordinates untuk hyperparameter search
52. Grid/random search score surface (3D atau contour)
53. Model comparison bar chart + error bar CI
54. Feature-count vs score curve
55. Metric-vs-fold dot/box plot (stabilitas CV)

## E. INTERPRETASI GLOBAL (XAI)

56. [W] Feature importance bar (impurity/gain)
57. [W] Permutation importance (box/violin, distribusi antar shuffle)
58. [W] SHAP summary / beeswarm plot
59. SHAP bar plot (mean |SHAP|)
60. SHAP heatmap
61. SHAP dependence scatter (warna = fitur interaksi)
62. [W] PDP 1D (partial dependence)
63. PDP 2D (heatmap / contour)
64. [W] ICE curves (individual conditional expectation)
65. [W] ALE plot (menggantikan PDP saat fitur berkorelasi)
66. H-statistic interaction heatmap
67. Surrogate decision tree diagram
68. Break-down / waterfall plot (kontribusi global)
69. LOFO importance plot
70. Functional decomposition (dekomposisi prediksi per komponen)

## F. INTERPRETASI LOKAL (satu prediksi)

71. [W] SHAP waterfall (satu observasi)
72. SHAP force plot
73. SHAP decision plot
74. LIME explanation bar
75. Counterfactual explanation (tabel / spider)
76. Anchor rules (scoped rules)
77. Ceteris paribus plot
78. ICE dengan satu kurva di-highlight

## G. KETIDAKPASTIAN & SIMULASI (termasuk Monte Carlo)

Catatan: "kurva Monte Carlo" bukan nama baku. Nama bakunya:

79. [W] Fan chart (p10/p50/p90, forecast cone)
80. [W] Spaghetti / ensemble plot (banyak run simulasi ditumpuk)
81. Cone of uncertainty (hurricane-style)
82. Quantile dotplot (distribusi sebagai titik yang bisa dihitung)
83. HOP (hypothetical outcome plot, animasi sampel)
84. Error bar / CI whisker
85. Box/violin dari sampel prediksi per observasi
86. Histogram output simulasi
87. CDF / survival curve hasil simulasi
88. [W] Tornado diagram (sensitivitas satu-arah, ranking driver)
89. Sobol index bar / PAWN index
90. Convergence / trace plot (MCMC, cek mixing)
91. Posterior predictive check fan (data vs replikasi)
92. Coverage plot interval (nominal vs aktual)
93. Prediction-interval width vs fitur (lebar ketidakpastian)
94. Reliability diagram ketidakpastian (uncertainty calibration)

## H. STRUKTUR MODEL / ARSITEKTUR (DIAGRAM)

95. [W] Block diagram / pipeline flowchart (data -> fitur -> model -> output)
96. DAG (alur komputasi atau kausal)
97. Computational graph (TensorBoard / Netron)
98. Neural network layer diagram
99. Single decision tree diagram
100. Ensemble architecture diagram (bagging/boosting stack)
101. Surrogate model diagram (glass-box pengganti black-box)
102. Arsitektur perbandingan model (side-by-side block)
103. P&ID (piping & instrumentation diagram) untuk domain proses
104. BHA / wellbore schematic (domain pengeboran)
105. Gantt chart (timeline operasi, mis. run BHA per sumur)
106. Swimlane diagram (SOP/eskalasi)
107. Venn / Euler diagram: HANYA untuk irisan himpunan (overlap fitur, overlap cluster, overlap prediksi antar model), bukan plot performa
108. UpSet plot (pengganti Venn saat >3 himpunan)
109. Quadrant / 2x2 matrix (risk-reward, severity-likelihood)

## I. DATA TINGGI & CLUSTER

110. [W] PCA scatter (PC1 vs PC2) berwarna label
111. PCA biplot (loading vektor fitur)
112. Scree plot (explained variance)
113. [W] t-SNE embedding
114. [W] UMAP embedding
115. MDS plot
116. [W] Dendrogram (hierarchical clustering)
117. [W] Silhouette plot
118. [W] Elbow plot (pemilihan k)
119. Gap statistic plot
120. Cluster profile heatmap (z-score per cluster)
121. Centroid radar / spider chart
122. Voronoi / decision-region map
123. Parallel coordinates (multivariat)
124. Andrews curves
125. Sankey diagram (aliran, mis. error propagation per komponen)
126. Chord diagram
127. Network graph (korelasi/interaksi fitur, graph model)

## J. WAKTU / FORECASTING

128. [W] Time series line + overlay forecast
129. Fan chart per horizon
130. Horizon-wise error bar (MAE per h)
131. ACF plot
132. PACF plot
133. STL / seasonal decomposition (trend-seasonal-residual)
134. Seasonal subseries plot
135. Calendar heatmap
136. Rolling error / rolling metric plot
137. Actual vs predicted overlay per horizon
138. Quantile forecast bands
139. Drift monitoring plot (distribusi fitur/target vs waktu)
140. Adversarial validation score plot (deteksi shift train vs test)

## K. DIAGNOSTIK DOMAIN / ENGINEERING

141. Control chart / SPC (batas kendali proses)
142. Pareto chart (80/20 penyebab)
143. Ishikawa / fishbone (root cause)
144. FMEA / RPN matrix
145. Risk matrix (likelihood x severity)
146. Kaplan-Meier survival curve
147. Weibull probability plot (life data)
148. RUL trajectory plot (remaining useful life)
149. Parameter-vs-depth log plot (mud logging, domain drilling)

## L. VALIDASI & ANTI-LEAKAGE

150. K-fold split diagram
151. Time-series CV split diagram (expanding/sliding window)
152. Metric per fold boxplot
153. Train vs test distribution overlay
154. SHAP stability across folds plot

---

## PETA CEPAT: PERTANYAAN -> PLOT

| Pertanyaan | Plot |
|---|---|
| Apakah model akurat? | predicted vs actual, residual, MAE/RMSE bar |
| Apakah model bisa memisahkan kelas? | ROC, PR, confusion matrix, decision boundary |
| Apakah probabilitas bisa dipercaya? | calibration / reliability diagram, Brier |
| Di mana model gagal? | confusion matrix, residual per segmen, error-by-bin |
| Fitur mana yang menggerakkan prediksi? | feature importance, permutation, SHAP beeswarm |
| Bagaimana bentuk pengaruh satu fitur? | PDP, ICE, ALE, SHAP dependence |
| Kenapa prediksi INI keluar? | SHAP waterfall/force, LIME, counterfactual |
| Apakah overfit/underfit? | learning curve, validation curve |
| Seberapa yakin? | fan chart, interval, quantile dotplot, HOP |
| Apa driver ketidakpastian terbesar? | tornado, Sobol |
| Apakah data terkelompok? | PCA/t-SNE/UMAP, dendrogram, silhouette |
| Apakah ada data leakage/drift? | CV split diagram, adversarial validation, drift plot |
| Bagaimana model dibangun? | block diagram, computational graph, tree diagram |

## KOREKSI TERHADAP 5 KANDIDAT

- Scatter plot: YA, paling fundamental (predicted-vs-actual, residual, SHAP dependence, embedding, decision boundary).
- Kurva Monte Carlo: istilah longgar. Wujud nyatanya fan chart, spaghetti/ensemble plot, quantile dotplot, HOP, histogram/CDF simulasi, tornado, Sobol, trace plot.
- Diagram blok: YA, tapi untuk arsitektur/pipeline, bukan performa.
- Diagram Venn: TIDAK untuk model prediktif. Hanya untuk irisan himpunan; untuk >3 himpunan pakai UpSet.
- Kluster: YA, sebagai scatter berlabel, dendrogram, silhouette, elbow, gap statistic, profile heatmap.

## SUBSET WAJIB UNTUK MODEL TABULAR (mis. klasifikasi kegagalan BHA)

1. Confusion matrix (raw + normalized)
2. ROC + PR curve (PR lebih informatif saat kelas timpang)
3. Calibration curve
4. Lift + cumulative gain (nilai bisnis/operasional)
5. Learning curve + validation curve
6. Residual/prediction-error 4-panel (jika regresi)
7. SHAP beeswarm + SHAP waterfall (global + lokal)
8. PDP atau ALE + ICE
9. Permutation importance dengan error bar
10. Fan chart + tornado (ketidakpastian & driver)
11. Dendrogram + silhouette (jika ada klaster rezim sumur)
12. Block diagram pipeline (untuk bab metode)

## SUMBER

- scikit-learn Visualizations: https://scikit-learn.org/stable/visualizations.html
- scikit-learn Inspection: https://scikit-learn.org/stable/inspection.html
- SHAP API (bar, waterfall, force, scatter, heatmap): https://shap.readthedocs.io/en/latest/api.html
- Interpretable ML Book, ALE: https://christophm.github.io/interpretable-ml-book/ale.html
- Lift & cumulative gain chart: https://www2.cs.uregina.ca/~dbd/cs831/notes/lift_chart/lift_chart.html
- Uncertainty visualization (ensemble/spaghetti, interval, violin): https://arxiv.org/html/2508.00937v1
- Padilla, Kay & Hullman, Uncertainty Visualization: http://space.ucmerced.edu/Downloads/publications/Uncertainty_Visualization_Padilla_Kay_Hullman_2022.pdf
- Wilke, HOP & uncertainty: https://clauswilke.com/dataviz/visualizing-uncertainty.html
- Raincloud plots: https://pmc.ncbi.nlm.nih.gov/articles/PMC6480976
- Euler/Venn vs UpSet untuk overlap: https://thenode.biologists.com/venn-euler-upset-visualize-overlaps-in-datasets/education
- Diagnostic plots regresi (UVA): https://library.virginia.edu/data/articles/diagnostic-plots
