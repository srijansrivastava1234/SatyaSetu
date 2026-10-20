# Member 4 Technical Runbook: Chrome Extension & Web Client Bridge

## 1. Machine Environment Checklist (Laptop 4)
- [ ] Google Chrome or Microsoft Edge browser installed
- [ ] Working directory: `e:\SMS HACKATHON\SatyaSetu\extension`
- [ ] Backend running on `http://127.0.0.1:8000` (or accessible over local hotspot)

---

## 2. Loading Manifest V3 Extension in Developer Mode
1. Open Google Chrome and navigate to: `chrome://extensions/`
2. Toggle on **"Developer mode"** in the top-right corner.
3. Click **"Load unpacked"** in the top-left toolbar.
4. Select the folder: `e:\SMS HACKATHON\SatyaSetu\extension`
5. Verify that **"SatyaSetu: TrustAI Misinformation Verifier"** appears in the extensions list with version `1.0.0`.

---

## 3. DOM & WhatsApp Web Context Menu Testing
1. Navigate to [web.whatsapp.com](https://web.whatsapp.com) or any news article / blog.
2. Highlight a suspicious claim (e.g., *"UNESCO declared Jana Gana Mana best anthem"*).
3. Right-click the highlighted text -> Select **"Verify with SatyaSetu"**.
4. Check behavior:
   - The background service worker sends an async POST request to `http://127.0.0.1:8000/api/verify`.
   - The verification verdict is stored into `chrome.storage.local`.
   - The extension badge updates: Displays a red **"!"** for `FALSE` claims, or a green **"✓"** for `VERIFIED`.
   - Clicking the extension icon opens `popup.html` displaying the full veracity breakdown and 1-click copy debunk button.

---

## 4. Debugging Background Service Worker
- In `chrome://extensions/`, click **"service worker"** under SatyaSetu.
- DevTools window opens:
  - Check the Console tab for network calls to `http://127.0.0.1:8000/api/verify`.
  - Check Application -> Storage -> Local Storage to inspect saved verification payloads.
