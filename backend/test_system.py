"""
SatyaSetu: Automated Benchmark Runner & Latency Profiler
Evaluates accuracy, false positives, and latency across 20 curated benchmark test cases.
Usage:
  python test_system.py [--local] [--dataset path_to_dataset.json]
"""

import os
import sys
import json
import time
import httpx

# Ensure Windows terminal UTF-8 encoding support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BACKEND_URL = "http://127.0.0.1:8000/api/verify"
DEFAULT_DATASET = os.path.join(os.path.dirname(__file__), "..", "test_dataset.json")
if not os.path.exists(DEFAULT_DATASET):
    DEFAULT_DATASET = "test_dataset.json"

def get_test_client():
    """Attempts to connect to live backend; falls back to in-process FastAPI TestClient if offline."""
    try:
        res = httpx.get("http://127.0.0.1:8000/api/health", timeout=1.0)
        if res.status_code == 200:
            return None  # Live server is up
    except Exception:
        pass
    
    # In-process TestClient fallback for offline / self-contained benchmarking
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        return TestClient(app)
    except Exception as e:
        print(f"[Warning] Could not initialize in-process test client: {e}")
        return None

def run_evaluation(dataset_path=DEFAULT_DATASET):
    print("=" * 72)
    print("SatyaSetu Benchmark Evaluation Runner (PS ID: 202611)")
    print(f"Loading test suite: {dataset_path}")
    print("=" * 72)

    if not os.path.exists(dataset_path):
        print(f"[X] Dataset file not found at: {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    local_client = get_test_client()
    mode_str = "In-Process FastAPI TestClient" if local_client else f"Live HTTP ({BACKEND_URL})"
    print(f"Evaluation Mode       : {mode_str}\n")

    total = len(test_cases)
    correct = 0
    false_positives = 0  # Authentic news mistakenly marked as false
    false_negatives = 0  # Hoaxes mistakenly marked as authentic
    unverifiable_count = 0
    latencies = []

    print(f"{'ID':<8} | {'Category':<18} | {'Expected':<10} | {'Output':<10} | {'Latency':<8} | {'Status'}")
    print("-" * 72)

    for case in test_cases:
        cid = case["id"]
        cat = case["category"]
        expected = case["expected_verdict"]
        claim = case["claim"]

        t0 = time.time()
        try:
            if local_client:
                res = local_client.post("/api/verify", json={"text": claim})
            else:
                res = httpx.post(BACKEND_URL, json={"text": claim}, timeout=6.0)
            latency_ms = (time.time() - t0) * 1000
            latencies.append(latency_ms)

            if res.status_code == 200:
                data = res.json()
                raw_verdict = (data.get("overall_verdict") or data.get("verdict") or "UNVERIFIED").upper()
                verdict = raw_verdict
            else:
                verdict = f"ERR_{res.status_code}"
        except Exception as err:
            latency_ms = (time.time() - t0) * 1000
            latencies.append(latency_ms)
            verdict = "NET_ERR"

        # Check match with semantic normalization
        if expected == "UNVERIFIABLE" and verdict in {"UNVERIFIED", "UNVERIFIABLE", "SUSPICIOUS / UNVERIFIED"}:
            matched = True
        elif expected == "VERIFIED" and verdict in {"VERIFIED", "TRUE", "AUTHENTIC"}:
            matched = True
        elif expected == "FALSE" and verdict in {"FALSE", "FABRICATED", "HOAX"}:
            matched = True
        else:
            matched = (verdict == expected)

        if matched:
            correct += 1
            status = "[PASS]"
        else:
            status = "[FAIL]"
            if expected == "VERIFIED" and verdict == "FALSE":
                false_positives += 1
            elif expected == "FALSE" and verdict == "VERIFIED":
                false_negatives += 1

        print(f"{cid:<8} | {cat[:17]:<18} | {expected:<10} | {verdict[:10]:<10} | {latency_ms:>6.1f}ms | {status}")

    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    accuracy = (correct / total) * 100 if total else 0.0

    print("\n" + "=" * 72)
    print("BENCHMARK SUMMARY & METRICS")
    print("=" * 72)
    print(f"Total Test Cases      : {total}")
    print(f"Accuracy Rate         : {accuracy:.1f}%")
    print(f"False Positive Rate   : {(false_positives / total)*100:.1f}%")
    print(f"False Negative Rate   : {(false_negatives / total)*100:.1f}%")
    print(f"Mean Latency          : {avg_latency:.1f}ms")
    print(f"Min Latency           : {min(latencies):.1f}ms")
    print(f"Max Latency           : {max(latencies):.1f}ms")
    print("=" * 72)

if __name__ == "__main__":
    run_evaluation()
