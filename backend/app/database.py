import sqlite3
import hashlib
import json
import os
import time
from typing import Optional, Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "satyasetu.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=5.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS verification_cache (
                query_hash TEXT PRIMARY KEY,
                raw_text TEXT NOT NULL,
                verdict TEXT NOT NULL,
                credibility_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                response_json TEXT NOT NULL,
                hits INTEGER DEFAULT 1,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS query_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_snippet TEXT NOT NULL,
                verdict TEXT NOT NULL,
                credibility_score INTEGER NOT NULL,
                latency_ms INTEGER NOT NULL,
                source_mode TEXT NOT NULL,
                created_at REAL NOT NULL
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_created ON query_telemetry(created_at);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cache_hash ON verification_cache(query_hash);")

def compute_hash(text: str) -> str:
    normalized = " ".join(text.lower().strip().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def get_cached_verification(text: str) -> Optional[Dict[str, Any]]:
    if not text or len(text.strip()) < 5:
        return None
    h = compute_hash(text)
    with get_connection() as conn:
        row = conn.execute(
            "SELECT response_json, hits FROM verification_cache WHERE query_hash = ?", (h,)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE verification_cache SET hits = hits + 1, updated_at = ? WHERE query_hash = ?",
                (time.time(), h)
            )
            data = json.loads(row["response_json"])
            data["cache_hit"] = True
            data["cache_reads"] = row["hits"] + 1
            return data
    return None

def save_verification(text: str, response_dict: Dict[str, Any], latency_ms: int):
    if not text or len(text.strip()) < 5:
        return
    h = compute_hash(text)
    now = time.time()
    resp_copy = dict(response_dict)
    resp_copy["cache_hit"] = False
    serialized = json.dumps(resp_copy)

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO verification_cache (query_hash, raw_text, verdict, credibility_score, risk_level, response_json, hits, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
            ON CONFLICT(query_hash) DO UPDATE SET
                response_json = excluded.response_json,
                verdict = excluded.verdict,
                credibility_score = excluded.credibility_score,
                risk_level = excluded.risk_level,
                hits = verification_cache.hits + 1,
                updated_at = excluded.updated_at;
        """, (
            h,
            text[:500],
            response_dict.get("overall_verdict", "UNVERIFIED"),
            response_dict.get("credibility_score", 50),
            response_dict.get("risk_level", "MODERATE_CAUTION"),
            serialized,
            now,
            now
        ))

        conn.execute("""
            INSERT INTO query_telemetry (query_snippet, verdict, credibility_score, latency_ms, source_mode, created_at)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (
            text[:100],
            response_dict.get("overall_verdict", "UNVERIFIED"),
            response_dict.get("credibility_score", 50),
            latency_ms,
            response_dict.get("data_source_mode", "Hybrid Pipeline"),
            now
        ))

def get_system_stats() -> Dict[str, Any]:
    with get_connection() as conn:
        total_queries = conn.execute("SELECT COUNT(*) as c FROM query_telemetry").fetchone()["c"]
        cached_entries = conn.execute("SELECT COUNT(*) as c FROM verification_cache").fetchone()["c"]
        total_cache_hits = conn.execute("SELECT COALESCE(SUM(hits - 1), 0) as s FROM verification_cache").fetchone()["s"]
        
        verdicts = conn.execute("SELECT verdict, COUNT(*) as c FROM query_telemetry GROUP BY verdict").fetchall()
        verdict_breakdown = {row["verdict"]: row["c"] for row in verdicts}

        avg_latency = conn.execute("SELECT COALESCE(AVG(latency_ms), 0) as a FROM query_telemetry").fetchone()["a"]

    return {
        "database_backend": "SQLite (WAL Mode)",
        "total_verifications_logged": total_queries,
        "cached_unique_claims": cached_entries,
        "cache_savings_hits": total_cache_hits,
        "avg_pipeline_latency_ms": round(avg_latency, 1),
        "verdict_distribution": verdict_breakdown
    }

def get_recent_history(limit: int = 8) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT query_snippet, verdict, credibility_score, latency_ms, created_at
            FROM query_telemetry
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
        
        return [
            {
                "query": row["query_snippet"],
                "verdict": row["verdict"],
                "credibility_score": row["credibility_score"],
                "latency_ms": row["latency_ms"],
                "timestamp": row["created_at"]
            }
            for row in rows
        ]
