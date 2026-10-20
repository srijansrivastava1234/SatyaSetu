# Ethics, Transparency & Zero-Hallucination NLI Architecture
*Presenter Notes & Talking Points for Model Ethics & Trust*

---

## The Core Philosophy: "NLI Stance Grounding vs. Generative Hallucination"

### 1. The Fundamental Problem with Generic LLMs
Most AI fact-checkers fail because they treat verification as a **creative text generation** problem. When you ask ChatGPT or standard Gemini, "Is this WhatsApp message true?", the model relies on internal parametric memory. If it has never seen the claim, it guesses or produces plausible-sounding hallucinations with high confidence.

### 2. The SatyaSetu Solution: Natural Language Inference (NLI)
SatyaSetu strictly decouples **Retrieval** from **Reasoning**:
- The LLM is **never** asked whether a claim is true in the abstract.
- The LLM is supplied with two strictly defined inputs:
  1. **Premise**: Real-time retrieved evidence from certified fact-checkers (AltNews, BOOM, PIB) or official government circulars.
  2. **Hypothesis**: The user's claim extracted from WhatsApp text or OCR.
- The LLM's task is reduced to formal mathematical stance classification:
  - Does the Premise **Entail** the Hypothesis? (`VERIFIED`)
  - Does the Premise **Contradict** the Hypothesis? (`FALSE`)
  - Is the Premise **Insufficient** to prove or disprove? (`UNVERIFIABLE`)

### 3. The "Right to Remain Silent" (Unverifiable Policy)
If no authoritative institutional record exists, SatyaSetu refuses to fabricate a verdict. It outputs `UNVERIFIABLE` alongside a transparency disclaimer:
> *"No certified fact-check record or official gazette confirms this claim. We advise citizens not to forward unverified information."*

### 4. Regional Linguistic Inclusivity
- Rural Indian misinformation thrives in Indic languages (Hindi, Hinglish, Marathi, Tamil).
- SatyaSetu extracts semantic claims across languages using Gemini's native multilingual embeddings, and returns twin WhatsApp rebuttals in both plain English and regional Hindi.
