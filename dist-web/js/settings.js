/* CaptainETA settings: theme, lang, wallpaper */
(function(){
  if (window.__settingsPatched) return;
  window.__settingsPatched = true;

  const THEMES = [
    {id:'default', label:'Default', preview:'linear-gradient(135deg,#0A192F,#64FFDA)'},
    {id:'ocean', label:'Ocean', preview:'linear-gradient(135deg,#072B4F,#00E5FF)'},
    {id:'midnight', label:'Midnight', preview:'linear-gradient(135deg,#0B0C10,#66FCF1)'},
    {id:'forest', label:'Forest', preview:'linear-gradient(135deg,#0E1A0F,#9AE66E)'},
    {id:'sunset', label:'Sunset', preview:'linear-gradient(135deg,#3A1628,#FF9A8B)'},
    {id:'slate', label:'Slate', preview:'linear-gradient(135deg,#1E293B,#38BDF8)'},
    {id:'bright', label:'Bright', preview:'linear-gradient(135deg,#F8FAFC,#0EA5E9)'},
    {id:'charcoal', label:'Charcoal', preview:'linear-gradient(135deg,#1a1a1a,#e0e0e0)'},
    {id:'navylight', label:'Navy / Sky', preview:'linear-gradient(135deg,#0B1D3A,#7DD3FC)'},
    {id:'burgundy', label:'Burgundy', preview:'linear-gradient(135deg,#3B0D1E,#FF8A9B)'},
    {id:'slateblue', label:'Slate Blue', preview:'linear-gradient(135deg,#20233E,#A5B4FC)'},
    {id:'tealstone', label:'Teal / Stone', preview:'linear-gradient(135deg,#0F2A2A,#D6D3D1)'},
    {id:'crimson', label:'Crimson', preview:'linear-gradient(135deg,#2A0A0A,#FCA5A5)'},
    {id:'mintcocoa', label:'Mint / Cocoa', preview:'linear-gradient(135deg,#1A2E1A,#D2B48C)'},
    {id:'sapphire', label:'Sapphire', preview:'linear-gradient(135deg,#0F1C3F,#93C5FD)'},
    {id:'plum', label:'Plum', preview:'linear-gradient(135deg,#2A102A,#E9D5FF)'}
  ];

  const WALLPAPERS = [
    {id:'local', label:'CaptainETA Local', url:'wallpaper.jpg'},
    {id:'__none__', label:'None (solid/theme)', url:'__none__'},
    {id:'#0B1D3A', label:'Navy Solid', url:'#0B1D3A'},
    {id:'#0B0C10', label:'Black Solid', url:'#0B0C10'},
    {id:'#3B3B3B', label:'Gray Solid', url:'#3B3B3B'},
    {id:'#4B5320', label:'Olive Solid', url:'#4B5320'},
    {id:'linear-gradient(135deg,#072B4F,#0B1D3A)', label:'Navy Gradient', url:'linear-gradient(135deg,#072B4F,#0B1D3A)'},
    {id:'linear-gradient(135deg,#0B0C10,#1F2833)', label:'Black Gradient', url:'linear-gradient(135deg,#0B0C10,#1F2833)'},
    {id:'linear-gradient(135deg,#3B3B3B,#6B7280)', label:'Gray Gradient', url:'linear-gradient(135deg,#3B3B3B,#6B7280)'},
    {id:'linear-gradient(135deg,#4B5320,#6B8E23)', label:'Olive Gradient', url:'linear-gradient(135deg,#4B5320,#6B8E23)'},
    {id:'https://images.unsplash.com/photo-1500917293891-34237746d88a?q=80&w=3840&auto=format&fit=crop', label:'Calm Sea', url:'https://images.unsplash.com/photo-1500917293891-34237746d88a?q=80&w=3840&auto=format&fit=crop'}
  ];

  const I18N = {
    en: {
      settings: 'Settings',
      theme: 'Theme',
      wallpaper: 'Wallpaper',
      close: 'Close',
      lang: 'Lang',
      recentPorts: 'Recent Ports',
      useOnForm: 'Use on form',
      savedVoyages: 'Saved Voyages',
      voyagePlanning: 'Voyage Planning',
      last10Port: 'Last 10 Port'
    },
    tr: {
      settings: 'Ayarlar',
      theme: 'Tema',
      wallpaper: 'Duvar kağıdı',
      close: 'Kapat',
      lang: 'Dil',
      recentPorts: 'Son Limanlar',
      useOnForm: 'Forma ekle',
      savedVoyages: 'Kayıtlı Seferler',
      voyagePlanning: 'Sefer Planlama',
      last10Port: 'Son 10 Liman'
    }
  };

  const storage = {
    get(k,d){ try{ const v=localStorage.getItem('ceta_'+k); return v ? v : JSON.stringify(d); }catch(e){ return JSON.stringify(d); } },
    set(k,v){ try{ localStorage.setItem('ceta_'+k, JSON.stringify(v)); }catch(e){} }
  };

  function applyTheme(id){
    const el=document.documentElement;
    if(!id || id==='default') el.removeAttribute('data-theme');
    else el.setAttribute('data-theme', String(id));
    storage.set('theme', id || 'default');
    document.querySelectorAll('.theme-swatch').forEach(b=>b.classList.toggle('active',String(b.dataset.theme)===(id||'default')));
  }
  function applyLang(l){
    document.documentElement.setAttribute('data-lang', String(l));
    storage.set('lang', String(l));
    document.querySelectorAll('.lang-btn').forEach(b=>b.classList.toggle('active',String(b.dataset.lang)===String(l)));
    dispatchLang(l);
  }
  function applyWallpaper(src){
    const val = !src || src === '__none__' ? 'none' : (src.startsWith('#') || src.startsWith('linear-gradient') ? src : 'url(' + src + ')');
    document.body.style.setProperty('--wallpaper', val);
    storage.set('wall', src || '');
    document.querySelectorAll('.wp-btn').forEach(b=>b.classList.toggle('active',String(b.dataset.src)===(src||'__none__')));
  }

  function dispatchLang(l){
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = String(el.getAttribute('data-i18n'));
      if (I18N[l] && I18N[l][key]) {
        if (el.tagName === 'INPUT' && el.type === 'submit') el.value = I18N[l][key];
        else el.textContent = I18N[l][key];
      }
    });
  }

  function tagStaticUI(l){
    const map = I18N[l] || I18N.en;
    const pairs = [
      ['.nav-btn[onclick*="calc"]', 'voyagePlanning'],
      ['.nav-btn[onclick*="saved"]', 'savedVoyages'],
      ['.nav-btn[onclick*="last10"]', 'last10Port'],
      ['.panel-title', null]
    ];
    pairs.forEach(([sel, key]) => {
      document.querySelectorAll(sel).forEach((el, idx) => {
        if (!key && el.closest('#viewLast10')) el.setAttribute('data-i18n', 'recentPorts');
        else if (!key && el.closest('#viewSaved')) el.setAttribute('data-i18n', 'savedVoyages');
        else if (key) el.setAttribute('data-i18n', key);
      });
    });
    const firstPanelTitle = document.querySelector('.panel-title');
    if (firstPanelTitle && !firstPanelTitle.hasAttribute('data-i18n')) firstPanelTitle.setAttribute('data-i18n', 'voyagePlanning');
    dispatchLang(l);
  }

  function buildUI(){
    const bar = document.querySelector('.nav-bar');
    if (!bar) return;

    const wrap = document.createElement('div');
    wrap.style.cssText = 'margin-left:auto;display:flex;align-items:center;gap:0.4rem';

    const langBtn = document.createElement('button');
    langBtn.className = 'nav-btn lang-btn';
    langBtn.textContent = 'TR / EN';
    langBtn.onclick = () => {
      const cur = document.documentElement.getAttribute('data-lang') === 'tr' ? 'tr' : 'en';
      applyLang(cur === 'tr' ? 'en' : 'tr');
    };
    wrap.appendChild(langBtn);
    bar.appendChild(wrap);

    const gear = document.createElement('button');
    gear.className = 'gear-btn'; gear.innerHTML = '⚙'; gear.title = 'Settings';
    document.body.appendChild(gear);
    const modal = document.createElement('div');
    modal.className = 'settings-modal'; modal.id = 'settingsModal';
    modal.innerHTML = `<div class="settings-panel"><h3 data-i18n="settings">⚙ Captain ETA Settings</h3>
      <div class="settings-row">
        <div class="setting-group">
          <label data-i18n="theme">Theme</label>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.5rem" id="themeGrid"></div>
        </div>
        <div class="setting-group">
          <label data-i18n="wallpaper">Wallpaper</label>
          <div id="wpList" style="display:flex;flex-direction:column;gap:0.4rem"></div>
        </div>
      </div>
      <div style="margin-top:1rem;display:flex;justify-content:flex-end;gap:0.5rem">
        <button class="close-btn" id="closeSettings" data-i18n="close">Close</button>
      </div>
    </div>`;
    document.body.appendChild(modal);

    const tg = document.getElementById('themeGrid');
    THEMES.forEach(th => {
      const b = document.createElement('button');
      b.className = 'theme-swatch'; b.dataset.theme = th.id;
      b.innerHTML = `<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:${th.preview};margin-right:6px"></span>${th.label}`;
      b.onclick = () => applyTheme(th.id === 'default' ? '' : th.id);
      tg.appendChild(b);
    });

    const wp = document.getElementById('wpList');
    WALLPAPERS.forEach(w => {
      const b = document.createElement('button');
      b.className = 'wp-btn theme-swatch';
      b.dataset.src = w.url ? w.url : '__none__';
      b.textContent = w.label;
      b.onclick = () => applyWallpaper(w.url ? w.url : '');
      wp.appendChild(b);
    });

    gear.onclick = () => modal.classList.add('open');
    document.getElementById('closeSettings').onclick = () => modal.classList.remove('open');
    modal.onclick = e => { if(e.target === modal) modal.classList.remove('open'); };

    const saved = storage.get('theme', 'default');
    const savedWall = storage.get('wall', 'wallpaper.jpg');
    const savedLang = storage.get('lang', 'en');
    applyTheme(saved === 'default' ? '' : saved);
    applyWallpaper(savedWall || '');
    applyLang(savedLang || 'en');

    tagStaticUI(savedLang || 'en');
  }

  const sty = document.createElement('style');
  sty.textContent = `.setting-group{flex:1 1 280px} .setting-group label{color:var(--text-muted);font-weight:600;letter-spacing:.5px}`;
  document.head.appendChild(sty);

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', buildUI); else buildUI();
})();
