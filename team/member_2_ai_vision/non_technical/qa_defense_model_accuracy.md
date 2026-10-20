# Member 2 Q&A Battle-Card: Model Stance, Accuracy & OCR
*Target Judge Focus: False Positives, Hallucination Prevention, OCR Noise, Regional Nuance*

---

### Question 1: "How do you guarantee that your model does not hallucinate false verdicts?"
**Direct Answer**:
> "We enforce a zero-generative policy through strict Natural Language Inference. The model is given temperature 0.1 and a Pydantic schema constraint where every verdict (`FALSE`, `VERIFIED`, `UNVERIFIABLE`) must cite an exact verbatim snippet from the retrieved evidence. If there is no grounding evidence in the retrieval payload, the system is architected to default to `UNVERIFIABLE`. The model is mathematically barred from inventing facts not present in the retrieved premise."

---

### Question 2: "What is your false positive rate, especially for satire or opinion pieces?"
**Direct Answer**:
> "Across our 20-case benchmark dataset, our false positive rate on factual claims is 0.0%. For satire or rhetorical opinion, SatyaSetu utilizes our psychological manipulation detector to score emotional valence and factual anchors. If a statement is clearly editorial commentary without a falsifiable factual claim, the system labels it as 'Opinion/Unverifiable' rather than falsely condemning it as a deliberate hoax."

---

### Question 3: "How does your OCR handle compressed, pixelated WhatsApp screenshots?"
**Direct Answer**:
> "Raw screenshots from WhatsApp have severe JPEG artifacting and variable compression. Before piping images into Tesseract or Gemini Vision, we run an adaptive OpenCV pipeline: grayscale normalization, Otsu's adaptive binarization, and median noise suppression. If optical confidence drops below 65%, the UI explicitly alerts the user with an 'Unclear Image' warning and prompts them to paste raw text or a higher-resolution crop."
