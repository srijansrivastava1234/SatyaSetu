# SatyaSetu (सत्यसेतु)
### Multi-Tier Digital Misinformation Intelligence & Fact-Checking Engine

[![Live Deployment](https://img.shields.io/badge/Live%20Demo-satyasetu--wtpy.onrender.com-0284c7.svg)](https://satyasetu-wtpy.onrender.com)
[![CI Pipeline](https://github.com/srijansrivastava1234/SatyaSetu/actions/workflows/ci.yml/badge.svg)](https://github.com/srijansrivastava1234/SatyaSetu/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/database-SQLite%20WAL-003B57.svg)](https://www.sqlite.org/)
[![Chrome Extension](https://img.shields.io/badge/extension-Manifest%20V3-brightgreen.svg)](https://developer.chrome.com/docs/extensions/mv3/intro/)
[![IFCN Grounded](https://img.shields.io/badge/standards-IFCN%20ClaimReview-orange.svg)](https://ifcncodeofprinciples.poynter.org/)

SatyaSetu is an institutional-grade disinformation intelligence platform designed to detect, deconstruct, and neutralize deceptive viral content across regional communications networks. It combines high-throughput deterministic fact-checking archives, authoritative government gazette retrieval, psychological manipulation signal extraction, and localized counter-messaging generation.

---

## Architecture Overview

```
                      +-----------------------------------+
                      |      Multi-Modal Ingestion       |
                      |  Web Portal | REST | Chrome Ext   |
                      +-----------------+-----------------+
                                        |
                                        v
                      +-----------------------------------+
                      |   SQLite High-Speed Cache (WAL)   |
                      |   SHA-256 Keyed / Query Telemetry  |
                      +--------+-----------------+--------+
                               |                 |
                         (Cache Hit)       (Cache Miss)
                               |                 |
                               |                 v
                               |     +---------------------------+
                               |     | Multi-Tier Verification   |
                               |     |                           |
                               |     | [Tier 1: IFCN Archive]    |
                               |     | Google FactCheck ClaimRev |
                               |     | AltNews/BOOM/PIB Factly   |
                               |     |                           |
                               |     | [Tier 2: Realtime Ground] |
                               |     | Google News RSS / Tavily  |
                               |     | Gazette Domain Filtering  |
                               |     | (pib/rbi/cbse/eci.gov.in) |
                               |     |                           |
                               |     | [Tier 3: Manipulation     |
                               |     |  Telemetry & Synthesis]   |
                               |     | LLM Reasoning & Scoring   |
                               |     +-------------+-------------+
                               |                   |
                               +---------> + <-----+
                                           |
                                           v
                      +-----------------------------------+
                      |     Consolidated Intelligence     |
                      | - Verdict & Credibility Score     |
                      | - Manipulation Signal Breakdown   |
                      | - Dual-Language Debunk (EN / HI)  |
                      | - One-Click WhatsApp Neutralizer  |
                      | - S.A.T.Y.A. Citizen Checklist    |
                      +-----------------------------------+
```

---

## Core Capabilities

### 1. Deterministic Two-Tier Verification
- **Tier 1 (Instant IFCN Archive Match)**: Queries the Google Fact Check Tools API (`factchecktools.googleapis.com`) to extract certified ClaimReview metadata from signatories of the International Fact-Checking Network (Alt News, BOOM Live, Factly, PIB Fact Check, Quint WebQoof).
- **Tier 2 (Authoritative Search & Gazette RAG)**: Queries live news feeds and official gazettes (`pib.gov.in`, `rbi.org.in`, `cbse.gov.in`, `eci.gov.in`) with strict topical keyword overlap filters to eliminate false-negative hallucinations on breaking news and regulatory circulars.

### 2. Psychological Manipulation & Deception Telemetry
Evaluates linguistic vectors characteristic of viral dis- and misinformation:
- **Manufactured Urgency Index** (0–100%): Detects artificial time constraints and panic cues (*"immediately"*, *"forward before midnight"*).
- **Emotional Outrage / Panic Score** (0–100%): Measures sentiment agitation calibrated against calm journalistic baselines.
- **Sensational Typography**: Flagging excessive exclamation chains, ALL-CAPS text blocks, and fear triggers.
- **Source Anchor Absence**: Identifies missing circular numbers, unattributed citations, and fabricated authorities.

### 3. Localized Viral Counter-Messaging & Visual Truth Cards
- **Dual-Language Debunks**: Produces human-verified, concise refutations in English and Hindi (`debunk_summary_en` and `debunk_summary_hi`).
- **One-Click WhatsApp Forwarding**: Outputs formatted text cards designed for instant copy-pasting directly into family and community chat threads to halt virality at the peer level.
- **1-Click Truth Card Image Generator**: Client-side HTML5 canvas synthesis generating downloadable PNG truth cards formatted for WhatsApp Status and social media debunking.
- **Full Bilingual UI Toggle**: 1-click `EN ⇋ हिन्दी` toggle instantly localizing dashboard headlines, gauges, and checklist items.

### 4. Multimodal & Audio Voice Note Ingestion
- **Messy Screenshot OCR**: Adaptive thresholding and Otsu binarization for low-resolution WhatsApp forward screenshots.
- **WhatsApp Voice Note Ingestion**: Integrated Web Speech API audio recognition transcribing Hindi and English voice notes into structured verification queries.

### 5. High-Performance SQLite WAL Caching & Telemetry
- **SHA-256 Cache Engine**: All verified claims are indexed by cryptographic digest, providing sub-5ms response times for repeated queries.
- **Audit Telemetry**: Comprehensive query logging tracking verdict distributions, pipeline latency, and cache hit ratios.

---

## Repository Structure

```
SatyaSetu/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI router definitions
│   │   ├── models/          # Strict Pydantic schemas
│   │   ├── services/        # Fact-check, search, OCR & LLM pipeline
│   │   ├── static/          # Modular institutional web UI (Zero build steps)
│   │   │   ├── css/app.css  # Production CSS design tokens & responsive layout
│   │   │   ├── js/app.js    # Client state, keyboard shortcuts & telemetry polling
│   │   │   └── index.html   # Accessible, semantic dashboard
│   │   ├── config.py        # Environment configuration
│   │   ├── database.py      # SQLite WAL persistence & audit logger
│   │   └── main.py          # Application entrypoint & static mount
│   ├── tests/               # Pytest automated test suite
│   ├── test_system.py       # 20-case precision benchmark runner
│   ├── requirements.txt     # Python production dependencies
│   └── .env.example         # Environment template
├── extension/               # Chrome Extension (Manifest V3)
│   ├── manifest.json        # Extension configuration
│   ├── background.js        # Service worker & context-menu hooks
│   ├── popup.html           # Extension browser action interface
│   ├── popup.css            # Extension styling
│   └── popup.js             # Extension client logic
└── tools/
    └── deck_utils/          # Utility scripts for presentation generation
```

---

## Quick Start & Local Development

### Prerequisites
- Python 3.11 or higher
- Google Gemini API key (recommended for synthesis; rule-based fallbacks activate when absent)
- Google Fact Check Tools API key (optional; search grounding activates automatically)

### 1. Environment Setup

```bash
cd backend
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Copy the environment template and populate your keys:
```bash
cp .env.example .env
```

### 2. Run the Engine

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The application is accessible at:
- **Web Interface**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **OpenAPI Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### 3. Load the Chrome Extension

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in upper right corner).
3. Click **Load unpacked** and select the `extension/` directory.
4. Pin SatyaSetu to your toolbar. Highlight any text on the web and click **Verify with SatyaSetu**.

---

## Automated Testing & Benchmarks

### 1. Integration & Unit Test Suite (`pytest`)
Executes unit tests validating endpoint contracts, HTTP validation, and SQLite WAL caching:

```bash
cd backend
python -m pytest tests/test_api.py -v
```

### 2. 20-Scenario Precision Benchmark Suite
Runs rigorous evaluation against real-world misinformation vectors (WhatsApp panic chains, fake RBI circulars, UNESCO award hoaxes, public health rumors, and legitimate government announcements):

```bash
cd backend
python test_system.py
```

Target evaluation criteria:
- **Sensitivity (Misinformation Detection)**: > 95%
- **Specificity (Legitimate Control Verification)**: 100%
- **Average Pipeline Latency**: < 1,500ms (Cold) / < 5ms (Cached)

---

## API Specification

### `POST /api/verify`
Analyzes a submitted claim through the multi-tier verification pipeline.

**Request Body:**
```json
{
  "text": "UNESCO has officially declared Jana Gana Mana as the best national anthem.",
  "language": "en"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "overall_verdict": "FALSE",
  "credibility_score": 8,
  "risk_level": "CRITICAL_DISINFORMATION",
  "atomic_claims": [
    {
      "id": 1,
      "text": "UNESCO officially declared India's national anthem as the best in the world",
      "target_entity": "UNESCO",
      "normalized_query": "UNESCO declared Jana Gana Mana best national anthem award"
    }
  ],
  "certified_evidence": [
    {
      "fact_checker": "AltNews",
      "claim_text": "UNESCO declared Jana Gana Mana as the best national anthem in the world",
      "rating": "False",
      "review_url": "https://www.altnews.in/unesco-declares-jana-gana-mana-best-national-anthem/",
      "is_ifcn_certified": true
    }
  ],
  "manipulation_breakdown": {
    "urgency_score": 88,
    "emotional_intensity": 75,
    "sensational_typography": true,
    "missing_source_anchor": true
  },
  "debunk_summary_en": "UNESCO has repeatedly clarified that it does not organize competitions or confer awards for national anthems.",
  "debunk_summary_hi": "यूनेस्को (UNESCO) ने बार-बार स्पष्ट किया है कि वह राष्ट्रगानों के लिए कोई प्रतियोगिता या पुरस्कार जारी नहीं करता है।",
  "is_cached": false,
  "total_latency_ms": 1180,
  "data_source_mode": "Certified Fact-Check Archive (Tier 1 Direct Match)"
}
```

### `GET /api/stats`
Returns system-level telemetry and database cache metrics.

```json
{
  "database_backend": "SQLite (WAL Mode)",
  "total_verifications_logged": 42,
  "cached_unique_claims": 20,
  "cache_savings_hits": 14,
  "avg_pipeline_latency_ms": 320.4,
  "verdict_distribution": {
    "FALSE": 35,
    "TRUE": 5,
    "MISLEADING": 2
  }
}
```

---

## License & Compliance
This software is provided under the MIT License. Fact-checking data retrieved via the ClaimReview schema conforms to IFCN standards and Google Fact Check Tools API terms of service.
