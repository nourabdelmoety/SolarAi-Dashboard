"""
Auto-sync helper — appended to every inject script.
Copies the latest solar_dashboard_v9.html + docs to D:\SolarAI_Dashboard
"""
import shutil, os

SRC_HTML  = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'
DST_HTML  = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'

BRAIN     = r'C:\Users\uik05263\.gemini\antigravity\brain\c35f913a-c181-485d-b140-76630402e85e\artifacts'
DST_DOCS  = r'D:\SolarAI_Dashboard\docs'

DOCS = [
    'implementation_plan.md',
    'walkthrough.md',
    'task.md',
    'dashboard_generator_guide.md',
]

def sync():
    # 1. Sync main dashboard HTML
    shutil.copy2(SRC_HTML, DST_HTML)

    # 2. Sync docs/artifacts
    os.makedirs(DST_DOCS, exist_ok=True)
    for doc in DOCS:
        src = os.path.join(BRAIN, doc)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DST_DOCS, doc))

    print(f'[sync] D:\\SolarAI_Dashboard updated successfully.')

if __name__ == '__main__':
    sync()
