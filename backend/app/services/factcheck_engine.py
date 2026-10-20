import httpx
from typing import List, Optional
from app.config import settings
from app.models.schemas import ClaimReviewEvidence

GOOGLE_FACTCHECK_ENDPOINT = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

async def query_google_factcheck(query: str, api_key: Optional[str] = None) -> List[ClaimReviewEvidence]:
    key = api_key or settings.GOOGLE_FACTCHECK_API_KEY
    if not key:
        return []

    params = {
        "query": query,
        "key": key,
        "pageSize": 5,
        "languageCode": "en"
    }

    evidence_list: List[ClaimReviewEvidence] = []
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.get(GOOGLE_FACTCHECK_ENDPOINT, params=params)
            if response.status_code == 200:
                data = response.json()
                claims = data.get("claims", [])
                for claim in claims:
                    claim_text = claim.get("text", "")
                    claimant = claim.get("claimant", "Viral Social Media")
                    reviews = claim.get("claimReview", [])
                    for review in reviews:
                        publisher_name = review.get("publisher", {}).get("name", "Certified Fact-Checker")
                        url = review.get("url", "")
                        rating = review.get("textualRating", "Unverified")
                        review_date = review.get("reviewDate", "")
                        
                        evidence_list.append(
                            ClaimReviewEvidence(
                                claim_text=claim_text,
                                claimant=claimant,
                                fact_checker=publisher_name,
                                rating=rating,
                                review_date=review_date,
                                review_url=url,
                                is_ifcn_certified=True
                            )
                        )
    except Exception as e:
        print(f"[FactCheckAPI] Non-fatal lookup error: {e}")

    return evidence_list
