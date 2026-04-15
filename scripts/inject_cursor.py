import os

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update `applyDOMTranslations()` to also scan and replace data-info attributes.
OLD_APPLY_DOM = '''function applyDOMTranslations(lang) {
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
}'''

NEW_APPLY_DOM = '''function applyDOMTranslations(lang) {
  const dict = lang === 'en' ? DE_TO_EN : EN_TO_DE;
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  let n;
  while(n = walk.nextNode()) {
    let txt = n.nodeValue.trim();
    if(dict[txt] !== undefined) {
       n.nodeValue = n.nodeValue.replace(txt, dict[txt]);
    } else {
        for(let key in dict) {
            if(n.nodeValue.includes(key) && key.length > 5) {
                n.nodeValue = n.nodeValue.replace(key, dict[key]);
            }
        }
    }
  }
  
  // Explicitly translate data-info tooltips via dictionary
  document.querySelectorAll('[data-info]').forEach(el => {
     let txt = el.getAttribute('data-info').trim();
     if (dict[txt] !== undefined) {
         el.setAttribute('data-info', dict[txt]);
     }
  });
}'''
content = content.replace(OLD_APPLY_DOM, NEW_APPLY_DOM)

# 2. Fix the cursor CSS and HTML
OLD_INFO_BTN = '<div class="lang-switch" id="info-toggle" onclick="toggleInfoMode()" title="Kontext-Hilfe">ℹ️ <span id="info-lbl">Info Modus</span></div>'
NEW_INFO_BTN = '<div class="lang-switch" id="info-toggle" onclick="toggleInfoMode()" title="Kontext-Hilfe" style="cursor:pointer; user-select:none;">ℹ️ <span id="info-lbl">Info Modus</span></div>'
content = content.replace(OLD_INFO_BTN, NEW_INFO_BTN)

# Apply CSS classes to other UI components to accept info mode
OLD_CSS_INFO = '.info-mode-active .stat-card { border-color: rgba(59,130,246,0.5); cursor: help; position: relative; }\n.info-mode-active .stat-card:hover::after {'
NEW_CSS_INFO = '.info-mode-active .stat-card, .info-mode-active .fin-card, .info-mode-active .sensor-card, .info-mode-active .card { border-color: rgba(59,130,246,0.5); cursor: help; position: relative; }\n.info-mode-active .stat-card:hover::after, .info-mode-active .fin-card:hover::after, .info-mode-active .sensor-card:hover::after, .info-mode-active .card:hover::after {'
content = content.replace(OLD_CSS_INFO, NEW_CSS_INFO)


# 3. Add tooltips to the extra boxes
OLD_ATTACH = '''function attachTooltips() {
  const cards = document.querySelectorAll('.stat-card');
  const tooltipsDE = [
    "Gesamtmenge des heute durch das Solarsystem erzeugten Stroms in Kilowattstunden.",
    "Potenzieller oder realisierter Erlös durch den Verkauf überschüssigen Stroms zum dynamischen Spotpreis.",
    "Geld, das gespart wurde, indem eigener statt teurer Netzstrom genutzt wurde.",
    "Anzahl der von der KI berechneten optimalen Betriebsmodi-Wechsel für heute.",
    "Grad der Unabhängigkeit vom externen Stromnetz basierend auf Eigenproduktion und Speicher."
  ];
  cards.forEach((card, i) => { if(tooltipsDE[i]) card.setAttribute('data-info', tooltipsDE[i]); });
}'''

NEW_ATTACH = '''function attachTooltips() {
  const statCards = document.querySelectorAll('.stat-card');
  const statTooltips = [
    "Gesamtmenge des heute durch das Solarsystem erzeugten Stroms in Kilowattstunden.",
    "Potenzieller oder realisierter Erlös durch den Verkauf überschüssigen Stroms zum dynamischen Spotpreis.",
    "Geld, das gespart wurde, indem eigener statt teurer Netzstrom genutzt wurde.",
    "Anzahl der von der KI berechneten optimalen Betriebsmodi-Wechsel für heute.",
    "Grad der Unabhängigkeit vom externen Stromnetz basierend auf Eigenproduktion und Speicher."
  ];
  statCards.forEach((card, i) => { if(statTooltips[i]) card.setAttribute('data-info', statTooltips[i]); });

  const finCards = document.querySelectorAll('.fin-card');
  const finTooltips = [
    "Rückblick des finanziellen Erlöses im ausgewählten Monatszeitraum.",
    "Rückblick der Einsparungen durch Vermeidung des Netzimports.",
    "Darstellung der hypothetischen Stromkosten ohne das SolarAI System."
  ];
  finCards.forEach((card, i) => { if(finTooltips[i]) card.setAttribute('data-info', finTooltips[i]); });
  
  const chartCard = document.querySelector('.timeline-card');
  if (chartCard) chartCard.setAttribute('data-info', 'Visuelle Darstellung der KI-Aktionen in Relation zum Spotpreis und der Solarproduktion.');

  const logCard = document.querySelector('.card');
  if (logCard) logCard.setAttribute('data-info', 'Detailliertes Protokoll aller Systemeingriffe und Modus-Wechsel.');
}'''
content = content.replace(OLD_ATTACH, NEW_ATTACH)

# 4. Insert new Tooltip translations to the Dictionary
DICT_INSERT = '''  'Rückblick des finanziellen Erlöses im ausgewählten Monatszeitraum.': 'Review of financial revenue in the selected monthly period.',
  'Rückblick der Einsparungen durch Vermeidung des Netzimports.': 'Review of savings by avoiding grid import.',
  'Darstellung der hypothetischen Stromkosten ohne das SolarAI System.': 'Representation of hypothetical electricity costs without the SolarAI system.',
  'Visuelle Darstellung der KI-Aktionen in Relation zum Spotpreis und der Solarproduktion.': 'Visual representation of AI actions in relation to spot price and solar production.',
  'Detailliertes Protokoll aller Systemeingriffe und Modus-Wechsel.': 'Detailed log of all system interventions and mode switches.',
'''
content = content.replace("const DE_TO_EN = {\n", "const DE_TO_EN = {\n" + DICT_INSERT)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Tooltips extended and translation fix applied.')
