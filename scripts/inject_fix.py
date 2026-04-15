import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Header HTML
OLD_LANG_HTML = '''      <div class="lang-switch" onclick="switchLang()">
        <span style="font-size:14px;">🌍</span> <span id="lang-lbl">EN / DE</span>
      </div>'''

NEW_LANG_HTML = '''      <div class="lang-dropdown" id="lang-menu" onclick="toggleLangDrop()">
        <div id="lang-active">🇩🇪 DE</div>
        <div class="lang-options" id="lang-options">
           <div class="lang-opt" onclick="setLang('en', event)" id="lang-inactive">🇬🇧 EN</div>
        </div>
      </div>'''
content = content.replace(OLD_LANG_HTML, NEW_LANG_HTML)

# 2. Update CSS for lang dropdown
OLD_CSS = '''.lang-switch { display: flex; align-items: center; gap: 6px; cursor: pointer; padding: 6px 12px; border-radius: 8px; background: var(--surface2); border: 1px solid var(--border2); font-size: 11px; font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--text); }
.lang-switch:hover { border-color: var(--store); color: var(--store); }'''

NEW_CSS = '''.lang-dropdown { position: relative; cursor: pointer; padding: 6px 12px; border-radius: 8px; background: var(--surface2); border: 1px solid var(--border2); font-size: 13px; font-family: 'JetBrains Mono', monospace; font-weight: 600; color: var(--text); display: flex; align-items: center; justify-content:center; width: 66px;}
.lang-dropdown:hover { border-color: var(--solar); }
.lang-options { display: none; position: absolute; top: calc(100% + 4px); left: 0; right: 0; background: var(--surface); border: 1px solid var(--border2); border-radius: 8px; overflow: hidden; z-index: 400; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.lang-options.open { display: block; }
.lang-opt { padding: 6px 12px; cursor: pointer; text-align: center; font-size: 13px; }
.lang-opt:hover { background: var(--surface2); color: var(--solar); }'''
content = content.replace(OLD_CSS, NEW_CSS)


# 3. Fix JS logic for Lang and Log redirect
OLD_JS_1 = '''function goToLog() {
  toggleNotif();
  document.querySelectorAll('.nav-tab')[4].click(); 
}'''

NEW_JS_1 = '''function goToLog() {
  toggleNotif();
  // Find the tab that redirects to maintenance
  const tabs = document.querySelectorAll('.nav-tab');
  for(let tab of tabs) {
    if(tab.getAttribute('onclick') && tab.getAttribute('onclick').includes('maintenance')) {
      tab.click();
      break;
    }
  }
}'''
content = content.replace(OLD_JS_1, NEW_JS_1)


OLD_JS_2 = '''let currentLang = 'de';
function switchLang() {
  currentLang = currentLang === 'de' ? 'en' : 'de';
  document.getElementById('lang-lbl').textContent = currentLang.toUpperCase();
  const select = document.querySelector('.goog-te-combo');
  if (select) {
    select.value = currentLang;
    select.dispatchEvent(new Event('change'));
  }
}'''

NEW_JS_2 = '''let currentLang = 'de';

function toggleLangDrop() {
  document.getElementById('lang-options').classList.toggle('open');
}
window.addEventListener('click', function(e) {
  if(!document.getElementById('lang-menu').contains(e.target)) {
    document.getElementById('lang-options').classList.remove('open');
  }
});

function setLang(lang, event) {
  event.stopPropagation();
  currentLang = lang;
  
  if(currentLang === 'en') {
    document.getElementById('lang-active').innerHTML = '🇬🇧 EN';
    document.getElementById('lang-inactive').innerHTML = '🇩🇪 DE';
    document.getElementById('lang-inactive').setAttribute('onclick', "setLang('de', event)");
  } else {
    document.getElementById('lang-active').innerHTML = '🇩🇪 DE';
    document.getElementById('lang-inactive').innerHTML = '🇬🇧 EN';
    document.getElementById('lang-inactive').setAttribute('onclick', "setLang('en', event)");
  }
  
  document.getElementById('lang-options').classList.remove('open');
  
  // Trigger google translate
  const select = document.querySelector('.goog-te-combo');
  if (select) {
    select.value = currentLang;
    select.dispatchEvent(new Event('change'));
  }
}'''

content = content.replace(OLD_JS_2, NEW_JS_2)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixes Complete")
