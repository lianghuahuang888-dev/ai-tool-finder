#!/usr/bin/env python3
"""AI Tool Finder Daily Monitoring - Run once per day"""
import requests, json, time, sys
from datetime import datetime

BASE = "https://lianghuahuang888-dev.github.io/ai-tool-finder"
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
    import argparse
    p = argparse.ArgumentParser(description="AI Tool Finder Daily Monitor")
    p.add_argument("--schedule", action="store_true", help="Run continuously, checking every 24h at 08:00")
    p.add_argument("--audit", action="store_true", help="Also run GEO audit and log score")
    p.add_argument("--oneshot", action="store_true", help="Run once and exit (default)")
    args = p.parse_args()
    
    if args.schedule:
        print("Daily Monitor started — will run every 24h at 08:00. Press Ctrl+C to stop.")
        import threading
        def daily_check():
            while True:
                now = datetime.now()
                target = now.replace(hour=8, minute=0, second=0, microsecond=0)
                if now >= target:
                    target = target.replace(day=target.day + 1)
                wait = (target - now).total_seconds()
                print(f"Next check: {target.strftime('%Y-%m-%d %H:%M')} (in {wait/3600:.1f}h)")
                time.sleep(wait)
                run_checks(args.audit)
        t = threading.Thread(target=daily_check, daemon=True)
        t.start()
        t.join()
    else:
        run_checks(args.audit or args.oneshot)
    
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
    print("   GSC: https://search.google.com/search-console?resource_id=https://lianghuahuang888-dev.github.io/ai-tool-finder/")
    print("   GA4: https://analytics.google.com/analytics/web/")
    print("   GitHub Actions: https://github.com/lianghuahuang888-dev/ai-tool-finder/actions")
