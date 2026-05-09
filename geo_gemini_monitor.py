#!/usr/bin/env python3
"""GEO Step 4: Monitor if Gemini/AI overviews mention our site for target keywords"""
import requests, json, datetime

TARGET_KEYWORDS = [
    "best AI coding tools 2026",
    "best AI image generator",
    "best AI writing assistant",
    "ChatGPT vs Claude",
    "best free AI tools",
    "AI tools for developers",
    "Cursor vs Copilot",
    "Midjourney alternatives free",
]

SITE_URL = "lianghuahuang888-dev.github.io/ai-tool-finder"

def check_gemini_mention():
    """Check if our site appears in AI search results (via llms.txt signal)"""
    print(f"GEO Monitoring — {datetime.datetime.now():%Y-%m-%d %H:%M}")
    print(f"Site: {SITE_URL}")
    print(f"Keywords tracked: {len(TARGET_KEYWORDS)}")
    print()
    print("Action: Manually query each keyword in Gemini + Perplexity")
    print("Track: Does our site appear in results? If not, what site DOES appear?")
    print()
    for kw in TARGET_KEYWORDS:
        print(f"  [ ] {kw}")

if __name__ == '__main__':
    check_gemini_mention()
