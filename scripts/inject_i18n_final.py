import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────────
# 1. FIX THERMAL STORAGE SUB-STATS (still show old 64°C values)
# ─────────────────────────────────────────────────────────────────
OLD_THERMAL_STATS = '''      <div class="therm-stat">
        <div class="therm-stat-lbl">Aktuelle Temperatur</div>
        <div class="therm-stat-val" style="color:var(--use);">64.0°C</div>
        <div class="therm-stat-sub">Sensor DS18B20 · GPIO 4</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl">Gespeicherte Wärmeenergie</div>
        <div class="therm-stat-val" style="color:var(--solar);">32.8 kWh</div>
        <div class="therm-stat-sub">bei 64°C vs. 20°C Umgebung · (4186 J/kg·K × 800L × 44K) / 3.6M</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl">Verlustrate</div>
        <div class="therm-stat-val" style="color:var(--text2);">0.3°C/h</div>
        <div class="therm-stat-sub">Gut isolierter Tank · entspricht ~0.28 kWh/h Verlust</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl">Geschätzte Haltezeit</div>
        <div class="therm-stat-val" style="color:var(--sell);">3.8 Tage</div>
        <div class="therm-stat-sub">bis 45°C Minimum · Ziel 75°C · Max 95°C (Sicherheitsventil)</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl">Heutiger Solarertrag → Wärme</div>
        <div class="therm-stat-val" style="color:var(--solar);">18.4 kWh</div>
        <div class="therm-stat-sub">8:00–14:00 Uhr · Solar→Heizung aktiv</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl">Heizstufe (aktuell)</div>
        <div class="therm-stat-val" style="color:var(--muted);">Standby</div>
        <div class="therm-stat-sub">Nacht · Solar nicht verfügbar · Wärmeschutz aktiv</div>
      </div>'''

NEW_THERMAL_STATS = '''      <div class="therm-stat">
        <div class="therm-stat-lbl" data-de="Aktuelle Temperatur" data-en="Current Temperature">Aktuelle Temperatur</div>
        <div class="therm-stat-val" style="color:var(--use);">250°C</div>
        <div class="therm-stat-sub" data-de="Sensor DS18B20 · GPIO 4" data-en="Sensor DS18B20 · GPIO 4">Sensor DS18B20 · GPIO 4</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl" data-de="Gespeicherte Wärmeenergie" data-en="Stored Thermal Energy">Gespeicherte Wärmeenergie</div>
        <div class="therm-stat-val" style="color:var(--solar);">147.5 kWh</div>
        <div class="therm-stat-sub" data-de="bei 250°C vs. 20°C Umgebung · (4186 J/kg·K × 800L × 230K) / 3.6M" data-en="at 250°C vs. 20°C ambient · (4186 J/kg·K × 800L × 230K) / 3.6M">bei 250°C vs. 20°C Umgebung · (4186 J/kg·K × 800L × 230K) / 3.6M</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl" data-de="Verlustrate" data-en="Loss Rate">Verlustrate</div>
        <div class="therm-stat-val" style="color:var(--text2);">0.3°C/h</div>
        <div class="therm-stat-sub" data-de="Gut isolierter Tank · entspricht ~0.28 kWh/h Verlust" data-en="Well insulated tank · equals ~0.28 kWh/h loss">Gut isolierter Tank · entspricht ~0.28 kWh/h Verlust</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl" data-de="Geschätzte Haltezeit" data-en="Estimated Hold Time">Geschätzte Haltezeit</div>
        <div class="therm-stat-val" style="color:var(--sell);">5.2 Tage</div>
        <div class="therm-stat-sub" data-de="bis 150°C Minimum · Ziel 400°C · Max 450°C (Sicherheitsabschaltung)" data-en="until 150°C minimum · Target 400°C · Max 450°C (Safety Shutdown)">bis 150°C Minimum · Ziel 400°C · Max 450°C (Sicherheitsabschaltung)</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl" data-de="Heutiger Solarertrag → Wärme" data-en="Today's Solar Yield → Heat">Heutiger Solarertrag → Wärme</div>
        <div class="therm-stat-val" style="color:var(--solar);">18.4 kWh</div>
        <div class="therm-stat-sub" data-de="8:00–14:00 Uhr · Solar→Heizung aktiv" data-en="08:00–14:00 · Solar→Heating active">8:00–14:00 Uhr · Solar→Heizung aktiv</div>
      </div>
      <div class="therm-stat">
        <div class="therm-stat-lbl" data-de="Heizstufe (aktuell)" data-en="Heating Level (current)">Heizstufe (aktuell)</div>
        <div class="therm-stat-val" style="color:var(--muted);">Standby</div>
        <div class="therm-stat-sub" data-de="Nacht · Solar nicht verfügbar · Wärmeschutz aktiv" data-en="Night · Solar unavailable · Heat protection active">Nacht · Solar nicht verfügbar · Wärmeschutz aktiv</div>
      </div>'''

content = content.replace(OLD_THERMAL_STATS, NEW_THERMAL_STATS)

# ─────────────────────────────────────────────────────────────────
# 2. MAKE sensorData LANGUAGE-AWARE  
# Replace sensor JS with a function that respects currentLang
# ─────────────────────────────────────────────────────────────────
OLD_SENSOR_DATA = '''function buildSensors() {
  const grid = document.getElementById('sensor-grid-full');
  if (!grid || grid.children.length > 0) return;
  sensorData.forEach(s => {
    const card = document.createElement('div');
    card.className = `sensor-card ${s.cardClass}`;
    const metaHtml = s.meta.map(m=>`<div class="sensor-meta-row"><span class="sensor-meta-key">${m[0]}</span><span class="sensor-meta-val">${m[1]}</span></div>`).join('');
    const sparkHtml = s.spark.map((v,i)=>{const mx=Math.max(...s.spark)||1;return `<div class="s-bar" style="height:${Math.max(4,(v/mx)*28)}px;background:${s.color};opacity:0.6;"></div>`;}).join('');
    const roleClass = s.role === 'storing' ? 'role-storing' : 'role-reporting';
    card.innerHTML = `
      <div class="sensor-header">
        <div><div class="sensor-id">${s.id} · ${s.model}</div><div class="sensor-name-big">${s.name}</div></div>
        <span class="sensor-chip ${s.chipClass}">${s.chip}</span>
      </div>
      <div><span class="sensor-val-big" style="color:${s.color};">${s.val}</span><span class="sensor-unit-lbl">${s.unit}</span></div>
      <div class="sensor-sparkline">${sparkHtml}</div>
      <div class="sensor-meta">${metaHtml}</div>
      <div class="sensor-role-badge ${roleClass}">
        ${s.role==='storing'?'💾 Speichernd':'📡 Nur meldend'} · Pin: ${s.pin} · ${s.protocol}<br>
        <span style="opacity:0.8;">${s.roleLabel}</span>
      </div>`;
    grid.appendChild(card);
  });
}'''

NEW_SENSOR_DATA = '''function buildSensors(rebuild) {
  const grid = document.getElementById('sensor-grid-full');
  if (!grid) return;
  if (grid.children.length > 0 && !rebuild) return;
  grid.innerHTML = '';
  const L = (de, en) => currentLang === 'en' ? en : de;
  sensorData.forEach(s => {
    const card = document.createElement('div');
    card.className = `sensor-card ${s.cardClass}`;
    const metaHtml = s.meta.map(m => {
      const keyDE = m[0]; const keyEN = s.metaEN ? s.metaEN[s.meta.indexOf(m)][0] : m[0];
      const valDE = m[1]; const valEN = s.metaEN ? s.metaEN[s.meta.indexOf(m)][1] : m[1];
      return `<div class="sensor-meta-row"><span class="sensor-meta-key">${L(keyDE,keyEN)}</span><span class="sensor-meta-val">${L(valDE,valEN)}</span></div>`;
    }).join('');
    const sparkHtml = s.spark.map((v)=>{const mx=Math.max(...s.spark)||1;return `<div class="s-bar" style="height:${Math.max(4,(v/mx)*28)}px;background:${s.color};opacity:0.6;"></div>`;}).join('');
    const roleClass = s.role === 'storing' ? 'role-storing' : 'role-reporting';
    const roleIcon = s.role === 'storing' ? `💾 ${L('Speichernd','Storing')}` : `📡 ${L('Nur meldend','Reporting only')}`;
    card.innerHTML = `
      <div class="sensor-header">
        <div><div class="sensor-id">${s.id} · ${s.model}</div><div class="sensor-name-big">${L(s.name, s.nameEN||s.name)}</div></div>
        <span class="sensor-chip ${s.chipClass}">${L(s.chip, s.chip==='AKTIV'?'ACTIVE':s.chip==='PASSIV'?'PASSIVE':s.chip)}</span>
      </div>
      <div><span class="sensor-val-big" style="color:${s.color};">${s.val}</span><span class="sensor-unit-lbl">${s.unit}</span></div>
      <div class="sensor-sparkline">${sparkHtml}</div>
      <div class="sensor-meta">${metaHtml}</div>
      <div class="sensor-role-badge ${roleClass}">
        ${roleIcon} · Pin: ${s.pin} · ${s.protocol}<br>
        <span style="opacity:0.8;">${L(s.roleLabel, s.roleLabelEN||s.roleLabel)}</span>
      </div>`;
    grid.appendChild(card);
  });
}'''

content = content.replace(OLD_SENSOR_DATA, NEW_SENSOR_DATA)

# ─────────────────────────────────────────────────────────────────
# 3. ENRICH sensorData OBJECTS WITH English translations (nameEN, roleLabelEN, metaEN)
# ─────────────────────────────────────────────────────────────────
OLD_SD_LINE = '''const sensorData = [
  { id:'S-01', name:'Solaranlage Ausgangsleistung', model:'SCT-013-030', protocol:'Analog (ADC)', pin:'GPIO34', role:'reporting', roleLabel:'Nur meldend — leitet Messwert an ESP32 weiter. Kein lokaler Speicher.', val:'5.2', unit:'kW', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--solar)', meta:[['Typ','Stromsensor (Klemmstromsensor)'],['Bereich','0–30 A'],['Genauigkeit','±1%'],['Abtastrate','jede 15 Sek.'],['Datenfluss','→ MQTT solar/sensors']], spark:[3.8,4.2,5.1,5.8,6.4,6.5,6.1,5.6,4.7,3.3,1.8,0.7] },
  { id:'S-02', name:'Batterie-Managementsystem (BMS)', model:'JBD-SP04S034', protocol:'UART / RS485', pin:'GPIO16/17', role:'storing', roleLabel:'Aktiv speichernd — BMS schreibt SOC, Zyklen und Zellspannungen in den eigenen Speicher. ESP32 liest via UART aus.', val:'78', unit:'%', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--store)', meta:[['Kapazität','12.5 kWh Li-Ion'],['Spannung','51.2 V (16S)'],['Max. Ladestrom','50 A'],['Zyklen gesamt','142'],['Datenfluss','→ MQTT solar/sensors']], spark:[72,74,75,77,80,84,82,78,72,70,74,78] },
  { id:'S-03', name:'Thermospeicher Temperatur', model:'DS18B20 (wasserdicht)', protocol:'1-Wire', pin:'GPIO4', role:'reporting', roleLabel:'Nur meldend — misst Wassertemperatur im Tank. Kein lokaler Speicher. Daten werden von ESP32 weitergeleitet.', val:'64', unit:'°C', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--use)', meta:[['Typ','Digitaler Temperatursensor'],['Bereich','-55°C bis +125°C'],['Genauigkeit','±0.5°C'],['Anschluss','3-Draht + 4.7kΩ Pull-up'],['Datenfluss','→ MQTT solar/sensors']], spark:[55,56,58,61,65,70,74,74,72,68,65,64] },
  { id:'S-04', name:'Netz-Energiemesser (bidirektional)', model:'PZEM-004T v3', protocol:'UART (Serial2)', pin:'GPIO16/17', role:'storing', roleLabel:'Aktiv speichernd — PZEM speichert kumulierte Energie (kWh) intern. ESP32 liest Messwerte via UART-Protokoll aus.', val:'0.31', unit:'€/kWh', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--sell)', meta:[['Spannung','242.1 V AC'],['Leistung','1.4 kW aktuell'],['kWh heute','11.6 kWh'],['Einspeisung heute','14.2 kWh'],['Datenfluss','→ MQTT solar/sensors']], spark:[0.18,0.17,0.16,0.23,0.27,0.29,0.27,0.25,0.27,0.32,0.34,0.31] },
  { id:'S-05', name:'Solare Einstrahlung', model:'BH1750FVI', protocol:'I2C', pin:'SDA=21 / SCL=22', role:'reporting', roleLabel:'Nur meldend — misst Lichtstärke (Lux) und konvertiert zu W/m². Daten fließen direkt in die KI-Entscheidung.', val:'16', unit:'W/m²', chip:'PASSIV', chipClass:'chip-passive', cardClass:'passive-card', color:'var(--solar)', meta:[['Bereich','0–65535 Lux'],['Auflösung','1 Lux'],['I2C-Adresse','0x23 oder 0x5C'],['Umrechnung','Lux ÷ 120 ≈ W/m²'],['Datenfluss','→ MQTT solar/sensors']], spark:[0,0,0,200,480,720,900,860,720,480,200,16] },
  { id:'S-06', name:'Außentemperatur & Luftfeuchtigkeit', model:'DHT22 (AM2302)', protocol:'Digital (Single-Wire)', pin:'GPIO5', role:'reporting', roleLabel:'Nur meldend — Umgebungsdaten fließen in Wetterkorrelation und Systemeffizienzberechnung der KI.', val:'18.4', unit:'°C', chip:'PASSIV', chipClass:'chip-passive', cardClass:'passive-card', color:'var(--text2)', meta:[['Luftfeuchtigkeit','52%'],['Messintervall','min. 2 Sekunden'],['Genauigkeit Temp','±0.5°C'],['Genauigkeit RH','±2–5%'],['Datenfluss','→ MQTT solar/sensors']], spark:[16,15,15,15,16,17,18,19,21,22,23,21] },
];'''

NEW_SD_LINE = '''const sensorData = [
  { id:'S-01', name:'Solaranlage Ausgangsleistung', nameEN:'Solar Output Power', model:'SCT-013-030', protocol:'Analog (ADC)', pin:'GPIO34', role:'reporting', roleLabel:'Nur meldend — leitet Messwert an ESP32 weiter. Kein lokaler Speicher.', roleLabelEN:'Reporting only — forwards reading to ESP32. No local storage.', val:'5.2', unit:'kW', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--solar)', meta:[['Typ','Stromsensor (Klemmstromsensor)'],['Bereich','0–30 A'],['Genauigkeit','±1%'],['Abtastrate','jede 15 Sek.'],['Datenfluss','→ MQTT solar/sensors']], metaEN:[['Type','Current Sensor (Clamp)'],['Range','0–30 A'],['Accuracy','±1%'],['Sampling Rate','every 15 sec.'],['Data Flow','→ MQTT solar/sensors']], spark:[3.8,4.2,5.1,5.8,6.4,6.5,6.1,5.6,4.7,3.3,1.8,0.7] },
  { id:'S-02', name:'Batterie-Managementsystem (BMS)', nameEN:'Battery Management System (BMS)', model:'JBD-SP04S034', protocol:'UART / RS485', pin:'GPIO16/17', role:'storing', roleLabel:'Aktiv speichernd — BMS schreibt SOC, Zyklen und Zellspannungen in den eigenen Speicher. ESP32 liest via UART aus.', roleLabelEN:'Actively storing — BMS writes SOC, cycles and cell voltages to its own storage. ESP32 reads via UART.', val:'78', unit:'%', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--store)', meta:[['Kapazität','12.5 kWh Li-Ion'],['Spannung','51.2 V (16S)'],['Max. Ladestrom','50 A'],['Zyklen gesamt','142'],['Datenfluss','→ MQTT solar/sensors']], metaEN:[['Capacity','12.5 kWh Li-Ion'],['Voltage','51.2 V (16S)'],['Max Charge Current','50 A'],['Total Cycles','142'],['Data Flow','→ MQTT solar/sensors']], spark:[72,74,75,77,80,84,82,78,72,70,74,78] },
  { id:'S-03', name:'Thermospeicher Temperatur', nameEN:'Thermal Storage Temperature', model:'DS18B20 (wasserdicht)', protocol:'1-Wire', pin:'GPIO4', role:'reporting', roleLabel:'Nur meldend — misst Wassertemperatur im Tank. Kein lokaler Speicher. Daten werden von ESP32 weitergeleitet.', roleLabelEN:'Reporting only — measures water temperature in tank. No local storage. Data forwarded by ESP32.', val:'250', unit:'°C', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--use)', meta:[['Typ','Digitaler Temperatursensor'],['Bereich','-55°C bis +400°C'],['Genauigkeit','±0.5°C'],['Anschluss','3-Draht + 4.7kΩ Pull-up'],['Datenfluss','→ MQTT solar/sensors']], metaEN:[['Type','Digital Temp. Sensor'],['Range','-55°C to +400°C'],['Accuracy','±0.5°C'],['Connection','3-Wire + 4.7kΩ Pull-up'],['Data Flow','→ MQTT solar/sensors']], spark:[120,135,150,170,190,220,240,248,252,250,250,250] },
  { id:'S-04', name:'Netz-Energiemesser (bidirektional)', nameEN:'Grid Energy Meter (bidirectional)', model:'PZEM-004T v3', protocol:'UART (Serial2)', pin:'GPIO16/17', role:'storing', roleLabel:'Aktiv speichernd — PZEM speichert kumulierte Energie (kWh) intern. ESP32 liest Messwerte via UART-Protokoll aus.', roleLabelEN:'Actively storing — PZEM stores cumulative energy (kWh) internally. ESP32 reads values via UART protocol.', val:'0.31', unit:'€/kWh', chip:'AKTIV', chipClass:'chip-active', cardClass:'active-card', color:'var(--sell)', meta:[['Spannung','242.1 V AC'],['Leistung','1.4 kW aktuell'],['kWh heute','11.6 kWh'],['Einspeisung heute','14.2 kWh'],['Datenfluss','→ MQTT solar/sensors']], metaEN:[['Voltage','242.1 V AC'],['Power','1.4 kW current'],['kWh today','11.6 kWh'],['Export today','14.2 kWh'],['Data Flow','→ MQTT solar/sensors']], spark:[0.18,0.17,0.16,0.23,0.27,0.29,0.27,0.25,0.27,0.32,0.34,0.31] },
  { id:'S-05', name:'Solare Einstrahlung', nameEN:'Solar Irradiance', model:'BH1750FVI', protocol:'I2C', pin:'SDA=21 / SCL=22', role:'reporting', roleLabel:'Nur meldend — misst Lichtstärke (Lux) und konvertiert zu W/m². Daten fließen direkt in die KI-Entscheidung.', roleLabelEN:'Reporting only — measures light intensity (Lux) and converts to W/m². Data flows directly into AI decision.', val:'16', unit:'W/m²', chip:'PASSIV', chipClass:'chip-passive', cardClass:'passive-card', color:'var(--solar)', meta:[['Bereich','0–65535 Lux'],['Auflösung','1 Lux'],['I2C-Adresse','0x23 oder 0x5C'],['Umrechnung','Lux ÷ 120 ≈ W/m²'],['Datenfluss','→ MQTT solar/sensors']], metaEN:[['Range','0–65535 Lux'],['Resolution','1 Lux'],['I2C Address','0x23 or 0x5C'],['Conversion','Lux ÷ 120 ≈ W/m²'],['Data Flow','→ MQTT solar/sensors']], spark:[0,0,0,200,480,720,900,860,720,480,200,16] },
  { id:'S-06', name:'Außentemperatur & Luftfeuchtigkeit', nameEN:'Ambient Temp & Humidity', model:'DHT22 (AM2302)', protocol:'Digital (Single-Wire)', pin:'GPIO5', role:'reporting', roleLabel:'Nur meldend — Umgebungsdaten fließen in Wetterkorrelation und Systemeffizienzberechnung der KI.', roleLabelEN:'Reporting only — ambient data flows into weather correlation and AI system efficiency calculation.', val:'18.4', unit:'°C', chip:'PASSIV', chipClass:'chip-passive', cardClass:'passive-card', color:'var(--text2)', meta:[['Luftfeuchtigkeit','52%'],['Messintervall','min. 2 Sekunden'],['Genauigkeit Temp','±0.5°C'],['Genauigkeit RH','±2–5%'],['Datenfluss','→ MQTT solar/sensors']], metaEN:[['Humidity','52%'],['Meas. Interval','min. 2 seconds'],['Accuracy Temp','±0.5°C'],['Accuracy RH','±2–5%'],['Data Flow','→ MQTT solar/sensors']], spark:[16,15,15,15,16,17,18,19,21,22,23,21] },
];'''

content = content.replace(OLD_SD_LINE, NEW_SD_LINE)

# ─────────────────────────────────────────────────────────────────
# 4. MAKE maintEvents LANGUAGE-AWARE via rebuild on lang switch
# ─────────────────────────────────────────────────────────────────
OLD_MAINT_BUILD = '''function buildMaintLog() {
  const log = document.getElementById('maint-log');
  if (!log || log.children.length > 0) return;
  maintEvents.forEach(e => {
    const row = document.createElement('div');
    row.className = `maint-row ${e.type}`;
    row.innerHTML = `<div class="maint-date">${e.date}</div><div class="maint-icon">${e.icon}</div><div class="maint-body"><div class="maint-title-text">${e.title}</div><div class="maint-desc">${e.desc}</div><div class="maint-tech">${e.tech}</div></div><span class="maint-badge ${e.badge}">${e.badgeLabel}</span>`;
    log.appendChild(row);
  });
}'''

NEW_MAINT_BUILD = '''const maintEventsEN = [
  { date: null, icon:'⚠', type:'warn-row', title:'Sensor S-05 (BH1750) — Lux Value Anomaly', desc:'Irradiance value shows unrealistic peak of 1450 Lux between 14:22 and 14:35. Possibly reflection by bird or dirt particles. Continue monitoring.', tech:'Sensor: BH1750 · GPIO21/22 · I2C · Automatic outlier filter active from next cycle', badge:'badge-warn', badgeLabel:'WARNING' },
  { date: null, icon:'✓', type:'ok-row', title:'Monthly Calibration — All Sensors', desc:'Plausibility check of all 6 sensors. SCT-013 aligned with reference multimeter (+0.3% deviation, within tolerance). PZEM meter reading manually verified.', tech:'Performed by: Admin · Duration: 45 min', badge:'badge-done', badgeLabel:'DONE' },
  { date: null, icon:'🔧', type:'info-row', title:'ESP32 Firmware Update — v1.2.3 → v1.3.0', desc:'MQTT reconnect logic improved. DS18B20 reading error at temps > 80°C fixed. Sampling rate increased from 30s to 15s for better AI baseline.', tech:'OTA Update via WiFi · Downtime: 12 Seconds · Rollback Version saved', badge:'badge-info', badgeLabel:'UPDATE' },
  { date: null, icon:'🌡', type:'info-row', title:'Thermal Storage Inspection — Heat Insulation', desc:'Visual inspection of PU foam insulation. No moisture damage visible. Loss rate 0.3°C/h meets specification. Safety valve tested — flawless.', tech:'Tank: 800L Buffer Storage · Insulation: 100mm PU-Foam · TÜV certified', badge:'badge-done', badgeLabel:'DONE' },
  { date: null, icon:'⚡', type:'ok-row', title:'Battery Check — Capacity Measurement', desc:'Full cycle test: 100% → 10% → 100%. Usable capacity: 12.3 kWh (Nominal 12.5 kWh, 98.4%). All 16 cells within 20mV voltage tolerance. No degradation detected.', tech:'BMS: JBD-SP04S034 · Cycle counter: 142 · Temperature during test: 22°C · SOH: 98.4%', badge:'badge-done', badgeLabel:'DONE' },
  { date: null, icon:'🚀', type:'info-row', title:'System Commissioning — Prototype Day 1', desc:'Initial commissioning of all system components. MQTT broker, InfluxDB, Node-RED, and Python AI-Controller successfully deployed. First test runs with simulated data. All sensors communicating correctly.', tech:'Stack: ESP32 + Mosquitto + Node-RED + InfluxDB v2.7 · Docker Compose', badge:'badge-info', badgeLabel:'START' },
  { date: null, icon:'📅', type:'info-row', title:'PLANNED: Solar Panel Cleaning', desc:'Biannual solar panel cleaning planned. Dirt and bird droppings can lower efficiency by 5-15%. Schedule appointment with roofer.', tech:'Estimated Duration: 2h · Cost: ~€ 80', badge:'badge-planned', badgeLabel:'PLANNED' },
];

function buildMaintLog(rebuild) {
  const log = document.getElementById('maint-log');
  if (!log) return;
  if (log.children.length > 0 && !rebuild) return;
  log.innerHTML = '';
  const events = currentLang === 'en' ? maintEventsEN : maintEvents;
  events.forEach((e, i) => {
    const dateStr = maintEvents[i].date;
    const row = document.createElement('div');
    row.className = `maint-row ${e.type}`;
    row.innerHTML = `<div class="maint-date">${dateStr}</div><div class="maint-icon">${e.icon}</div><div class="maint-body"><div class="maint-title-text">${e.title}</div><div class="maint-desc">${e.desc}</div><div class="maint-tech">${e.tech}</div></div><span class="maint-badge ${e.badge}">${e.badgeLabel}</span>`;
    log.appendChild(row);
  });
}'''

content = content.replace(OLD_MAINT_BUILD, NEW_MAINT_BUILD)

# ─────────────────────────────────────────────────────────────────
# 5. MAKE setLang TRIGGER SENSOR AND MAINT REBUILDS
# ─────────────────────────────────────────────────────────────────
OLD_SET_LANG = '''  document.getElementById('lang-options').classList.remove('open');
  
  applyDOMTranslations(currentLang);
}'''

NEW_SET_LANG = '''  document.getElementById('lang-options').classList.remove('open');
  
  applyDOMTranslations(currentLang);
  buildSensors(true);
  buildMaintLog(true);

  // Also update data-de/data-en marked elements
  document.querySelectorAll('[data-de]').forEach(el => {
    el.textContent = currentLang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-de');
  });
}'''

content = content.replace(OLD_SET_LANG, NEW_SET_LANG)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('All sensor + maint + thermal labels updated.')
