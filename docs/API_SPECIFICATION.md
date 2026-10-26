# SatyaSetu REST API Specification

This document details the public API surface exposed by the SatyaSetu backend engine (`FastAPI`). All endpoints adhere to JSON request and response payloads with standard HTTP status code semantics.

---

## Base URL
* **Development:** `http://localhost:8000`
* **Production:** `https://satyasetu-wtpy.onrender.com`

---

## Endpoints Summary

| Method | Endpoint | Description | Auth Required | Cacheable |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/verify` | Submit claim text or base64 image for verification | No | Yes (SHA-256) |
| `GET` | `/api/health` | Service health status and version | No | No |
| `GET` | `/api/scenarios` | Pre-configured test scenario catalog | No | Static |
| `GET` | `/api/stats` | Telemetry, cache hit rates, database status | No | No |
| `GET` | `/api/history` | Chronological verification logs | No | No |

---

## 1. Verify Claim

### `POST /api/verify`
Runs the multi-tier disinformation verification pipeline:
1. **Cache Lookup:** Computes SHA-256 hash of normalized text/image. If cached, returns instant verified response.
2. **Deconstruction:** Extracts atomic verifiable propositions and detects manipulation tactics (urgency, sensationalism, authority name-dropping).
3. **Evidence Retrieval:** Queries IFCN ClaimReview archives (Google Fact Check Tools API) and authorized governmental sources.
4. **Debunk Synthesis:** Formulates credibility score, verdict, dual-language debunk cards (EN / HI), and WhatsApp-ready counter-messaging.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Body (`VerifyRequest`)
```json
{
  "text": "UNESCO has declared the Indian National Anthem as the best anthem in the world.",
  "image_base64": null,
  "language": "en"
}
```

* **`text`** *(string, optional)*: Raw claim text or message forward. Required if `image_base64` is omitted.
* **`image_base64`** *(string, optional)*: Base64 data URL or raw base64 string of infographic or forwarded image.
* **`language`** *(string, default: "en")*: Target language code (`en`, `hi`).

#### Response Body (`VerificationResponse`) - HTTP 200 OK
```json
{
  "status": "success",
  "overall_verdict": "FALSE",
  "credibility_score": 15,
  "risk_level": "CRITICAL",
  "is_cached": false,
  "extracted_text": "UNESCO has declared the Indian National Anthem as the best anthem in the world.",
  "atomic_claims": [
    {
      "id": 1,
      "text": "UNESCO has declared the Indian National Anthem as the best anthem in the world.",
      "normalized_query": "UNESCO Indian National Anthem best",
      "target_entity": "UNESCO"
    }
  ],
  "manipulation_breakdown": {
    "urgency_score": 25,
    "emotional_intensity": 20,
    "sensationalism_score": 35,
    "credibility_index": 70,
    "detected_tactics": [
      "Institutional Name-Dropping (UNESCO)"
    ],
    "linguistic_markers": [],
    "missing_elements": [
      "No publication date or timeline anchor",
      "No primary source citation or verifiable link"
    ]
  },
  "certified_evidence": [
    {
      "claim_text": "UNESCO declared Jana Gana Mana as best anthem",
      "claimant": "WhatsApp Viral Post",
      "fact_checker": "BOOM Live",
      "rating": "False",
      "review_date": "2021-08-15",
      "review_url": "https://www.boomlive.in/...",
      "is_ifcn_certified": true
    }
  ],
  "shareable_card": {
    "headline_en": "FALSE: UNESCO Did NOT Declare Indian National Anthem Best in the World",
    "headline_hi": "गलत: यूनेस्को ने राष्ट्रगान को सर्वश्रेष्ठ घोषित नहीं किया",
    "verdict": "FALSE",
    "bullet_points_en": [
      "UNESCO has repeatedly clarified no such announcement or contest exists.",
      "The message is a recurring viral hoax circulating since 2008."
    ],
    "bullet_points_hi": [
      "यूनेस्को ने स्पष्ट किया है कि ऐसी कोई घोषणा नहीं की गई है।",
      "यह 2008 से प्रसारित होने वाला पुराना फर्जी संदेश है।"
    ],
    "whatsapp_format_text_en": "*FACT CHECK: FALSE* ❌\n...",
    "whatsapp_format_text_hi": "*सत्यता जांच: गलत* ❌\n...",
    "verification_source_tag": "SatyaSetu Certified Multi-Tier Verification"
  },
  "satya_action_guide": [
    {
      "letter": "S",
      "title": "Stop Forwarding",
      "instruction": "Do not circulate this message further."
    }
  ],
  "pipeline_steps": [
    {
      "name": "Deconstruction",
      "status": "completed",
      "detail": "Extracted 1 atomic claims",
      "elapsed_ms": 32
    }
  ]
}
```

#### Error Codes
* `400 Bad Request`: When neither `text` nor `image_base64` is provided.
* `422 Unprocessable Entity`: Request body validation error (Pydantic schema failure).
* `500 Internal Server Error`: Unhandled pipeline exception.

---

## 2. Health & Uptime

### `GET /api/health`
Returns service availability, execution mode, and active version tag.

#### Response Body - HTTP 200 OK
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-10-26T12:00:00Z"
}
```

---

## 3. Scenario Catalog

### `GET /api/scenarios`
Retrieves pre-configured scenario benchmarks categorized by disinformation vectors (e.g. Health Myths, Financial Scams, Institutional Hoaxes).

#### Response Body - HTTP 200 OK
```json
{
  "scenarios": [
    {
      "id": "scenario_unesco_anthem",
      "title": "UNESCO Best Anthem Hoax",
      "category": "Institutional Impersonation",
      "expected_verdict": "FALSE",
      "sample_text": "UNESCO has declared the Indian National Anthem as the best..."
    }
  ]
}
```

---

## 4. Telemetry & Analytics

### `GET /api/stats`
Returns system metrics from the SQLite persistence layer including total verifications processed and cache hit counts.

#### Response Body - HTTP 200 OK
```json
{
  "total_verifications_logged": 142,
  "cached_unique_claims": 89,
  "cache_savings_hits": 53,
  "database_backend": "SQLite (WAL Mode)"
}
```

---

## 5. Audit History

### `GET /api/history`
Retrieves recent verification transactions.

#### Query Parameters
* `limit` *(integer, optional, default: 20)*: Number of records to return (1-100).

#### Response Body - HTTP 200 OK
```json
{
  "history": [
    {
      "id": 1,
      "query_hash": "a1b2c3d4...",
      "claim_preview": "UNESCO has declared...",
      "verdict": "FALSE",
      "credibility_score": 15,
      "created_at": "2026-10-26T12:15:00"
    }
  ]
}
```
