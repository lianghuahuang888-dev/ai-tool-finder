#!/usr/bin/env python3
"""AI Tool Finder Daily Monitoring - Run once per day"""
import requests, json, time, sys
from datetime import datetime

BASE = "https://pullnova.com"
PAGES = ["/", "/about", "/contact", "/compare.html", "/blog.html"]

def check_uptime():
    """Verify critical pages return 200"""
    failures = []
    for page in PAGES:
        try:
            r = requests.head(BASE + page, allow_redirects=True, timeout=10,
                             headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code >= 400:
                failures.append(f"{page} -> {r.status_code}")
        except Exception as e:
            failures.append(f"{page} -> {str(e)[:50]}")
    return failures

def check_deployment():
    """Check if the site is serving the latest version"""
    try:
        r = requests.get(BASE + "/", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        old_links = r.text.count("/ai-tool-finder/")
        has_rss = "feed.xml" in r.text.lower() or 'application/rss+xml' in r.text.lower()
        return {"old_links": old_links, "has_rss_reference": has_rss}
    except:
        return {"error": "can't reach site"}

if __name__ == "__main__":
    print(f"=== AI Tool Finder Daily Monitor === {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    failures = check_uptime()
    if failures:
        print(f"\n❌ UPTIME ISSUES ({len(failures)}):")
        for f in failures:
            print(f"   {f}")
    else:
        print("\n✅ All critical pages UP")
    
    deploy = check_deployment()
    if deploy.get("old_links", 0) > 0:
        print(f"❌ {deploy['old_links']} old /ai-tool-finder/ links still in page!")
    else:
        print("✅ No old link remnants")
    
    if deploy.get("has_rss_reference"):
        print("✅ RSS feed reference found")
    else:
        print("⚠️ RSS feed not referenced in homepage")
    
    print("\n📊 Manual checks needed:")
    print("   GSC: https://search.google.com/search-console?resource_id=https://pullnova.com/")
    print("   GA4: https://analytics.google.com/analytics/web/")
    print("   GitHub Actions: https://github.com/lianghuahuang888-dev/ai-tool-finder/actions")
