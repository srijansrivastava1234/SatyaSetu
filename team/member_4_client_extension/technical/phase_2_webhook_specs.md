# Phase 2 Architecture: WhatsApp Business Cloud API & Telegram Bot
*Zero-Install Verification Pipeline for Rural & Grassroots Demographics*

---

## 1. The Core Rationale
While power users and fact-checking journalists utilize desktop browsers and Chrome extensions, over 85% of India's misinformation victims interact exclusively via smartphone messaging apps (WhatsApp and Telegram). They will never install a browser extension. Phase 2 integrates SatyaSetu directly into chat applications.

---

## 2. WhatsApp Business Cloud API Integration Flow

```
[ User forwards text/image to SatyaSetu WhatsApp Number ]
                          │
                          ▼
             Meta Graph API Webhook Event
           (POST /webhooks/whatsapp/incoming)
                          │
                          ▼
            [ FastAPI Webhook Ingestion Router ]
                          │
       ┌──────────────────┴──────────────────┐
       │ (If Image / Poster)                 │ (If Text Message)
       ▼                                     ▼
[ OCR Normalization Pipeline ]        [ Atomic Extractor ]
       │                                     │
       └──────────────────┬──────────────────┘
                          │
                          ▼
              [ SatyaSetu Orchestrator ]
        (L1 Cache -> L2 FactCheck API -> L3 NLI)
                          │
                          ▼
     [ Formatted WhatsApp Interactive Card Response ]
  - Verdict Banner: 🚨 FALSE / HOAX
  - 2-Sentence Plain Language Explanation
  - 1-Click "Forward Debunk to Group" Quick-Reply Button
```

---

## 3. Webhook Endpoint Contract (FastAPI Specification)

```python
from fastapi import APIRouter, Request, HTTPException
import httpx

router = APIRouter(prefix="/webhooks/whatsapp")

VERIFY_TOKEN = "satyasetu_secure_webhook_token_2026"
META_WHATSAPP_TOKEN = "your_meta_system_user_token"

@router.get("/")
async def verify_webhook(request: Request):
    """Handles Meta webhook handshake challenge."""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@router.post("/")
async def receive_whatsapp_message(payload: dict):
    """Processes incoming forwarded claims and sends immediate debunk replies."""
    entry = payload.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    message = changes.get("value", {}).get("messages", [{}])[0]
    
    from_number = message.get("from")
    text_body = message.get("text", {}).get("body")
    
    # Process through SatyaSetu Core Orchestrator
    # Send asynchronous response using Meta Graph API messages endpoint
    return {"status": "queued"}
```
