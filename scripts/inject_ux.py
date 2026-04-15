import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS Injection
CSS = '''
/* UX/UI ENHANCEMENTS: AI Insights, Export, Info Mode */
.insight-box { background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.3); border-radius: 12px; padding: 18px 24px; margin-bottom: 24px; animation: fadeUp 0.3s ease; }
.in-header { color: var(--store); font-size: 13px; font-weight: 700; margin-bottom: 8px; font-family: 'Syne', sans-serif;}
.in-body { font-size: 13px; color: var(--text); line-height: 1.5; }

.export-btn { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; background: var(--surface2); border: 1px solid var(--border2); border-radius: 8px; color: var(--text); font-family: 'JetBrains Mono', monospace; font-size: 11px; cursor: pointer; transition: all 0.2s; margin-top: 16px; font-weight: 600;}
.export-btn:hover { background: var(--surface3); border-color: var(--store); color: var(--store); }

.info-mode-active .stat-card { border-color: rgba(59,130,246,0.5); cursor: help; position: relative; }
.info-mode-active .stat-card:hover::after { content: attr(data-info); position: absolute; bottom: 105%; left: 50%; transform: translateX(-50%); background: var(--store); color: #fff; padding: 10px 14px; border-radius: 8px; font-family: 'JetBrains Mono', monospace; font-size: 11px; white-space: pre-wrap; width: 220px; text-align: center; z-index: 100; box-shadow: 0 4px 14px rgba(0,0,0,0.4); animation: fadeUp 0.15s; }
'''
content = content.replace("</style>", CSS + "\n</style>")

# 2. Header Info Mode Toggle
HEADER_ANCHOR = '<div class="notif-bell"'
HEADER_INSERT = '''<div class="lang-switch" id="info-toggle" onclick="toggleInfoMode()" title="Kontext-Hilfe">ℹ️ <span id="info-lbl">Info Modus</span></div>
      '''
content = content.replace(HEADER_ANCHOR, HEADER_INSERT + HEADER_ANCHOR)


# 3. Actionable AI Insights Widget
INSIGHT_ANCHOR = '<div class="timeline-wrap">'
INSIGHT_INSERT = '''  <div class="insight-box" id="ai-insight-box">
    <div class="in-header">🧠 Automatisierte System-Einblicke</div>
    <div class="in-body" id="ai-insight-text">Analysiere aktuelle Marktdaten und Speicherzustand...</div>
  </div>
'''
content = content.replace(INSIGHT_ANCHOR, INSIGHT_INSERT + INSIGHT_ANCHOR)


# 4. Export CSV Button
EXPORT_ANCHOR = '<div class="band-wrap" id="band-section">'
EXPORT_INSERT = '''<button class="export-btn" onclick="exportDataCSV()"><span style="font-size:14px;">⬇️</span> <span>Daten als CSV Exportieren</span></button>\n      '''
content = content.replace(EXPORT_ANCHOR, EXPORT_INSERT + EXPORT_ANCHOR)


# 5. JS Logic
JS = '''
// --- UX ENHANCEMENTS ---
function toggleInfoMode() {
  document.body.classList.toggle('info-mode-active');
  const btn = document.getElementById('info-toggle');
  if (document.body.classList.contains('info-mode-active')) {
    btn.style.background = 'rgba(59,130,246,0.2)';
    btn.style.borderColor = 'var(--store)';
  } else {
    btn.style.background = '';
    btn.style.borderColor = '';
  }
}

function attachTooltips() {
  const cards = document.querySelectorAll('.stat-card');
  const tooltipsDE = [
    "Gesamtmenge des heute durch das Solarsystem erzeugten Stroms in Kilowattstunden.",
    "Potenzieller oder realisierter Erlös durch den Verkauf überschüssigen Stroms zum dynamischen Spotpreis.",
    "Geld, das gespart wurde, indem eigener statt teurer Netzstrom genutzt wurde.",
    "Anzahl der von der KI berechneten optimalen Betriebsmodi-Wechsel für heute.",
    "Grad der Unabhängigkeit vom externen Stromnetz basierend auf Eigenproduktion und Speicher."
  ];
  cards.forEach((card, i) => { if(tooltipsDE[i]) card.setAttribute('data-info', tooltipsDE[i]); });
}

function generateInsights() {
  const insightText = document.getElementById('ai-insight-text');
  if(!insightText) return;
  
  // Calculate avg spot price
  let avgPrice = 0; 
  if (spotEur && spotEur.length > 0) {
    avgPrice = spotEur.reduce((a,b)=>a+b,0) / spotEur.length;
  }
  
  let rec = "";
  if (avgPrice < 0.20) {
    rec = `Spotpreise sind aktuell extrem niedrig (Ø €${avgPrice.toFixed(2)}). Die KI empfiehlt dringend, nachts den Heimspeicher über das Netz aufzuladen.`;
  } else if (avgPrice > 0.28) {
    rec = `Hohe Spotpreise im Tagesdurchschnitt (Ø €${avgPrice.toFixed(2)}). Fokussiere Eigenverbrauch und primären Verkauf ins Netz während der Spitzenzeiten.`;
  } else {
    rec = `Durchschnittliche Marktlage. Führe Standard-Eigenversorgungs-Protokoll aus.`;
  }
  
  insightText.textContent = `Datenlage analysiert: ${rec}`;
}

function exportDataCSV() {
  if (!spotEur || spotEur.length === 0) return;
  let csvContent = "data:text/csv;charset=utf-8,Uhrzeit;Solarproduktion_kW;Spotpreis_EUR\\n";
  for (let i = 0; i < hours.length; i++) {
    csvContent += `${hours[i]};${solarKw[i]};${spotEur[i]}\\n`;
  }
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', 'SolarAI_Tagesdaten.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
'''

INIT_ANCHOR = "document.addEventListener('DOMContentLoaded', () => {"
content = content.replace(INIT_ANCHOR, JS + "\n" + INIT_ANCHOR + "\n  attachTooltips();\n  setTimeout(generateInsights, 1500);")


# 6. Update Dictionary additions safely by finding const DE_TO_EN = { and injecting keys
DICT_INSERT = '''
  'Info Modus': 'Info Mode',
  'Automatisierte System-Einblicke': 'Automated System Insights',
  'Analysiere aktuelle Marktdaten und Speicherzustand...': 'Analyzing current market data and storage state...',
  'Daten als CSV Exportieren': 'Export Data as CSV',
  'Gesamtmenge des heute durch das Solarsystem erzeugten Stroms in Kilowattstunden.': 'Total amount of self-produced solar power today in kilowatt-hours.',
  'Potenzieller oder realisierter Erlös durch den Verkauf überschüssigen Stroms zum dynamischen Spotpreis.': 'Potential or realized revenue from selling excess power at dynamic spot prices.',
  'Geld, das gespart wurde, indem eigener statt teurer Netzstrom genutzt wurde.': 'Money saved by using own power instead of expensive grid electricity.',
  'Anzahl der von der KI berechneten optimalen Betriebsmodi-Wechsel für heute.': 'Number of optimal operating mode switches calculated by AI for today.',
  'Grad der Unabhängigkeit vom externen Stromnetz basierend auf Eigenproduktion und Speicher.': 'Degree of independence from the external power grid based on self-production and storage.',
  'Spotpreise sind aktuell extrem niedrig (Ø €': 'Spot prices are currently extremely low (Ø €',
  '). Die KI empfiehlt dringend, nachts den Heimspeicher über das Netz aufzuladen.': '). The AI strongly recommends charging home storage from the grid at night.',
  'Hohe Spotpreise im Tagesdurchschnitt (Ø €': 'High spot prices daily average (Ø €',
  '). Fokussiere Eigenverbrauch und primären Verkauf ins Netz während der Spitzenzeiten.': '). Focus on self-consumption and primary sales to the grid during peak times.',
  'Durchschnittliche Marktlage. Führe Standard-Eigenversorgungs-Protokoll aus.': 'Average market condition. Executing standard self-supply protocol.',
  'Datenlage analysiert: ': 'Data analyzed: ',\n'''

content = content.replace("const DE_TO_EN = {\n", "const DE_TO_EN = {\n" + DICT_INSERT)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("UX elements heavily injected.")
