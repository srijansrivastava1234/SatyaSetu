# SatyaSetu (सत्यसेतु) — Complete Stage Presentation Master Guide
**Event**: RotaTech 2026 | **Problem Statement ID**: 202611 (TrustAI: Tackling Digital Misinformation)  
**Team Name**: HexaDevs / SatyaSetu  
**Presentation Deck**: [`HexaDevs-SMS.pptx`](file:///e:/SMS%20HACKATHON/SatyaSetu/HexaDevs-SMS.pptx)  
**Total Presentation Time**: 4 Minutes Hard Stop + 2 Minutes Jury Q&A  

---

## Stage Timing & Member Roster

```
[0:00 - 0:45] (45s) Speaker 1: Anshika Pandey    --> Slide 1: Title & The 500M Victim Problem
[0:45 - 1:30] (45s) Speaker 2: Suryansh Pandey   --> Slide 2: Why Rumors Spread & 4 Solution Steps
[1:30 - 2:20] (50s) Speaker 3: Srijan Srivastava --> Slide 3: 3-Tier Technical Engine & Zero Guessing
[2:20 - 3:05] (45s) Speaker 4: Amit Kumar Rajput --> Slide 4: 100% Benchmark Score & Risk Defense
[3:05 - 3:55] (50s) Speaker 5: Akhilesh Sharma   --> Slides 5 & 6: Grassroots Impact, 1-to-256 Loop & References
[3:55 - 4:00] (05s) Transition to Stage Jury Q&A
[4:00 - 6:00] (2m)  All Members                  --> Jury Defense Protocol
```

---

## SLIDE 1: Title Page & Executive Overview

![Slide 1 Screenshot](../docs/presentation_screenshots/ppt_slides/slide_1.png)

### Speaker & Slide Details
* **Speaker**: **Anshika Pandey** (Team Leader & Lead Anchor)
* **Time**: `0:00 – 0:45` (~45 Seconds)
* **3-Word Memory Anchor**: **Pension Scam ➔ 500M People ➔ SatyaSetu**

### What is on This Slide
* Event title: **ROTATECH 2026**
* Problem Statement ID: **202611** | Title: **TrustAI (Tackling Digital Misinformation)**
* Theme: **Digital Trust & Misinformation**
* Team Name: **HexaDevs**
* Complete 5-member team roster and operational responsibilities

### Word-for-Word Simple Script to Say
> "Respected judges, imagine an elderly grandfather in a small village.
> 
> He gets a forwarded WhatsApp message:  
> *'URGENT: Free Government Laptop Scheme ends tonight. Click here to register.'*
> 
> Wanting to help his granddaughter study, he clicks the link, types his bank details, and within five minutes, all his pension savings are stolen.
> 
> This does not happen once in a while. It happens every single day to over **500 million WhatsApp users** across India.
> 
> People fall for it because nobody reads long news articles before forwarding. And standard AI chatbots often make up fake facts.
> 
> That is why we built **SatyaSetu**. It is a simple, zero-lie verification tool that gives instant, bilingual truth cards right where rumors spread.
> 
> To explain how fake news spreads and how we stop it, here is **Suryansh**."

---

## SLIDE 2: Idea Title & Proposed Solution

![Slide 2 Screenshot](../docs/presentation_screenshots/ppt_slides/slide_2.png)

### Speaker & Slide Details
* **Speaker**: **Suryansh Pandey** (AI Vision & Multimodal Lead)
* **Time**: `0:45 – 1:30` (~45 Seconds)
* **3-Word Memory Anchor**: **Fake Panic ➔ Read Screenshot ➔ Truth Card**

### What is on This Slide
* **The Problem Cycle**: Fabricated Claim ➔ Manufactured Urgency ➔ Zero Source Anchors ➔ Blind Panic Forwarding
* **SatyaSetu's 4 Solution Steps**:
  1. *Reads Any Screenshot*: OpenCV cleans blurry WhatsApp images and reads text.
  2. *Checks Real Fact-Checkers*: Queries PIB, AltNews, and BOOM Live in real time.
  3. *Measures the Danger*: Deception telemetry gauges for Urgency %, Outrage %, and Missing Circulars %.
  4. *Makes a 1-Click Truth Card*: Polite Hindi/English rebuttal cards for instant sharing.

### Word-for-Word Simple Script to Say
> "Thank you, Anshika. On Slide 2, you can see how rumors trick people.
> 
> A scammer writes a scary message with fake urgency like *'Forward to 10 people immediately'*, with zero official links. People panic and forward it blindly.
> 
> **SatyaSetu stops this in four simple steps**:
> 
> 1. **Reads Any Screenshot**: Users don't type text. They just send blurry WhatsApp screenshots. Our tool cleans the image and reads the text instantly.
> 2. **Checks Real Fact-Checkers**: We search verified organizations like PIB Fact Check, AltNews, and BOOM Live in less than a second.
> 3. **Measures the Danger**: Our meters show how much fake urgency and emotional drama is inside the message.
> 4. **Makes a 1-Click Truth Card**: We create a polite card in Hindi and English. Users can paste it straight back into their family groups to calm everyone down.
> 
> To explain our backend technology, here is our architect, **Srijan**."

---

## SLIDE 3: Technical Approach & Verification Pipeline

![Slide 3 Screenshot](../docs/presentation_screenshots/ppt_slides/slide_3.png)

### Speaker & Slide Details
* **Speaker**: **Srijan Srivastava** (Full-Stack System Architect)
* **Time**: `1:30 – 2:20` (~50 Seconds)
* **3-Word Memory Anchor**: **Fast Cache ➔ Govt Sites ➔ Zero Guessing**

### What is on This Slide
* **FastAPI Backend Pipeline**:
  - **Tier 1 (Instant Cache)**: Local SQLite WAL cache, resolves repeat rumors in <15ms at zero cost.
  - **Tier 2 (IFCN Desks)**: Queries Google Fact Check Tools API with Schema.org ClaimReview.
  - **Tier 3 (Government Gazettes)**: Real-time scraper checking `pib.gov.in`, `rbi.org.in`, and Google News RSS.
* **The Zero-Hallucination AI Rule**: Strict Natural Language Inference (NLI) constraint (temp=0.1). If evidence is missing, it outputs `UNVERIFIABLE`.

### Word-for-Word Simple Script to Say
> "Thank you, Suryansh. On Slide 3, here is how our engine works:
> 
> We built a 3-layer system:
> 
> - **Layer 1 (Instant Memory)**: 80% of WhatsApp rumors are the exact same repeated hoaxes. Our system remembers them and answers in **under 15 milliseconds** at **zero cost**.
> - **Layer 2 (Certified Fact Desks)**: For new claims, we check international fact-checking databases in under half a second.
> - **Layer 3 (Official Government Portals)**: For breaking news, our live engine checks real government websites like `pib.gov.in` and `rbi.org.in`.
> 
> Most importantly, we have one golden rule for our AI: **It is strictly forbidden from guessing.**
> 
> If there is no official proof, it simply says: **UNVERIFIABLE**. This guarantees 100% honesty.
> 
> To share our test results, here is **Amit**."

---

## SLIDE 4: Feasibility and Viability (Benchmarks & Risk Matrix)

![Slide 4 Screenshot](../docs/presentation_screenshots/ppt_slides/slide_4.png)

### Speaker & Slide Details
* **Speaker**: **Amit Kumar Rajput** (Fact-Checking Architect & Safety Lead)
* **Time**: `2:20 – 3:05` (~45 Seconds)
* **3-Word Memory Anchor**: **100% Score ➔ Works Offline ➔ Safe Data**

### What is on This Slide
* **Empirical Benchmark Numbers**:
  - `100.0%`: Accuracy rate across 20 adversarial edge cases.
  - `0.0%`: False alarm rate (authentic government gazettes never wrongly marked).
  - `<15 ms`: In-memory cached lookup speed.
  - `2.2 s`: Total cold web investigation speed.
* **4 Real-World Mitigations**:
  - *No Wi-Fi*: Local loopback (`127.0.0.1:8000`) offline mode.
  - *API Outages*: Local regex scam heuristics and deception scoring.
  - *Privacy*: Zero-storage stateless architecture (no phone numbers or chats saved).
  - *Cost*: 80% free cache hits; novel AI checks cost just 4 paise.

### Word-for-Word Simple Script to Say
> "Thank you, Srijan. On Slide 4, here are our real test results:
> 
> We tested SatyaSetu against 20 difficult real-world cases, including banking scams, medical rumors, and real government notices:
> - **100% Detection Rate**: We caught every single hoax and scam.
> - **Zero False Alarms**: Real news from PIB and ISRO was never wrongly marked as fake.
> 
> We also designed it for real-world risks:
> 1. **No Wi-Fi in the hall?** No problem. Our system runs fully offline on our laptop.
> 2. **Outside APIs down?** It keeps working using smart built-in scam filters.
> 3. **What about privacy?** We store zero phone numbers, zero chats, and zero personal data.
> 4. **What about cost?** Because 80% of searches use our free memory cache, each check costs just 4 paise.
> 
> To show our impact on real people, here is **Akhilesh**."

---

## SLIDE 5: Impact and Benefits (Grassroots Scale & Viral Loop)

![Slide 5 Screenshot](../docs/presentation_screenshots/ppt_slides/slide_5.png)

### Speaker & Slide Details
* **Speaker**: **Akhilesh Sharma** (Frontend & UI Lead)
* **Time**: `3:05 – 3:35` (~30 Seconds)
* **3-Word Memory Anchor**: **Senior Citizens ➔ 1-to-256 Loop ➔ Real Truth**

### What is on This Slide
* **Target Beneficiaries**:
  - Rural citizens in Tier-2/3 India
  - Senior citizens targeted by utility disconnection and pension frauds
  - WhatsApp family and community group admins
* **The 1-to-256 WhatsApp Viral Loop**:
  - 1 user verifies a claim ➔ 1 bilingual truth card shared ➔ 255 group members protected simultaneously.
* **Channels**: Responsive Web App, Chrome Extension, Phase 2 WhatsApp Business Helpline.

---

## SLIDE 6: Research and References

![Slide 6 Screenshot](../docs/presentation_screenshots/ppt_slides/slide_6.png)

### Speaker & Slide Details
* **Speaker**: **Akhilesh Sharma** (Continues to Conclude Deck)
* **Time**: `3:35 – 3:55` (~20 Seconds)
* **What is on This Slide**:
  - **Academic NLP Grounding**: Vaswani et al. (Transformers), Thorne et al. (FEVER benchmark), Kiela et al. (Multimodal reasoning).
  - **Verified Government Registries**: Press Information Bureau (PIB), Reserve Bank of India (RBI), CBSE, UNESCO.
  - **Open Data Standards**: Schema.org ClaimReview, Poynter IFCN Code of Principles.

### Word-for-Word Simple Script to Say (Slides 5 & 6 Together)
> "Thank you, Amit. Slide 5 shows who SatyaSetu protects:
> - **Rural Citizens** who only use WhatsApp.
> - **Senior Citizens** targeted by fake power-cut warnings and pension frauds.
> - **Family Group Admins** who want polite facts to stop arguments.
> 
> Now look at our **1-to-256 Viral Loop**:
> When one person checks a rumor and pastes our truth card back into their 256-person group, **one single check protects 255 people at the same time!**
> 
> Our web app and Chrome extension are live right now. Next, we are launching our direct WhatsApp helpline number.
> 
> *(Referencing Slide 6)*: Everything we do is backed by verified standards from PIB, RBI, and international fact-checking guidelines.
> 
> Fake news spreads fast because it plays with fear. With SatyaSetu, the truth is finally faster, easier, and free for everyone.
> 
> We are Team HexaDevs. Thank you!"

---

## 2-MINUTE JURY Q&A DEFENSE PROTOCOL

**Dispatcher Rule**: **Anshika** catches every question first, buys 3 seconds, and immediately directs it to the right specialist:

1. **"Does your AI hallucinate or generate false information?"**  
   ➔ **Route to Suryansh / Srijan**:  
   *"No. Our AI is mathematically locked down using Natural Language Inference with temperature 0.1. It is strictly forbidden from guessing. If official proof is not found in government gazettes, it outputs UNVERIFIABLE."*

2. **"How does the system handle high traffic or slow internet?"**  
   ➔ **Route to Srijan**:  
   *"80% of WhatsApp rumors are repeats. Our local SQLite WAL cache answers them in under 15 milliseconds without needing external APIs. We also run an async connection pool in FastAPI."*

3. **"How do you ensure fact-checking sources are unbiased?"**  
   ➔ **Route to Amit**:  
   *"We exclusively whitelist organizations certified by the International Fact-Checking Network (IFCN) under the Poynter Code of Principles, and cross-reference them directly against official government gazettes at pib.gov.in."*

4. **"How will rural citizens who don't know technology use this?"**  
   ➔ **Route to Akhilesh**:  
   *"They don't have to download any heavy app. Whenever someone checks a rumor, they share our simple Hindi truth card back into their WhatsApp group. One person educates 255 people."*

5. **"What about user privacy and data security?"**  
   ➔ **Route to Anshika**:  
   *"We enforce a zero-storage architecture. We store zero phone numbers, zero chats, and zero personal profiles. All checks are processed as stateless hashes."*
