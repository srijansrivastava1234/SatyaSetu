from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ClaimVerifyRequest(BaseModel):
    text: Optional[str] = Field(None, description="Raw text or WhatsApp forward message")
    url: Optional[str] = Field(None, description="URL of article or tweet to analyze")
    image_base64: Optional[str] = Field(None, description="Base64 encoded screenshot or image")
    language: Optional[str] = Field("en", description="Preferred output language ('en', 'hi', 'bilingual')")
    scenario_id: Optional[str] = Field(None, description="Optional ID to load pre-verified demo scenario")
    api_key_override: Optional[str] = Field(None, description="Temporary Gemini API key provided from frontend")

class AtomicClaim(BaseModel):
    id: int
    text: str
    normalized_query: str
    target_entity: str
    verdict: str = "UNVERIFIED"

class ClaimReviewEvidence(BaseModel):
    claim_text: str
    claimant: str
    fact_checker: str
    rating: str
    review_date: str
    review_url: str
    is_ifcn_certified: bool = True

class ManipulationSignals(BaseModel):
    urgency_score: int = Field(..., ge=0, le=100)
    emotional_intensity: int = Field(..., ge=0, le=100)
    sensationalism_score: int = Field(..., ge=0, le=100)
    credibility_index: int = Field(..., ge=0, le=100)
    detected_tactics: List[str]
    linguistic_markers: List[str]
    missing_elements: List[str]

class ShareableDebunkCard(BaseModel):
    headline_en: str
    headline_hi: str
    verdict: str
    bullet_points_en: List[str]
    bullet_points_hi: List[str]
    whatsapp_format_text_en: str
    whatsapp_format_text_hi: str
    verification_source_tag: str

class PipelineStep(BaseModel):
    name: str
    status: str
    detail: str
    elapsed_ms: int

class VerificationResponse(BaseModel):
    status: str
    overall_verdict: str
    credibility_score: int
    risk_level: str
    extracted_text: Optional[str] = None
    atomic_claims: List[AtomicClaim]
    certified_evidence: List[ClaimReviewEvidence]
    web_grounding_citations: List[Dict[str, Any]]
    manipulation_breakdown: ManipulationSignals
    debunk_summary_en: str
    debunk_summary_hi: str
    verification_checklist: List[str]
    shareable_card: ShareableDebunkCard
    pipeline_steps: List[PipelineStep]
    total_latency_ms: int
    data_source_mode: str
