"""
Migrate all inject scripts to target D:\SolarAI_Dashboard\solar_dashboard_v9.html directly.
Removes the sync footer (no longer needed) and removes Downloads copy of the HTML.
"""
import os, glob, re, shutil

SCRIPTS_DIR = r'C:\Users\uik05263\Downloads'
OLD_PATH    = r'C:\Users\uik05263\Downloads\solar_dashboard_v9.html'
NEW_PATH    = r'D:\SolarAI_Dashboard\solar_dashboard_v9.html'

scripts = glob.glob(os.path.join(SCRIPTS_DIR, 'inject*.py'))
scripts.append(os.path.join(SCRIPTS_DIR, 'sync_to_d.py'))
scripts.append(os.path.join(SCRIPTS_DIR, 'extract.py'))
scripts.append(os.path.join(SCRIPTS_DIR, 'patch_autosync.py'))

SYNC_FOOTER_MARKER = '# ── AUTO-SYNC TO D:\\SolarAI_Dashboard'

for path in sorted(set(scripts)):
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace old path references with new D: path
    updated = content.replace(
        r"C:\Users\uik05263\Downloads\solar_dashboard_v9.html",
        r"D:\SolarAI_Dashboard\solar_dashboard_v9.html"
    ).replace(
        r"C:\\Users\\uik05263\\Downloads\\solar_dashboard_v9.html",
        r"D:\\SolarAI_Dashboard\\solar_dashboard_v9.html"
    )

    # 2. Remove auto-sync footer block (no longer needed)
    if SYNC_FOOTER_MARKER in updated:
        footer_idx = updated.find('\n\n' + SYNC_FOOTER_MARKER)
        if footer_idx == -1:
            footer_idx = updated.find(SYNC_FOOTER_MARKER)
        if footer_idx != -1:
            updated = updated[:footer_idx].rstrip() + '\n'

    if updated != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f'[updated] {os.path.basename(path)}')
    else:
        print(f'[no change] {os.path.basename(path)}')

# 3. Also copy the updated scripts to D:\SolarAI_Dashboard\scripts\
for path in sorted(set(scripts)):
    if not os.path.exists(path):
        continue
    basename = os.path.basename(path)
    dst = os.path.join(r'D:\SolarAI_Dashboard\scripts', basename)
    shutil.copy2(path, dst)

print('\nAll scripts now target D:\\SolarAI_Dashboard\\solar_dashboard_v9.html directly.')

# 4. Delete the Downloads copy of the HTML (D: is now the single source of truth)
if os.path.exists(OLD_PATH):
    os.remove(OLD_PATH)
    print(f'Deleted Downloads copy: {OLD_PATH}')

print('\nMigration complete. D:\\SolarAI_Dashboard is now the single source of truth.')
print('The small inject scripts in Downloads are just launchers (~50KB total).')
