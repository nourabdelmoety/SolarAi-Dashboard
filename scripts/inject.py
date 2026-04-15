import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

CSS_ADDITION = '''
/* ── NOTIFICATIONS & TRANSLATE & NEWS ───────────────────────── */
.header-actions { display: flex; align-items: center; gap: 12px; border-left: 1px solid var(--border2); padding-left: 12px; margin-left: 4px; }
.notif-bell { position: relative; cursor: pointer; font-size: 16px; padding: 4px; color: var(--muted); transition: color 0.15s; }
.notif-bell:hover { color: var(--text); }
.notif-dot { position: absolute; top: 2px; right: 2px; width: 6px; height: 6px; background: var(--warn); border-radius: 50%; display: block; box-shadow: 0 0 4px var(--warn); animation: pulseDot 2s infinite;}
@keyframes pulseDot { 0% { box-shadow: 0 0 0 rgba(239, 68, 68, 0.4); } 50% { box-shadow: 0 0 8px rgba(239, 68, 68, 0.8); } 100% { box-shadow: 0 0 0 rgba(239, 68, 68, 0); } }
.notif-drop { display: none; position: absolute; top: 60px; right: 32px; width: 340px; background: var(--surface); border: 1px solid var(--border2); border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.4); z-index: 300; overflow: hidden; animation: fadeUp 0.15s ease; }
.notif-drop.open { display: block; }
.notif-header { padding: 12px 16px; border-bottom: 1px solid var(--border); font-size: 12px; font-weight: 600; display: flex; justify-content: space-between; }
.notif-tabs { display: flex; gap: 12px; }
.notif-tab { cursor: pointer; color: var(--muted); }
.notif-tab.active { color: var(--text); border-bottom: 2px solid var(--solar); }
.notif-body { max-height: 380px; overflow-y: auto; }
.notif-item { padding: 12px 16px; border-bottom: 1px solid var(--border); display: flex; gap: 10px; cursor: pointer; transition: background 0.15s; }
.notif-item:hover { background: var(--surface2); }
.notif-item.danger { border-left: 3px solid var(--warn); }
.notif-item.info { border-left: 3px solid var(--store); }
.n-ico { font-size: 16px; }
.n-time { font-size: 10px; color: var(--muted); font-family: 'JetBrains Mono', monospace; margin-top: 4px; }

/* DANGEROUS MODAL */
.danger-modal { display: none; position: fixed; inset: 0; z-index: 999; background: rgba(239, 68, 68, 0.2); backdrop-filter: blur(8px); align-items: center; justify-content: center; }
.danger-modal.open { display: flex; }
.danger-box { background: var(--surface); border: 1px solid var(--warn); border-radius: 16px; padding: 32px; max-width: 420px; text-align: center; box-shadow: 0 0 60px rgba(239, 68, 68, 0.25); animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
@keyframes popIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.d-icon { font-size: 48px; margin-bottom: 16px; animation: pulseRed 2s infinite; }
@keyframes pulseRed { 0% { text-shadow: 0 0 0 rgba(239, 68, 68, 0.6); } 50% { text-shadow: 0 0 20px rgba(239, 68, 68, 0.2); } 100% { text-shadow: 0 0 0 rgba(239, 68, 68, 0); } }
.d-btn { margin-top: 24px; padding: 10px 24px; background: var(--warn); color: #fff; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; font-family: 'JetBrains Mono', monospace; font-size: 13px; }

/* GOOGLE TRANSLATE STYLING OVERRIDES */
#google_translate_element { display: none; }
.goog-te-banner-frame { display: none !important; }
body { top: 0 !important; }
.lang-switch { display: flex; align-items: center; gap: 6px; cursor: pointer; padding: 6px 12px; border-radius: 8px; background: var(--surface2); border: 1px solid var(--border2); font-size: 11px; font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--text); }
.lang-switch:hover { border-color: var(--store); color: var(--store); }

/* NEWS TAB */
.news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-top: 16px; }
.news-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; transition: border-color 0.2s; display: flex; flex-direction: column; }
.news-card:hover { border-color: var(--solar); }
.news-date { font-size: 10px; color: var(--muted); font-family: 'JetBrains Mono', monospace; margin-bottom: 8px; }
.news-title { font-size: 15px; font-weight: 600; margin-bottom: 10px; line-height: 1.4; color: var(--text); }
.news-desc { font-size: 12px; color: var(--text2); line-height: 1.6; margin-bottom: 16px; flex: 1; }
.news-link { font-size: 11px; font-family: 'JetBrains Mono', monospace; color: var(--store); text-decoration: none; align-self: flex-start; }
'''

NAV_TAB_ADDITION = '''    <div class="nav-tab" onclick="showPage('news',this)">Markt-News</div>
'''

HEADER_RIGHT_ADDITION = '''    <div class="header-actions">
      <div class="notif-bell" onclick="toggleNotif()" title="Benachrichtigungen">
        🔔<span class="notif-dot" id="notif-dot"></span>
      </div>
      <div class="lang-switch" onclick="switchLang()">
        <span style="font-size:14px;">🌍</span> <span id="lang-lbl">EN / DE</span>
      </div>
      <div id="google_translate_element"></div>
    </div>
'''

NOTIF_MODAL_ADDITION = '''
<div class="notif-drop" id="notif-drop">
  <div class="notif-header">
    <div class="notif-tabs">
      <div class="notif-tab active" onclick="switchNotifTab('sys',this)">System (2)</div>
      <div class="notif-tab" onclick="switchNotifTab('news',this)">News (Neu)</div>
    </div>
    <span style="cursor:pointer;color:var(--muted);font-size:14px;" onclick="toggleNotif()">✕</span>
  </div>
  <div class="notif-body" id="notif-sys-list">
    <div class="notif-item danger" onclick="goToLog()">
      <div class="n-ico">⚠️</div>
      <div>
        <div style="font-size:12px;font-weight:600;">Netzausfall erkannt</div>
        <div class="n-time">Vor 2 Minuten</div>
      </div>
    </div>
    <div class="notif-item info" onclick="goToLog()">
      <div class="n-ico">ℹ️</div>
      <div>
        <div style="font-size:12px;font-weight:600;">Speicher > 70% geladen</div>
        <div class="n-time">Vor 15 Minuten</div>
      </div>
    </div>
  </div>
  <div class="notif-body" id="notif-news-list" style="display:none;"></div>
</div>

<div class="danger-modal" id="danger-modal">
  <div class="danger-box">
    <div class="d-icon">⚠️</div>
    <div style="font-size:18px;font-weight:700;color:var(--warn);margin-bottom:8px;">KRITISCHER SYSTEMALARM</div>
    <div style="font-size:13px;color:var(--text2);margin-bottom:16px;">Wechselrichter meldet Übertemperatur (85°C). Sicherheitsabschaltung wurde eingeleitet. Bitte Anlage sofort prüfen!</div>
    <button class="d-btn" onclick="closeDangerModal()">Akzeptieren & Schließen</button>
  </div>
</div>
'''

PAGE_NEWS_ADDITION = '''
<div class="page" id="page-news">
<main>
  <div class="sec-label" style="margin-top:8px;">Live Energy News — Clean Energy Wire & Partner</div>
  <div class="news-grid" id="news-grid">
    <div style="padding:20px;color:var(--muted);font-size:12px;">Lade aktuelle Nachrichten von rss2json API...</div>
  </div>
</main>
</div>
'''

JS_ADDITION = '''
// --- NOTIFICATION & LANG ---
function toggleNotif() {
  document.getElementById('notif-drop').classList.toggle('open');
  document.getElementById('notif-dot').style.display = 'none';
}
function switchNotifTab(t, el) {
  document.querySelectorAll('.notif-tab').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('notif-sys-list').style.display = t === 'sys' ? 'block' : 'none';
  document.getElementById('notif-news-list').style.display = t === 'news' ? 'block' : 'none';
}
function goToLog() {
  toggleNotif();
  document.querySelectorAll('.nav-tab')[4].click(); 
}
function triggerDangerModal() {
  document.getElementById('danger-modal').classList.add('open');
}
function closeDangerModal() {
  document.getElementById('danger-modal').classList.remove('open');
}

// Randomly trigger danger modal after 15 seconds for demonstration
setTimeout(triggerDangerModal, 15000);

let currentLang = 'de';
function switchLang() {
  currentLang = currentLang === 'de' ? 'en' : 'de';
  document.getElementById('lang-lbl').textContent = currentLang.toUpperCase();
  const select = document.querySelector('.goog-te-combo');
  if (select) {
    select.value = currentLang;
    select.dispatchEvent(new Event('change'));
  }
}

// Ensure Google Translate loads
const gtScript = document.createElement('script');
gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateInit';
document.head.appendChild(gtScript);
window.googleTranslateInit = function() {
  new google.translate.TranslateElement({pageLanguage: 'de', includedLanguages: 'en,de', autoDisplay: false}, 'google_translate_element');
};

// --- REAL API FETCHES ---
async function fetchPrices() {
  try {
    const res = await fetch('https://api.energy-charts.info/price?bzn=DE-LU');
    const data = await res.json();
    if(data.price && data.price.length > 0) {
      return data.price.slice(-24).map(p => p / 1000);
    }
  } catch(e) { console.error('Price API failed', e); }
  return null;
}

async function fetchNews() {
  try {
    const res = await fetch('https://api.rss2json.com/v1/api.json?rss_url=https://www.cleanenergywire.org/rss.xml');
    const data = await res.json();
    
    const grid = document.getElementById('news-grid');
    grid.innerHTML = data.items.slice(0, 12).map(i => `
      <div class="news-card">
        <div class="news-date">${i.pubDate.split(' ')[0]}</div>
        <div class="news-title">${i.title}</div>
        <div class="news-desc">${i.description.replace(/<[^>]+>/g, '').substring(0,120)}...</div>
        <a href="${i.link}" target="_blank" class="news-link">VOLLSTÄNDIGER ARTIKEL →</a>
      </div>
    `).join('');

    const drop = document.getElementById('notif-news-list');
    drop.innerHTML = data.items.slice(0, 4).map(i => `
      <div class="notif-item" onclick="window.open('${i.link}')">
        <div class="n-ico">📰</div>
        <div>
          <div style="font-size:11px;font-weight:600;">${i.title.substring(0,40)}...</div>
          <div class="n-time">${i.pubDate.split(' ')[0]}</div>
        </div>
      </div>
    `).join('');
  } catch(e) { console.error('News API failed', e); }
}

// Intercept buildChart to fetch prices first
const originalBuildChart = buildChart;
window.buildChart = async function(scale) {
  if (scale === 'day') {
    const livePrices = await fetchPrices();
    if (livePrices) {
      spotEur.splice(0, spotEur.length, ...livePrices);
    }
  }
  originalBuildChart(scale);
}

// Call fetch news initially
fetchNews();
'''

# 1. CSS
content = content.replace("</style>", CSS_ADDITION + "\n</style>")

# 2. NAV TAB
nav_anchor = '''    <div class="nav-tab" onclick="showPage('maintenance',this)">Wartungslog</div>'''
content = content.replace(nav_anchor, NAV_TAB_ADDITION + nav_anchor)

# 3. HEADER
# Find the exact sys-status div from v9
header_anchor = '''    <div class="sys-status">System: <span style="color:var(--sell);margin-left:4px;">● Online</span></div>
  </div>'''
content = content.replace(header_anchor, header_anchor + "\n" + HEADER_RIGHT_ADDITION)

# 4. MODALS
modal_anchor = "<!-- ─── ADMIN OVERRIDE MODAL ────────────────────────────────── -->"
content = content.replace(modal_anchor, NOTIF_MODAL_ADDITION + "\n" + modal_anchor)

# 5. PAGE NEWS BEFORE SCRIPT
script_anchor = "\n<script>"
content = content.replace(script_anchor, PAGE_NEWS_ADDITION + script_anchor)

# 6. INIT SCRIPT
init_anchor = "// ── INIT ──────────────────────────────────────────────────────"
content = content.replace(init_anchor, JS_ADDITION + "\n" + init_anchor)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injections complete")
