/* Halaman Prediksi. Semua angka dari window.PRED, bukan karangan. */
(function () {
  const { card, table, viewHead, esc, nf } = window.UI;
  const P = window.PRED;

  const fmt = (x, d = 3) => (x == null ? "—" : nf(x, d));
  const rng = (a, d = 3) => `${fmt(a[0], d)}–${fmt(a[1], d)}`;
  const tone = (t) => `<span class="badge ${t === "ok" ? "p3" : t === "warn" ? "p2" : "p4"}">${t === "ok" ? "KUAT" : t === "warn" ? "LEMAH" : "TIDAK LAYAK"}</span>`;

  function frame(W, H, L, R, T, B) {
    return { W, H, L, R, T, B, sx: (x) => L + x * (W - L - R), sy: (y) => H - B - y * (H - T - B) };
  }

  function prChart() {
    const f = frame(380, 220, 42, 12, 14, 30);
    const ymax = 0.15;
    const sy = (v) => f.sy(v / ymax);
    const pts = P.pr.points.map(([r, p]) => `${f.sx(r).toFixed(1)},${sy(p).toFixed(1)}`).join(" ");
    const base = sy(P.pr.baseline);
    const last = P.pr.points[P.pr.points.length - 1];
    return `<svg class="chart" viewBox="0 0 ${f.W} ${f.H}" role="img" aria-label="Kurva presisi-recall STUCK onset">
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.W - f.R}" y2="${f.H - f.B}" class="axis"/>
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.L}" y2="${f.T}" class="axis"/>
      ${[0, 0.05, 0.1, 0.15].map((v) => `<line x1="${f.L}" y1="${sy(v)}" x2="${f.W - f.R}" y2="${sy(v)}" class="gridline"/><text x="4" y="${sy(v) + 3}">${v.toFixed(2).replace(".", ",")}</text>`).join("")}
      ${[0, 0.5, 1].map((v) => `<text x="${f.sx(v) - 6}" y="${f.H - 10}">${v.toFixed(1).replace(".", ",")}</text>`).join("")}
      <polygon points="${f.sx(0)},${f.H - f.B} ${pts} ${f.sx(1)},${f.H - f.B}" fill="var(--red)" opacity=".08"/>
      <line x1="${f.L}" y1="${base}" x2="${f.W - f.R}" y2="${base}" stroke="var(--text-3)" stroke-dasharray="4 3"/>
      <polyline points="${pts}" class="series"/>
      <circle cx="${f.sx(last[0])}" cy="${sy(last[1])}" r="3.5" class="point"/>
      <text x="${f.L + 4}" y="${f.T + 10}" class="label">AUPRC ${fmt(P.pr.auprc, 3)} · baseline ${fmt(P.pr.baseline, 3)}</text>
      <text x="${f.W - 142}" y="${f.T + 10}" class="label">Y dipotong 0–0,15</text>
    </svg>`;
  }

  function calChart() {
    const f = frame(340, 210, 40, 12, 14, 28);
    const ymax = 0.2;
    const sy = (v) => f.sy(v / ymax);
    const diag = `M ${f.sx(0)} ${sy(0)} L ${f.sx(1)} ${sy(1)}`;
    return `<svg class="chart" viewBox="0 0 ${f.W} ${f.H}" role="img" aria-label="Kurva kalibrasi STUCK onset">
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.W - f.R}" y2="${f.H - f.B}" class="axis"/>
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.L}" y2="${f.T}" class="axis"/>
      ${[0, 0.05, 0.1, 0.15, 0.2].map((v) => `<line x1="${f.L}" y1="${sy(v)}" x2="${f.W - f.R}" y2="${sy(v)}" class="gridline"/><text x="4" y="${sy(v) + 3}">${v.toFixed(2).replace(".", ",")}</text>`).join("")}
      ${[0, 0.5, 1].map((v) => `<text x="${f.sx(v) - 6}" y="${f.H - 10}">${v.toFixed(1).replace(".", ",")}</text>`).join("")}
      <path d="${diag}" fill="none" stroke="var(--text-3)" stroke-dasharray="4 3"/>
      ${P.calib.map((d) => `<circle cx="${f.sx(d.pred)}" cy="${sy(d.obs)}" r="3.5" class="point"><title>${d.bin}: prediksi ${fmt(d.pred, 3)}, observasi ${fmt(d.obs, 3)}, n=${d.n}</title></circle>`).join("")}
      <text x="${f.W - 132}" y="${f.T + 10}" class="label">Y dipotong 0–0,2</text>
    </svg>`;
  }

  function tauChart(rows, color) {
    const f = frame(340, 200, 34, 12, 14, 30);
    const n = rows.length;
    const x = (i) => f.L + (n <= 1 ? 0 : (i / (n - 1)) * (f.W - f.L - f.R));
    const prec = rows.map((d, i) => `${x(i).toFixed(1)},${f.sy(d.precision).toFixed(1)}`).join(" ");
    const rec = rows.map((d, i) => `${x(i).toFixed(1)},${f.sy(d.recall).toFixed(1)}`).join(" ");
    return `<svg class="chart" viewBox="0 0 ${f.W} ${f.H}" role="img" aria-label="Trade-off ambang">
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.W - f.R}" y2="${f.H - f.B}" class="axis"/>
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.L}" y2="${f.T}" class="axis"/>
      ${[0, 0.5, 1].map((v) => `<line x1="${f.L}" y1="${f.sy(v)}" x2="${f.W - f.R}" y2="${f.sy(v)}" class="gridline"/><text x="2" y="${f.sy(v) + 3}">${v.toFixed(1).replace(".", ",")}</text>`).join("")}
      <polyline points="${prec}" fill="none" stroke="${color}" stroke-width="2"/>
      <polyline points="${rec}" fill="none" stroke="var(--text-2)" stroke-width="1.5" stroke-dasharray="4 3"/>
      ${rows.map((d, i) => `<circle cx="${x(i)}" cy="${f.sy(d.precision)}" r="2.8" fill="${color}"/><circle cx="${x(i)}" cy="${f.sy(d.recall)}" r="2.8" fill="var(--text-2)"/>`).join("")}
      ${rows.map((d, i) => `<text x="${x(i) - 6}" y="${f.H - 10}">${String(d.tau).replace(".", ",")}</text>`).join("")}
    </svg>`;
  }

  function headChart() {
    const f = frame(380, 230, 42, 12, 14, 30);
    const color = (t) => (t === "TREN" ? "var(--green)" : t === "PERINGATAN-BERPENGAWAS" ? "var(--amber)" : "var(--red)");
    return `<svg class="chart" viewBox="0 0 ${f.W} ${f.H}" role="img" aria-label="Peta presisi dan recall 20 kepala">
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.W - f.R}" y2="${f.H - f.B}" class="axis"/>
      <line x1="${f.L}" y1="${f.H - f.B}" x2="${f.L}" y2="${f.T}" class="axis"/>
      ${[0, 0.25, 0.5, 0.75, 1].map((v) => `<line x1="${f.L}" y1="${f.sy(v)}" x2="${f.W - f.R}" y2="${f.sy(v)}" class="gridline"/><text x="4" y="${f.sy(v) + 3}">${v.toFixed(2).replace(".", ",")}</text>`).join("")}
      ${[0, 0.5, 1].map((v) => `<text x="${f.sx(v) - 6}" y="${f.H - 10}">${v.toFixed(1).replace(".", ",")}</text>`).join("")}
      ${P.heads.map((h) => `<circle cx="${f.sx(h.r)}" cy="${f.sy(h.p)}" r="4" fill="${color(h.tier)}" stroke="var(--card)" stroke-width="1"><title>${esc(h.engine)}/${esc(h.head)} · presisi ${fmt(h.p, 3)}, recall ${fmt(h.r, 3)}, ${esc(h.tier)}</title></circle>`).join("")}
      <text x="${f.W - 88}" y="${f.H - 10}" class="label">recall</text>
      <text x="4" y="${f.T + 12}" class="label">presisi</text>
    </svg>`;
  }

  function foldChart() {
    const f = frame(380, 180, 52, 12, 14, 26);
    const groups = [
      { name: "VIB", rows: P.vibFolds, color: "var(--green)" },
      { name: "STUCK", rows: P.stuckFolds, color: "var(--amber)" },
      { name: "SHK", rows: P.shkFolds, color: "var(--red)" }
    ];
    const y = (i) => f.T + 18 + i * 42;
    return `<svg class="chart" viewBox="0 0 ${f.W} ${f.H}" role="img" aria-label="AUPRC per fold">
      <line x1="${f.L}" y1="${f.T}" x2="${f.L}" y2="${f.H - f.B}" class="axis"/>
      ${[0, 0.25, 0.5, 0.75, 1].map((v) => `<line x1="${f.sx(v)}" y1="${f.T}" x2="${f.sx(v)}" y2="${f.H - f.B}" class="gridline"/><text x="${f.sx(v) - 8}" y="${f.H - 8}">${v.toFixed(2).replace(".", ",")}</text>`).join("")}
      ${groups.map((g, i) => `<text x="4" y="${y(i) + 3}" class="label">${g.name}</text>${g.rows.map((r) => `<circle cx="${f.sx(r.auprc)}" cy="${y(i)}" r="4" fill="${g.color}" stroke="var(--card)" stroke-width="1"><title>${g.name} ${r.well}: AUPRC ${fmt(r.auprc, 3)}, baseline ${fmt(r.prev, 3)}</title></circle>`).join("")}`).join("")}
    </svg>`;
  }

  function prediksi() {
    const tasks = P.tasks.map((t) => card({
      span: "span-4",
      title: t.name,
      sub: `${t.kind} · horizon ${t.horizon}`,
      right: tone(t.tone),
      body: `<div class="stat-grid">
        <div class="stat"><div class="k">AUPRC median</div><div class="v" style="font-size:24px">${fmt(t.auprcMed, 3)}</div><div class="n">rentang ${rng(t.auprc, 3)}</div></div>
        <div class="stat"><div class="k">Baseline</div><div class="v" style="font-size:24px">${fmt(t.prevMed, 3)}</div><div class="n">prevalensi</div></div>
        <div class="stat"><div class="k">Lift</div><div class="v" style="font-size:24px">${fmt(t.liftMed, 2)}×</div><div class="n">median antar fold</div></div>
      </div>
      <p class="small muted" style="margin-top:8px">${t.verdict}</p>`,
      foot: `<span>${t.engine}</span><a class="link" href="#bukti">Sumber</a>`
    })).join("");

    const horizon = [
      ["Sekarang", "Status berlangsung", "VIB, SHK", "ok"],
      ["10 menit", "Onset STUCK", "stuck_k2", "warn"],
      ["8 jam", "Rencana shift", "belum ada model", "bad"],
      ["7 hari", "RUL / servis", "belum ada model", "bad"]
    ].map(([h, what, who, t]) => `<div class="card inner" style="padding:12px;border-left:2px solid ${t === "ok" ? "var(--green)" : t === "warn" ? "var(--amber)" : "var(--red)"}">
      <div class="k" style="font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--text-3)">${h}</div>
      <div style="font-weight:600;font-size:13px;margin-top:3px">${what}</div>
      <div class="small muted" style="margin-top:2px">${who}</div>
    </div>`).join("");

    return `<section class="view">
      ${viewHead("Prediksi", "Apa yang benar-benar diprediksi, seberapa kuat, dan pada horizon apa.", `Sumber: v9_e_ML_*_RESULTS<br>${P.meta.n_heads} kepala punya metrik presisi/recall`)}
      <div class="banner-note warn span-12" style="margin-bottom:10px"><strong>Ini bukan live dashboard.</strong> Halaman ini menampilkan bukti model dari hasil uji. Tidak ada RUL, tidak ada forecast 7 hari, dan tidak ada alarm otomatis.</div>
      <div class="grid">${tasks}</div>
      <div class="grid" style="margin-top:10px">
        ${card({ span: "span-7", title: "Kurva presisi-recall · STUCK onset", sub: `X recall · Y presisi · ${P.pr.model} · ${nf(P.pr.n, 0)} jendela · ${nf(P.pr.pos, 0)} positif. Garis putus-putus adalah baseline.`, body: prChart(), foot: `<span>AUPRC ${fmt(P.pr.auprc, 3)} vs baseline ${fmt(P.pr.baseline, 3)}</span><a class="link" href="#batas">Batas</a>` })}
        ${card({ span: "span-5", title: "Kalibrasi · STUCK onset", sub: "X prediksi · Y observasi per bin. Titik di bawah garis berarti model terlalu yakin.", body: calChart() + `<p class="small muted" style="margin-top:6px">Sumbu Y dipotong di 0,2 agar titik terlihat. Model memberi probabilitas sampai 0,82, sedangkan frekuensi observasi tertinggi 0,17: skor belum bisa dibaca sebagai peluang.</p>`, foot: `<span>${P.calib.length} bin</span><a class="link" href="#kamus">Arti</a>` })}
      </div>
      <div class="grid" style="margin-top:10px">
        ${card({ span: "span-6", title: "Ambang VIB", sub: "X ambang · Y presisi/recall. FAR ada di tabel bawah.", body: tauChart(P.vibTau, "var(--green)") + `<div class="legend" style="margin-top:6px"><span><i style="background:var(--green)"></i>presisi (garis penuh)</span><span><i style="background:var(--text-2)"></i>recall (garis putus)</span></div><div style="margin-top:8px">${table(["Tau", "Presisi", "Recall", "FAR/24j"], P.vibTau.map((d) => ({ cells: [String(d.tau).replace(".", ","), fmt(d.precision, 3), fmt(d.recall, 3), fmt(d.far, 1)] })), { cls: "compact" })}</div>`, foot: `<span>VIB · fold 0</span><a class="link" href="#mesin">Mesin</a>` })}
        ${card({ span: "span-6", title: "Ambang STUCK", sub: "X ambang · Y presisi/recall. Perhatikan FAR yang tinggi.", body: tauChart(P.stuckTau, "var(--amber)") + `<div class="legend" style="margin-top:6px"><span><i style="background:var(--amber)"></i>presisi (garis penuh)</span><span><i style="background:var(--text-2)"></i>recall (garis putus)</span></div><div style="margin-top:8px">${table(["Tau", "Presisi", "Recall", "FAR/24j"], P.stuckTau.map((d) => ({ cells: [String(d.tau).replace(".", ","), fmt(d.precision, 3), fmt(d.recall, 3), fmt(d.far, 1)] })), { cls: "compact" })}</div>`, foot: `<span>STUCK · fold 0</span><a class="link" href="#batas">Batas</a>` })}
      </div>
      <div class="grid" style="margin-top:10px">
        ${card({ span: "span-7", title: "Peta 20 kepala", sub: "Presisi lawan recall. Warna adalah tier bukti, bukan status alarm.", body: headChart() + `<div class="legend" style="margin-top:6px"><span><i style="background:var(--green)"></i>TREN</span><span><i style="background:var(--amber)"></i>PERINGATAN-BERPENGAWAS</span><span><i style="background:var(--red)"></i>BELUM LAYAK PAKAI</span></div>`, foot: `<span>${P.heads.length} dari 27 kepala punya presisi dan recall</span><a class="link" href="#kepercayaan">Kepercayaan</a>` })}
        ${card({ span: "span-5", title: "AUPRC per fold", sub: "Setiap titik satu sumur uji. Sebaran lebar berarti performa tidak stabil.", body: foldChart(), foot: `<span>VIB 4 fold · STUCK 4 fold · SHK 9 fold</span><a class="link" href="#bukti">Bukti</a>` })}
      </div>
      <div class="grid" style="margin-top:10px">
        ${card({ span: "span-12", title: "Horizon prediksi", sub: "Pertanyaan operasional yang bisa dijawab hari ini, dan yang belum.", body: `<div class="grid" style="gap:8px">${horizon}</div>`, foot: `<span>Horizon 10 menit bukan RUL</span><a class="link" href="#batas">Batas data</a>` })}
      </div>
    </section>`;
  }

  window.VIEWS.prediksi = prediksi;
})();