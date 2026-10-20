# Slide 3: 3-Tier Multi-Source Retrieval & Low-Latency Architecture
*Presenter Notes for Slide 3 (Backend & Data Pipeline Flow)*

---

## 1. Visual Flow Diagram (For PPT/Figma)

```
[ Incoming User Query / Screenshot OCR / URL ]
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│     TIER 1: In-Memory Certified Canonical Cache        │
│     • Latency: < 15ms                                  │
│     • Hit Condition: Pre-indexed viral WhatsApp hoaxes │
└───────────────────────┬────────────────────────────────┘
                        │ Miss
                        ▼
┌────────────────────────────────────────────────────────┐
│     TIER 2: Google Fact Check Tools API (IFCN Desk)    │
│     • Latency: 250 - 450ms                             │
│     • Schema: ClaimReview (AltNews, BOOM, PIB Fact)    │
└───────────────────────┬────────────────────────────────┘
                        │ Low Confidence / Novel Claim
                        ▼
┌────────────────────────────────────────────────────────┐
│     TIER 3: Authoritative Gazette RAG & NLI Engine     │
│     • Latency: 800 - 1400ms                            │
│     • Target Sources: pib.gov.in, rbi.org.in, cbse...  │
│     • Model: Gemini 2.5 Flash Natural Language Infer.  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Key Slide Bullet Points (Verbatim for Slide Text)
1. **Multi-Tier Retrieval Strategy**:
   - Zero-latency serving for known viral hoaxes via our in-memory L1 cache.
   - Authoritative fact-checking verification via the Google Fact Check Tools API (certified IFCN signatories).
   - Domain-restricted gazette retrieval for novel claims.
2. **Sub-Second Performance**:
   - Asynchronous non-blocking architecture powered by FastAPI and HTTPX.
   - Live stage telemetry showing transparent breakdown of retrieval vs synthesis latency.
3. **Resilience & Fault Tolerance**:
   - Dual search fallbacks to prevent single-point-of-failure if an API is throttled or offline.
   - Complete zero-network local regex and heuristic fallback mode.
