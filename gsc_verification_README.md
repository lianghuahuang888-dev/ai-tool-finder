# Google Search Console Setup Guide

## No Domain Required
GSC can verify via HTML file upload (free GitHub Pages), no paid domain needed.

## Steps:
1. Go to https://search.google.com/search-console
2. Add property: https://lianghuahuang888-dev.github.io/ai-tool-finder
3. Choose "HTML tag" verification method
4. Copy the meta tag provided by GSC (looks like `<meta name="google-site-verification" content="...">`)
5. Add it to index.html <head> section
6. Click "Verify" in GSC

## After Verification:
- Submit sitemap: https://lianghuahuang888-dev.github.io/ai-tool-finder/sitemap.xml
- Check Index coverage
- Monitor Search Analytics (clicks, impressions, CTR, avg position)

## Automated Keyword Tracking:
Once GSC is connected, keyword_strategy.json contains:
- 15 tool pages as primary keywords
- 5 content clusters for traffic scaling
- 4 long-tail opportunities
- GSC-driven eval: drop keywords with avg position > 30 for 6+ months
