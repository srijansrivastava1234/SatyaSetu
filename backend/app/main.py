import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.config import settings
from app.models.schemas import ClaimVerifyRequest, VerificationResponse
from app.services.orchestrator import run_verification_pipeline
from app.services.seed_scenarios import SEED_SCENARIOS
from app.database import (
    init_db,
    get_cached_verification,
    save_verification,
    get_system_stats,
    get_recent_history
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("satyasetu")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
STATIC_HTML_PATH = os.path.join(STATIC_DIR, "index.html")
STATIC_404_PATH = os.path.join(STATIC_DIR, "404.html")
STATIC_FAVICON_PATH = os.path.join(STATIC_DIR, "favicon.svg")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database cache & telemetry schemas
    logger.info("Initializing SQLite persistent cache and telemetry store...")
    init_db()
    logger.info("SatyaSetu core engine ready.")
    yield
    logger.info("Shutting down SatyaSetu engine.")

app = FastAPI(
    title=settings.APP_NAME,
    description="Institutional Misinformation Intelligence Engine with IFCN ClaimReview grounding and SQLite caching.",
    version="1.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static asset directory
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon.svg", include_in_schema=False)
async def serve_favicon():
    if os.path.exists(STATIC_FAVICON_PATH):
        with open(STATIC_FAVICON_PATH, "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="image/svg+xml")
    return Response(status_code=404)

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    if os.path.exists(STATIC_HTML_PATH):
        with open(STATIC_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>SatyaSetu Engine Online</h1>"

@app.get("/404", response_class=HTMLResponse)
async def serve_404():
    if os.path.exists(STATIC_404_PATH):
        with open(STATIC_404_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>404 Not Found</h1>"

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    if os.path.exists(STATIC_404_PATH):
        with open(STATIC_404_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=404)
    return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)

@app.get("/api/health")
async def health_check():
    stats = get_system_stats()
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.1.0",
        "gemini_api_configured": bool(settings.GEMINI_API_KEY),
        "factcheck_api_configured": bool(settings.GOOGLE_FACTCHECK_API_KEY),
        "available_scenarios_count": len(SEED_SCENARIOS),
        "cache_metrics": stats
    }

@app.get("/api/stats")
async def get_stats():
    """Returns database telemetry, query distributions, and cache metrics."""
    return get_system_stats()

@app.get("/api/history")
async def get_history(limit: int = 10):
    """Returns recent anonymized verification records from SQLite store."""
    return {"history": get_recent_history(limit=min(limit, 50))}

@app.get("/api/scenarios")
async def get_demo_scenarios():
    """Returns verified reference scenarios for testing and demonstration."""
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
    """Main verification endpoint with high-speed SQLite caching."""
    if not req.text and not req.image_base64 and not req.url and not req.scenario_id:
        raise HTTPException(status_code=400, detail="Provide at least one input: text, url, image_base64, or scenario_id")

    query_input = (req.text or req.url or "").strip()

    # Step 0: Check SQLite cache for text queries (if not using scenario_id or image)
    if query_input and not req.image_base64 and not req.scenario_id:
        cached = get_cached_verification(query_input)
        if cached:
            logger.info("Serving verification response from SQLite WAL cache: '%s...'", query_input[:40])
            cached["data_source_mode"] = f"SatyaSetu High-Speed SQLite Cache (Hit #{cached.get('cache_reads', 1)})"
            cached["is_cached"] = True
            return VerificationResponse(**cached)

    try:
        t0 = time.time()
        result = await run_verification_pipeline(req)
        latency_ms = int((time.time() - t0) * 1000)

        # Cache valid responses
        if query_input and not req.image_base64:
            save_verification(query_input, result.model_dump(), latency_ms)

        return result
    except Exception as e:
        logger.error("Pipeline execution failure: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
