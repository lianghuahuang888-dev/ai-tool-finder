# 🤖 AI Model Food Source Map — 2026 Edition
## How Each Major AI Model Gets Its Data & How to Get Cited

Research compiled 2026-05-09. Sources: Google AI Overviews, xAI Docs, Pixelmojo, Trakkr, 2POINT Agency, Erlin AI.

---

## 1. Gemini (Google) — The Reddit Feeder
| Attribute | Detail |
|-----------|--------|
| **Search Backend** | Google Search Index |
| **Unique Source** | Reddit data (Google pays Reddit $60M/yr) |
| **Citation Style** | Inline in AI Overviews + Gemini responses |
| **Overlap** | ✅ Google Ranking → Gemini citation (direct pipeline) |
| **Key Signals** | EEAT, schema markup, Reddit presence |

**How to get cited:**
- Google-indexed content ✅ (sitemap, robots.txt)
- Reddit answers with comparison format
- AI-friendly schema (featureList, Review, FAQPage)
- llms.txt file for crawler directives

---

## 2. ChatGPT / GPT (OpenAI) — The Bing + Authority Feeder
| Attribute | Detail |
|-----------|--------|
| **Search Backend** | **Bing** (73-87% overlap with Bing results) |
| **Top Sources** | Wikipedia, YouTube, Reddit, news media |
| **Citation Rate** | Only 6.8-7.8% of Bing top-3 results get cited |
| **Authority Threshold** | 32,000+ referring domains → **3.5x more likely cited** |
| **Content Format** | "Answer Capsules" — 50-150 words after H2 headers |
| **Bot** | GPTBot (user-agent in robots.txt) |
| **Tools** | Bing Webmaster Tools, Bing AI Performance Report |

**How to get cited (priority order):**
1. **Bing Webmaster Tools** — Register & submit sitemap (🔴 CRITICAL)
2. **Answer Capsules** — Direct 50-150 word answers after every H2
3. **Schema** — FAQPage + HowTo + Article (3+ types = 13% higher citation)
4. **Authority** — Wikipedia mention, LinkedIn verified, media coverage
5. **Data Density** — 19+ data points per article → higher citation rates
6. **GPTBot** — Allow in robots.txt
7. **Refresh** — Monthly content updates favored

**Our project gaps:**
- ❌ NOT registered in Bing Webmaster Tools
- ❌ No GPTBot directive in robots.txt
- ❌ Low <a href="https://www.drlinkcheck.com" target="_blank" rel="noopener">referring domains</a> (GitHub Pages = 0 domain authority)
- 🟡 Schema present but only 1-2 types per page

---

## 3. Grok (xAI) — The X/Twitter + Real-Time Feeder
| Attribute | Detail |
|-----------|--------|
| **Search Backend** | Web search + **X/Twitter** (exclusive) |
| **Unique Source** | X posts, trending topics, X account classifications |
| **Citation Style** | Inline + Source list (API accessible) |
| **Quality Issue** | **>50% of cited URLs are fabricated** (hallucination) |
| **Key Driver** | First authoritative voice on trending topic = default citation |
| **Account System** | X accounts have classification tiers |

**How to get cited:**
1. **Active X account** — Must have verified, active presence on X
2. **Trending topics** — Post when topic is first emerging (first-mover advantage)
3. **X account classification** — Ask Grok: "Which classification does my @handle have?"
4. **Web presence** — Standard SEO + schema still helps for web search component
5. **Real-time data** — Grok values recency more than authority

**Our project gaps:**
- ❌ No X/Twitter account linked to the project
- ❌ No real-time content strategy

---

## 4. Perplexity — The Multi-Backend Aggregator
| Attribute | Detail |
|-----------|--------|
| **Search Backend** | Multiple search engines (Google, Bing, proprietary) |
| **Citation Style** | Inline numbered citations + source sidebar |
| **Coverage** | ChatGPT dominates 78% of AI traffic; Perplexity is #2 |
| **Key Signal** | Content quality + structural clarity |

**How to get cited:**
- Standard web indexing (Google + Bing)
- Clear, well-structured answers
- Authoritative sources preferred
- Fresh content favored

---

## 5. Claude (Anthropic) — The Web Search + Training Data Hybrid
| Attribute | Detail |
|-----------|--------|
| **Search Backend** | Web search (when enabled by user) + training data |
| **Citation** | Cites sources when using web search |
| **Bot** | ClaudeBot / anthropic-ai (already in our robots.txt ✅) |
| **Key Signal** | Training data quality matters (not just live search) |

**How to get cited:**
- ClaudeBot already allowed ✅
- Content in training data corpus
- Web search optimization (similar to Bing/Google SEO)

---

## 6. DeepSeek
| Attribute | Detail |
|-----------|--------|
| **Search Backend** | Web search (when enabled) |
| **Citation** | Source links in responses |
| **Key Signal** | Chinese + English content coverage |

---

## 🔥 PRIORITY ACTION PLAN — Maximize Coverage Across ALL Models

| Priority | Action | Models Covered | Effort |
|:---:|------|------|:---:|
| 🔴 P0 | **Register in Bing Webmaster Tools** + submit sitemap | ChatGPT, Perplexity, Claude | Low |
| 🔴 P0 | **Add GPTBot to robots.txt** | ChatGPT | 1 line |
| 🟡 P1 | **Create X/Twitter account** @aitoolfinder + post weekly | Grok | Medium |
| 🟡 P1 | **Add Answer Capsules** (50-150 word direct answers after H2) | ChatGPT, Perplexity | Medium |
| 🟡 P1 | **Boost referring domains** — get links from blogs, directories | ChatGPT (authority signal) | High |
| 🟢 P2 | Wikipedia mention | ChatGPT (authority signal) | High |
| 🟢 P2 | Data density: 19+ data points per comparison post | ChatGPT | Low |

---

## 📊 Coverage Matrix

| Channel | Gemini | ChatGPT | Grok | Perplexity | Claude |
|---------|:------:|:-------:|:----:|:----------:|:------:|
| Google Index | ✅ | ✅ | - | ✅ | ✅ |
| Bing Index | - | ✅ | - | ✅ | ✅ |
| X/Twitter | - | - | ✅ | - | - |
| Reddit | ✅ | ✅ | - | - | - |
| Schema Markup | ✅ | ✅ | - | ✅ | - |
| llms.txt | ✅ | - | - | - | ✅ |
| robots.txt crawl | ✅ | ✅ | ✅ | ✅ | ✅ |