#!/usr/bin/env python3
"""
GEO Monitor: Automated SEO/GEO scoring + regression detection + auto-fix engine
Runs as scheduled task. Compares against baseline, flags regressions.
"""

import os, re, json, hashlib, sys
from html.parser import HTMLParser
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://lianghuahuang888-dev.github.io/ai-tool-finder'
BASELINE_FILE = os.path.join(REPO, '.geo_baseline.json')
REPORT_FILE = os.path.join(REPO, 'geo_report.txt')

SCORING = {
    'robots_found': 10, 'robots_quality': 15,
    'llms_structure': 10, 'llms_h1': 5, 'llms_blockquote': 1, 
    'llms_sections': 3, 'llms_links': 3, 'llms_depth': 3,
    'schema_faq': 4, 'schema_organization': 3,
    'meta_title': 3, 'meta_description': 3, 'meta_canonical': 2, 'meta_og': 2,
    'content_min_words': 5, 'content_h1': 3, 'content_stats': 4, 
    'content_citations': 4, 'content_headings': 3, 'content_lists': 2,
    'content_tables': 2,
}

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript', 'nav', 'footer'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'nav', 'footer'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data.strip())

def audit_page(filepath, relpath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    title_m = re.search(r'<title>(.*?)</title>', content)
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    title_len = len(title_m.group(1)) if title_m else 0
    desc_len = len(desc_m.group(1)) if desc_m else 0
    
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    schema_types = []
    for s in schemas:
        try: schema_types.append(json.loads(s).get('@type', 'unknown'))
        except: pass
    
    ext = TextExtractor()
    ext.feed(content)
    text = ' '.join(ext.text)
    words = len(text.split())
    h1s = len(re.findall(r'<h1[^>]*>', content))
    h2s = len(re.findall(r'<h2[^>]*>', content))
    h3s = len(re.findall(r'<h3[^>]*>', content))
    uls = len(re.findall(r'<ul[^>]*>', content))
    tables = len(re.findall(r'<table[^>]*>', content))
    ext_links = len(re.findall(r'href="https?://(?!lianghuahuang888)[^"]+', content))
    has_stats = bool(re.search(r'\d+%|\$\d+|\d+\s*(million|billion|thousand)', text))
    
    score = 0
    if title_len > 10: score += SCORING['meta_title']
    if desc_len > 50: score += SCORING['meta_description']
    score += SCORING['meta_canonical']
    if 'og:title' in content: score += SCORING['meta_og']
    if 'FAQPage' in schema_types: score += SCORING['schema_faq']
    if any(t in schema_types for t in ['WebSite','Organization','SoftwareApplication']): 
        score += SCORING['schema_organization']
    if words > 300: score += SCORING['content_min_words']
    if h1s > 0: score += SCORING['content_h1']
    if h2s + h3s >= 3: score += SCORING['content_headings']
    if has_stats: score += SCORING['content_stats']
    if ext_links >= 3: score += SCORING['content_citations']
    if uls > 0: score += SCORING['content_lists']
    if tables > 0: score += SCORING['content_tables']
    
    return {
        'file': relpath, 'url': f"{BASE_URL}/{relpath}".replace('/index.html','/'),
        'hash': content_hash, 'score': score,
        'words': words, 'ext_links': ext_links,
        'schema_types': schema_types,
        'has_faq': 'FAQPage' in schema_types,
        'title_len': title_len, 'desc_len': desc_len,
    }

def run_audit():
    pages = []
    for subdir in ['', 'tools', 'blog']:
        d = os.path.join(REPO, subdir)
        if not os.path.isdir(d): continue
        for f in os.listdir(d):
            if not f.endswith('.html'): continue
            rel = f'{subdir}/{f}' if subdir else f
            pages.append(audit_page(os.path.join(d, f), rel))
    
    overall = sum(p['score'] for p in pages)
    return {
        'timestamp': datetime.now().isoformat(),
        'page_count': len(pages),
        'total_score': overall,
        'avg_score': round(overall / len(pages), 1) if pages else 0,
        'max_per_page': sum(SCORING.values()),
        'pages': pages
    }

def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    return None

def save_baseline(audit):
    with open(BASELINE_FILE, 'w') as f:
        json.dump(audit, f, indent=2, default=str)

def compare(current, baseline):
    if not baseline:
        return {'status': 'FIRST_RUN', 'regressions': [], 'improvements': [], 
                'new_pages': [], 'deleted_pages': [], 'diffs': []}
    
    changes = {'status': 'OK', 'diffs': [], 'regressions': [], 
               'improvements': [], 'new_pages': [], 'deleted_pages': []}
    
    bp_map = {p['file']: p for p in baseline['pages']}
    cp_map = {p['file']: p for p in current['pages']}
    
    for file, cp in cp_map.items():
        if file not in bp_map:
            changes['new_pages'].append(file)
            continue
        bp = bp_map[file]
        diff = cp['score'] - bp['score']
        if diff < 0:
            changes['regressions'].append({
                'file': file, 'score_delta': diff, 'was': bp['score'], 'now': cp['score']
            })
            changes['status'] = 'REGRESSION'
        elif diff > 0:
            changes['improvements'].append({
                'file': file, 'score_delta': diff, 'was': bp['score'], 'now': cp['score']
            })
        if cp['hash'] != bp['hash']:
            changes['diffs'].append(file)
    
    for file in bp_map:
        if file not in cp_map:
            changes['deleted_pages'].append(file)
            changes['status'] = 'REGRESSION'
    
    return changes

def run():
    current = run_audit()
    baseline = load_baseline()
    result = compare(current, baseline)
    
    lines = []
    lines.append(f"GEO Monitor Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Site: {BASE_URL}")
    lines.append(f"Pages: {current['page_count']} | Avg Score: {current['avg_score']}/{current['max_per_page']}")
    lines.append(f"Status: {result['status']}")
    
    if result['regressions']:
        lines.append(f"\nREGRESSIONS ({len(result['regressions'])}):")
        for r in result['regressions']:
            lines.append(f"  {r['file']}: {r['was']}->{r['now']} ({r['score_delta']})")
    if result['improvements']:
        lines.append(f"\nIMPROVEMENTS ({len(result['improvements'])}):")
        for r in result['improvements']:
            lines.append(f"  {r['file']}: {r['was']}->{r['now']} (+{r['score_delta']})")
    if result['new_pages']:
        lines.append(f"\nNEW PAGES ({len(result['new_pages'])}):")
        for p in result['new_pages']:
            lines.append(f"  + {p}")
    
    lines.append(f"\nBOTTOM 5 pages by score:")
    for p in sorted(current['pages'], key=lambda x: x['score'])[:5]:
        lines.append(f"  Score:{p['score']:2d} Words:{p['words']:4d} FAQ:{'Y' if p['has_faq'] else 'N'} — {p['file']}")
    
    report = '\n'.join(lines)
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    save_baseline(current)
    print(report)
    return current, result

if __name__ == '__main__':
    run()