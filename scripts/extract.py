import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.in_script_or_style = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_script_or_style = True
        for attr in attrs:
            if attr[0] in ('title', 'placeholder', 'data-tip'):
                t = attr[1].strip()
                if t and len(t)>2 and not re.match(r'^[\d\s\.,€%°+-]+$', t):
                    self.texts.append(t)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_script_or_style = False

    def handle_data(self, data):
        if not self.in_script_or_style:
            t = data.strip()
            if t and len(t) > 1 and not re.match(r'^[\d\s\.,€%°+-]+$', t):
                self.texts.append(t)

path = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

parser = MyHTMLParser()
parser.feed(content)

scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
js_texts = []
for s in scripts:
    strings = re.findall(r'\'([^\']*)\'|\"([^\"]*)\"|\`([^\`]*)\`', s)
    for tup in strings:
        for t in tup:
            t = t.strip()
            if t and len(t) > 2 and not re.match(r'^[\W\d_a-zA-Z0-9\.]+$', t) and 'var(' not in t and 'px' not in t and '{' not in t and 'function' not in t and 'getElementById' not in t and '<' not in t:
                js_texts.append(t)

all_texts = sorted(list(set(parser.texts + js_texts)))

with open(r'D:\SolarAI_Dashboard\docs\scratch_texts.txt', 'w', encoding='utf-8') as f:
    for t in all_texts:
        if t: f.write(t + '\n')
