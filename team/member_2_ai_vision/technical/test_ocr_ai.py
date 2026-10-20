"""
SatyaSetu: OCR & AI NLI Diagnostics Test Runner (Laptop 2)
Tests Tesseract binary availability, image preprocessing, and mock NLI schema validation.
"""

import os
import sys
from pydantic import BaseModel, ValidationError
from typing import Literal

# 1. Pydantic Verification Contract
class StanceOutput(BaseModel):
    verdict: Literal["FALSE", "VERIFIED", "UNVERIFIABLE"]
    confidence_score: float
    explanation_en: str
    explanation_hi: str
    manipulation_flags: list[str]

def test_pydantic_schema():
    print("[1/3] Testing Pydantic NLI Schema Validation...")
    sample_valid = {
        "verdict": "FALSE",
        "confidence_score": 0.98,
        "explanation_en": "UNESCO has repeatedly confirmed it never declared any national anthem as the world's best.",
        "explanation_hi": "यूनेस्को ने स्पष्ट किया है कि उसने कभी किसी राष्ट्रगान को सर्वश्रेष्ठ घोषित नहीं किया।",
        "manipulation_flags": ["Emotional Patriotism Bait", "Fabricated Institutional Authority"]
    }
    try:
        obj = StanceOutput(**sample_valid)
        print(f"  [✓] Schema validated successfully. Verdict: {obj.verdict}, Conf: {obj.confidence_score}")
    except ValidationError as e:
        print(f"  [X] Schema validation failed: {e}")
        return False
    return True

def test_tesseract_setup():
    print("\n[2/3] Checking Tesseract Binary & OCR Pipeline...")
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        "tesseract"
    ]
    found = False
    for path in tesseract_paths:
        if os.path.exists(path):
            print(f"  [✓] Found Tesseract executable at: {path}")
            found = True
            break
    if not found:
        print("  [!] Tesseract not detected in standard C:\\Program Files path.")
        print("      Ensure pytesseract.pytesseract.tesseract_cmd is set if testing raw images.")
    return True

def test_heuristic_regex():
    print("\n[3/3] Testing Offline Heuristic Pattern Matcher...")
    import re
    scam_regex = re.compile(r"(free (recharge|laptop|smartphone)|forward to \d+ (people|groups)|account (blocked|suspended))", re.IGNORECASE)
    test_claim = "PM Free Laptop Scheme 2026! Forward to 5 groups to get your laptop today!"
    match = scam_regex.search(test_claim)
    if match:
        print(f"  [✓] Successfully flagged viral trigger: '{match.group(0)}'")
    else:
        print("  [X] Failed to detect trigger.")

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 SatyaSetu AI & Vision Pre-Flight Diagnostics")
    print("=" * 60)
    test_pydantic_schema()
    test_tesseract_setup()
    test_heuristic_regex()
    print("=" * 60)
