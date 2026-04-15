import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Google Translate init
OLD_GT = '''// Ensure Google Translate loads
const gtScript = document.createElement('script');
gtScript.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateInit';
document.head.appendChild(gtScript);
window.googleTranslateInit = function() {
  new google.translate.TranslateElement({pageLanguage: 'de', includedLanguages: 'en,de', autoDisplay: false}, 'google_translate_element');
};'''
content = content.replace(OLD_GT, '')

# 2. Add I18N Dictionary and Function
OLD_SETLANG = '''function setLang(lang, event) {
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
    select.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
  } else {
    // Retry if Google Translate hasn't fully loaded the widget yet
    setTimeout(() => {
        const retrySelect = document.querySelector('.goog-te-combo');
        if(retrySelect) {
            retrySelect.value = currentLang;
            retrySelect.dispatchEvent(new Event('change', { bubbles: true, cancelable: true }));
        }
    }, 500);
  }
}'''

NEW_SETLANG = '''
const DE_TO_EN = {
  'Übersicht': 'Overview',
  'Wetter': 'Weather',
  'Thermospeicher': 'Thermal Storage',
  'Sensoren': 'Sensors',
  'Wartungslog': 'Maintenance Log',
  'Markt-News': 'Market News',
  'Energiemanagement · Süddeutschland': 'Energy Management · South Germany',
  'Online': 'Online',
  'System': 'System',
  'Benachrichtigungen': 'Notifications',
  'News (Neu)': 'News (New)',
  'Netzausfall erkannt': 'Power Grid Failure Detected',
  'Vor 2 Minuten': '2 Minutes Ago',
  'Vor 15 Minuten': '15 Minutes Ago',
  'Speicher > 70% geladen': 'Battery > 70% Charged',
  'KRITISCHER SYSTEMALARM': 'CRITICAL SYSTEM ALARM',
  'Akzeptieren & Schließen': 'Accept & Close',
  'Heutige Ausbeute': 'Daily Yield',
  'Netz-Import': 'Grid Import',
  'Batteriespeicher': 'Battery Storage',
  'Heutige Speicherkosten': 'Daily Storage Cost',
  'Verdient durch Einspeisung': 'Earned by Export',
  'Gesamteinsparung': 'Total Savings',
  'Speichernetzwerk & Leistungskurve': 'Storage Network & Power Curve',
  'Aktivität / Prognose': 'Activity / Forecast',
  '24h Historie': '24h History',
  '30 Tage': '30 Days',
  '12 Monate': '12 Months',
  'Aktuelles Wetter': 'Current Weather',
  'Sonnenaufgang': 'Sunrise',
  'Sonnenuntergang': 'Sunset',
  'Wolkendecke': 'Cloud Cover',
  'Stündliche Prognose': 'Hourly Forecast',
  'Thermische Schichtung': 'Thermal Stratification',
  'Wechselrichter meldet Übertemperatur (85°C). Sicherheitsabschaltung wurde eingeleitet. Bitte Anlage sofort prüfen!': 'Inverter reports overtemperature (85°C). Safety shutdown initiated. Please check system immediately!',
  'Wartungslog — KI Aktionen': 'Maintenance Log — AI Actions',
  'Letzte Systemanpassungen': 'Recent System Adjustments',
  'Admin Override': 'Admin Override',
  'Manuelle Steuerung': 'Manual Control',
  'KI-Steuerung wiederhergestellt — automatischer Betrieb aktiv': 'AI Control Restored — Automatic mode active',
  'Tag': 'Day',
  'Heute': 'Today',
  'Morgen': 'Tomorrow',
  'KI: SELL': 'AI: SELL',
  'KI: USE': 'AI: USE',
  'KI: STORE': 'AI: STORE',
  'KI-Ziel erreicht': 'AI Target Reached',
  'Preis: €': 'Price: €',
  'Strombedarf aus Storage gedeckt': 'Electricity demand met from Storage',
  'Einspeisung': 'Export',
  'Laden': 'Store',
  'Eigenverbrauch': 'Self-consumption'
};

const EN_TO_DE = {};
for(let k in DE_TO_EN) EN_TO_DE[DE_TO_EN[k]] = k;

function applyDOMTranslations(lang) {
  const dict = lang === 'en' ? DE_TO_EN : EN_TO_DE;
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  let n;
  while(n = walk.nextNode()) {
    let txt = n.nodeValue.trim();
    if(dict[txt] !== undefined) {
       n.nodeValue = n.nodeValue.replace(txt, dict[txt]);
    } else {
        // Partial matching for dynamic/sub-sentence text
        for(let key in dict) {
            if(n.nodeValue.includes(key) && key.length > 5) {
                n.nodeValue = n.nodeValue.replace(key, dict[key]);
            }
        }
    }
  }
  
  // Extra care for placeholders or specifically selected deep nodes if needed
}

function setLang(lang, event) {
  event.stopPropagation();
  if (currentLang === lang) return;
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
  
  applyDOMTranslations(currentLang);
}
'''
if OLD_SETLANG in content:
    content = content.replace(OLD_SETLANG, NEW_SETLANG)
    content = content.replace('<div id="google_translate_element"></div>', '')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Dictionary-based i18n added successfully.')
else:
    print('Failed to find OLD block.')
