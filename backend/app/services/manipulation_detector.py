import re
from typing import List, Dict, Any
from app.models.schemas import ManipulationSignals

# Viral triggers common in WhatsApp misinformation
URGENCY_TRIGGERS = [
    r"urgent", r"immediately", r"share before deleted", r"breaking", r"forward to all",
    r"don't ignore", r"share maximum", r"warning", r"alert", r"आज रात", r"तुरंत",
    r"जल्दी फॉरवर्ड करें", r"सावधान", r"चेतावनी", r"डिलीट होने से पहले", r"सबको भेजो",
    r"emergency", r"viral", r"shocking", r"must watch", r"100% true", r"satya"
]

APPEAL_TO_AUTHORITY_PATTERNS = [
    r"nasa", r"unesco", r"who\b", r"world health organization", r"rbi\b", r"supreme court",
    r"modi", r"prime minister", r"oxford", r"aiims", r"unicef", r"bbc", r"scientist",
    r"डॉक्टर", r"नासा", r"यूनेस्को", r"आरबीआई", r"एम्स"
]

EMOTIONAL_ANGER_FEAR_PATTERNS = [
    r"destroy", r"conspiracy", r"poison", r"danger", r"ban\b", r"arrest", r"kidnap",
    r"threat", r"deadly", r"riot", r"धोखा", r"साजिश", r"खतरा", r"जहर", r"हमला", r"दंगा"
]

SCAM_PHISHING_PATTERNS = [
    r"loan.*without collateral", r"disconnected tonight", r"electricity bill unpaid",
    r"chargeable.*monday", r"send.*to \d+ contacts", r"won \d+ lakh", r"lottery",
    r"update bank account", r"call.*immediately at \d{10}", r"govt-free-.*\.in",
    r"\.(xyz|top|link|tk|ml|ga|cf|gq)\b", r"shut down all private bank"
]

SUBJECTIVE_OPINION_PATTERNS = [
    r"spiritually", r"less stressful", r"healthier than", r"in my opinion",
    r"personally believe", r"better place to live", r"philosophically"
]

def analyze_manipulation_tactics(text: str) -> ManipulationSignals:
    if not text:
        return ManipulationSignals(
            urgency_score=10,
            emotional_intensity=10,
            sensationalism_score=10,
            credibility_index=90,
            detected_tactics=[],
            linguistic_markers=[],
            missing_elements=["No text content provided"]
        )

    lower_text = text.lower()
    detected_tactics = []
    linguistic_markers = []
    missing_elements = []

    # 1. Punctuation & Capitalization sensationalism
    exclamations = text.count("!")
    question_marks = text.count("?")
    caps_count = sum(1 for c in text if c.isupper())
    letters_count = sum(1 for c in text if c.isalpha())
    caps_ratio = (caps_count / letters_count) if letters_count > 0 else 0

    sensational_points = 0
    if exclamations >= 2:
        sensational_points += min(35, exclamations * 10)
        linguistic_markers.append(f"Excessive exclamation marks ({exclamations}x)")
    if question_marks >= 2:
        sensational_points += min(20, question_marks * 8)
        linguistic_markers.append(f"Rhetorical questioning ({question_marks}x)")
    if caps_ratio > 0.35 and len(text) > 30:
        sensational_points += 30
        linguistic_markers.append("Aggressive ALL-CAPS typography")

    # 2. Urgency triggers
    urgency_points = 0
    matched_urgency = []
    for pattern in URGENCY_TRIGGERS:
        if re.search(pattern, lower_text):
            matched_urgency.append(pattern)
            urgency_points += 20
    if matched_urgency:
        detected_tactics.append("Manufactured Panic & Urgency (Forced Viral Loop)")

    # 3. Fabricated or Unverified Authority invocation
    matched_authority = []
    for pattern in APPEAL_TO_AUTHORITY_PATTERNS:
        if re.search(pattern, lower_text):
            matched_authority.append(pattern)
    if matched_authority:
        detected_tactics.append(f"Institutional Name-Dropping ({', '.join(set(matched_authority[:3])).upper()})")

    # 4. Fear / Outrage Induction
    matched_fear = []
    for pattern in EMOTIONAL_ANGER_FEAR_PATTERNS:
        if re.search(pattern, lower_text):
            matched_fear.append(pattern)
    if matched_fear:
        detected_tactics.append("Fear-Mongering & Outrage Bait")

    # 4b. Phishing & Advance Fee Scam Vector
    matched_scam = []
    for pattern in SCAM_PHISHING_PATTERNS:
        if re.search(pattern, lower_text):
            matched_scam.append(pattern)
    if matched_scam:
        detected_tactics.append("Financial / Phishing Deception Vector")
        urgency_points += 35

    # 4c. Subjective Opinion Detection
    matched_opinion = []
    for pattern in SUBJECTIVE_OPINION_PATTERNS:
        if re.search(pattern, lower_text):
            matched_opinion.append(pattern)
    if matched_opinion:
        detected_tactics.append("Subjective Qualitative Opinion (Non-Falsifiable)")

    # 5. Missing Elements of Trustworthy Journalism
    has_date = bool(re.search(r"\b(202[0-9]|january|february|march|april|may|june|july|august|september|october|november|december|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", lower_text))
    has_hyperlink = bool(re.search(r"https?://", text))
    has_source_ref = bool(re.search(r"(press release|gazette|official notification|spokesperson|spokesman|circular no)", lower_text))

    if not has_date:
        missing_elements.append("No publication date or timeline anchor")
    if not has_hyperlink and not has_source_ref:
        missing_elements.append("No primary source citation or verifiable link")
    if "forwarded as received" in lower_text or "forwarded" in lower_text:
        linguistic_markers.append("WhatsApp 'Forwarded' disavowal signature")
        detected_tactics.append("Syndicated Forward Vector")

    # Calculate bounded scores
    urgency_score = min(100, max(5, urgency_points))
    emotional_intensity = min(100, max(10, (len(matched_fear) * 25) + (len(matched_urgency) * 15)))
    sensationalism_score = min(100, max(5, sensational_points + (15 if len(matched_urgency) > 0 else 0)))

    # Composite Credibility Index (Inverse of manipulation metrics)
    risk_aggregate = (urgency_score * 0.35) + (emotional_intensity * 0.35) + (sensationalism_score * 0.30)
    credibility_index = max(5, min(95, int(100 - risk_aggregate)))

    return ManipulationSignals(
        urgency_score=urgency_score,
        emotional_intensity=emotional_intensity,
        sensationalism_score=sensationalism_score,
        credibility_index=credibility_index,
        detected_tactics=detected_tactics,
        linguistic_markers=linguistic_markers,
        missing_elements=missing_elements
    )
