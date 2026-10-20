from app.services.search_engine import (
    search_live_grounding,
    DEBUNK_KEYWORDS,
    TRUSTED_NEWS_SOURCES,
    FACTCHECK_PUBLISHERS
)
from app.services.factcheck_engine import query_google_factcheck as query_factcheck_tools

async def fallback_web_search(query: str):
    res = await search_live_grounding(query)
    return res.get("citations", [])
