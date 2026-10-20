# Captain Anchor Protocol: 2-Minute Q&A Defense Management
*Speaker A (Member 5): Team Captain Anchor for Judge Interrogation*

---

## 1. The Captain Anchor Rule
Judges often ask questions that prompt multiple team members to speak over each other, creating an impression of disorganization.  
**Strict Protocol**:
1. **Member 5 intercepts every question** from the judges with eye contact.
2. Member 5 delivers a crisp, confident **1-sentence strategic frame**.
3. Member 5 immediately **delegates technical depth** to the designated specialist:
   - Infrastructure, Latency, API Cost, Offline: -> **Member 1**
   - AI, Hallucination, Stance Detection, OCR: -> **Member 2**
   - UI, UX, Accessibility, Telemetry: -> **Member 3**
   - Adoption, Privacy, Scaling, WhatsApp Bot: -> **Member 4**

---

## 2. Delegation Scripts & Routing Matrix

| Judge Question Domain | Member 5 One-Sentence Anchor | Delegation Cue | Designated Speaker |
| :--- | :--- | :--- | :--- |
| **API Costs & Rate Limits** | *"Our cost model is near-zero because 80% of queries hit our local in-memory L1 cache without external API spend."* | *"Member 1, walk the judges through our caching and API fallback layer."* | **Member 1** |
| **Model Hallucination & Accuracy** | *"We do not allow generative guessing; every verdict is constrained by formal Natural Language Inference."* | *"Member 2, explain our NLI premise-hypothesis verification and prompt temperature."* | **Member 2** |
| **OCR for Blurry Photos** | *"We run an adaptive OpenCV preprocessing pipeline before optical extraction."* | *"Member 2, explain our noise-filtering and adaptive binarization."* | **Member 2** |
| **User Privacy & WhatsApp Encryption** | *"SatyaSetu operates on a strict zero-storage architecture with no personal chat logs saved."* | *"Member 4, detail our zero-PII data boundary."* | **Member 4** |
| **Rural Adoption & Literacy** | *"We do not expect users to install complex apps; we meet them directly inside WhatsApp in regional Hindi."* | *"Member 4, outline our Phase 2 WhatsApp Business bot roadmap."* | **Member 4** |
| **Competition Benchmarks** | *"We evaluated SatyaSetu across a 20-case adversarial Indian dataset with 0.0% false positives on real news."* | *(Member 5 answers directly using [`test_dataset.json`](file:///e:/SMS%20HACKATHON/SatyaSetu/test_dataset.json)).* | **Member 5** |

---

## 3. The Golden Rules of Q&A
- **Never defensive**: Acknowledge the judge's insight before framing the engineering countermeasure.
- **Never guess**: If a question probes an unimplemented feature, answer: *"In our current Phase 1 prototype, that is handled via X; our Phase 2 architecture roadmap specifies Y."*
- **Keep answers under 25 seconds**: Keep responses punchy so judges can ask 3-4 questions within the 2-minute limit.
