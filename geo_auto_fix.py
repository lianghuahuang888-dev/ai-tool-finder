#!/usr/bin/env python3
"""GEO Auto-Fix Engine: Automatically fixes low-hanging SEO issues detected by geo_monitor.py"""

import os, re, sys, json
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).parent
FIX_LOG = REPO / ".geo_fix_log.json"

def load_log():
    if FIX_LOG.exists():
        return json.loads(FIX_LOG.read_text(encoding='utf-8'))
    return {"fixes": [], "last_run": None}

def save_log(log):
    log["last_run"] = datetime.now().isoformat()
    FIX_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding='utf-8')

def fix_meta_description(filepath, content):
    if '<meta name="description"' in content:
        return content, False
    title_m = re.search(r'<title>(.*?)</title>', content)
    if not title_m:
        return content, False
    title = title_m.group(1).strip()
    desc = f'Review of {title} - AI tool finder with ratings, pricing, and comparisons.'
    meta_tag = f'    <meta name="description" content="{desc}">'
    if '<meta charset' in content:
        content = content.replace('<meta charset', meta_tag + '\n    <meta charset', 1)
    elif '<head>' in content:
        content = content.replace('<head>', '<head>\n' + meta_tag)
    return content, True

def fix_canonical(filepath, content):
    if 'rel="canonical"' in content:
        return content, False
    fname = Path(filepath).name
    url = f'https://lianghuahuang888-dev.github.io/ai-tool-finder/tools/{fname}'
    if fname == 'index.html':
        url = 'https://lianghuahuang888-dev.github.io/ai-tool-finder/'
    elif Path(filepath).parent.name != 'tools':
        url = f'https://lianghuahuang888-dev.github.io/ai-tool-finder/{fname}'
    canonical = f'    <link rel="canonical" href="{url}">'
    if '<meta charset' in content:
        content = content.replace('<meta charset', canonical + '\n    <meta charset', 1)
    return content, True

def scan_and_fix(html_files=None):
    if html_files is None:
        html_files = list(REPO.rglob('*.html'))
    else:
        html_files = [Path(f) for f in html_files]
    log = load_log()
    fixes_applied = []
    for fpath in html_files:
        if '.git' in str(fpath):
            continue
        try:
            original = fpath.read_text(encoding='utf-8')
        except:
            continue
        content = original
        changes = []
        for fix_fn, name in [(fix_meta_description, 'meta_description'),
                              (fix_canonical, 'canonical')]:
            content, fixed = fix_fn(str(fpath), content)
            if fixed:
                changes.append(name)
        if changes and content != original:
            fpath.write_text(content, encoding='utf-8')
            fixes_applied.append({"file": str(fpath.relative_to(REPO)), "fixes": changes})
    log["fixes"].append({
        "timestamp": datetime.now().isoformat(),
        "fixes_applied": fixes_applied
    })
    save_log(log)
    return fixes_applied, log

if __name__ == '__main__':
    fixes, log = scan_and_fix()
    print(f"Auto-fix complete: {len(fixes)} files fixed")
    for f in fixes:
        print(f"  {f['file']}: {', '.join(f['fixes'])}")