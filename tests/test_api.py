"""Run with: pytest  (works in MOCK mode, no API key or network needed)."""
import os
os.environ["ANTHROPIC_API_KEY"] = ""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
PNG = (b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["llm_mode"] == "mock"


def test_safety_upload():
    r = client.post("/api/safety/analyze", files={"image": ("s.png", PNG, "image/png")})
    assert r.status_code == 200
    body = r.json()
    assert body["overall_risk"] in {"low", "medium", "high", "critical"} and body["hazards"]


def test_rejects_non_image():
    r = client.post("/api/cracks/analyze", files={"image": ("a.txt", b"hello", "text/plain")})
    assert r.status_code == 400


def test_crack_upload():
    r = client.post("/api/cracks/analyze", files={"image": ("c.png", PNG, "image/png")}, data={"element": "wall"})
    assert r.status_code == 200 and r.json()["crack_detected"] is True


def test_valuation_contract():
    r = client.post("/api/valuation/estimate", json={"location": "Indore", "area_sqft": 1200})
    d = r.json()
    assert r.status_code == 200 and d["estimated_value_low"] < d["estimated_value_mid"] < d["estimated_value_high"]


def test_valuation_validation():
    assert client.post("/api/valuation/estimate", json={"location": "Indore", "area_sqft": -5}).status_code == 422


def test_planning():
    r = client.post("/api/planning/generate", json={"project_name": "Villa", "location": "Indore", "built_up_area_sqft": 2000})
    assert r.status_code == 200 and len(r.json()["phases"]) >= 5


def test_assistant_and_knowledge():
    r = client.post("/api/assistant/daily", json={"tasks": ["Pour slab", "Inspect rebar"]})
    assert r.status_code == 200 and len(r.json()["priorities"]) == 2
    r = client.post("/api/knowledge/ask", json={"question": "What is M25 concrete?"})
    assert r.status_code == 200 and r.json()["answer"]
