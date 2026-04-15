import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Z-Index / Overflow Fix
CSS_INSERT = '''
/* UX Overrides */
.info-mode-active .fin-card, .info-mode-active .timeline-card, .info-mode-active .sensor-card, .info-mode-active .card { overflow: visible !important; }
.info-mode-active .stat-card { overflow: visible !important; }
'''
content = content.replace('</style>', CSS_INSERT + '\n</style>')

# 2. Thermal Storage UI Update
OLD_THERMAL = '''<div class="tank-labels">
    <div class="t-lbl" style="bottom: 95%;">■ 95°C — Max (Sicherheitsventil)</div>
    <div class="t-lbl" style="bottom: 75%;">■ 75°C — Zieltemperatur</div>
    <div class="t-lbl" style="bottom: 64%; color:var(--text); font-weight:700;">■ 64°C — Aktuell ◀</div>
    <div class="t-lbl" style="bottom: 45%;">■ 45°C — Minimum für Heizung</div>
    <div class="t-lbl" style="bottom: 20%; color:var(--muted);">20°C — Kalt / Leer</div>
  </div>'''

NEW_THERMAL = '''<div class="tank-labels">
    <div class="t-lbl" style="bottom: 95%; color:var(--warn) !important;">■ 450°C — Max Warnung</div>
    <div class="t-lbl" style="bottom: 85%;">■ 400°C — Max Zieltemperatur</div>
    <div class="t-lbl" style="bottom: 64%; color:var(--text); font-weight:700;">■ 250°C — Aktuell (Berechnet) ◀</div>
    <div class="t-lbl" style="bottom: 45%;">■ 150°C — Minimum Betrieb</div>
    <div class="t-lbl" style="bottom: 5%; color:var(--muted);">20°C — Raumtemperatur</div>
  </div>'''
content = content.replace(OLD_THERMAL, NEW_THERMAL)


# 3. Add to DE_TO_EN Dictionary for Sensors and Maintenance
NEW_DICT_ENTRIES = '''
  '■ 450°C — Max Warnung': '■ 450°C — Max Warning',
  '■ 400°C — Max Zieltemperatur': '■ 400°C — Max Target Temp',
  '■ 250°C — Aktuell (Berechnet) ◀': '■ 250°C — Current (Calculated) ◀',
  '■ 150°C — Minimum Betrieb': '■ 150°C — Minimum Operation',
  '20°C — Raumtemperatur': '20°C — Room Temperature',
  'Sensor DS18B20 · GPIO 4': 'Sensor DS18B20 · GPIO 4',
  'Nur meldend — Umgebungsdaten fließen in Wetterkorrelation und Systemeffizienzberechnung der KI.': 'Reporting only — ambient data flows into weather correlation and AI system efficiency calculation.',
  'Systemstatus': 'System Status',
  'Aktion': 'Action',
  'Details': 'Details',
  'Sensor': 'Sensor',
  'Protokoll': 'Protocol',
  'Status': 'Status',
  'Wartung': 'Maintenance',
  'Log': 'Log',
  'Ereignis': 'Event',
  'Kritisch': 'Critical',
  'Warnung': 'Warning',
  'Info': 'Info',
  'Temperatur': 'Temperature',
  'Speicher': 'Storage',
  'Verlust': 'Loss',
  'Sicherheitsventil': 'Safety Valve',
  'Feuchtigkeit': 'Humidity',
  'Lichtstärke': 'Light Intensity',
  'Netz': 'Grid',
  'Inverter': 'Inverter',
  'Ausfall': 'Failure',
  'Neustart': 'Restart',
  'Firmware': 'Firmware',
  'Update': 'Update',
  'Erfolgreich': 'Successful',
  'Test': 'Test',
  'Abgeschlossen': 'Completed',
  'Aktiv': 'Active',
  'Inaktiv': 'Inactive',
  'Warte auf Daten': 'Waiting for data',
  'Verbunden': 'Connected',
  'Getrennt': 'Disconnected',
  'Sensoren initialisiert': 'Sensors initialized',
  'Datenbank verbunden': 'Database connected',
  'KI gestartet': 'AI started',
  'System bereit': 'System ready',
'''
content = content.replace("const DE_TO_EN = {", "const DE_TO_EN = {\n" + NEW_DICT_ENTRIES)

# 4. Make applyDOMTranslations handle text nodes deeper matching
OLD_DOM = '''        for(let key in dict) {
            if(n.nodeValue.includes(key) && key.length > 5) {
                n.nodeValue = n.nodeValue.replace(key, dict[key]);
            }
        }'''

NEW_DOM = '''        for(let key in dict) {
            if(n.nodeValue.includes(key) && key.length > 3) {
                n.nodeValue = n.nodeValue.replace(key, dict[key]);
            }
        }'''
content = content.replace(OLD_DOM, NEW_DOM)


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Finished updates.")
