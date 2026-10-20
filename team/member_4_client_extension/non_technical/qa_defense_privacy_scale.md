# Member 4 Q&A Battle-Card: Privacy, Encryption & Grassroots Scale
*Target Judge Focus: User Privacy, Chat Archiving, Data Protection, Low-Bandwidth Networks*

---

### Question 1: "Does SatyaSetu read or store private WhatsApp chats and metadata?"
**Direct Answer**:
> "Absolutely not. SatyaSetu adheres strictly to zero-storage privacy by design. When a user highlights text or forwards a message, only the isolated factual claim is transmitted to our verification API. No contact books, no user phone numbers, no chat histories, and no personal identifying information (PII) are ever logged or persisted to disk. Furthermore, incoming text is stripped of names and phone numbers via regex before reaching our inference layer."

---

### Question 2: "How does the system perform on low-bandwidth 2G/3G connections in rural areas?"
**Direct Answer**:
> "Our client payloads are micro-optimized: an API verification request is less than 1 kilobyte of compressed JSON. If an image is uploaded on a weak connection, client-side downscaling shrinks the image to 800x800 resolution before transmission, reducing payload size by over 80%. When network speed is severely degraded, the client can fall back to plain-text SMS or lightweight USSD verification queries."

---

### Question 3: "How do you achieve mass adoption without huge marketing spend?"
**Direct Answer**:
> "Our adoption mechanism is inherently viral and self-distributing. Every time a citizen uses SatyaSetu to debunk a rumor in a 256-person WhatsApp group, that debunk card acts as a free, organic product demonstration to 255 other citizens. One debunked rumor turns into dozens of new users without a single rupee spent on paid customer acquisition."
