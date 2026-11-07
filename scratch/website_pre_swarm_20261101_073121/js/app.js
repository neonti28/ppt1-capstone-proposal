/* Router, interaksi, dan keadaan. Tanpa dependensi eksternal. */

(function () {
  const D = window.DATA;
  const viewEl = document.getElementById("view");
  const navLinks = Array.from(document.querySelectorAll("#nav a"));
  const titleEl = document.querySelector(".topbar-title h1");
  const searchEl = document.getElementById("global-search");
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modal-title");
  const modalSub = document.getElementById("modal-sub");
  const modalBody = document.getElementById("modal-body");
  const modalFoot = document.getElementById("modal-foot");
  const toastEl = document.getElementById("toast");
  const stateSelect = document.getElementById("state-select");
  const stateBanner = document.getElementById("state-banner");
  const stateTitle = document.getElementById("state-title");
  const stateDesc = document.getElementById("state-desc");

  const TITLES = {
    beranda: "Ruang keputusan perawatan",
    kepercayaan: "Kepercayaan dan batas",
    perencanaan: "Perencanaan shift",
    data: "Kesiapan data",
    mesin: "Mesin dan kepala",
    linimasa: "Linimasa keputusan",
    bukti: "Bukti dan rujukan",
    batas: "Batas data",
    kamus: "Kamus dan latihan",
    "alat-bantu": "Alat bantu"
  };

  const SUBTITLES = {
    beranda: "Prediksi kegagalan sumur, bukti angka, dan keputusan yang tetap di tangan manusia",
    kepercayaan: "Pita, batas kelas, dan bacaan yang tidak boleh dilebihkan",
    perencanaan: "Antrean, beban, dan titik operasi",
    data: "Kanal, label, dan jendela",
    mesin: "Tujuh mesin, 27 kepala, nol alarm otomatis",
    linimasa: "Kuorum, konflik, dan log keputusan",
    bukti: "Setiap angka membawa sumber",
    batas: "Abstain, Layer B, dan grafik terlarang",
    kamus: "Istilah, contoh, dan latihan",
    "alat-bantu": "Panduan, skrip, dan formulir"
  };

  let current = "beranda";
  let lastFocus = null;
  let toastTimer = null;
  let wizardStep = 0;

  const requests = (() => {
    try { return JSON.parse(sessionStorage.getItem("volve.requests") || "[]"); }
    catch { return []; }
  })();

  function routeFromHash() {
    const h = location.hash.replace(/^#/, "");
    return window.VIEWS[h] ? h : "beranda";
  }

  function render(route) {
    current = route;
    viewEl.innerHTML = window.VIEWS[route]();
    const section = viewEl.firstElementChild;
    if (section) section.classList.add("active");
    navLinks.forEach((a) => {
      if (a.dataset.route === route) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
    titleEl.textContent = TITLES[route] || TITLES.beranda;
    const sub = document.querySelector(".topbar-title p");
    if (sub) sub.textContent = SUBTITLES[route] || SUBTITLES.beranda;
    document.title = `${TITLES[route] || "Volve Advisory"} · Volve Advisory`;
    searchEl.value = "";
    clearSearch();
    window.scrollTo({ top: 0, behavior: "auto" });
    bindView(route);
  }

  function navigate(route, replace) {
    if (!window.VIEWS[route]) route = "beranda";
    if (replace) history.replaceState(null, "", `#${route}`);
    else location.hash = route;
    if (route !== current) render(route);
  }

  /* ---------- Search ---------- */

  function clearSearch() {
    const active = document.querySelector(".view.active");
    if (!active) return;
    active.querySelectorAll(".card.hit").forEach((c) => c.classList.remove("hit"));
    active.querySelectorAll(".card.hide").forEach((c) => c.classList.remove("hide"));
    const note = active.querySelector(".search-note");
    if (note) note.classList.remove("show");
  }

  const ALIASES = {
    hyd: ["hidraulik", "hidrolik"],
    vib: ["getaran", "vibrasi"],
    shk: ["kejut", "shock"],
    ssi: ["ssi", "sand"],
    stuck: ["terjepit", "macet"],
    bit_wear: ["aus bit", "mata bor"],
    tool_wear: ["aus alat"],
    tk: ["tk-"]
  };

  function applySearch(q) {
    const active = document.querySelector(".view.active");
    if (!active) return;
    const cards = Array.from(active.querySelectorAll(".grid > .card, .hscroll > .card"))
      .filter((c) => !c.parentElement.closest(".card"));
    const needle = q.trim().toLowerCase();
    const terms = [needle].concat(ALIASES[needle] || []);
    let hits = 0;
    cards.forEach((c) => {
      const hay = c.textContent.toLowerCase();
      const hit = !needle || terms.some((t) => hay.includes(t));
      c.classList.toggle("hide", !!needle && !hit);
      c.classList.toggle("hit", !!needle && hit);
      if (hit) hits += 1;
    });
    let note = active.querySelector(".search-note");
    if (!note) {
      note = document.createElement("div");
      note.className = "search-note";
      const head = active.querySelector(".view-head");
      if (head) head.after(note);
    }
    note.classList.toggle("show", !!needle);
    note.innerHTML = needle
      ? `<svg width="12" height="12"><use href="#i-search"/></svg> ${hits} kartu cocok untuk <span class="mono">"${escapeHtml(q.trim())}"</span> <button class="link" type="button" data-clear-search>Bersihkan</button>`
      : "";
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  /* ---------- Toast ---------- */

  function toast(msg, bad) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.toggle("bad", !!bad);
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("show"), 3200);
  }

  /* ---------- Modal ---------- */

  function openModal(title, sub, body, foot) {
    lastFocus = document.activeElement;
    modalTitle.textContent = title;
    modalSub.textContent = sub || "";
    modalBody.innerHTML = body || "";
    modalFoot.innerHTML = foot || `<button class="btn" type="button" data-modal-close>Tutup</button>`;
    modal.hidden = false;
    document.body.classList.add("no-scroll");
    const close = document.getElementById("modal-close");
    if (close) close.focus();
  }

  function closeModal() {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.classList.remove("no-scroll");
    modalBody.innerHTML = "";
    modalFoot.innerHTML = "";
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
    lastFocus = null;
  }

  function queueById(id) {
    return D.queue.find((q) => q.id === id) || D.queue.find((q) => q.code === id);
  }

  function openQueue(id) {
    const q = queueById(id);
    if (!q) return;
    const pita = q.pita ? `P${q.pita}` : "Abstain";
    openModal(q.claim, `${q.id} · ${q.well} · jendela ${q.window}`, `
      <div class="stat-grid">
        <div class="stat"><div class="k">Keyakinan</div><div class="v" style="font-size:24px">${fmt(q.conf, 2)}</div></div>
        <div class="stat"><div class="k">Pita</div><div class="v" style="font-size:24px">${pita}</div></div>
        <div class="stat"><div class="k">Kepala</div><div class="v" style="font-size:24px">${q.heads}</div></div>
        <div class="stat"><div class="k">Umur</div><div class="v" style="font-size:24px">${q.age}</div></div>
      </div>
      <dl class="kv">
        <dt>Status</dt><dd>${q.status}</dd>
        <dt>Sinyal</dt><dd class="mono">${q.signal}</dd>
        <dt>Lead</dt><dd class="mono">${q.lead}</dd>
        <dt>Biaya tinjau</dt><dd class="mono">${q.minutes} menit</dd>
        <dt>Catatan</dt><dd>${q.note}</dd>
      </dl>
      <div class="banner-note info"><div><strong>Batas:</strong> baris ini adalah usulan tinjauan, bukan perintah. Menutup baris berarti sudah ditinjau, bukan berarti masalah selesai.</div></div>
    `, `
      <button class="btn" type="button" data-modal-close>Batal</button>
      <button class="btn" type="button" data-modal-action="defer" data-id="${q.id}">Tunda</button>
      <button class="btn primary" type="button" data-modal-action="close-row" data-id="${q.id}">Tutup baris</button>
    `);
  }

  function openClaim(code) {
    const d = D.damages.find((x) => x.code === code);
    if (!d) return;
    openModal(d.name, d.task, `
      <div class="stat-grid">
        <div class="stat"><div class="k">K_segmen</div><div class="v" style="font-size:24px">${d.k}</div></div>
        <div class="stat"><div class="k">Batas kelas</div><div class="v" style="font-size:24px">${d.cap}</div></div>
        <div class="stat"><div class="k">Pita</div><div class="v" style="font-size:24px">${d.pita ? "P" + d.pita : "Abstain"}</div></div>
        <div class="stat"><div class="k">Bobot</div><div class="v" style="font-size:24px">${d.weight}</div></div>
      </div>
      <p class="small" style="color:var(--text-2)">${d.evidence}</p>
      <div class="banner-note warn"><div><strong>Batas:</strong> ${d.limit}</div></div>
      <div class="banner-note"><div><strong>Suara dewan:</strong> ${d.vote}. Batas kelas tidak bisa dinaikkan dengan skor.</div></div>
    `);
  }

  function openDecision() {
    openModal("Catat keputusan", "Log sesi ini, bukan audit resmi", `
      <form id="decision-form" class="stack">
        <div class="field"><label for="dec-claim">Klaim</label><select id="dec-claim">${D.queue.map((q) => `<option value="${q.id}">${q.id} · ${q.claim} · ${q.well}</option>`).join("")}</select></div>
        <div class="field"><label for="dec-action">Tindakan</label><select id="dec-action"><option>Tinjau</option><option>Tunda</option><option>Pantau</option><option>Prioritas</option></select></div>
        <div class="field"><label for="dec-reason">Alasan</label><textarea id="dec-reason" required placeholder="Tulis alasan yang bisa dibaca shift berikutnya."></textarea></div>
        <button class="btn primary" type="submit">Simpan keputusan</button>
      </form>
    `, "");
  }

  function openRequest(dataName) {
    const options = ["CRPM", "Flow meter", "Label per kejadian", "Jadwal inspeksi", "Biaya operasi"];
    openModal("Minta data", dataName ? `Kebutuhan: ${dataName}` : "Catat kebutuhan data", `
      <form id="request-modal-form" class="stack">
        <div class="field"><label for="reqm-data">Data</label><select id="reqm-data">${options.map((o) => `<option${o === dataName ? " selected" : ""}>${o}</option>`).join("")}</select></div>
        <div class="field-row">
          <div class="field"><label for="reqm-well">Sumur</label><select id="reqm-well">${D.wells.map((w) => `<option>${w}</option>`).join("")}<option>Semua</option></select></div>
          <div class="field"><label for="reqm-due">Tenggat</label><input id="reqm-due" type="date" value="2026-11-15"></div>
        </div>
        <div class="field"><label for="reqm-note">Alasan</label><textarea id="reqm-note" placeholder="Contoh: ssi tidak bisa dinilai tanpa CRPM."></textarea></div>
        <button class="btn primary" type="submit">Catat permintaan</button>
      </form>
    `, "");
  }

  function openHelp() {
    openModal("Bantuan dan legenda", "Cara membaca, keadaan data, dan pintasan", `
      <div class="stack">
        <div><h4>Pita</h4><div class="stack-sm">
          <div class="flex-between"><span class="badge p1">P1</span><span class="small muted">Tidak ada indikasi</span></div>
          <div class="flex-between"><span class="badge p2">P2</span><span class="small muted">Indikasi lemah</span></div>
          <div class="flex-between"><span class="badge p3">P3</span><span class="small muted">Perlu tinjauan</span></div>
          <div class="flex-between"><span class="badge p4">P4</span><span class="small muted">Keyakinan kuat</span></div>
          <div class="flex-between"><span class="badge p5">P5</span><span class="small muted">Keyakinan tinggi</span></div>
        </div></div>
        <div><h4>Provenance</h4><div class="stack-sm">
          <div class="flex-between"><span class="prov prov-ok">TERUKUR</span><span class="small muted">Diukur langsung</span></div>
          <div class="flex-between"><span class="prov prov-note">TURUNAN</span><span class="small muted">Dihitung dari angka lain</span></div>
          <div class="flex-between"><span class="prov prov-block">BELUM KUTIP</span><span class="small muted">Belum ada rujukan</span></div>
        </div></div>
        <div><h4>Keadaan data</h4><p class="small muted">Pilih di kaki halaman. Normal, memuat, kosong, dan galat adalah keadaan yang dirancang, bukan halaman rusak. Pada keadaan kosong, konten disembunyikan dan banner menjelaskan bahwa tidak ada baris.</p></div>
        <div><h4>Pintasan</h4><p class="small muted"><span class="mono">/</span> fokus ke pencarian. <span class="mono">Esc</span> menutup dialog.</p></div>
        <div class="banner-note info"><div><strong>Tema gelap dipilih</strong> karena ini alat kontrol industri yang dipakai di ruang redup. Bukan default gaya, dan bukan alasan untuk mengorbankan kontras.</div></div>
      </div>
    `);
  }

  /* ---------- Actions ---------- */

  function setQueueStatus(id, status) {
    const q = queueById(id);
    if (!q) return;
    q.status = status;
    closeModal();
    render(current);
    toast(status === "Ditunda" ? "Baris ditunda. Alasan dicatat di modal." : "Baris ditutup sebagai sudah ditinjau.");
  }

  function copyText(text) {
    const done = () => toast("Rujukan disalin.");
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
    } else {
      fallbackCopy(text, done);
    }
  }

  function fallbackCopy(text, done) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); done(); }
    catch { toast("Gagal menyalin. Pilih teks secara manual.", true); }
    document.body.removeChild(ta);
  }

  function fmt(n, d) {
    return Number(n).toLocaleString("id-ID", { minimumFractionDigits: d, maximumFractionDigits: d });
  }

  function setState(value) {
    document.body.dataset.state = value;
    const map = {
      loading: ["Memuat", "Data sedang dimuat. Kartu ditampilkan redup sampai selesai."],
      empty: ["Kosong", "Tidak ada baris pada potongan ini. Ini ketiadaan data, bukan nilai nol."],
      error: ["Galat", "Gagal memuat berkas. Coba lagi, atau buka Batas data untuk melihat penyebab."]
    };
    if (value === "normal") {
      stateBanner.setAttribute("aria-hidden", "true");
    } else {
      stateBanner.removeAttribute("aria-hidden");
      stateTitle.textContent = map[value][0];
      stateDesc.textContent = map[value][1];
    }
  }

  /* ---------- Per-view bindings ---------- */

  function bindView(route) {
    if (route === "perencanaan") {
      const ids = ["calc-checks", "calc-minutes", "calc-shifts"];
      ids.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.addEventListener("input", updateCalc);
      });
      updateCalc();
    }
    if (route === "kamus") {
      const input = document.getElementById("term-search");
      if (input) {
        input.addEventListener("input", () => {
          const q = input.value.trim().toLowerCase();
          let shown = 0;
          document.querySelectorAll("#term-list .term").forEach((el) => {
            const hit = !q || (el.dataset.term || "").includes(q);
            el.hidden = !hit;
            if (hit) shown += 1;
          });
          const empty = document.getElementById("term-empty");
          if (empty) empty.hidden = shown > 0;
        });
      }
    }
    if (route === "alat-bantu") {
      wizardStep = 0;
      showWizard(0);
      const list = document.getElementById("quality-list");
      if (list) {
        list.addEventListener("change", updateChecks);
        updateChecks();
      }
    }
  }

  function updateCalc() {
    const checks = Number(document.getElementById("calc-checks")?.value || 0);
    const minutes = Number(document.getElementById("calc-minutes")?.value || 0);
    const shifts = Number(document.getElementById("calc-shifts")?.value || 0);
    const total = Math.max(0, checks * minutes * shifts);
    const outMin = document.getElementById("calc-out-min");
    const outHour = document.getElementById("calc-out-hour");
    if (outMin) outMin.textContent = fmt(total, 0);
    if (outHour) outHour.textContent = fmt(total / 60, 1);
  }

  function showWizard(n) {
    wizardStep = Math.max(0, Math.min(3, n));
    document.querySelectorAll(".wizard-step").forEach((el) => {
      el.classList.toggle("active", Number(el.dataset.step) === wizardStep);
    });
    const count = document.getElementById("wizard-count");
    if (count) count.textContent = `${wizardStep + 1} / 4`;
    const prev = document.getElementById("wizard-prev");
    const next = document.getElementById("wizard-next");
    if (prev) prev.disabled = wizardStep === 0;
    if (next) next.textContent = wizardStep === 3 ? "Selesai" : "Lanjut";
  }

  function updateChecks() {
    const boxes = Array.from(document.querySelectorAll("#quality-list input[type=checkbox]"));
    const n = boxes.filter((b) => b.checked).length;
    const count = document.getElementById("check-count");
    const bar = document.getElementById("check-bar");
    if (count) count.textContent = `${n} / ${boxes.length}`;
    if (bar) bar.style.width = `${boxes.length ? (n / boxes.length) * 100 : 0}%`;
    boxes.forEach((b) => b.closest("label")?.classList.toggle("done", b.checked));
  }

  function checkQuiz() {
    let score = 0;
    D.quiz.forEach((q, i) => {
      const item = document.querySelector(`.quiz-item[data-q="${i}"]`);
      if (!item) return;
      const selected = item.querySelector(`input[name="q${i}"]:checked`);
      const why = item.querySelector(".quiz-why");
      item.classList.remove("correct", "wrong");
      if (selected && Number(selected.value) === q.answer) {
        score += 1;
        item.classList.add("correct");
      } else {
        item.classList.add("wrong");
      }
      if (why) why.hidden = false;
    });
    const result = document.getElementById("quiz-result");
    const scoreEl = document.getElementById("quiz-score");
    if (scoreEl) scoreEl.textContent = `${score} / 10`;
    if (result) {
      result.style.display = "flex";
      result.className = "banner-note " + (score >= 8 ? "" : "bad");
      result.innerHTML = `<div><strong>${score} dari 10 benar.</strong> ${score >= 8 ? "Bacaan sudah kuat. Tetap cek sumber sebelum memakai angka." : "Baca ulang istilah yang salah, lalu coba lagi. Jangan menebak."}</div>`;
    }
  }

  /* ---------- Global events ---------- */

  document.addEventListener("click", (e) => {
    const copy = e.target.closest("[data-copy]");
    if (copy) { e.preventDefault(); copyText(copy.dataset.copy); return; }

    const clear = e.target.closest("[data-clear-search]");
    if (clear) { e.preventDefault(); searchEl.value = ""; applySearch(""); searchEl.focus(); return; }

    const qbtn = e.target.closest("[data-queue]");
    if (qbtn) { e.preventDefault(); openQueue(qbtn.dataset.queue); return; }

    const defer = e.target.closest("[data-defer]");
    if (defer) { e.preventDefault(); setQueueStatus(defer.dataset.defer, "Ditunda"); return; }

    const row = e.target.closest("[data-queue-row]");
    if (row) { e.preventDefault(); openQueue(row.dataset.queueRow); return; }

    const claim = e.target.closest("[data-claim]");
    if (claim) { e.preventDefault(); openClaim(claim.dataset.claim); return; }

    const req = e.target.closest("[data-request]");
    if (req) { e.preventDefault(); openRequest(req.dataset.request); return; }

    const dec = e.target.closest("[data-decide]");
    if (dec) { e.preventDefault(); openDecision(); return; }

    const mode = e.target.closest("[data-mode]");
    if (mode) {
      e.preventDefault();
      const i = Number(mode.dataset.mode);
      const m = D.hydModes[i];
      if (!m) return;
      document.querySelectorAll("#mode-seg button").forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.mode) === i)));
      const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
      set("op-fp", fmt(m.fp, 0));
      set("op-p", fmt(m.p, 4));
      set("op-r", fmt(m.r, 4));
      set("op-far", fmt(m.far, 4));
      set("op-note", m.note);
      set("op-folds", `${m.folds} memenuhi FAR dan recall`);
      return;
    }

    const modalAction = e.target.closest("[data-modal-action]");
    if (modalAction) {
      e.preventDefault();
      if (modalAction.dataset.modalAction === "close-row") setQueueStatus(modalAction.dataset.id, "Ditinjau");
      if (modalAction.dataset.modalAction === "defer") setQueueStatus(modalAction.dataset.id, "Ditunda");
      return;
    }

    if (e.target.closest("[data-modal-close]")) { e.preventDefault(); closeModal(); return; }
    if (e.target.id === "modal") { closeModal(); return; }

    if (e.target.closest("#help-btn")) { e.preventDefault(); openHelp(); return; }
    if (e.target.closest("#state-reset")) { e.preventDefault(); if (stateSelect) stateSelect.value = "normal"; setState("normal"); return; }
    if (e.target.closest("#modal-close")) { e.preventDefault(); closeModal(); return; }
    if (e.target.closest("#quiz-check")) { e.preventDefault(); checkQuiz(); return; }
    if (e.target.closest("#wizard-prev")) { e.preventDefault(); showWizard(wizardStep - 1); return; }
    if (e.target.closest("#wizard-next")) { e.preventDefault(); showWizard(wizardStep + 1); return; }
  });

  document.addEventListener("submit", (e) => {
    if (e.target.id === "decision-form") {
      e.preventDefault();
      const claim = document.getElementById("dec-claim").value;
      const action = document.getElementById("dec-action").value;
      const reason = document.getElementById("dec-reason").value.trim();
      if (!reason) { toast("Alasan wajib diisi.", true); return; }
      const q = queueById(claim);
      const now = new Date();
      const time = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
      D.decisions.unshift({ time, actor: "Sesi ini", claim: q ? `${q.claim} ${q.well}` : claim, action, reason });
      closeModal();
      render(current);
      toast("Keputusan dicatat di log sesi.");
      return;
    }

    if (e.target.id === "request-form" || e.target.id === "request-modal-form") {
      e.preventDefault();
      const prefix = e.target.id === "request-form" ? "req" : "reqm";
      const data = document.getElementById(`${prefix}-data`)?.value || "";
      const well = document.getElementById(`${prefix}-well`)?.value || "";
      const due = document.getElementById(`${prefix}-due`)?.value || "";
      const note = document.getElementById(`${prefix}-note`)?.value || "";
      requests.push({ data, well, due, note, at: new Date().toISOString() });
      try { sessionStorage.setItem("volve.requests", JSON.stringify(requests)); } catch { /* session storage may be full */ }
      closeModal();
      toast(`Permintaan dicatat: ${data} · ${well} · ${due}`);
      return;
    }
  });

  searchEl.addEventListener("input", () => applySearch(searchEl.value));

  stateSelect.addEventListener("change", () => setState(stateSelect.value));

  window.addEventListener("hashchange", () => {
    const route = routeFromHash();
    if (route !== current) render(route);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeModal(); return; }
    if (e.key === "Tab" && !modal.hidden) {
      const focusable = Array.from(modal.querySelectorAll("a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex='-1'])"))
        .filter((el) => el.offsetParent !== null);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      return;
    }
    if (e.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      searchEl.focus();
    }
  });

  /* ---------- Boot ---------- */

  const initial = routeFromHash();
  if (!location.hash) history.replaceState(null, "", "#beranda");
  render(initial);
})();
