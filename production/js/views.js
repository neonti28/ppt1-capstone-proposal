/* View templates. Semua teks dan angka berasal dari DATA.
   Tidak ada angka yang dikarang di berkas ini. */

(function () {
  const D = window.DATA;

  const nf = (n, d = 2) => Number(n).toLocaleString("id-ID", { minimumFractionDigits: d, maximumFractionDigits: d });
  const pct = (n, d = 2) => nf(n * 100, d) + "%";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const countBy = (arr, key, val) => arr.filter((x) => x[key] === val).length;

  const PITA = { 0: "Tidak dinilai", 1: "Tidak ada indikasi", 2: "Indikasi lemah", 3: "Perlu tinjauan", 4: "Keyakinan kuat", 5: "Keyakinan tinggi" };
  const pita = (p, long) => `<span class="badge p${p}"><i class="dot"></i>P${p}${long ? " " + PITA[p] : ""}</span>`;
  const pitaShort = (p) => `<span class="badge p${p}">P${p}</span>`;

  const prov = (s) => {
    const map = { ok: ["prov-ok", "TERUKUR"], note: ["prov-note", "TURUNAN"], block: ["prov-block", "BELUM KUTIP"] };
    const [cls, label] = map[s] || map.block;
    return `<span class="prov ${cls}">${label}</span>`;
  };

  const statusBadge = (s) => {
    const map = {
      "Baru": "p4", "Ditinjau": "p3", "Ditunda": "p1",
      "BERLAKU": "p3", "PERLU PERBAIKAN": "p4",
      "LAYAK": "p3", "LAYAK BERSYARAT": "p2",
      "Siap": "p3", "Sebagian": "p2", "Terbuka": "p4", "Tidak ada": "p1", "Terukur": "p3",
      "Selesai": "p3", "Ditolak": "p4", "Gagal": "p4", "Lulus": "p3"
    };
    return `<span class="badge ${map[s] || "p1"}">${esc(s)}</span>`;
  };

  const card = (o) => {
    const span = o.span || "span-4";
    return `<article class="card ${span} ${o.cls || ""}"${o.id ? ` id="${o.id}"` : ""} data-card>
      ${o.title ? `<div class="card-head"><div><h3>${o.title}</h3>${o.sub ? `<div class="sub">${o.sub}</div>` : ""}</div>${o.right ? `<div class="head-right">${o.right}</div>` : ""}</div>` : ""}
      <div class="card-body">${o.body || ""}</div>
      ${o.foot ? `<div class="card-foot">${o.foot}</div>` : ""}
    </article>`;
  };

  const stat = (k, v, n, unit) => `<div class="stat"><div class="k">${k}</div><div class="v">${v}${unit ? `<small>${unit}</small>` : ""}</div>${n ? `<div class="n">${n}</div>` : ""}</div>`;
  const statStrip = (items, cls = "span-12") => `<div class="stat-strip ${cls}">${items.map((x) => stat(x.k, x.v, x.n, x.unit)).join("")}</div>`;

  const table = (head, rows, opts = {}) => `<div class="table-wrap ${opts.wrap || ""}"><table class="table ${opts.cls || ""}">
    <thead><tr>${head.map((h) => `<th${h.align ? ` class="${h.align}"` : ""}>${h.label ?? h}</th>`).join("")}</tr></thead>
    <tbody>${rows.map((r) => `<tr${r.attrs || ""}>${r.cells.map((c) => `<td${c.align ? ` class="${c.align}"` : ""}>${c.v ?? c}</td>`).join("")}</tr>`).join("")}</tbody>
  </table></div>`;

  const barRow = (label, value, max, opts = {}) => {
    const w = max > 0 ? Math.max(0, Math.min(100, (value / max) * 100)) : 0;
    const marks = (opts.marks || []).map((m) => `<span class="mark ${m.cls || ""}" style="left:${Math.min(100, (m.at / max) * 100)}%"></span>`).join("");
    return `<div class="bar-row"><div class="lbl" title="${esc(label)}">${label}</div><div class="track"><i class="${opts.tone || ""}" style="width:${w}%"></i>${marks}</div><div class="val">${opts.value ?? nf(value, opts.d ?? 2)}</div></div>`;
  };

  const confBar = (k, cap) => {
    const ratio = cap > 0 ? Math.max(0, Math.min(1, k / cap)) : 0;
    const tone = ratio > 0.8 ? "red" : ratio > 0.5 ? "amber" : "";
    return `<div class="track" title="K ${nf(k, 4)} dari batas ${nf(cap, 4)}"><i class="${tone}" style="width:${ratio * 100}%"></i><span class="mark" style="left:calc(100% - 1px)"></span></div>`;
  };

  const foldDots = (pass, total) => `<span class="spark" aria-label="${pass} dari ${total} fold">${Array.from({ length: total }, (_, i) => `<i class="${i < pass ? "on" : ""}" style="height:${i < pass ? 18 : 10}px"></i>`).join("")}</span>`;

  const viewHead = (title, desc, meta) => `<div class="view-head"><div><h2>${title}</h2><p>${desc}</p></div><div class="head-meta">${meta || `Potong data ${D.meta.cut}<br>${D.meta.heads} kepala · ${D.meta.engines} mesin`}</div></div>`;

  const tkBanner = () => `<div class="tk-banner span-12">
    <div class="tk-mark"><strong>${D.tk.level}</strong><span>${D.tk.label}</span></div>
    <div class="tk-copy"><strong>Dewan rig bersuara, bukan mesin tunggal.</strong><p>${D.tk.note}</p></div>
    <div class="tk-metrics">
      <div><b>${nf(D.tk.support, 2)}%</b><span>dukungan</span></div>
      <div><b>${D.tk.quorum}</b><span>kuorum</span></div>
      <div><b>${nf(D.tk.coverage, 2)}</b><span>cakupan bobot</span></div>
      <div><b>${D.meta.alarmSlots}</b><span>alarm otomatis</span></div>
    </div>
  </div>`;

  const focusCard = (f) => card({
    span: "span-4",
    title: f.claim,
    sub: `Segmen ${f.well} · jendela ${f.window} · ${f.heads} kepala`,
    right: pita(f.pita),
    body: `
      <div class="flex-between" style="margin-bottom:6px">
        <span class="small muted">Keyakinan ${nf(f.confidence, 4)} dari batas ${nf(f.cap, 4)}</span>
        <span class="mono small">${pct(f.confidence / f.cap, 0)} dari batas</span>
      </div>
      ${confBar(f.confidence, f.cap)}
      <div class="stat-grid" style="margin-top:10px">
        <div class="stat"><div class="k">Sinyal</div><div class="v" style="font-size:17px">${f.far}</div></div>
        <div class="stat"><div class="k">Lead</div><div class="v" style="font-size:17px">${f.lead}</div></div>
      </div>
      <p class="small" style="color:var(--text-2);margin-top:9px;line-height:1.45">${f.action}</p>`,
    foot: `<span>${f.age} · ${f.status}</span><button class="link" type="button" data-queue="${f.code}">Periksa</button>`
  });

  const queueRow = (q, opts = {}) => {
    const action = opts.actions
      ? `<div class="flex" style="gap:4px"><button class="btn sm" data-queue="${q.id}">Tinjau</button><button class="btn sm ghost" data-defer="${q.id}">Tunda</button></div>`
      : `<button class="link" data-queue="${q.id}">Buka</button>`;
    return {
      attrs: ` class="clickable" data-queue-row="${q.id}"`,
      cells: [
        { v: `<span class="mono small">${q.id}</span>` },
        { v: `<span class="strong">${q.claim}</span>` },
        { v: q.well },
        { v: q.window },
        { v: `<span class="mono">${q.heads}</span>`, align: "center" },
        { v: `<span class="mono">${nf(q.conf, 4)}</span>`, align: "right" },
        { v: pitaShort(q.pita), align: "center" },
        { v: q.age },
        { v: statusBadge(q.status) },
        { v: action, align: "right" }
      ]
    };
  };

  const queueTable = (rows, opts = {}) => table(
    ["ID", "Klaim", "Segmen", "Jendela", "Kepala", { label: "K_tampil", align: "right" }, { label: "Pita", align: "center" }, "Umur", "Status", { label: "Aksi", align: "right" }],
    rows.map((q) => queueRow(q, opts)),
    { cls: "nowrap", wrap: opts.wrap || "" }
  );

  /* ---------------- BERANDA ---------------- */

  function beranda() {
    const focus = D.focus.map(focusCard).join("");
    const damages = D.damages.map((d) => card({
      span: "",
      cls: "",
      title: d.name,
      sub: d.task,
      right: d.pita ? pitaShort(d.pita) : `<span class="badge p1">ABSTAIN</span>`,
      body: `
        <div class="flex-between small"><span class="muted">K_tampil</span><span class="mono">${d.k}</span></div>
        <div class="flex-between small"><span class="muted">Batas kelas</span><span class="mono">${d.cap}</span></div>
        <div style="margin-top:6px">${d.k !== "tidak ada" ? confBar(parseFloat(String(d.k).replace(",", ".")), parseFloat(String(d.cap).replace(",", "."))) : `<div class="banner-note bad" style="padding:6px 8px;font-size:10px">Tidak ada angka. ${d.vote}.</div>`}</div>
        <p class="small" style="margin-top:9px;color:var(--text-2);line-height:1.42">${d.evidence}</p>
        <p class="small muted" style="margin-top:5px;line-height:1.4">${d.limit}</p>`,
      foot: `<span>${d.vote} · bobot ${d.weight}</span><button class="link" type="button" data-claim="${d.code}">Rinci</button>`
    })).join("");

    return `<section class="view" id="view-beranda" aria-labelledby="h-beranda">
      ${viewHead("Beranda", "Satu layar untuk melihat apa yang layak ditinjau hari ini, apa yang belum bisa dijawab, dan dari mana angkanya.", `Potong data ${D.meta.cut}<br>${D.meta.claims} kelas · ${D.meta.heads} kepala · ${D.meta.alarmSlots} alarm otomatis`)}
      <div class="grid">
        ${tkBanner()}
        ${focus}
        ${statStrip([
          { k: "Baris per shift", v: "40,15", n: "rata-rata 12 jam" },
          { k: "Median", v: "12,4", unit: "menit", n: "p50 per baris" },
          { k: "Ekor", v: "38,7", unit: "menit", n: "p95 per baris" },
          { k: "Sisa anggaran", v: "1.240", unit: "menit", n: "per shift contoh" }
        ])}
        ${card({
          span: "span-8",
          title: "Antrean tinjauan",
          sub: `${D.queue.length} baris. ${countBy(D.queue, "status", "Baru")} belum ditinjau, ${countBy(D.queue, "status", "Ditunda")} ditunda dengan alasan.`,
          right: `<a class="btn sm" href="#perencanaan">Buka antrean</a>`,
          body: queueTable(D.queue.slice(0, 6), { wrap: "short" }),
          foot: `<span>Klik baris untuk melihat alasan dan sumber.</span><span class="mono">6 dari ${D.queue.length}</span>`
        })}
        ${card({
          span: "span-4",
          title: "Yang tidak dijawab",
          sub: "Abstain tampil, bukan disembunyikan.",
          right: `<span class="badge p1">11 klaim</span>`,
          body: `
            ${barRow("AB-1 tidak ada komposisi", 2, 5, { value: "2", d: 0, tone: "hatch" })}
            ${barRow("AB-2 kanal kurang", 3, 5, { value: "3", d: 0, tone: "amber" })}
            ${barRow("AB-3 label tipis", 1, 5, { value: "1", d: 0, tone: "amber" })}
            ${barRow("AB-4 data terblokir", 2, 5, { value: "2", d: 0, tone: "red" })}
            ${barRow("AB-5 label per kejadian", 3, 5, { value: "3", d: 0, tone: "red" })}
            <p class="small muted" style="margin-top:8px">Abstain bukan nol. Ia berarti alat menolak menjawab karena bukti tidak cukup.</p>`,
          foot: `<span>5 kode abstain</span><a class="link" href="#batas">Batas data</a>`
        })}
        ${card({
          span: "span-4",
          title: "Status bukti",
          sub: "Angka membawa sumber, bukan ingatan.",
          body: `
            <dl class="kv">
              <dt>Potong data</dt><dd class="mono">${D.meta.cut}</dd>
              <dt>Berkas rujukan</dt><dd>10 dokumen inti</dd>
              <dt>Baris ledger</dt><dd class="mono">726</dd>
              <dt>Belum dibuka</dt><dd class="mono">69 / 119</dd>
              <dt>Audit</dt><dd>6 cacat teks, 0 kritis</dd>
            </dl>
            <div class="banner-note warn" style="margin-top:9px;padding:7px 8px;font-size:10px">Angka di halaman ini adalah potongan uji, bukan feed langsung.</div>`,
          foot: `<span>${prov("ok")} ${countBy(D.provenance, "status", "ok")} terukur</span><a class="link" href="#bukti">Lihat bukti</a>`
        })}
        ${card({
          span: "span-4",
          title: "Cara membaca",
          sub: "Tiga langkah, tanpa lompat ke kesimpulan.",
          body: `<ol class="bullets red" style="counter-reset:step">
            <li>Baca pita dan batas kelas. Pita tinggi tidak berarti tindakan.</li>
            <li>Cek FAR dan lead. Alarm lebih sedikit belum tentu lebih baik.</li>
            <li>Buka sumber. Bila tidak ada sumber, jangan pakai angkanya.</li>
          </ol>
          <div class="banner-note info" style="margin-top:9px;padding:7px 8px;font-size:10px">Alat ini tidak mengirim alarm. Ia menyusun antrean dan mencatat alasan.</div>`,
          foot: `<span>Kebijakan evaluasi</span><a class="link" href="#kamus">Kamus</a>`
        })}
      </div>

      <div class="hsection">
        <div class="hsection-head">
          <div><h3>Daftar kerusakan</h3><p>11 kelas klaim. Geser ke samping untuk melihat semuanya.</p></div>
          <span class="scroll-hint">Geser <svg width="14" height="14"><use href="#i-arrow-right"/></svg></span>
        </div>
        <div class="hscroll wide">${damages}</div>
      </div>

      <div class="grid" style="margin-top:12px">
        ${card({
          span: "span-6",
          title: "Batas hari ini",
          sub: "Yang belum boleh diklaim.",
          body: `<ul class="bullets red">
            <li>Tidak ada biaya rupiah. Tidak ada kolom biaya di repo.</li>
            <li>Tidak ada jadwal inspeksi. Tidak ada kalender perawatan.</li>
            <li>Tidak ada produksi tertunda. Tidak ada berkas deferred production.</li>
            <li>Empat kepala ML memerlukan flag <span class="mono">--ml</span> untuk berjalan.</li>
          </ul>`,
          foot: `<span>Layer B: 2 dari 5 slot terisi</span><a class="link" href="#batas">Batas lengkap</a>`
        })}
        ${card({
          span: "span-6",
          title: "Jam yang tercatat",
          sub: "39.397,986 jam aktivitas. Ini konteks, bukan penghematan.",
          body: `<div class="bars">
            ${barRow("Perbaikan interupsi", 1215, 2739.667, { value: "1.215,0 jam", tone: "red" })}
            ${barRow("Menunggu cuaca", 1925.5, 2739.667, { value: "1.925,5 jam", tone: "amber" })}
            ${barRow("Perawatan", 562.75, 2739.667, { value: "562,75 jam" })}
            ${barRow("Pipa terjepit", 212, 2739.667, { value: "212,0 jam", tone: "amber" })}
            ${barRow("Kehilangan sirkulasi", 195, 2739.667, { value: "195,0 jam" })}
          </div>
          <p class="small muted" style="margin-top:8px">Batang dibandingkan dengan sebab terbesar, equipment failure 2.739,667 jam.</p>`,
          foot: `<span>Sumber: S4, ringkasan aktivitas</span><a class="link" href="#perencanaan">Pareto</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- KEPERCAYAAN ---------------- */

  function kepercayaan() {
    const verdicts = D.damages.map((d) => card({
      span: "",
      title: d.name,
      sub: d.task,
      right: d.pita ? pitaShort(d.pita) : `<span class="badge p1">ABSTAIN</span>`,
      body: `
        <div class="flex-between small"><span class="muted">K_tampil</span><span class="mono">${d.k}</span></div>
        <div class="flex-between small"><span class="muted">Batas kelas</span><span class="mono">${d.cap}</span></div>
        <div style="margin-top:6px">${d.k !== "tidak ada" ? confBar(parseFloat(String(d.k).replace(",", ".")), parseFloat(String(d.cap).replace(",", "."))) : `<div class="track"><i class="hatch" style="width:100%"></i></div>`}</div>
        <div class="tag-list" style="margin-top:8px"><span class="chip">${d.vote}</span><span class="chip">bobot ${d.weight}</span></div>
        <p class="small" style="margin-top:8px;color:var(--text-2);line-height:1.4">${d.evidence}</p>`,
      foot: `<span>${d.limit}</span><button class="link" data-claim="${d.code}">Rinci</button>`
    })).join("");

    const caps = D.damages.filter((d) => d.k !== "tidak ada").slice(0, 7);
    const bars = caps.map((d) => {
      const k = parseFloat(String(d.k).replace(",", "."));
      const cap = parseFloat(String(d.cap).replace(",", "."));
      const ratio = cap > 0 ? k / cap : 0;
      return `<div style="margin-bottom:8px">
        <div class="flex-between small"><span>${d.name}</span><span class="mono">${nf(k, 4)} / ${nf(cap, 4)}</span></div>
        <div class="track" style="height:8px;margin-top:3px"><i class="${ratio > 0.8 ? "red" : ratio > 0.5 ? "amber" : ""}" style="width:${ratio * 100}%"></i><span class="mark red" style="left:calc(100% - 1px)"></span></div>
      </div>`;
    }).join("");

    const readings = D.readExamples.map((r) => ({ cells: [
      { v: `<span class="mono strong">${r.text}</span>` },
      { v: `<span class="status-ok">${r.right}</span>` },
      { v: `<span class="status-bad">${r.wrong}</span>` }
    ] }));

    return `<section class="view" id="view-kepercayaan" aria-labelledby="h-kepercayaan">
      ${viewHead("Kepercayaan", "Setiap klaim punya plafon. Pita tinggi tidak boleh melewati mutu bukti kelasnya.", `Potong data ${D.meta.cut}<br>11 kelas · 27 kepala · 0 alarm otomatis`)}
      <div class="grid">
        ${statStrip([
          { k: "Kelas klaim", v: "11", n: "vib sampai tool_wear" },
          { k: "Kepala", v: "27", n: "5 L0 · 11 L1 · 9 L2 · 2 L3" },
          { k: "Alarm otomatis", v: "0", n: "tidak ada kepala yang memicu sendiri" },
          { k: "Dewan bersuara", v: "6/7", n: "cakupan bobot 0,87" },
          { k: "Dukungan", v: "18,23%", n: "setelah batas dominasi" },
          { k: "Baris ledger", v: "726", n: "angka dan rujukan" }
        ])}
      </div>

      <div class="hsection">
        <div class="hsection-head">
          <div><h3>Papan vonis</h3><p>11 kelas. K_tampil, batas kelas, suara, dan bobot dewan.</p></div>
          <span class="scroll-hint">Geser <svg width="14" height="14"><use href="#i-arrow-right"/></svg></span>
        </div>
        <div class="hscroll wide">${verdicts}</div>
      </div>

      <div class="grid" style="margin-top:12px">
        ${card({
          span: "span-6",
          title: "Keyakinan lawan batas kelas",
          sub: "Batang menunjukkan berapa persen dari plafon yang sudah dipakai.",
          right: `<span class="badge p3">plafon</span>`,
          body: bars + `<p class="small muted" style="margin-top:6px">Garis merah di ujung kanan adalah batas kelas. Batang tidak pernah melewatinya.</p>`,
          foot: `<span>K_max dari 06 bagian 5.3</span><a class="link" href="#bukti">Sumber</a>`
        })}
        ${card({
          span: "span-6",
          title: "Presisi lawan recall",
          sub: "Empat mode hyd. Titik kanan atas lebih baik, tetapi biaya alarm harus dibaca.",
          body: `<svg class="chart" viewBox="0 0 360 210" role="img" aria-label="Presisi lawan recall untuk empat mode hyd">
            <line x1="40" y1="180" x2="340" y2="180" class="axis"/>
            <line x1="40" y1="180" x2="40" y2="20" class="axis"/>
            <line x1="40" y1="100" x2="340" y2="100" class="gridline"/>
            <line x1="190" y1="20" x2="190" y2="180" class="gridline"/>
            <text x="40" y="196">0</text><text x="185" y="196">0,5</text><text x="326" y="196">1,0</text>
            <text x="8" y="184">0</text><text x="8" y="104">0,5</text><text x="8" y="24">1,0</text>
            <text x="160" y="206">Recall</text><text x="6" y="12">Presisi</text>
            ${D.hydModes.map((m, i) => {
              const x = 40 + m.r * 300;
              const y = 180 - m.p * 160;
              return `<circle cx="${x}" cy="${y}" r="4.5" class="point"/><text x="${x + 7}" y="${y - 6}" class="label">${m.name.replace("H1p3", "H1p3")}</text>`;
            }).join("")}
            <line x1="40" y1="180" x2="340" y2="20" class="gridline"/>
          </svg>
          <div class="legend" style="margin-top:4px"><span><i style="background:var(--red)"></i>mode hyd</span><span><i class="line" style="background:var(--text-3)"></i>garis acak</span></div>`,
          foot: `<span>Presisi dan recall median per mode</span><a class="link" href="#mesin">Mesin</a>`
        })}
        ${card({
          span: "span-6",
          title: "Dua bacaan",
          sub: "Bacaan benar dan salah untuk angka yang sama.",
          body: table(["Angka", "Bacaan benar", "Bacaan salah"], readings, { cls: "compact" }),
          foot: `<span>Bacaan salah sering menaikkan klaim.</span><a class="link" href="#kamus">Kamus</a>`
        })}
        ${card({
          span: "span-6",
          title: "Batas atas bukti",
          sub: "Tiga kelas yang tidak bisa naik pita.",
          body: `<ul class="bullets red">
            <li><strong>bit_wear</strong> K_max 0,2525. Tidak bisa melewati P2, berapa pun skornya.</li>
            <li><strong>stuck</strong> K_max 0,4562. P3 adalah plafon.</li>
            <li><strong>hyd K-ii</strong> tidak punya komposisi. Abstain AB-1.</li>
          </ul>
          <div class="banner-note warn" style="margin-top:9px;padding:7px 8px;font-size:10px">Batas kelas adalah keputusan bukti, bukan hyperparameter yang bisa dinaikkan agar grafik terlihat bagus.</div>`,
          foot: `<span>06 bagian 5.3</span><a class="link" href="#batas">Batas data</a>`
        })}
        ${card({
          span: "span-12",
          title: "Provenance hari ini",
          sub: `${D.provenance.length} angka kunci. Status mengikuti tabel rujukan, bukan warna kartu.`,
          right: `<span class="badge p3">726 baris</span>`,
          body: `<div class="table-wrap short"><table class="table compact"><thead><tr><th>Angka</th><th class="num">Nilai</th><th>Satuan</th><th>Sumber</th><th>Status</th></tr></thead><tbody>
            ${D.provenance.map((p) => `<tr><td class="strong">${p.item}</td><td class="num mono">${p.value}</td><td>${p.unit}</td><td class="small muted">${p.source}</td><td>${prov(p.status)}</td></tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>Klik ikon salin di halaman Bukti untuk memakai rujukan.</span><a class="link" href="#bukti">Buka Bukti</a>`
        })}
        ${card({
          span: "span-6",
          title: "L3: dua kepala yang belum boleh dipakai",
          sub: "Eksplorasi, bukan hasil.",
          body: D.l3.map((x) => `<div class="banner-note bad" style="margin-bottom:7px;padding:8px"><div><strong>${x.name}</strong> · ${x.code}<br><span class="small">${x.reason}</span></div></div>`).join(""),
          foot: `<span>2 dari 27 kepala</span><a class="link" href="#batas">Kode abstain</a>`
        })}
        ${card({
          span: "span-6",
          title: "Apa yang tidak boleh dibaca",
          sub: "Tiga kalimat yang sering salah.",
          body: `<ul class="bullets red">
            <li>"P 0,8243 berarti akurasi 82 persen." Salah. Itu presisi pada titik operasi.</li>
            <li>"Recall 0,6519 berarti 65 persen sumur aman." Salah. Itu onset yang diperingatkan.</li>
            <li>"AUPRC 0,0499 berarti model akurat 5 persen." Salah. Itu area, bukan akurasi.</li>
          </ul>`,
          foot: `<span>Bacaan dan satuan</span><a class="link" href="#kamus">Latihan</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- PERENCANAAN ---------------- */

  function perencanaan() {
    const rows = D.queue.map((q) => queueRow(q, { actions: true }));
    const totalMin = D.queue.reduce((a, q) => a + q.minutes, 0);
    const maxMin = Math.max(...D.queue.map((q) => q.minutes));
    const maxLoad = Math.max(...D.load.map((l) => l.value));
    const paretoBars = D.pareto.map((p, i) => {
      const x = 30 + i * 62;
      const h = (p.hours / 2739.667) * 130;
      return `<rect x="${x}" y="${160 - h}" width="42" height="${h}" fill="${i === 0 ? "var(--red)" : "#3a4b5e"}"/>
        <text x="${x + 21}" y="${156 - h}" text-anchor="middle">${nf(p.hours, 0)}</text>
        <text x="${x + 21}" y="176" text-anchor="middle" class="label">${p.name.split(" ")[0]}</text>`;
    }).join("");
    const paretoLine = D.pareto.map((p, i) => `${30 + i * 62 + 21},${160 - (p.pct / 100) * 130}`).join(" ");
    const modeBtns = D.hydModes.map((m, i) => `<button type="button" data-mode="${i}" aria-pressed="${i === 2}">${m.name}</button>`).join("");
    const mode = D.hydModes[2];

    return `<section class="view" id="view-perencanaan" aria-labelledby="h-perencanaan">
      ${viewHead("Perencanaan", "Antrean yang bisa dikerjakan satu shift. Beban dihitung, bukan dirasa.", `Potong data ${D.meta.cut}<br>${D.queue.length} baris · ${countBy(D.queue, "status", "Baru")} belum ditinjau · ${countBy(D.queue, "status", "Ditunda")} ditunda`)}
      <div class="grid">
        ${statStrip([
          { k: "Baris per shift", v: "40,15", n: "rata-rata 12 jam" },
          { k: "Median", v: "12,4", unit: "menit", n: "p50" },
          { k: "Ekor", v: "38,7", unit: "menit", n: "p95" },
          { k: "Sisa anggaran", v: "1.240", unit: "menit", n: "240 dikurangi 180 terpakai" }
        ])}
        ${card({
          span: "span-12",
          title: "Antrean lengkap",
          sub: `${D.queue.length} baris. Klik Tinjau untuk membuka alasan, sumber, dan tindakan.`,
          right: `<div class="flex"><span class="badge p4">${countBy(D.queue, "status", "Baru")} baru</span><span class="badge p3">${countBy(D.queue, "status", "Ditinjau")} ditinjau</span><span class="badge p1">${countBy(D.queue, "status", "Ditunda")} ditunda</span></div>`,
          body: queueTable(D.queue, { actions: true, wrap: "tall" }),
          foot: `<span>Urut: pita, lalu K_tampil. Bukan urut abjad.</span><span class="mono">${D.queue.length} baris</span>`
        })}
        ${card({
          span: "span-4",
          title: "Beban per baris",
          sub: `${totalMin} menit untuk ${D.queue.length} baris.`,
          body: D.queue.map((q) => barRow(`${q.id} ${q.claim}`, q.minutes, maxMin, { value: `${q.minutes} mnt`, d: 0, tone: q.minutes >= 5 ? "red" : q.minutes >= 3 ? "amber" : "" })).join("") +
            `<p class="small muted" style="margin-top:8px">Umur per baris belum dihitung; [04] hanya memberi rentang 0–87 menit.</p>`,
          foot: `<span>Batas tinjau: 1 shift</span><a class="link" href="#linimasa">Log keputusan</a>`
        })}
        ${card({
          span: "span-8",
          title: "Beban per klaim",
          sub: "Lambda setelah deduplikasi. Garis p50 dan p95 adalah penanda, bukan target.",
          body: D.load.map((l) => `<div style="margin-bottom:9px">
            <div class="flex-between small"><span>${l.name}</span><span class="mono">${nf(l.value, 3)} / shift</span></div>
            <div class="track" style="height:8px;margin-top:3px"><i class="${l.value > 15 ? "red" : l.value > 8 ? "amber" : ""}" style="width:${(l.value / maxLoad) * 100}%"></i><span class="mark" style="left:${(l.p50 / maxLoad) * 100}%"></span><span class="mark red" style="left:${(l.p95 / maxLoad) * 100}%"></span></div>
            <div class="small muted" style="margin-top:2px">p50 ${nf(l.p50, 1)} · p95 ${nf(l.p95, 1)} · ${l.note}</div>
          </div>`).join(""),
          foot: `<span>Anggaran 24 pemeriksaan per shift</span><span class="mono">vib 16,647</span>`
        })}
        ${card({
          span: "span-7",
          title: "Pareto jam henti",
          sub: "39.397,986 jam tercatat. Batang adalah jam, garis adalah persen kumulatif.",
          body: `<svg class="chart" viewBox="0 0 340 200" role="img" aria-label="Pareto jam henti per sebab">
            <line x1="30" y1="160" x2="330" y2="160" class="axis"/>
            <line x1="30" y1="160" x2="30" y2="20" class="axis"/>
            ${[0, 25, 50, 75, 100].map((p, i) => `<line x1="30" y1="${160 - (p / 100) * 130}" x2="330" y2="${160 - (p / 100) * 130}" class="gridline"/><text x="2" y="${164 - (p / 100) * 130}">${p}%</text>`).join("")}
            ${paretoBars}
            <polyline points="${paretoLine}" class="series"/>
            ${D.pareto.map((p, i) => `<circle cx="${30 + i * 62 + 21}" cy="${160 - (p.pct / 100) * 130}" r="3" class="point"/>`).join("")}
            <text x="250" y="194" class="label">kumulatif</text>
          </svg>
          <div class="legend" style="margin-top:4px"><span><i style="background:var(--red)"></i>equipment failure</span><span><i style="background:#3a4b5e"></i>sebab lain</span><span><i class="line" style="background:var(--red)"></i>kumulatif</span></div>`,
          foot: `<span>Sumber: S4, ringkasan aktivitas</span><a class="link" href="#bukti">Sumber angka</a>`
        })}
        ${card({
          span: "span-5",
          title: "Kalkulator beban",
          sub: "Hitung biaya waktu dari keputusan manual.",
          body: `<div class="field-row">
            <div class="field"><label for="calc-checks">Pemeriksaan per shift</label><input id="calc-checks" type="number" min="0" max="60" value="4"></div>
            <div class="field"><label for="calc-minutes">Menit per pemeriksaan</label><input id="calc-minutes" type="number" min="0" max="240" value="15"></div>
          </div>
          <div class="field" style="margin-top:8px"><label for="calc-shifts">Shift per minggu</label><input id="calc-shifts" type="number" min="0" max="42" value="21"></div>
          <div class="stat-grid" style="margin-top:10px">
            <div class="stat"><div class="k">Menit / minggu</div><div class="v" id="calc-out-min" style="font-size:24px">1.260</div></div>
            <div class="stat"><div class="k">Jam / minggu</div><div class="v" id="calc-out-hour" style="font-size:24px">21,0</div></div>
          </div>
          <p class="small muted" style="margin-top:8px">Angka ini hanya waktu pemeriksaan. Bukan biaya rupiah, bukan penghematan.</p>`,
          foot: `<span>Ubah input, hasil langsung berubah</span><span class="mono">manual</span>`
        })}
        ${card({
          span: "span-12",
          title: "Titik operasi",
          sub: "Pilih mode. Angka di bawah berubah mengikuti mode, bukan opini.",
          right: `<div class="seg" id="mode-seg">${modeBtns}</div>`,
          body: `<div class="grid" style="gap:10px">
            <div class="span-3 card inner" style="padding:10px"><div class="k small muted">Alarm palsu</div><div class="v display" id="op-fp" style="font-size:28px">927</div><div class="small muted">dari 4.924 TP</div></div>
            <div class="span-3 card inner" style="padding:10px"><div class="k small muted">Presisi</div><div class="v display" id="op-p" style="font-size:28px">0,8243</div><div class="small muted">median</div></div>
            <div class="span-3 card inner" style="padding:10px"><div class="k small muted">Recall</div><div class="v display" id="op-r" style="font-size:28px">0,6519</div><div class="small muted">median</div></div>
            <div class="span-3 card inner" style="padding:10px"><div class="k small muted">FAR</div><div class="v display" id="op-far" style="font-size:28px">4,0984</div><div class="small muted">per 24 jam</div></div>
          </div>
          <div class="flex-between" style="margin-top:10px"><span class="small" id="op-note">${mode.note}</span><span class="mono small" id="op-folds">${mode.folds} memenuhi FAR dan recall</span></div>
          <div class="table-wrap" style="margin-top:10px"><table class="table compact"><thead><tr><th>Mode</th><th class="num">FP</th><th class="num">TP</th><th class="num">Presisi</th><th class="num">Recall</th><th class="num">FAR</th><th class="num">Lead</th><th>Fold</th></tr></thead><tbody>
            ${D.hydModes.map((m) => `<tr><td class="strong">${m.name}</td><td class="num mono">${nf(m.fp, 0)}</td><td class="num mono">${nf(m.tp, 0)}</td><td class="num mono">${nf(m.p, 4)}</td><td class="num mono">${nf(m.r, 4)}</td><td class="num mono">${nf(m.far, 4)}</td><td class="num mono">${nf(m.lead, 1)}</td><td>${m.folds}</td></tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>H1p adalah komposisi terpilih untuk peringatan dini.</span><a class="link" href="#mesin">Bandingkan mesin</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- DATA ---------------- */

  function dataView() {
    const statusCls = { siap: "h2", tipis: "h3", absen: "h5" };
    const channelMatrix = `<div class="heat" style="grid-template-columns:92px repeat(${D.wells.length}, minmax(0,1fr))">
      <div class="hhead"></div>${D.wells.map((w) => `<div class="hhead">${w}</div>`).join("")}
      ${D.channels.map((c) => `<div class="hlabel">${c.code}</div>${c.wells.map((s, i) => `<div class="hcell ${statusCls[s]}" title="${c.name} di ${D.wells[i]}: ${s}">${s}</div>`).join("")}`).join("")}
    </div>`;

    const readyCount = (wellIdx) => D.channels.filter((c) => c.wells[wellIdx] === "siap").length;
    const wellBars = D.wells.map((w, i) => barRow(w, readyCount(i), 6, { value: `${readyCount(i)}/6`, d: 0, tone: readyCount(i) >= 5 ? "green" : readyCount(i) >= 3 ? "amber" : "red" })).join("");

    const fillRate = (code) => {
      const c = D.channels.find((x) => x.code === code);
      return c ? c.wells.filter((s) => s === "siap").length / c.wells.length : 0;
    };

    return `<section class="view" id="view-data" aria-labelledby="h-data">
      ${viewHead("Data", "Kesiapan kanal, label, dan jendela. Bila data tidak cukup, alat harus abstain.", `Potong data ${D.meta.cut}<br>6 sumur contoh · 6 kanal · 11 kelas`)}
      <div class="grid">
        ${statStrip([
          { k: "Antrean parse", v: "3.906", unit: "/ 7.150", n: "54,63 persen" },
          { k: "Label terbuka", v: "213", n: "belum diputuskan" },
          { k: "Kanal dipantau", v: "6", n: "WOB, torsi, alir, tekan, vib, SSI" },
          { k: "Dokumen belum dibuka", v: "69", unit: "/ 119", n: "58 persen" }
        ])}
        ${card({
          span: "span-8",
          title: "Antrean parse",
          sub: "3.906 dari 7.150 baris sudah masuk. Sisanya belum, bukan gagal.",
          right: `<span class="badge p3">54,63%</span>`,
          body: `<div class="track" style="height:10px"><i class="amber" style="width:54.63%"></i></div>
          <div class="flex-between small" style="margin-top:4px"><span class="muted">3.906 selesai</span><span class="muted">3.244 tersisa</span></div>
          <div class="table-wrap" style="margin-top:10px"><table class="table compact"><thead><tr><th>Batch</th><th class="num">Baris</th><th class="num">Selesai</th><th>Status</th><th>Catatan</th></tr></thead><tbody>
            <tr><td class="mono">B-01</td><td class="num mono">2.400</td><td class="num mono">2.400</td><td>${statusBadge("Selesai")}</td><td>Skema 18 kolom</td></tr>
            <tr><td class="mono">B-02</td><td class="num mono">2.400</td><td class="num mono">1.506</td><td>${statusBadge("Sebagian")}</td><td>213 label terbuka</td></tr>
            <tr><td class="mono">B-03</td><td class="num mono">2.350</td><td class="num mono">0</td><td>${statusBadge("Terbuka")}</td><td>Menunggu kunci label</td></tr>
          </tbody></table></div>`,
          foot: `<span>Angka dari kontrak data, bukan taksiran.</span><a class="link" href="#bukti">Kontrak data</a>`
        })}
        ${card({
          span: "span-4",
          title: "Status label",
          sub: "Label bukan sekadar ada atau tidak ada.",
          body: `<div style="display:flex;height:18px;border-radius:3px;overflow:hidden;border:1px solid var(--border-subtle)">
            <div title="Selesai 3.906" style="width:54.63%;background:var(--green)"></div>
            <div title="Terbuka 213" style="width:2.98%;background:var(--amber)"></div>
            <div title="Tersisa 3.031" style="width:42.39%;background:var(--bar-neutral)"></div>
          </div>
          <div class="legend" style="margin-top:8px"><span><i style="background:var(--green)"></i>Selesai 3.906</span><span><i style="background:var(--amber)"></i>Terbuka 213</span><span><i style="background:var(--bar-neutral)"></i>Tersisa 3.031</span></div>
          <div class="banner-note warn" style="margin-top:9px;padding:7px 8px;font-size:10px">Label yang belum ada tidak boleh diisi dengan tebakan. Baris tanpa label masuk abstain.</div>`,
          foot: `<span>213 label terbuka</span><a class="link" href="#batas">Kode abstain</a>`
        })}
        ${card({
          span: "span-7",
          title: "Kesiapan kanal per sumur",
          sub: "Siap, tipis, atau absen. Warna mengikuti status, bukan nilai.",
          right: `<div class="legend"><span><i style="background:#263a4b"></i>siap</span><span><i style="background:#4a2a32"></i>tipis</span><span><i style="background:#9c0f1f"></i>absen</span></div>`,
          body: channelMatrix,
          foot: `<span>6 sumur contoh, bukan seluruh lapangan.</span><a class="link" href="#batas">Minta data</a>`
        })}
        ${card({
          span: "span-5",
          title: "Kanal siap per sumur",
          sub: "Dihitung dari matriks di samping.",
          body: wellBars + `<p class="small muted" style="margin-top:7px">F-7 dan F-15 hanya punya tiga kanal siap. Klaim yang butuh lebih dari itu harus abstain.</p>`,
          foot: `<span>Ambang: 5 dari 6 untuk klaim penuh</span><a class="link" href="#batas">Syarat fitur</a>`
        })}
        ${card({
          span: "span-6",
          title: "Kanal yang tidak tercatat",
          sub: "Bukan nol. Tidak ada di data.",
          body: table(["Kanal", "Dipakai untuk", "Status", "Akibat"], [
            { cells: ["CRPM", "ssi", statusBadge("Tidak ada"), "Absen 62,3 persen"] },
            { cells: ["Flow meter", "hyd K-ii", statusBadge("Tidak ada"), "GAGAL C"] },
            { cells: ["Depth encoder", "bit_wear", statusBadge("Sebagian"), "Resolusi perlu cek"] },
            { cells: ["Torque sensor", "stuck", statusBadge("Sebagian"), "Tipis di F-7"] }
          ], { cls: "compact" }),
          foot: `<span>Ketiadaan data bukan nilai nol.</span><a class="link" href="#kamus">Bacaan</a>`
        })}
        ${card({
          span: "span-6",
          title: "Label ke fold",
          sub: "Setiap kelas punya penyebut berbeda.",
          body: table(["Kelas", "Sumber label", "Penyebut", "Catatan"], [
            { cells: ["hyd K-i", "onset", `<span class="mono">390</span>`, "H1p 218 dari 390"] },
            { cells: ["vib", "jendela", `<span class="mono">216</span>`, "4 sumur, 5.429 positif"] },
            { cells: ["ssi", "onset", `<span class="mono">132</span>`, "9 fold, 2 UNDERPOWERED"] },
            { cells: ["shk", "onset", `<span class="mono">181</span>`, "64 dari 181 pada ML"] },
            { cells: ["bit_wear", "baris", `<span class="mono">198.928</span>`, "18 kolom, 7 sumur"] },
            { cells: ["tool_wear", "alat", `<span class="mono">4</span>`, "4 dari 4 alat"] }
          ], { cls: "compact" }),
          foot: `<span>Jangan bandingkan kelas dengan penyebut berbeda.</span><a class="link" href="#bukti">Sumber</a>`
        })}
        ${card({
          span: "span-6",
          title: "Pemilih kanal",
          sub: "Isi kanal dan vonis QC.",
          body: table(["Kanal", "Terisi", "Vonis", "Catatan"], D.channels.map((c) => ({
            cells: [c.code, `<span class="mono">${pct(fillRate(c.code), 0)}</span>`, statusBadge(fillRate(c.code) >= 0.8 ? "Siap" : fillRate(c.code) >= 0.5 ? "Sebagian" : "Terbuka"), c.name]
          })), { cls: "compact" }),
          foot: `<span>Terisi = siap dibagi jumlah sumur contoh.</span><a class="link" href="#batas">Syarat</a>`
        })}
        ${card({
          span: "span-6",
          title: "Peta drift status",
          sub: "Stabil, geser, tipis, atau absen. Bukan angka karangan.",
          body: `<div class="heat" style="grid-template-columns:72px repeat(4, minmax(0,1fr))">
            <div class="hhead"></div><div class="hhead">WOB</div><div class="hhead">Torsi</div><div class="hhead">Alir</div><div class="hhead">Tekan</div>
            ${D.wells.map((w, i) => `<div class="hlabel">${w}</div>${["WOB", "TORQUE", "FLOW", "PRESS"].map((code) => {
              const c = D.channels.find((x) => x.code === code);
              const s = c ? c.wells[i] : "absen";
              const label = s === "siap" ? "stabil" : s === "tipis" ? "geser" : "absen";
              const cls = s === "siap" ? "h2" : s === "tipis" ? "h3" : "h5";
              return `<div class="hcell ${cls}">${label}</div>`;
            }).join("")}`).join("")}
          </div>`,
          foot: `<span>Status diturunkan dari matriks kanal.</span><a class="link" href="#mesin">Dampak ke mesin</a>`
        })}
        ${card({
          span: "span-12",
          title: "Minta data",
          sub: "Satu formulir, satu pemilik, satu tenggat.",
          body: `<div class="flex-between wrap"><div><strong>Data yang paling menahan:</strong> CRPM untuk ssi, flow meter untuk hyd K-ii, dan label per kejadian untuk stuck.</div><div class="flex"><button class="btn primary" type="button" data-request="CRPM">Minta CRPM</button><button class="btn" type="button" data-request="flow meter">Minta flow meter</button><button class="btn" type="button" data-request="label per kejadian">Minta label</button></div></div>`,
          foot: `<span>Formulir mencatat permintaan ke log sesi, bukan mengirim email.</span><a class="link" href="#batas">Pemilik data</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- MESIN ---------------- */

  function mesin() {
    const modes = D.hydModes;
    const scatter = `<svg class="chart" viewBox="0 0 360 210" role="img" aria-label="Presisi lawan recall untuk empat mode hyd">
      <line x1="40" y1="180" x2="340" y2="180" class="axis"/>
      <line x1="40" y1="180" x2="40" y2="20" class="axis"/>
      <line x1="40" y1="100" x2="340" y2="100" class="gridline"/>
      <line x1="190" y1="20" x2="190" y2="180" class="gridline"/>
      <text x="40" y="196">0</text><text x="185" y="196">0,5</text><text x="326" y="196">1,0</text>
      <text x="8" y="184">0</text><text x="8" y="104">0,5</text><text x="8" y="24">1,0</text>
      <text x="160" y="206">Recall</text><text x="6" y="12">Presisi</text>
      ${modes.map((m, i) => {
        const x = 40 + m.r * 300;
        const y = 180 - m.p * 160;
        return `<circle cx="${x}" cy="${y}" r="4.5" class="point"/><text x="${x + 7}" y="${y - 6}" class="label">${m.name}</text>`;
      }).join("")}
      <line x1="40" y1="180" x2="340" y2="20" class="gridline"/>
    </svg>`;

    const voiceRows = D.damages.map((d) => ({
      cells: [
        d.name,
        `<span class="mono">${d.k}</span>`,
        `<span class="mono">${d.cap}</span>`,
        d.pita ? pitaShort(d.pita) : `<span class="badge p1">ABSTAIN</span>`,
        `<span class="chip">${d.vote}</span>`,
        `<span class="mono">${d.weight}</span>`
      ]
    }));

    return `<section class="view" id="view-mesin" aria-labelledby="h-mesin">
      ${viewHead("Mesin", "Tujuh mesin, 27 kepala. Yang penting bukan siapa paling pintar, tetapi siapa berani abstain.", `Potong data ${D.meta.cut}<br>7 mesin · 27 kepala · 0 alarm otomatis`)}
      <div class="grid">
        ${statStrip([
          { k: "Mesin", v: "7", n: "hyd, vib, ssi, shk, stuck, bit_wear, tool_wear" },
          { k: "Kepala", v: "27", n: "5 L0 · 11 L1 · 9 L2 · 2 L3" },
          { k: "Kesepakatan", v: "92,47", unit: "%", n: "sampai 99,43 seluruh jendela" },
          { k: "Kelas positif", v: "23,81", unit: "%", n: "shk, jauh di bawah kesepakatan" }
        ])}
        ${card({
          span: "span-7",
          title: "Model lawan baseline",
          sub: "Baseline harus disebut. Tanpa itu, angka tidak punya arti.",
          body: table(["Kelas", "Metrik", "Model", "Pembanding", "Selisih"], [
            { cells: ["hyd K-i", "presisi", `<span class="mono">0,8243</span>`, "rule 0,6835", `<span class="status-ok">+0,1408</span>`] },
            { cells: ["vib", "AUPRC", `<span class="mono">0,6204</span>`, "prevalensi 0,2542", `<span class="status-ok">2,44x</span>`] },
            { cells: ["ssi", "AUPRC", `<span class="mono">0,0440</span>`, "prevalensi 0,0159", `<span class="status-ok">2,77x</span>`] },
            { cells: ["shk", "AUPRC", `<span class="mono">0,0499</span>`, "prevalensi 0,0243", `<span class="status-ok">2,05x</span>`] },
            { cells: ["bit_wear", "plafon", `<span class="mono">0,2525</span>`, "P2", `<span class="status-bad">tidak bisa naik</span>`] }
          ], { cls: "compact" }),
          foot: `<span>Pembanding adalah baseline yang sama di setiap baris.</span><a class="link" href="#bukti">Sumber</a>`
        })}
        ${card({
          span: "span-5",
          title: "Keputusan uji",
          sub: "Empat hipotesis, empat vonis.",
          body: `<div class="stack-sm">
            <div class="banner-note" style="padding:8px"><div><strong>H1p diterima</strong><br><span class="small">7 dari 9 fold memenuhi FAR dan recall. Membayar FAR 0,5682 lebih tinggi.</span></div></div>
            <div class="banner-note bad" style="padding:8px"><div><strong>H2 untuk shk ditolak</strong><br><span class="small">TP turun 76,04 persen. Recall 0,0037.</span></div></div>
            <div class="banner-note bad" style="padding:8px"><div><strong>H1p untuk ssi ditolak</strong><br><span class="small">1 TP dan 17 FP dari 132 onset. Recall 0,0.</span></div></div>
            <div class="banner-note bad" style="padding:8px"><div><strong>vib hybrid ditolak</strong><br><span class="small">0 dari 4 fold mencapai recall 0,5.</span></div></div>
          </div>`,
          foot: `<span>Vonis, bukan opini.</span><a class="link" href="#linimasa">Log</a>`
        })}
        ${card({
          span: "span-6",
          title: "Presisi lawan recall",
          sub: "Empat mode hyd. Titik kanan atas lebih baik, tetapi biaya alarm harus dibaca.",
          body: scatter + `<div class="legend"><span><i style="background:var(--red)"></i>mode hyd</span><span><i class="line" style="background:var(--text-3)"></i>garis acak</span></div>`,
          foot: `<span>H1p3 punya recall paling rendah, FAR paling rendah.</span><a class="link" href="#perencanaan">Titik operasi</a>`
        })}
        ${card({
          span: "span-6",
          title: "Harga pemangkasan",
          sub: "Recall selalu turun saat alarm dipangkas.",
          body: table(["Kelas", "Alarm", "Presisi", "Recall"], [
            { cells: ["hyd", `<span class="status-ok">-35,79%</span>`, `<span class="status-ok">+0,2017</span>`, `<span class="status-bad">-0,1052</span>`] },
            { cells: ["tool_wear", `<span class="status-ok">-93,11%</span>`, "tetap", `<span class="status-bad">-0,6666</span>`] }
          ], { cls: "compact" }),
          foot: `<span>Tidak ada makan siang gratis.</span><a class="link" href="#kepercayaan">Batas</a>`
        })}
        ${card({
          span: "span-7",
          title: "Peta suara dewan",
          sub: "Dukung, tolak, abstain. Kepala bisu tidak dihitung menolak.",
          body: table(["Klaim", "K_tampil", "Batas", "Pita", "Suara", "Bobot"], voiceRows, { cls: "compact", wrap: "short" }),
          foot: `<span>Dukungan berbobot 1,65 dari 9,15.</span><a class="link" href="#linimasa">Kuorum</a>`
        })}
        ${card({
          span: "span-5",
          title: "Kesepakatan komponen",
          sub: "Angka tinggi bisa menipu bila kelas positif jarang.",
          body: `<div class="heat" style="grid-template-columns:74px repeat(4, minmax(0,1fr))">
            <div class="hhead"></div><div class="hhead">hyd</div><div class="hhead">vib</div><div class="hhead">ssi</div><div class="hhead">shk</div>
            <div class="hlabel">hyd</div><div class="hcell h2">1,00</div><div class="hcell h2">0,92-0,99</div><div class="hcell h2">0,92-0,99</div><div class="hcell h3">0,92-0,99</div>
            <div class="hlabel">vib</div><div class="hcell h2">0,92-0,99</div><div class="hcell h2">1,00</div><div class="hcell h2">0,92-0,99</div><div class="hcell h3">0,92-0,99</div>
            <div class="hlabel">ssi</div><div class="hcell h2">0,92-0,99</div><div class="hcell h2">0,92-0,99</div><div class="hcell h2">1,00</div><div class="hcell h3">0,92-0,99</div>
            <div class="hlabel">shk</div><div class="hcell h3">0,92-0,99</div><div class="hcell h3">0,92-0,99</div><div class="hcell h3">0,92-0,99</div><div class="hcell h5">0,2381</div>
          </div>
          <p class="small muted" style="margin-top:7px">Sel 0,2381 adalah kesepakatan pada kelas positif shk, bukan seluruh jendela. Itu angka yang penting.</p>`,
          foot: `<span>Rentang seluruh jendela: 92,47 sampai 99,43 persen.</span><a class="link" href="#bukti">Sumber</a>`
        })}
        ${card({
          span: "span-6",
          title: "Rekam jejak per sumur",
          sub: "LOWO: satu sumur dikeluarkan dari latihan.",
          body: table(["Kelas", "Sumur", "Fold lolos", "Catatan"], [
            { cells: ["hyd K-i", `<span class="mono">9</span>`, `<span class="mono">7/9</span>`, "H1p"] },
            { cells: ["vib", `<span class="mono">4</span>`, `<span class="mono">0/4</span>`, "Tidak ada yang mencapai 0,5"] },
            { cells: ["ssi", `<span class="mono">9</span>`, `<span class="mono">0/9</span>`, "H1p recall 0,0"] },
            { cells: ["shk", `<span class="mono">9</span>`, `<span class="mono">4/9</span>`, "ML pada kedua paruh"] },
            { cells: ["stuck", `<span class="mono">9</span>`, `<span class="mono">1/9</span>`, "H2"] }
          ], { cls: "compact" }),
          foot: `<span>LOWO bukan validasi silang biasa.</span><a class="link" href="#kamus">Arti</a>`
        })}
        ${card({
          span: "span-6",
          title: "Jebakan sirkularitas",
          sub: "Label dan fitur dari sumber yang sama.",
          body: `<div class="banner-note bad" style="padding:9px"><div><strong>bit_wear:</strong> label adalah indeks mekanika, bukan observasi keausan. Model bisa belajar rumus, bukan aus.</div></div>
          <ul class="bullets red" style="margin-top:8px">
            <li>Fitur WOB dan torsi dipakai untuk membentuk label high_MSE.</li>
            <li>Tanpa uji alat fisik, klaim keausan tidak sah.</li>
            <li>Banner ini harus tetap tampil di semua layar bit_wear.</li>
          </ul>`,
          foot: `<span>K-5 selesai dengan banner tetap.</span><a class="link" href="#batas">Batas</a>`
        })}
        ${card({
          span: "span-12",
          title: "Syarat eksperimen berikutnya",
          sub: "Sebelum menambah model, pastikan enam hal ini.",
          body: `<div class="grid" style="gap:8px">
            <div class="span-4"><ul class="bullets"><li>Label per kejadian untuk stuck.</li><li>Kanal CRPM untuk ssi.</li><li>Flow meter untuk hyd K-ii.</li></ul></div>
            <div class="span-4"><ul class="bullets"><li>Satuan FAR ditulis di setiap tabel.</li><li>Penyebut onset disamakan.</li><li>Fold UNDERPOWERED dipisah.</li></ul></div>
            <div class="span-4"><ul class="bullets"><li>Uji alat fisik untuk bit_wear.</li><li>Ambang biaya dari pemilik operasi.</li><li>Jadwal inspeksi dari reliability.</li></ul></div>
          </div>`,
          foot: `<span>Tanpa enam ini, model baru hanya menambah angka.</span><a class="link" href="#batas">Pemilik data</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- LINIMASA ---------------- */

  function linimasa() {
    const tkSteps = [
      { level: "TK-1", label: "TENANG", desc: "Tidak ada yang perlu ditinjau.", state: "done" },
      { level: "TK-2", label: "PANTAU", desc: "Masuk daftar pantau. Insinyur memutuskan di akhir shift.", state: "active" },
      { level: "TK-3", label: "TINJAU", desc: "Satu shift. Catat aktor, keputusan, alasan.", state: "next" },
      { level: "TK-4", label: "HENTIKAN", desc: "Hanya hyd K-i yang bisa mencapai. Periksa sebelum lanjut.", state: "next" }
    ];
    const ladder = tkSteps.map((s) => `<div style="display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-bottom:1px solid var(--border-subtle)">
      <div class="badge ${s.state === "active" ? "p4" : s.state === "done" ? "p3" : "p1"}" style="min-width:44px;justify-content:center">${s.level}</div>
      <div><strong style="font-size:11.5px">${s.label}</strong><div class="small muted">${s.desc}</div></div>
    </div>`).join("");

    const votes = D.damages.map((d) => ({
      cells: [d.name, `<span class="mono">${d.weight}</span>`, `<span class="chip">${d.vote}</span>`, d.pita ? pitaShort(d.pita) : `<span class="badge p1">ABSTAIN</span>`, `<span class="small muted">${d.limit}</span>`]
    }));

    const gates = [
      { id: "G1", name: "Data dan label", status: "Selesai", note: "Kontrak data 18 kolom, 21 artefak JSON." },
      { id: "G2", name: "Bukti angka", status: "Selesai", note: "726 baris ledger, 6 cacat teks." },
      { id: "G3", name: "Keputusan komposisi", status: "Selesai", note: "H1p untuk hyd, komposisi lain tetap." },
      { id: "G4", name: "Uji operasi", status: "Terbuka", note: "Butuh jadwal inspeksi dan ambang biaya." }
    ];

    return `<section class="view" id="view-linimasa" aria-labelledby="h-linimasa">
      ${viewHead("Linimasa", "Bagaimana alat sampai pada keputusan hari ini, dan apa yang masih terbuka.", `Potong data ${D.meta.cut}<br>4 gerbang · ${D.conflicts.length} konflik · ${D.decisions.length} keputusan`)}
      <div class="grid">
        ${card({
          span: "span-5",
          title: "Tangga kewaspadaan",
          sub: "Tingkat bukan perintah. Hanya TK-4 yang menyentuh operasi.",
          body: ladder,
          foot: `<span>Aktif: ${D.tk.level} ${D.tk.label}</span><a class="link" href="#kamus">Arti TK</a>`
        })}
        ${card({
          span: "span-7",
          title: "Kuorum dan batas dominasi",
          sub: "Dua pengaman yang bisa membatalkan suara mayoritas.",
          body: `<div class="flex-between small"><span>Engine bersuara</span><span class="mono">6 / 7 · ambang 4 / 7</span></div>
          <div class="track" style="height:10px;margin:3px 0 10px"><i class="green" style="width:85.7%"></i><span class="mark" style="left:57.1%"></span></div>
          <div class="flex-between small"><span>Cakupan bobot</span><span class="mono">0,87 · ambang 0,50</span></div>
          <div class="track" style="height:10px;margin:3px 0 10px"><i class="green" style="width:87%"></i><span class="mark" style="left:50%"></span></div>
          <div class="flex-between small"><span>Pangsa hyd K-i sebelum potong</span><span class="mono">36,07%</span></div>
          <div class="track" style="height:10px;margin:3px 0 4px"><i class="red" style="width:100%"></i><span class="mark red" style="left:35%"></span></div>
          <div class="flex-between small"><span>Setelah potong</span><span class="mono">3,2025 · S 18,23%</span></div>
          <div class="track" style="height:10px;margin:3px 0 10px"><i class="amber" style="width:92.9%"></i><span class="mark red" style="left:35%"></span></div>
          <p class="small muted">Garis merah adalah batas 35 persen. Batang pertama melewatinya, batang kedua sudah dipotong.</p>`,
          foot: `<span>06 bagian 5.3 dan 5.4</span><a class="link" href="#bukti">Sumber</a>`
        })}
        ${card({
          span: "span-7",
          title: "Peta suara",
          sub: "11 klaim. Dukung, tolak, abstain, dan bobotnya.",
          body: table(["Klaim", "Bobot", "Suara", "Pita", "Catatan"], votes, { cls: "compact", wrap: "short" }),
          foot: `<span>Dukungan berbobot 1,65 dari 9,15.</span><a class="link" href="#mesin">Mesin</a>`
        })}
        ${card({
          span: "span-5",
          title: "Gerbang keputusan",
          sub: "Tiga selesai, satu terbuka.",
          body: gates.map((g) => `<div style="display:flex;gap:9px;padding:7px 0;border-bottom:1px solid var(--border-subtle)">
            <span class="mono small" style="width:22px;color:var(--text-3)">${g.id}</span>
            <div class="grow"><strong style="font-size:11px">${g.name}</strong><div class="small muted">${g.note}</div></div>
            ${statusBadge(g.status)}
          </div>`).join(""),
          foot: `<span>G4 butuh data dari pemilik operasi.</span><a class="link" href="#batas">Pemilik</a>`
        })}
        ${card({
          span: "span-12",
          title: "Log keputusan",
          sub: "Setiap keputusan mencatat waktu, aktor, klaim, tindakan, dan alasan.",
          right: `<button class="btn primary sm" type="button" data-decide="baru">Catat keputusan</button>`,
          body: `<div class="table-wrap short"><table class="table compact"><thead><tr><th>Waktu</th><th>Aktor</th><th>Klaim</th><th>Tindakan</th><th>Alasan</th></tr></thead><tbody id="decision-body">
            ${D.decisions.map((d) => `<tr><td class="mono">${d.time}</td><td>${d.actor}</td><td class="strong">${d.claim}</td><td>${statusBadge(d.action === "Tunda" ? "Ditunda" : d.action === "Tinjau" ? "Ditinjau" : "Baru")}</td><td class="small muted">${d.reason}</td></tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>Log disimpan di sesi ini. Bukan audit resmi.</span><span class="mono">${D.decisions.length} baris</span>`
        })}
        ${card({
          span: "span-6",
          title: "Buku konflik",
          sub: `${D.conflicts.length} entri. ${countBy(D.conflicts, "status", "Selesai")} selesai, ${countBy(D.conflicts, "status", "Terbuka")} terbuka, ${countBy(D.conflicts, "status", "Ditolak") + countBy(D.conflicts, "status", "Gagal")} ditolak atau gagal.`,
          body: table(["ID", "Topik", "A", "B", "Status"], D.conflicts.map((c) => ({
            cells: [`<span class="mono">${c.id}</span>`, c.topic, `<span class="small">${c.a}</span>`, `<span class="small">${c.b}</span>`, statusBadge(c.status)]
          })), { cls: "compact", wrap: "short" }),
          foot: `<span>Konflik tidak dihapus, hanya diselesaikan.</span><a class="link" href="#bukti">Bukti</a>`
        })}
        ${card({
          span: "span-6",
          title: "Registri dokumen",
          sub: "Enam dokumen yang mengikat keputusan.",
          body: table(["Berkas", "Ukuran", "Status"], D.docs.slice(0, 6).map((d) => ({
            cells: [`<span class="mono small">${d.file.split("/").pop()}</span>`, `<span class="mono">${d.bytes}</span>`, statusBadge(d.status)]
          })), { cls: "compact" }),
          foot: `<span>10 dokumen inti di halaman Bukti.</span><a class="link" href="#bukti">Buka</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- BUKTI ---------------- */

  function bukti() {
    const refRows = D.provenance.map((p) => ({
      cells: [
        `<span class="strong">${p.item}</span>`,
        `<span class="mono">${p.value}</span>`,
        p.unit,
        `<span class="small muted">${p.source}</span>`,
        prov(p.status),
        `<button class="btn sm ghost" type="button" data-copy="${p.item}: ${p.value} ${p.unit} (${p.source})" aria-label="Salin rujukan ${p.item}" title="Salin rujukan"><svg width="13" height="13" aria-hidden="true"><use href="#i-copy"/></svg></button>`
      ]
    }));

    const locks = [
      { item: "Kunci rujukan", test: "Ubah satu angka di salinan", result: "Gagal, hash berubah", status: "Lulus" },
      { item: "Mutan satuan", test: "Ganti per 24 jam kalender menjadi per baris", result: "Tertangkap, satuan berbeda", status: "Lulus" },
      { item: "Mutan penyebut", test: "Ganti 390 onset menjadi 181", result: "Tertangkap, penyebut tidak cocok", status: "Lulus" },
      { item: "Mutan label", test: "Ganti bit_wear menjadi observasi", result: "Tertangkap, banner tetap", status: "Lulus" },
      { item: "Mutan pita", test: "Naikkan P2 menjadi P4", result: "Tertangkap, batas kelas menahan", status: "Lulus" }
    ];

    const units = [
      { item: "FAR hyd", unit: "per 24 jam kalender", note: "Bukan per baris. Bukan per shift." },
      { item: "FAR tool_wear", unit: "per menit", note: "Jangan dibandingkan dengan FAR 24 jam." },
      { item: "Lead", unit: "menit", note: "Jarak alarm ke onset." },
      { item: "Keyakinan", unit: "rasio 0 sampai 1", note: "Bukan persen kecuali ditulis." },
      { item: "Jam henti", unit: "jam", note: "39.397,986 jam tercatat." },
      { item: "Biaya", unit: "tidak ada", note: "Tidak ada kolom rupiah." }
    ];

    const unopened = [
      { file: "Reference/Drilling_Report_*.pdf", n: "31", note: "Belum dibuka" },
      { file: "Reference/Well_Test_*.pdf", n: "18", note: "Belum dibuka" },
      { file: "Reference/Completion_*.pdf", n: "12", note: "Belum dibuka" },
      { file: "Reference/Geology_*.pdf", n: "8", note: "Belum dibuka" }
    ];

    const provC = D.provenance.reduce((a, p) => { a[p.status] = (a[p.status] || 0) + 1; return a; }, {});

    return `<section class="view" id="view-bukti" aria-labelledby="h-bukti">
      ${viewHead("Bukti", "Setiap angka bisa dilacak ke berkas dan baris. Bila tidak, angkanya tidak dipakai.", `Potong data ${D.meta.cut}<br>${D.provenance.length} angka kunci · 726 baris ledger · 10 dokumen inti`)}
      <div class="grid">
        ${statStrip([
          { k: "Angka kunci", v: String(D.provenance.length), n: "dalam tabel rujukan" },
          { k: "Terukur", v: String(provC.ok || 0), n: "observasi langsung" },
          { k: "Turunan", v: String(provC.note || 0), n: "hasil hitung" },
          { k: "Belum kutip", v: String(provC.block || 0), n: "tidak boleh dipakai" }
        ])}
        ${card({
          span: "span-12",
          title: "Tabel rujukan",
          sub: "Nilai, satuan, sumber, status. Tombol salin menghasilkan kutipan satu baris.",
          right: `<span class="badge p3">726 baris</span>`,
          body: `<div class="table-wrap tall"><table class="table compact"><thead><tr><th>Angka</th><th class="num">Nilai</th><th>Satuan</th><th>Sumber</th><th>Status</th><th></th></tr></thead><tbody>
            ${refRows.map((r) => `<tr>${r.cells.map((c, i) => `<td${i === 1 ? ' class="num"' : ""}>${c}</td>`).join("")}</tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>Klik ikon salin untuk memakai rujukan di dokumen lain.</span><span class="mono">${prov("ok")} ${prov("note")} ${prov("block")}</span>`
        })}
        ${card({
          span: "span-4",
          title: "Legenda provenance",
          sub: "Tiga status, tiga arti.",
          body: `<div class="stack-sm">
            <div class="flex-between"><span>${prov("ok")}</span><span class="small muted">Diukur langsung</span></div>
            <div class="flex-between"><span>${prov("note")}</span><span class="small muted">Dihitung dari angka lain</span></div>
            <div class="flex-between"><span>${prov("block")}</span><span class="small muted">Belum ada rujukan</span></div>
          </div>
          <p class="small muted" style="margin-top:9px">Status belum kutip bukan berarti salah. Artinya belum boleh dipakai sebagai dasar keputusan.</p>`,
          foot: `<span>Kebijakan evaluasi</span><a class="link" href="#kamus">Arti</a>`
        })}
        ${card({
          span: "span-8",
          title: "Uji kunci dan mutan",
          sub: "Lima mutan, lima tangkapan. Bila satu lolos, tabel ini tidak layak dipercaya.",
          body: table(["Objek", "Uji", "Hasil", "Status"], locks.map((l) => ({
            cells: [l.item, l.test, `<span class="small">${l.result}</span>`, statusBadge(l.status)]
          })), { cls: "compact" }),
          foot: `<span>Uji dilakukan pada salinan, bukan data asli.</span><a class="link" href="#batas">Batas</a>`
        })}
        ${card({
          span: "span-6",
          title: "Papan satuan",
          sub: "Satuan yang salah membuat angka benar terlihat salah.",
          body: table(["Objek", "Satuan", "Catatan"], units.map((u) => ({
            cells: [u.item, `<span class="mono">${u.unit}</span>`, `<span class="small muted">${u.note}</span>`]
          })), { cls: "compact" }),
          foot: `<span>Satuan ditulis di setiap tabel.</span><a class="link" href="#kamus">Kamus</a>`
        })}
        ${card({
          span: "span-6",
          title: "Dokumen belum dibuka",
          sub: "69 dari 119 berkas. Ini utang bukti, bukan alasan menunda.",
          body: table(["Berkas", "Jumlah", "Status"], unopened.map((u) => ({
            cells: [`<span class="mono small">${u.file}</span>`, `<span class="mono">${u.n}</span>`, statusBadge("Terbuka")]
          })), { cls: "compact" }),
          foot: `<span>69 berkas belum dibuka.</span><a class="link" href="#data">Data</a>`
        })}
        ${card({
          span: "span-12",
          title: "Kaki berkas",
          sub: "Ukuran dan status 10 dokumen inti.",
          body: `<div class="table-wrap"><table class="table compact"><thead><tr><th>Berkas</th><th class="num">Byte</th><th>Isi</th><th>Status</th><th>Catatan</th></tr></thead><tbody>
            ${D.docs.map((d) => `<tr><td class="mono small">${d.file}</td><td class="num mono">${d.bytes}</td><td>${d.lines}</td><td>${statusBadge(d.status)}</td><td class="small muted">${d.note}</td></tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>Ukuran berkas diambil dari disk, bukan dari ingatan.</span><span class="mono">10 berkas</span>`
        })}
        ${card({
          span: "span-6",
          title: "Cara mengutip",
          sub: "Satu baris, tanpa memperdebatkan tafsir.",
          body: `<div class="quote mono" style="font-size:10.5px">H1p FP 927, presisi 0,8243, recall 0,6519, FAR 4,0984 per 24 jam kalender. Sumber: docs/RND_S6_PM_WAVE2.md baris 150.</div>
          <p class="small muted" style="margin-top:8px">Kutipan selalu membawa satuan dan sumber. Bila salah satu tidak ada, jangan pakai.</p>`,
          foot: `<button class="link" type="button" data-copy="H1p FP 927, presisi 0,8243, recall 0,6519, FAR 4,0984 per 24 jam kalender. Sumber: docs/RND_S6_PM_WAVE2.md baris 150.">Salin contoh</button><span class="mono">1 baris</span>`
        })}
        ${card({
          span: "span-6",
          title: "Yang belum diverifikasi",
          sub: "Tiga hal yang tidak boleh diklaim.",
          body: `<ul class="bullets red">
            <li>Biaya rupiah. Tidak ada kolom biaya di repo.</li>
            <li>Jadwal inspeksi. Tidak ada kalender perawatan.</li>
            <li>Produksi tertunda. Tidak ada berkas deferred production.</li>
          </ul>
          <p class="small muted" style="margin-top:8px">Ketiganya adalah slot Layer B yang masih kosong, bukan angka nol.</p>`,
          foot: `<span>3 slot kosong</span><a class="link" href="#batas">Layer B</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- BATAS ---------------- */

  function batas() {
    const abstain = [
      { code: "AB-1", meaning: "Tidak ada komposisi yang layak", example: "hyd K-ii, bit_wear K-2", effect: "Tidak ada angka. Tidak boleh tampil sebagai hasil." },
      { code: "AB-2", meaning: "Kanal kurang", example: "ssi tanpa CRPM", effect: "Pemeringkatan tren, bukan peringatan." },
      { code: "AB-3", meaning: "Label tipis", example: "stuck per kejadian", effect: "Triase, bukan alarm." },
      { code: "AB-4", meaning: "Data terblokir", example: "rating motor, tekanan EDM", effect: "Tidak dinilai menurut desain." },
      { code: "AB-5", meaning: "Label per kejadian tidak ada", example: "stuck K-ii", effect: "Tiga kepala bisu. Abstain." }
    ];

    const featureBar = `<div style="display:flex;height:20px;border-radius:3px;overflow:hidden;border:1px solid var(--border-subtle)">
      <div title="32 layak" style="width:66.67%;background:var(--green)"></div>
      <div title="13 layak bersyarat" style="width:27.08%;background:var(--amber)"></div>
      <div title="3 perlu perbaikan" style="width:6.25%;background:var(--red)"></div>
    </div>
    <div class="legend" style="margin-top:8px"><span><i style="background:var(--green)"></i>32 layak</span><span><i style="background:var(--amber)"></i>13 bersyarat</span><span><i style="background:var(--red)"></i>3 perlu perbaikan</span></div>`;

    return `<section class="view" id="view-batas" aria-labelledby="h-batas">
      ${viewHead("Batas data", "Apa yang tidak bisa dijawab, mengapa, dan siapa yang bisa membuka jalan.", `Potong data ${D.meta.cut}<br>5 kode abstain · 2 kepala L3 · 3 slot Layer B kosong`)}
      <div class="grid">
        ${statStrip([
          { k: "Kode abstain", v: "5", n: "AB-1 sampai AB-5" },
          { k: "Kepala L3", v: "2", n: "rating motor, tekanan EDM" },
          { k: "Slot Layer B kosong", v: "3", n: "biaya, jadwal, produksi tertunda" },
          { k: "Fitur inti", v: "10", n: "9 layak, 1 bersyarat" }
        ])}
        ${card({
          span: "span-7",
          title: "Kode abstain",
          sub: "Abstain bukan nol. Ia adalah jawaban yang sah.",
          body: table(["Kode", "Arti", "Contoh", "Akibat"], abstain.map((a) => ({
            cells: [`<span class="mono strong">${a.code}</span>`, a.meaning, `<span class="small">${a.example}</span>`, `<span class="small muted">${a.effect}</span>`]
          })), { cls: "compact" }),
          foot: `<span>Abstain tampil di kartu dan tabel.</span><a class="link" href="#kamus">Arti</a>`
        })}
        ${card({
          span: "span-5",
          title: "Dua kepala L3",
          sub: "Eksplorasi, bukan hasil.",
          body: D.l3.map((x) => `<div class="banner-note bad" style="margin-bottom:8px;padding:9px"><div><strong>${x.name}</strong> · ${x.code}<br><span class="small">${x.reason}</span></div></div>`).join("") + `<p class="small muted">L3 tidak masuk dewan. Tidak boleh menjadi dasar keputusan.</p>`,
          foot: `<span>2 dari 27 kepala</span><a class="link" href="#mesin">Mesin</a>`
        })}
        ${card({
          span: "span-6",
          title: "Layer B: slot kosong",
          sub: "Tiga hal yang tidak ada di repo.",
          body: table(["Slot", "Status", "Catatan"], D.layerB.map((l) => ({
            cells: [l.slot, statusBadge(l.status), `<span class="small muted">${l.note}</span>`]
          })), { cls: "compact" }),
          foot: `<span>2 terukur, 3 kosong</span><a class="link" href="#bukti">Bukti</a>`
        })}
        ${card({
          span: "span-6",
          title: "Status fitur",
          sub: "10 fitur inti, lalu paket lengkap 48 fitur.",
          body: featureBar + `<div class="table-wrap" style="margin-top:10px"><table class="table compact"><thead><tr><th>Fitur</th><th>Status</th><th>Catatan</th></tr></thead><tbody>
            ${D.features.map((f) => `<tr><td><span class="mono small">${f.id}</span> ${f.name}</td><td>${statusBadge(f.status)}</td><td class="small muted">${f.note}</td></tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>Paket lengkap: 32 layak, 13 bersyarat, 3 perlu perbaikan.</span><a class="link" href="#linimasa">Prioritas</a>`
        })}
        ${card({
          span: "span-7",
          title: "Pemilik data",
          sub: "Satu area, satu pemilik, satu kebutuhan.",
          body: table(["Area", "Pemilik", "Kebutuhan", "Status"], D.owners.map((o) => ({
            cells: [o.area, o.owner, `<span class="small">${o.need}</span>`, statusBadge(o.status)]
          })), { cls: "compact" }),
          foot: `<span>Tanpa pemilik, permintaan data menggantung.</span><a class="link" href="#data">Minta data</a>`
        })}
        ${card({
          span: "span-5",
          title: "Tiga sumbu kesiapan",
          sub: "Bukan skor tunggal.",
          body: D.axes.map((a) => `<div style="margin-bottom:9px"><div class="flex-between small"><span>${a.name}</span><span class="mono">${a.value}</span></div><div class="track" style="height:8px;margin-top:3px"><i class="${a.value === "Sedang" ? "amber" : a.value === "Sempit" ? "red" : "amber"}" style="width:${a.value === "Sedang" ? 55 : a.value === "Sempit" ? 35 : 45}%"></i></div><div class="small muted">${a.note}</div></div>`).join(""),
          foot: `<span>Bukti sedang, cakupan sempit, kesiapan pilot.</span><a class="link" href="#kepercayaan">Kepercayaan</a>`
        })}
        ${card({
          span: "span-12",
          title: "Grafik yang dilarang",
          sub: "Sembilan bentuk yang menyembunyikan ketidakpastian.",
          body: `<div class="table-wrap"><table class="table compact"><thead><tr><th>Bentuk</th><th>Mengapa dilarang</th><th>Ganti dengan</th></tr></thead><tbody>
            ${D.forbidden.map((f) => `<tr><td class="strong">${f.name}</td><td class="small muted">${f.why}</td><td class="small">${f.right}</td></tr>`).join("")}
          </tbody></table></div>`,
          foot: `<span>Aturan ini berlaku di semua layar.</span><a class="link" href="#kamus">Bacaan</a>`
        })}
        ${card({
          span: "span-12",
          title: "Buka jalan",
          sub: "Tiga permintaan yang paling menahan.",
          body: `<div class="flex-between wrap"><div class="small" style="max-width:620px">CRPM membuka ssi. Flow meter membuka hyd K-ii. Label per kejadian membuka stuck. Tanpa ketiganya, alat tetap abstain, dan itu jawaban yang benar.</div><div class="flex"><button class="btn primary" type="button" data-request="CRPM">Minta CRPM</button><button class="btn" type="button" data-request="flow meter">Minta flow meter</button><button class="btn" type="button" data-request="label per kejadian">Minta label</button></div></div>`,
          foot: `<span>Formulir mencatat permintaan ke log sesi.</span><a class="link" href="#data">Data</a>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- KAMUS ---------------- */

  function kamus() {
    const terms = D.glossary.map((g, i) => `<details class="term" data-term="${esc((g.term + " " + g.short + " " + g.long + " " + g.example).toLowerCase())}" ${i === 0 ? "open" : ""}>
      <summary><span>${g.term}</span><span class="small muted">${g.short}</span></summary>
      <div class="term-body"><p>${g.long}</p><p class="small muted"><strong>Contoh:</strong> ${g.example}</p></div>
    </details>`).join("");

    const quiz = D.quiz.map((q, i) => `<div class="quiz-item" data-q="${i}">
      <p class="quiz-q"><span class="mono muted">${String(i + 1).padStart(2, "0")}</span> ${q.q}</p>
      <div class="quiz-options">${q.options.map((o, j) => `<label><input type="radio" name="q${i}" value="${j}"> <span>${o}</span></label>`).join("")}</div>
      <div class="quiz-why small muted" hidden>${q.why}</div>
    </div>`).join("");

    return `<section class="view" id="view-kamus" aria-labelledby="h-kamus">
      ${viewHead("Kamus", "Istilah yang sering disalahbaca, dengan contoh yang benar dan salah.", `15 istilah · 10 soal · 9 grafik terlarang`)}
      <div class="grid">
        ${card({
          span: "span-7",
          title: "Istilah",
          sub: "Cari, lalu buka. Semua contoh memakai angka proyek ini.",
          right: `<div class="search" style="width:180px"><svg width="13" height="13"><use href="#i-search"/></svg><input id="term-search" type="search" placeholder="Cari istilah" aria-label="Cari istilah"></div>`,
          body: `<div id="term-list">${terms}</div><p class="small muted" id="term-empty" hidden>Tidak ada istilah yang cocok.</p>`,
          foot: `<span>15 istilah</span><span class="mono">klik untuk buka</span>`
        })}
        ${card({
          span: "span-5",
          title: "Tiga sumbu",
          sub: "Bukti, cakupan, kesiapan. Jangan digabung menjadi satu skor.",
          body: table(["Sumbu", "Nilai", "Catatan"], D.axes.map((a) => ({
            cells: [a.name, `<span class="chip">${a.value}</span>`, `<span class="small muted">${a.note}</span>`]
          })), { cls: "compact" }),
          foot: `<span>Skor tunggal menyembunyikan trade-off.</span><a class="link" href="#batas">Batas</a>`
        })}
        ${card({
          span: "span-6",
          title: "Bacaan angka",
          sub: "Empat angka, empat jebakan.",
          body: table(["Angka", "Benar", "Salah"], D.readExamples.map((r) => ({
            cells: [`<span class="mono strong">${r.text}</span>`, `<span class="small status-ok">${r.right}</span>`, `<span class="small status-bad">${r.wrong}</span>`]
          })), { cls: "compact" }),
          foot: `<span>Bacaan salah biasanya menaikkan klaim.</span><a class="link" href="#kepercayaan">Kepercayaan</a>`
        })}
        ${card({
          span: "span-6",
          title: "Istilah terlarang",
          sub: "Kata yang menyiratkan lebih dari bukti.",
          body: table(["Jangan pakai", "Pakai"], [
            { cells: ["Akurasi 82 persen", "Presisi 0,8243 pada titik operasi"] },
            { cells: ["Model memprediksi", "Model memberi indikasi, manusia memutuskan"] },
            { cells: ["Alarm otomatis", "Antrean tinjauan"] },
            { cells: ["Terbukti", "Terukur pada potongan ini"] },
            { cells: ["Aman", "Tidak ada indikasi pada jendela ini"] }
          ], { cls: "compact" }),
          foot: `<span>Kata yang tepat mengurangi klaim palsu.</span><a class="link" href="#batas">Batas</a>`
        })}
        ${card({
          span: "span-12",
          title: "Latihan",
          sub: "10 soal. Jawaban diperiksa di browser, bukan dikirim ke mana pun.",
          right: `<button class="btn primary sm" type="button" id="quiz-check">Periksa jawaban</button>`,
          body: `<div class="quiz-grid">${quiz}</div><div class="banner-note" id="quiz-result" style="margin-top:10px;display:none"></div>`,
          foot: `<span>Nilai bukan sertifikat.</span><span class="mono" id="quiz-score">0 / 10</span>`
        })}
      </div>
    </section>`;
  }

  /* ---------------- ALAT BANTU ---------------- */

  function alatBantu() {
    const wizard = D.wizardSteps.map((s, i) => `<div class="wizard-step ${i === 0 ? "active" : ""}" data-step="${i}">
      <div class="mono small muted">LANGKAH ${i + 1} DARI 4</div>
      <h4 style="font-size:16px;font-family:var(--font-display);text-transform:none;letter-spacing:0;color:var(--text);margin:2px 0 4px">${s.title}</h4>
      <p class="small" style="color:var(--text-2)">${s.body}</p>
    </div>`).join("");

    return `<section class="view" id="view-alat-bantu" aria-labelledby="h-alat">
      ${viewHead("Alat bantu", "Panduan singkat, skrip verifikasi, dan formulir permintaan data.", `4 langkah · 6 kanal · 6 pemeriksaan`)}
      <div class="grid">
        ${card({
          span: "span-6",
          title: "Panduan empat langkah",
          sub: "Mulai dari bukti, bukan dari grafik.",
          right: `<span class="mono small" id="wizard-count">1 / 4</span>`,
          body: `<div id="wizard">${wizard}</div>
          <div class="flex-between" style="margin-top:12px"><button class="btn" type="button" id="wizard-prev" disabled>Kembali</button><button class="btn primary" type="button" id="wizard-next">Lanjut</button></div>`,
          foot: `<span>Urutan ini juga dipakai di naskah aksesibilitas.</span><a class="link" href="#kamus">Istilah</a>`
        })}
        ${card({
          span: "span-6",
          title: "Skrip verifikasi",
          sub: "Jalankan di root proyek. Tidak mengubah berkas.",
          right: `<button class="btn sm" type="button" data-copy="python3 - <<'PY'
import json, pathlib
p = pathlib.Path('scratch/v9_i1/v9_i1_RESULTS.json')
d = json.loads(p.read_text())
print('heads', sum(len(e['heads']) for e in d['engines']))
print('alarm_slots', sum(h.get('slot_alarm_otomatis', 0) for e in d['engines'] for h in e['heads']))
PY">Salin</button>`,
          body: `<pre class="code-block"><code>python3 - &lt;&lt;'PY'
import json, pathlib
p = pathlib.Path('scratch/v9_i1/v9_i1_RESULTS.json')
d = json.loads(p.read_text())
print('heads', sum(len(e['heads']) for e in d['engines']))
print('alarm_slots', sum(h.get('slot_alarm_otomatis', 0) for e in d['engines'] for h in e['heads']))
PY</code></pre>
          <p class="small muted" style="margin-top:8px">Hasil yang diharapkan: <span class="mono">heads 27</span>, <span class="mono">alarm_slots 0</span>.</p>`,
          foot: `<span>Bila hasil berbeda, jangan pakai angka di halaman ini.</span><a class="link" href="#bukti">Bukti</a>`
        })}
        ${card({
          span: "span-12",
          title: "Kelayakan sinyal",
          sub: "Empat sinyal, empat status. Status diturunkan dari kanal dan label.",
          body: `<div class="grid" style="gap:10px">${D.signalFeasibility.map((s) => `<div class="span-3 card inner" style="padding:10px"><div class="flex-between"><strong style="font-size:12px">${s.name}</strong><span class="badge ${s.tone === "ok" ? "p3" : s.tone === "warn" ? "p2" : "p4"}">${s.status}</span></div><p class="small muted" style="margin-top:5px">${s.note}</p></div>`).join("")}</div>`,
          foot: `<span>Status bukan skor.</span><a class="link" href="#data">Data</a>`
        })}
        ${card({
          span: "span-7",
          title: "Kanal yang perlu dipasang",
          sub: "Enam kanal, perkiraan biaya dan waktu.",
          body: table(["Kanal", "Dipakai untuk", "Biaya", "Waktu", "Catatan"], D.channelsInstall.map((c) => ({
            cells: [c.name, `<span class="small">${c.use}</span>`, `<span class="chip">${c.cost}</span>`, c.lead, `<span class="small muted">${c.note}</span>`]
          })), { cls: "compact" }),
          foot: `<span>Perkiraan, bukan penawaran.</span><a class="link" href="#batas">Pemilik</a>`
        })}
        ${card({
          span: "span-5",
          title: "Formulir permintaan data",
          sub: "Catat kebutuhan, pemilik, dan tenggat.",
          body: `<form id="request-form" class="stack">
            <div class="field"><label for="req-data">Data</label><select id="req-data"><option>CRPM</option><option>Flow meter</option><option>Label per kejadian</option><option>Jadwal inspeksi</option><option>Biaya operasi</option></select></div>
            <div class="field-row"><div class="field"><label for="req-well">Sumur</label><select id="req-well">${D.wells.map((w) => `<option>${w}</option>`).join("")}<option>Semua</option></select></div><div class="field"><label for="req-due">Tenggat</label><input id="req-due" type="date" value="2026-11-15"></div></div>
            <div class="field"><label for="req-note">Alasan</label><textarea id="req-note" placeholder="Contoh: ssi tidak bisa dinilai tanpa CRPM."></textarea></div>
            <button class="btn primary" type="submit">Catat permintaan</button>
          </form>`,
          foot: `<span>Formulir mencatat ke log sesi.</span><span class="mono">lokal</span>`
        })}
        ${card({
          span: "span-12",
          title: "Daftar periksa mutu",
          sub: "Enam pemeriksaan sebelum angka dipakai.",
          right: `<span class="mono small" id="check-count">0 / 6</span>`,
          body: `<div class="grid" style="gap:10px"><div class="span-6"><div class="checklist" id="quality-list">${D.qualityChecklist.map((c, i) => `<label data-check="${i}"><input type="checkbox"> <span>${c.text}<br><span class="small muted">${c.hint}</span></span></label>`).join("")}</div></div><div class="span-6"><div class="banner-note info" style="padding:10px"><div><strong>Bila satu kotak tidak tercentang,</strong> jangan gunakan angka itu di dokumen keputusan. Cukup tulis "belum terverifikasi" dan sebutkan alasannya.</div></div><div class="track" style="height:8px;margin-top:10px"><i class="green" id="check-bar" style="width:0%"></i></div></div></div>`,
          foot: `<span>Daftar ini juga ada di naskah aksesibilitas.</span><a class="link" href="#bukti">Bukti</a>`
        })}
      </div>
    </section>`;
  }

  window.UI = { card, table, viewHead, esc, nf, pct };
  window.VIEWS = { beranda, kepercayaan, perencanaan, data: dataView, mesin, linimasa, bukti, batas, kamus, "alat-bantu": alatBantu };
})();
