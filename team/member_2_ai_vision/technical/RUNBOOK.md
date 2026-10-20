# Member 2 Technical Runbook: AI Engine, OCR & Benchmark Evaluation

## 1. Machine Environment Checklist (Laptop 2)
- [ ] Python 3.10+ installed
- [ ] Windows Tesseract OCR binary installed:
  - Path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- [ ] Dependencies installed:
  ```powershell
  pip install google-genai pytesseract pillow opencv-python pydantic httpx
  ```
- [ ] `GEMINI_API_KEY` set in environment or `.env`

---

## 2. Gemini 2.5 Flash SDK Integration & NLI Prompting
- **Engine Configuration**:
  - Model: `gemini-2.5-flash`
  - Temperature: `0.1` (Grounded strictly in retrieved evidence).
- **Natural Language Inference (NLI) Stance Contract**:
  - Strict categorical stances: `FALSE`, `VERIFIED`, `UNVERIFIABLE`.
  - Zero-hallucination requirement: Model must quote an exact snippet from the retrieved context.

---

## 3. OCR Pre-Flight & Diagnostics (Tesseract on Windows)
1. **File Owned**: [`backend/ocr_engine.py`](file:///e:/SMS%20HACKATHON/SatyaSetu/backend/ocr_engine.py)
2. **Pre-processing**: Grayscale -> Otsu binarization -> Median blur.
3. **Execution Command**:
   ```powershell
   python "e:\SMS HACKATHON\SatyaSetu\team\member_2_ai_vision\technical\test_ocr_ai.py"
   ```

---

## 4. Automated Benchmark Evaluation Runner (Reassigned to Member 2)
Member 2 is the custodian of model accuracy and runs the 20-case benchmark test suite after every code change:
```powershell
cd "e:\SMS HACKATHON\SatyaSetu\backend"
python test_system.py --eval
```
- **Accuracy Target**: >= 95.0%
- **False Positive Target on Real News**: 0.0%
- **Latency Profiling**:
  - Cache hits: < 25ms
  - Cold RAG: < 1200ms
