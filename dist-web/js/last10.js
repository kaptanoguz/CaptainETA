/* CaptainETA — Last 10 Port view helper (uses existing #viewLast10) */
(function(){
  if(window.__last10Patched) return;
  window.__last10Patched = true;

  const PORT_LOCODE = {
    "Istanbul, Turkey":"TRIST","Mersin, Turkey":"TRMER","Piraeus, Greece":"GRPIR",
    "Genoa, Italy":"ITGOA","Rotterdam, Netherlands":"NLRTM","Antwerp, Belgium":"BEANR",
    "Hamburg, Germany":"DEHAM","London, UK":"GBLON","Copenhagen, Denmark":"DKCPH",
    "Sydney, Australia":"AUSYD","New York, USA":"USNYC","Singapore, Singapore":"SGSIN",
    "Dubai, UAE":"AEDXB","Tokyo, Japan":"JPTYO","Shanghai, China":"CNSHA","Hong Kong, China":"HKHKG",
    "Barcelona, Spain":"ESBCN","Valencia, Spain":"ESVLC","Marseille, France":"FRMRS",
    "Le Havre, France":"FRLEH","Lisbon, Portugal":"PTLIS","Gibraltar":"GIGIB",
    "Casablanca, Morocco":"MACAS","Algiers, Algeria":"DZALG","Tunis, Tunisia":"TNTUN",
    "Sfax, Tunisia":"TNSFA","Trieste, Italy":"ITTRS","Venice, Italy":"ITVCE"
  };

  const PORT_SECURITY = {
    "Istanbul, Turkey":1,"Mersin, Turkey":1,"Piraeus, Greece":1,"Genoa, Italy":1,
    "Rotterdam, Netherlands":1,"Antwerp, Belgium":1,"Hamburg, Germany":1,"London, UK":1,
    "Copenhagen, Denmark":1,"Sydney, Australia":1,"New York, USA":1,"Singapore, Singapore":1,
    "Dubai, UAE":1,"Tokyo, Japan":1,"Shanghai, China":1,"Hong Kong, China":1,
    "Barcelona, Spain":1,"Valencia, Spain":1,"Marseille, France":1,"Le Havre, France":1,
    "Lisbon, Portugal":1,"Gibraltar":2,"Casablanca, Morocco":2,"Algiers, Algeria":2,
    "Tunis, Tunisia":2,"Sfax, Tunisia":2,"Trieste, Italy":1,"Venice, Italy":1
  };

  function securityPort(n){
    const lv = PORT_SECURITY[n];
    if (lv == null) return '—';
    const color = lv === 1 ? 'var(--accent)' : 'var(--highlight)';
    return '<span style="color:' + color + ';font-weight:700">L' + lv + '</span>';
  }

  function loadSecOverrides(){
    try{ const v=localStorage.getItem('ceta_sec'); return v?JSON.parse(v):{}; }catch(e){ return {}; }
  }
  function saveSecOverride(port,level){
    const cur=loadSecOverrides(); cur[port]=level;
    try{ localStorage.setItem('ceta_sec',JSON.stringify(cur)); }catch(e){}
  }
  function effectiveSec(port){
    const o=loadSecOverrides(); if(o && o[port]) return o[port];
    const lv=PORT_SECURITY[port]; return lv == null ? null : lv;
  }
  function secBadge(port){
    const lv=effectiveSec(port);
    if (lv == null) return '—';
    const color = lv === 1 ? 'var(--accent)' : 'var(--highlight)';
    return '<span style="color:' + color + ';font-weight:700">L' + lv + '</span>';
  }
  function secSelect(port){
    const cur=effectiveSec(port);
    const opts=[1,2,3].map(lv=>'<option value="'+lv+'"'+(cur===lv?' selected':'')+'>SL '+lv+'</option>').join('');
    return '<select onchange="window._setPortSec&&window._setPortSec(\''+port.replace(/'/g,"\\'")+'\',this.value)" style="background:var(--surface);color:var(--text-main);border:1px solid var(--border);border-radius:4px;padding:2px 6px;font-size:0.78rem">'+opts+'</select>';
  }

  function locode(n){ return PORT_LOCODE[n] || '—'; }

  function flag(n){
    const lc = locode(n);
    if (!lc || lc === '—') return '';
    const c = lc.slice(0, 2).toUpperCase();
    const map = {TR:'🇹🇷',GR:'🇬🇷',IT:'🇮🇹',ES:'🇪🇸',FR:'🇫🇷',DE:'🇩🇪',NL:'🇳🇱',BE:'🇧🇪',GB:'🇬🇧',JP:'🇯🇵',CN:'🇨🇳',SG:'🇸🇬',AE:'🇦🇪',US:'🇺🇸',AU:'🇦🇺',GR:'🇬🇷'};
    return map[c] || '';
  }

  function esc(s){
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderLast10(){
    const wrap = document.getElementById('last10Wrap');
    if (!wrap) return;
    const v = sortVoyages(getVoyages());
    if (!v.length){
      wrap.innerHTML = '<p style="text-align:center;padding:2rem;color:var(--text-muted)">Henüz secured voyage yok.</p>';
      return;
    }
    const count = {}, src = {};
    v.forEach(x => {
      [x.loadPort, x.dischPort].forEach(p => {
        if (!p || p === 'N/A') return;
        count[p] = (count[p] || 0) + 1;
        if (!src[p]) src[p] = x;
      });
    });
    const ports = Object.keys(count).sort((a, b) => {
      if (count[b] !== count[a]) return count[b] - count[a];
      return (src[b].departure || '') < (src[a].departure || '') ? 1 : -1;
    }).slice(0, 10);

    let h = '<table><thead><tr><th>#</th><th>Port</th><th>LOCODE</th><th>Flag</th><th>Security</th><th>Visits</th><th>Last Voyage</th><th>Last Dep</th></tr></thead><tbody>';
    ports.forEach((p, i) => {
      const s = src[p];
      const dep = (s && s.departure || '—').replace('T', ' ');
      h += '<tr><td>' + (i + 1) + '</td><td>' + esc(p) + '</td>' +
           '<td style="font-family:var(--font-mono);color:var(--accent)">' + locode(p) + '</td>' +
           '<td style="font-size:1.1rem">' + flag(p) + '</td>' +
           '<td>' + secSelect(p) + '</td>' +
           '<td>' + (count[p] || 0) + '</td>' +
           '<td>' + esc(s ? s.voyageNo : '—') + '</td>' +
           '<td style="font-family:var(--font-mono);font-size:0.78rem">' + esc(dep) + '</td></tr>';
    });
    h += '</tbody></table>';
    h += '<div style="margin-top:0.75rem;color:var(--text-muted);font-size:0.75rem">Toplam ' + v.length + ' secured voyage, ' + ports.length + ' liman gösteriliyor.</div>';
    wrap.innerHTML = h;
  }

  function useLast10Ports(){
    const wrap = document.getElementById('last10Wrap');
    const td = wrap && wrap.querySelector('tbody tr td:nth-child(2)');
    if (!td){ alert('Henüz port yok'); return; }
    const p = td.textContent.trim();
    const ld = document.getElementById('loadPort');
    const di = document.getElementById('dischPort');
    if (!ld.value) ld.value = p;
    else if (!di.value) di.value = p;
    else di.value = p;
    if (typeof tryAutoDist === 'function') tryAutoDist();
    if (typeof calculate === 'function') calculate();
    switchView('calc');
  }

  function exportLast10PDF(){
    const wrap = document.getElementById('last10Wrap');
    if (!wrap) return;
    const rows = [...wrap.querySelectorAll('tbody tr')].map(tr => [...tr.querySelectorAll('td')].map(td => td.textContent.trim()));
    if (!rows.length) return;
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4');
    doc.text('Captain ETA - Recent Ports', 14, 15);
    doc.autoTable({ head: [['#', 'Port', 'LOCODE', 'Flag', 'Security', 'Visits', 'Last Voyage', 'Last Dep']], body: rows });
    doc.save('last10-ports.pdf');
  }

  function exportLast10XLSX(){
    const wrap = document.getElementById('last10Wrap');
    if (!wrap) return;
    const rows = [...wrap.querySelectorAll('tbody tr')].map(tr => {
      const cells = [...tr.querySelectorAll('td')].map(td => td.textContent.trim());
      return { no: cells[0], port: cells[1], locode: cells[2], flag: cells[3], security: cells[4], visits: cells[5], lastVoyage: cells[6], lastDep: cells[7] };
    });
    if (!rows.length) return;
    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Last10');
    XLSX.writeFile(wb, 'last10-ports.xlsx');
  }

  const origSwitch = window.switchView;
  window.switchView = function(v){
    if (v === 'last10'){
      document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
      const view = document.getElementById('viewLast10');
      if (view) view.classList.add('active');
      const navs = document.querySelectorAll('.nav-btn');
      const idx = [...navs].findIndex(b => b.getAttribute('onclick') && b.getAttribute('onclick').includes('last10'));
      if (idx >= 0) navs[idx].classList.add('active');
      renderLast10();
      return;
    }
    if (origSwitch) origSwitch(v);
  };

  window.renderLast10 = renderLast10;
  window.useLast10Ports = useLast10Ports;
  window.exportLast10PDF = exportLast10PDF;
  window.exportLast10XLSX = exportLast10XLSX;
})();
