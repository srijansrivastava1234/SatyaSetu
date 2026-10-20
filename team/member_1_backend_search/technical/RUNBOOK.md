# Member 1 Technical Runbook: Backend & Search Engine

## 1. Machine Environment Checklist (Laptop 1)
- [ ] Python 3.10+ installed and added to system `PATH`
- [ ] Working directory: `e:\SMS HACKATHON\SatyaSetu\backend`
- [ ] Dependencies installed:
  ```powershell
  pip install fastapi uvicorn httpx pydantic python-dotenv duckduckgo_search
  ```
- [ ] Environment file `.env` configured in `backend/`:
  ```env
  GOOGLE_FACTCHECK_API_KEY=your_google_api_key_here
  GEMINI_API_KEY=your_gemini_api_key_here
  PORT=8000
  HOST=127.0.0.1
  ```

---

## 2. Server Lifecycle Management
### Command to Start Server
Run the production Uvicorn instance bound strictly to local loopback:
```powershell
cd "e:\SMS HACKATHON\SatyaSetu\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Note: Binding to `127.0.0.1` ensures that stage demo machines connecting locally or via a local mobile hotspot will never suffer timeouts from external venue Wi-Fi.*

### Verifying Service Health
In a secondary terminal or browser:
```powershell
curl http://127.0.0.1:8000/docs
```
Confirm the OpenAPI documentation renders and all endpoints are responsive.

---

## 3. Cache Layer & Latency Target (< 20ms)
- **Mechanism**: The backend leverages `SESSION_CACHE` and pre-warmed canonical keys inside `app/services/seed_scenarios.py` and `app/services/orchestrator.py`.
- **Pre-warming Procedure**: Before stepping on stage, fire curl requests for the 3 demo claims to guarantee warm memory cache:
  ```powershell
  python "e:\SMS HACKATHON\SatyaSetu\team\member_1_backend_search\technical\verify_backend.py"
  ```
- Any repeated stage query will return in `< 20ms` with the telemetry response header `X-Cache-Hit: true`.

---

## 4. Search Retrieval Pipeline & Fallbacks
1. **Tier 1 (Google Fact Check Tools API)**:
   - File: [`backend/search_engine.py`](file:///e:/SMS%20HACKATHON/SatyaSetu/backend/search_engine.py)
   - Function: `query_factcheck_tools(query, api_key)`
   - Timeout threshold: `3.5s` max.
2. **Tier 2 (DuckDuckGo Fallback & Authoritative Gazettes)**:
   - Function: `fallback_web_search(query)`
   - Direct querying restricted to certified domains (`pib.gov.in`, `rbi.org.in`, `altnews.in`, `boomlive.in`).
3. **Tier 3 (Zero-Network Synthetic Cache)**:
   - If both external network searches throw timeouts, the orchestrator gracefully degrades to the local regex scam database and pre-computed credibility scores without crashing.

---

## 5. Stage Emergency Contingency Drill
- **Issue**: Port 8000 is occupied or blocked by another process.
  - **Resolution**:
    ```powershell
    netstat -ano | findstr :8000
    taskkill /PID <PID> /F
    ```
- **Issue**: Google Fact Check Tools API returns HTTP 429 (Rate Limit).
  - **Resolution**: Backend automatically suppresses the error and routes the query to `fallback_web_search` and pre-computed scenario seeds.
