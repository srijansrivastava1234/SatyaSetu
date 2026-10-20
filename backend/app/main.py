from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.schemas import ClaimVerifyRequest, VerificationResponse
from app.services.orchestrator import run_verification_pipeline
from app.services.seed_scenarios import SEED_SCENARIOS

app = FastAPI(
    title=settings.APP_NAME,
    description="TrustAI Misinformation Detection Engine: Multimodal OCR, Google Fact Check API, & WhatsApp viral debunking.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from fastapi.responses import HTMLResponse

STATIC_HTML_PATH = os.path.join(os.path.dirname(__file__), "static", "index.html")
STATIC_404_PATH = os.path.join(os.path.dirname(__file__), "static", "404.html")

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    if os.path.exists(STATIC_HTML_PATH):
        with open(STATIC_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>SatyaSetu Backend Online</h1>"

@app.get("/404", response_class=HTMLResponse)
async def serve_404():
    if os.path.exists(STATIC_404_PATH):
        with open(STATIC_404_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>404 Not Found</h1>"

@app.exception_handler(404)
async def custom_404_handler(request, exc):
    if os.path.exists(STATIC_404_PATH):
        with open(STATIC_404_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=404)
    return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)



@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "gemini_api_configured": bool(settings.GEMINI_API_KEY),
        "factcheck_api_configured": bool(settings.GOOGLE_FACTCHECK_API_KEY),
        "available_scenarios_count": len(SEED_SCENARIOS)
    }

@app.get("/api/scenarios")
async def get_demo_scenarios():
    """Returns curated viral scenarios for instant stage demo testing"""
    scenarios_list = []
    for s_id, s_data in SEED_SCENARIOS.items():
        scenarios_list.append({
            "id": s_id,
            "title": s_data["title"],
            "category": s_data["category"],
            "sample_input": s_data["sample_input"],
            "expected_verdict": s_data["response"].overall_verdict
        })
    return {"scenarios": scenarios_list}

@app.post("/api/verify", response_model=VerificationResponse)
async def verify_claim(req: ClaimVerifyRequest):
    """Main verification endpoint supporting text, screenshots, and URLs"""
    if not req.text and not req.image_base64 and not req.url and not req.scenario_id:
        raise HTTPException(status_code=400, detail="Provide at least one input: text, url, image_base64, or scenario_id")
    
    try:
        result = await run_verification_pipeline(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
