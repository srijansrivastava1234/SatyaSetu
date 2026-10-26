import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from app.services.manipulation_detector import analyze_manipulation_tactics
from app.services.atomic_extractor import extract_claims_and_ocr
from app.services.factcheck_engine import query_google_factcheck


def test_manipulation_empty_text():
    """Verify that analyzing empty or whitespace-only text returns safe defaults."""
    res = analyze_manipulation_tactics("")
    assert res.credibility_index == 90
    assert "No text content provided" in res.missing_elements

    res_none = analyze_manipulation_tactics(None)
    assert res_none.credibility_index == 90


def test_manipulation_urgency_and_sensationalism():
    """Verify detection of excessive capitalization, exclamations, and urgent forwarding appeals."""
    viral_text = (
        "URGENT WARNING!!! SHARE IMMEDIATELY TO ALL YOUR CONTACTS BEFORE IT IS DELETED!! "
        "NASA AND UNESCO CONFIRMED THIS DEADLY POISON IN TAP WATER! DO NOT DRINK!"
    )
    res = analyze_manipulation_tactics(viral_text)

    assert res.urgency_score >= 40
    assert res.sensationalism_score >= 30
    assert res.emotional_intensity >= 30
    # Ensure detected tactics and linguistic markers flagged
    tactic_names = res.detected_tactics
    assert any("Panic" in name or "Urgency" in name for name in tactic_names)
    assert any("Institutional" in name or "Authority" in name or "Name-Dropping" in name for name in tactic_names)
    assert any("Fear-Mongering" in name or "Outrage" in name for name in tactic_names)

    markers = res.linguistic_markers
    assert any("exclamation" in m.lower() for m in markers)
    assert any("all-caps" in m.lower() for m in markers)


def test_manipulation_phishing_and_scam_patterns():
    """Verify detection of predatory financial and scam hooks."""
    scam_text = (
        "Dear customer, your electricity bill is unpaid. Connection will be disconnected tonight. "
        "Update bank account immediately at http://govt-free-subsidy.xyz or won 25 lakh lottery will expire!"
    )
    res = analyze_manipulation_tactics(scam_text)

    tactic_names = res.detected_tactics
    assert any("Scam" in name or "Phishing" in name for name in tactic_names)


def test_manipulation_neutral_factual_statement():
    """Verify that measured, non-sensational text produces low manipulation scores."""
    clean_text = (
        "The Reserve Bank of India announced a 25 basis point change in the benchmark repo rate "
        "following the monetary policy committee meeting on Friday."
    )
    res = analyze_manipulation_tactics(clean_text)

    assert res.urgency_score <= 20
    assert res.sensationalism_score <= 20
    assert res.emotional_intensity <= 20
    assert res.credibility_index >= 75


@pytest.mark.asyncio
async def test_atomic_extractor_heuristic_fallback():
    """Ensure heuristic extractor decomposes sentences into atomic claims without LLM key."""
    raw_message = (
        "UNESCO has declared the Indian National Anthem as the best anthem in the world. "
        "The announcement was made during the annual cultural summit in Geneva yesterday."
    )
    extracted_text, claims = await extract_claims_and_ocr(
        text=raw_message,
        image_base64=None,
        api_key_override=None
    )

    assert extracted_text == raw_message
    assert len(claims) >= 1
    assert claims[0].id == 1
    assert "UNESCO" in claims[0].target_entity or "General Source" in claims[0].target_entity
    assert len(claims[0].normalized_query) > 0


@pytest.mark.asyncio
async def test_factcheck_no_key_returns_empty():
    """Verify factcheck query returns an empty list gracefully when no API key is supplied."""
    with patch("app.services.factcheck_engine.settings") as mock_settings:
        mock_settings.GOOGLE_FACTCHECK_API_KEY = None
        results = await query_google_factcheck(query="COVID vaccine chip", api_key=None)
        assert results == []


@pytest.mark.asyncio
async def test_factcheck_response_parsing():
    """Verify parsing of valid Google Fact Check Tools API response payload."""
    mock_payload = {
        "claims": [
            {
                "text": "The government is giving free 500 recharge to all mobile users.",
                "claimant": "WhatsApp Viral Post",
                "claimReview": [
                    {
                        "publisher": {"name": "PIB Fact Check"},
                        "url": "https://factcheck.pib.gov.in/claim1",
                        "textualRating": "Fake",
                        "reviewDate": "2026-03-15T00:00:00Z"
                    }
                ]
            }
        ]
    }

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = mock_payload

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_resp
        evidence = await query_google_factcheck(query="free recharge", api_key="dummy_api_key")

        assert len(evidence) == 1
        item = evidence[0]
        assert item.claimant == "WhatsApp Viral Post"
        assert item.fact_checker == "PIB Fact Check"
        assert item.rating == "Fake"
        assert item.review_url == "https://factcheck.pib.gov.in/claim1"
        assert item.is_ifcn_certified is True
