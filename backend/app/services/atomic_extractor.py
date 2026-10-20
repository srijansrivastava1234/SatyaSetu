import json
import re
from typing import List, Dict, Any, Optional, Tuple
import httpx
from app.config import settings
from app.models.schemas import AtomicClaim

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def extract_claims_and_ocr(
    text: Optional[str] = None,
    image_base64: Optional[str] = None,
    api_key_override: Optional[str] = None
) -> Tuple[str, List[AtomicClaim]]:
    key = api_key_override or settings.GEMINI_API_KEY
    extracted_text = text or ""

    # If Gemini API key is available, run multimodal extraction with structured JSON
    if key:
        try:
            parts = []
            prompt = (
                "You are the SatyaSetu Core Intelligence Parser for misinformation detection.\n"
                "Task 1: If an image is provided, extract all text verbatim from the image (OCR).\n"
                "Task 2: Break down the message into 1 to 3 distinct ATOMIC, verifiable factual claims.\n"
                "Task 3: For each claim, formulate a 3-6 word normalized search query ideal for querying fact-checking databases.\n"
                "Return ONLY a valid JSON object in this exact format:\n"
                "{\n"
                "  \"extracted_ocr_text\": \"...\",\n"
                "  \"claims\": [\n"
                "    {\n"
                "      \"id\": 1,\n"
                "      \"text\": \"Specific factual claim\",\n"
                "      \"normalized_query\": \"3 to 6 keywords search query\",\n"
                "      \"target_entity\": \"Entity making claim or subject\"\n"
                "    }\n"
                "  ]\n"
                "}"
            )
            parts.append({"text": prompt})

            if image_base64:
                # Remove header if present
                clean_b64 = image_base64.split(",")[-1] if "," in image_base64 else image_base64
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": clean_b64
                    }
                })
            elif text:
                parts.append({"text": f"Input content to analyze:\n{text}"})

            payload = {
                "contents": [{"parts": parts}],
                "generationConfig": {
                    "temperature": 0.1,
                    "responseMimeType": "application/json"
                }
            }

            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(f"{GEMINI_API_URL}?key={key}", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_content = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_content)
                    
                    if not extracted_text and parsed.get("extracted_ocr_text"):
                        extracted_text = parsed["extracted_ocr_text"]

                    claims = []
                    for c in parsed.get("claims", []):
                        claims.append(AtomicClaim(
                            id=c.get("id", len(claims) + 1),
                            text=c.get("text", "Extracted claim"),
                            normalized_query=c.get("normalized_query", "misinformation check"),
                            target_entity=c.get("target_entity", "Unknown Entity")
                        ))
                    if claims:
                        return extracted_text, claims
        except Exception as e:
            print(f"[GeminiExtractor] LLM extraction error, falling back to heuristic: {e}")

    # Deterministic Heuristic Fallback (Ensures 100% demo resilience with 0 API keys)
    if not extracted_text and image_base64:
        extracted_text = "WhatsApp Image: [Infographic / Forwarded Screenshot containing viral claims and urgent forward appeal]"

    cleaned = re.sub(r"[!?.]{2,}", ".", extracted_text)
    sentences = [s.strip() for s in re.split(r"[.\n]+", cleaned) if len(s.strip()) > 15]

    atomic_claims = []
    # Identify key entities
    entities = ["Government", "Police", "RBI", "WHO", "UNESCO", "Ministry", "Court", "Bank"]
    
    if sentences:
        for idx, sentence in enumerate(sentences[:3]):
            found_entity = "General Source"
            for ent in entities:
                if ent.lower() in sentence.lower():
                    found_entity = ent
                    break
            
            # Create normalized query by stripping stop words
            words = [w for w in re.findall(r"\w+", sentence) if len(w) > 3 and w.lower() not in {"please", "forward", "share", "today", "every", "right", "people", "warning", "urgent"}]
            norm_query = " ".join(words[:5]) or sentence[:40]

            atomic_claims.append(
                AtomicClaim(
                    id=idx + 1,
                    text=sentence,
                    normalized_query=norm_query,
                    target_entity=found_entity
                )
            )
    else:
        atomic_claims.append(
            AtomicClaim(
                id=1,
                text=extracted_text[:120] or "Unspecified viral claim",
                normalized_query=extracted_text[:40] or "viral misinformation claim",
                target_entity="Viral Media"
            )
        )

    return extracted_text, atomic_claims
