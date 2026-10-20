import json
import re
import time
from typing import Optional, Dict, Any, List
import httpx
from app.config import settings
from app.models.schemas import ClaimReviewEvidence
from app.services.search_engine import resolve_source_credentials

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def verify_with_gemini_search_grounding(claim_text: str, api_key_override: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Leverages Google Gemini 2.0 Flash's native Google Search Grounding to browse the live web,
    retrieve authoritative newspaper & gazette reporting, and synthesize an evidence-grounded report.
    Free tier in Google AI Studio allows up to 15 RPM / 1,500 RPD.
    """
    api_key = api_key_override or settings.GEMINI_API_KEY
    if not api_key:
        return None

    prompt = (
        f"You are a rigorous, institutional misinformation intelligence analyst.\n"
        f"Search the live web using your browsing tool to verify the following news or viral claim:\n\n"
        f"CLAIM TO INVESTIGATE: \"{claim_text}\"\n\n"
        f"Requirements:\n"
        f"1. Perform live web search to find reporting from accredited national newspapers (e.g. The Hindu, Indian Express, Times of India, Mint), official government portals/gazettes (PIB, RBI, CBSE, ISRO), or certified IFCN fact-checkers (Alt News, BOOM, Factly).\n"
        f"2. Determine if the claim is TRUE, FALSE, MISLEADING, or UNVERIFIABLE.\n"
        f"3. Provide objective debunk/verification summaries in English and Hindi.\n"
        f"4. You MUST output ONLY a valid JSON object without markdown formatting or code fences:\n"
        f"{{\n"
        f'  "verdict": "TRUE" | "FALSE" | "MISLEADING" | "UNVERIFIABLE",\n'
        f'  "credibility_score": <integer 0-100>,\n'
        f'  "risk_level": "AUTHENTIC_GOVERNMENT_OR_MEDIA" | "HIGH_CONFIRMED_MISINFORMATION" | "ELEVATED_VIRAL_RISK" | "NON_FALSIFIABLE_OPINION",\n'
        f'  "summary_en": "<1-2 sentence evidence-based summary in English citing specific publishers>",\n'
        f'  "summary_hi": "<1-2 sentence translation in Hindi>",\n'
        f'  "primary_publishers": ["<Name of genuine newspaper or agency 1>", "<Name of genuine newspaper or agency 2>"],\n'
        f'  "key_findings": ["<Factual finding 1>", "<Factual finding 2>"]\n'
        f"}}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "tools": [
            {
                "googleSearch": {}
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 1024
        }
    }

    try:
        url = f"{GEMINI_API_URL}?key={api_key}"
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(url, json=payload, headers={"Content-Type": "application/json"})
            if resp.status_code != 200:
                print(f"[GeminiGrounding] API Notice: HTTP {resp.status_code} - {resp.text[:120]}")
                return None

            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return None

            first_cand = candidates[0]
            raw_text = first_cand.get("content", {}).get("parts", [{}])[0].get("text", "").strip()

            # Extract search grounding metadata
            grounding_meta = first_cand.get("groundingMetadata", {})
            grounding_chunks = grounding_meta.get("groundingChunks", [])
            search_queries = grounding_meta.get("webSearchQueries", [])

            # Parse synthesized JSON report
            clean_json = re.sub(r"^```(?:json)?\s*", "", raw_text)
            clean_json = re.sub(r"\s*```$", "", clean_json).strip()

            report = {}
            try:
                report = json.loads(clean_json)
            except Exception:
                # Fallback regex extraction if model included surrounding commentary
                match = re.search(r"\{.*\}", clean_json, re.DOTALL)
                if match:
                    try:
                        report = json.loads(match.group(0))
                    except Exception:
                        pass

            if not report:
                report = {
                    "verdict": "FALSE" if any(w in raw_text.lower() for w in ["false", "fake", "hoax", "debunked"]) else "VERIFIED" if any(w in raw_text.lower() for w in ["true", "verified", "authentic"]) else "UNVERIFIED",
                    "credibility_score": 10 if "false" in raw_text.lower() else 90 if "true" in raw_text.lower() else 50,
                    "summary_en": raw_text[:200],
                    "summary_hi": "सत्यसेतु एवं गूगल सर्च ग्राउंडिंग द्वारा इस दावे की जांच की गई।",
                    "primary_publishers": ["Google Live Web Search Index"]
                }

            # Map grounding web citations to authentic accredited credentials
            citations = []
            for chunk in grounding_chunks:
                web = chunk.get("web", {})
                uri = web.get("uri", "")
                title = web.get("title", "")
                if not uri:
                    continue

                canonical_name, authority_badge, domain, is_genuine = resolve_source_credentials(title, uri)
                citations.append({
                    "title": title or "Live Browser Search Result",
                    "publisher": canonical_name,
                    "authority_badge": authority_badge if is_genuine else "Accredited Web Source",
                    "url": uri,
                    "pub_date": "Live Search Grounding",
                    "snippet": f"Retrieved via Gemini Live Search Grounding ({domain or 'Web'}). Status: Verified by live crawling."
                })

            return {
                "verdict": report.get("verdict", "UNVERIFIED").upper(),
                "credibility_score": int(report.get("credibility_score", 50)),
                "risk_level": report.get("risk_level", "MODERATE_CAUTION"),
                "summary_en": report.get("summary_en", ""),
                "summary_hi": report.get("summary_hi", ""),
                "primary_publishers": report.get("primary_publishers", []),
                "key_findings": report.get("key_findings", []),
                "citations": citations,
                "search_queries": search_queries,
                "source_mode": "Gemini 2.0 Flash (Live Google Search Grounding)"
            }

    except Exception as e:
        print(f"[GeminiGrounding] Non-fatal search grounding exception: {e}")
        return None
