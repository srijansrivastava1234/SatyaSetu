# SatyaSetu (सत्यसेतु): TrustAI Digital Misinformation Engine

> **Problem Statement 11 (PS ID: 202611)**: TrustAI: Tackling Digital Misinformation  
> **Pitch Format**: 5 Minutes Presentation + 2 Minutes Q&A  
> **Live Web App**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Quick Start (Run Locally)

### 1. Launch FastAPI Engine & Web UI
```powershell
cd "e:\SMS HACKATHON\SatyaSetu\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser to test the full interface.

---

## Core Capabilities Addressing Problem Statement 11

1. **Multimodal Input Suite (`ClaimInputModal`)**:
   - Supports raw text, WhatsApp chain messages, screenshot posters via OCR, and URLs.
2. **Deterministic Two-Tier Verification Engine**:
   - **Tier 1 (Instant IFCN Match)**: Queries Google Fact Check Tools API (`factchecktools.googleapis.com`) to extract certified ClaimReview schemas from AltNews, BOOM Live, Factly, and PIB Fact Check.
   - **Tier 2 (Authoritative Search RAG)**: Cross-references official gazettes (`pib.gov.in`, `rbi.org.in`, `cbse.gov.in`).
3. **Psychological Manipulation & Deception Telemetry (`ManipulationBreakdown`)**:
   - Manufactured Urgency Score (0-100%).
   - Emotional Outrage/Panic Intensity (0-100%).
   - Sensational Typography & Punctuation abuse (`!!!`, ALL CAPS).
   - Missing Journalistic Anchors (No circular number, no date, no source link).
4. **WhatsApp Viral Neutralizer & Chat Simulator (`WhatsAppSimulator`)**:
   - Live chat thread simulator showing the incoming rumor bubble alongside the SatyaSetu debunk card.
   - 1-click **"Copy English Debunk"** and **"Copy Hindi Debunk"** buttons with WhatsApp markdown ready to forward back into family groups.
5. **S.A.T.Y.A. Citizen Pre-Forwarding Protocol (`VerificationChecklist`)**:
   - Actionable 4-step checklist guiding citizens on how to verify before sharing.
