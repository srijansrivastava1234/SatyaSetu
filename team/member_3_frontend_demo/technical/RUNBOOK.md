# Member 3 Technical Runbook: Stage Presentation Laptop (Laptop 3)

## 1. Laptop 3 Hardware & Display Pre-Flight
- [ ] Connect HDMI / USB-C to projector:
  - Set Display Mode: **Duplicate / Mirror Displays** (`Win + P` -> "Duplicate").
  - Target Resolution: `1920x1080` @ 60Hz.
- [ ] Chrome / Edge Browser Settings:
  - Set default browser zoom to **125%** or **150%** so judges at the back of the auditorium can clearly read latency badges and debunk cards.
  - Disable browser notifications & Do Not Disturb (`Win + Focus Assist` -> On).
  - Pre-approve clipboard write permissions: Click lock icon on URL bar -> Clipboard: **Allow**.

---

## 2. Browser Tab Unification (`Ctrl + Tab` Protocol)
Do not fiddle with window resizing or minimizing on stage. Set up two full-screen tabs in a single browser window:
- **Tab 1**: Presentation Slide Deck (Figma / PDF / PPT in web presentation mode).
- **Tab 2**: SatyaSetu Web Interface ([http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:5173/](http://localhost:5173/)).
- **Stage Transition**: When Speaker A says *"Let us see how SatyaSetu stops a viral rumor in real time..."* (Minute 1:10), press `Ctrl + Tab` once to transition seamlessly into the live app.

---

## 3. UI Telemetry & Visual State Verification
1. **Telemetry Badge Dynamic States**:
   - Check that the latency badge renders properly:
     - `⚡ 12ms [CACHE HIT: INSTANT TIER 1]` (Green background)
     - `🌐 840ms [LIVE RAG SYNTHESIS: TIER 3]` (Blue background)
2. **Psychological Manipulation Breakdown**:
   - Ensure the gauge dials animate smoothly:
     - Urgency Score (High: Red)
     - Emotional Outrage Score (Amber/Red)
     - Missing Journalistic Anchors badge
3. **WhatsApp Simulator & Clipboard Action**:
   - Click **"Copy English Debunk"** -> Confirm green toast: *"Debunk text copied to clipboard! Ready to paste in WhatsApp."*
   - Click **"Copy Hindi Debunk"** -> Confirm clipboard contains clean WhatsApp formatting (`*सत्यसेतु फैक्ट चेक*`).

---

## 4. Emergency Offline Local Hosting
If Laptop 1 Wi-Fi drops, Laptop 3 can run the backend locally on port 8000:
```powershell
cd "e:\SMS HACKATHON\SatyaSetu\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Then load [http://127.0.0.1:8000/](http://127.0.0.1:8000/) directly.
