"""
Appends auto-sync footer to all inject_*.py scripts that don't already have it.
Run once — idempotent.
"""
import os, glob

SCRIPTS_DIR = r'D:\SolarAI_Dashboard\scripts'
SYNC_FOOTER = '''

# ── AUTO-SYNC TO D:\\SolarAI_Dashboard ────────────────────────
import sys as _sys
_sys.path.insert(0, r'D:\\SolarAI_Dashboard\\scripts')
try:
    from sync_to_d import sync as _sync
    _sync()
except Exception as _e:
    print(f'[sync] Warning: could not sync to D: — {_e}')
'''

scripts = glob.glob(os.path.join(SCRIPTS_DIR, 'inject*.py'))
scripts.append(os.path.join(SCRIPTS_DIR, 'inject_i18n_final.py'))

patched = 0
for path in set(scripts):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'AUTO-SYNC TO D:' in content:
        print(f'[skip]  {os.path.basename(path)} — already has sync')
        continue
    with open(path, 'a', encoding='utf-8') as f:
        f.write(SYNC_FOOTER)
    print(f'[patch] {os.path.basename(path)} — sync footer added')
    patched += 1

# Copy sync_to_d.py itself to D:\SolarAI_Dashboard\scripts
import shutil
shutil.copy2(
    os.path.join(SCRIPTS_DIR, 'sync_to_d.py'),
    r'D:\SolarAI_Dashboard\scripts\sync_to_d.py'
)
print(f'\nPatched {patched} scripts. sync_to_d.py copied to D:\\SolarAI_Dashboard\\scripts\\')

# Run one immediate sync to confirm it works
from sync_to_d import sync
sync()
