import urllib.parse
import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Any, Optional, Tuple
import httpx
from app.models.schemas import ClaimReviewEvidence

DEBUNK_KEYWORDS = {
    "fake", "hoax", "debunk", "fact check", "factcheck", "fact-check",
    "false", "myth", "busted", "misleading", "denies", "fraud",
    "scam", "warns", "warning", "counterfeit", "rumour", "rumor",
    "does not", "did not", "no such", "not true", "bogus", "untrue", "clarifies"
}

TRUSTED_NEWS_SOURCES = {
    "the hindu", "indian express", "times of india", "hindustan times",
    "ndtv", "isro", "pib", "rbi", "cbse", "businessline", "economic times",
    "livemint", "ani", "pti", "dd news", "news on air", "akashvani",
    "reuters", "bbc", "bloomberg", "the wire", "business standard"
}

FACTCHECK_PUBLISHERS = {
    "alt news", "boom", "pib fact check", "factly", "the quint",
    "india today fact check", "vishvas news", "newschecker", "logically facts"
}

STOP_WORDS = {
    "please", "forward", "share", "today", "yesterday", "tomorrow",
    "every", "all", "this", "that", "with", "from", "have", "will",
    "been", "into", "their", "about", "which", "there", "under"
}

async def search_live_grounding(query: str) -> Dict[str, Any]:
    clean_query = re.sub(r"[!?,.:;\"']+", " ", query).strip()
    words = [w for w in clean_query.split() if len(w) > 2 and w.lower() not in STOP_WORDS]
    search_q = " ".join(words[:7]) or clean_query[:50]

    # Specific non-generic keywords from the claim to ensure topical relevance
    specific_keywords = set(w.lower() for w in words if len(w) > 3 and w.lower() not in {"government", "official", "india", "people", "minister"})

    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(search_q)}&hl=en-IN&gl=IN&ceid=IN:en"
    
    articles = []
    debunks: List[ClaimReviewEvidence] = []
    authentic_items: List[Dict[str, Any]] = []

    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            res = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SatyaSetu/1.0"})
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                for item in root.findall(".//item")[:15]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_elem = item.find("pubDate")
                    source_elem = item.find("source")

                    title = title_elem.text if title_elem is not None else ""
                    link = link_elem.text if link_elem is not None else ""
                    pub_date = pub_elem.text if pub_elem is not None else ""
                    source_name = source_elem.text if source_elem is not None else "National Media"

                    if not title:
                        continue

                    lower_title = title.lower()
                    lower_source = source_name.lower()

                    has_debunk_kw = any(k in lower_title for k in DEBUNK_KEYWORDS)
                    is_factchecker = any(fp in lower_source for fp in FACTCHECK_PUBLISHERS)
                    is_debunk = has_debunk_kw or (is_factchecker and ("check" in lower_title or "claim" in lower_title))
                    is_trusted = any(s in lower_source for s in TRUSTED_NEWS_SOURCES) or is_factchecker

                    # Topical overlap check: does the news title actually address the claim's core subjects?
                    title_words = set(re.findall(r"\w+", lower_title))
                    overlap_count = len(specific_keywords.intersection(title_words))

                    item_dict = {
                        "title": title,
                        "url": link,
                        "source": source_name,
                        "pub_date": pub_date,
                        "is_debunk": is_debunk,
                        "is_trusted": is_trusted,
                        "overlap": overlap_count
                    }
                    articles.append(item_dict)

                    if is_debunk:
                        debunks.append(
                            ClaimReviewEvidence(
                                claim_text=title,
                                claimant="Viral Social Media / WhatsApp",
                                fact_checker=source_name,
                                rating="False / Debunked",
                                review_date=pub_date[:16] if pub_date else "Recent",
                                review_url=link,
                                is_ifcn_certified=any(fp in lower_source for fp in FACTCHECK_PUBLISHERS)
                            )
                        )
                    elif is_trusted and overlap_count >= 2:
                        authentic_items.append(item_dict)
    except Exception as e:
        print(f"[SearchEngine] Live grounding query notice: {e}")

    citations = []
    for art in articles[:4]:
        citations.append({
            "title": art["title"],
            "publisher": art["source"],
            "url": art["url"],
            "snippet": f"Published coverage ({art['pub_date'][:16] if art['pub_date'] else 'Current'}). Status: {'[Fact-Check Debunk]' if art['is_debunk'] else '[Institutional News Reporting]'}"
        })

    return {
        "articles": articles,
        "debunks": debunks,
        "authentic_items": authentic_items,
        "citations": citations,
        "has_debunk": len(debunks) > 0,
        "has_authentic_coverage": len(authentic_items) >= 2,
        "total_results": len(articles)
    }
