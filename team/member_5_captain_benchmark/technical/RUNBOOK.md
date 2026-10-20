# Member 5 Technical Runbook: Benchmark Evaluation & System Testing

## 1. Machine Environment Checklist (Laptop 5)
- [ ] Python 3.10+ installed
- [ ] Dependencies installed:
  ```powershell
  pip install httpx tabulate
  ```
- [ ] Backend running on `http://127.0.0.1:8000` (hosted by Member 1)

---

## 2. Running Automated System Evaluation
Execute the benchmark harness against the 20-case dataset:
```powershell
cd "e:\SMS HACKATHON\SatyaSetu\backend"
python test_system.py --eval
```
Or directly from the Member 5 directory:
```powershell
python "e:\SMS HACKATHON\SatyaSetu\team\member_5_captain_benchmark\technical\test_system.py"
```

---

## 3. Metrics Reported by Benchmark Harness
- **Overall Accuracy**: Target >= 95%
- **False Positive Rate**: Target <= 0.0% (Real news must never be flagged as hoaxes)
- **Mean Cache Hit Latency**: Target < 25ms
- **Mean Cold Synthesis Latency**: Target < 1200ms
- **Confusion Matrix Breakdown**: True Positives (Hoaxes correctly caught), True Negatives (Authentic news verified).

---

## 4. Adversarial Stress Testing Procedure
Before the final pitch, Member 5 feeds 5 adversarial edge cases to test resilience:
1. **Noisy Text**: Insert random typos and duplicate punctuation (`!!! ???`).
2. **Hinglish Slang**: Test transliterated WhatsApp messages (`"bhai ye sach hai kya forwarded as received"`).
3. **Truncated Claims**: Test claims missing subjects to ensure graceful `UNVERIFIABLE` fallback rather than 500 Internal Server Errors.
4. **URL Domain Spoofs**: Test lookalike domains like `pib-gov-in.site` or `rbi-update.co.in`.
