"""
SatyaSetu: Backend Pre-Flight & Health Verification Script (Laptop 1)
Run this script to verify server health, test API response times, and warm the memory cache.
"""

import time
import httpx

BACKEND_URL = "http://127.0.0.1:8000"

DEMO_QUERIES = [
    "UNESCO officially declared India's National Anthem Jana Gana Mana as the best in the world",
    "PM Free Laptop Scheme 2026 apply now at govt-free-laptop.in",
    "ISRO successfully launched the latest solar monitoring satellite"
]

def verify_system():
    print("=" * 60)
    print("⚡ SatyaSetu Backend Verification & Cache Pre-Warming")
    print("=" * 60)

    # 1. Test Root / Health Endpoint
    try:
        t0 = time.time()
        res = httpx.get(f"{BACKEND_URL}/", timeout=3.0)
        dt = (time.time() - t0) * 1000
        print(f"[✓] Root Endpoint Status: {res.status_code} in {dt:.1f}ms")
    except Exception as e:
        print(f"[X] Backend is NOT reachable at {BACKEND_URL}: {e}")
        print("    -> Run: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
        return

    # 2. Test Verification & Pre-warm Cache
    for i, claim in enumerate(DEMO_QUERIES, 1):
        print(f"\n[Test {i}/3] Checking claim: \"{claim[:45]}...\"")
        try:
            # First pass (Populate / Test)
            t0 = time.time()
            res = httpx.post(f"{BACKEND_URL}/api/verify", json={"text": claim}, timeout=5.0)
            latency1 = (time.time() - t0) * 1000
            
            # Second pass (Warm Cache Test)
            t1 = time.time()
            res2 = httpx.post(f"{BACKEND_URL}/api/verify", json={"text": claim}, timeout=2.0)
            latency2 = (time.time() - t1) * 1000

            print(f"    Pass 1 (Cold): {latency1:.1f}ms | Status: {res.status_code}")
            print(f"    Pass 2 (Warm): {latency2:.1f}ms | Status: {res2.status_code} (Target < 20ms)")
            
            if latency2 < 50:
                print("    -> [READY FOR STAGE DEMO]")
            else:
                print("    -> [WARNING: Cache latency higher than expected]")
        except Exception as err:
            print(f"    [X] Verification endpoint error: {err}")

    print("\n" + "=" * 60)
    print("Pre-flight check completed.")
    print("=" * 60)

if __name__ == "__main__":
    verify_system()
