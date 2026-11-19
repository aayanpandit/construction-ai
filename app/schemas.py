"""Strict JSON contracts. Every AI response is validated against these models
before it reaches the frontend."""
from typing import Literal, Optional
from pydantic import BaseModel, Field

Level = Literal["low", "medium", "high", "critical"]
DISCLAIMER = "AI-generated advisory. Verify with a qualified professional before acting."


# ---------- Safety ----------
class Hazard(BaseModel):
    type: str
    severity: Level
    description: str
    recommendation: str


class SafetyResponse(BaseModel):
    overall_risk: Level
    safety_score: int = Field(ge=0, le=100)
    ppe_compliance: bool
    ppe_findings: list[str]
    hazards: list[Hazard]
    immediate_actions: list[str]
    summary: str
    disclaimer: str = DISCLAIMER


# ---------- Cracks ----------
class CrackResponse(BaseModel):
    crack_detected: bool
    crack_type: str
    severity: Level
    estimated_width_mm: Optional[float] = None
    structural_risk: Level
    probable_causes: list[str]
    recommended_actions: list[str]
    repair_methods: list[str]
    monitoring_advice: str
    summary: str
    disclaimer: str = DISCLAIMER


# ---------- Valuation ----------
class ValuationRequest(BaseModel):
    location: str = Field(min_length=2)
    property_type: Literal["apartment", "villa", "independent house", "plot", "commercial"] = "apartment"
    area_sqft: float = Field(gt=0)
    bedrooms: int = Field(default=2, ge=0, le=20)
    bathrooms: int = Field(default=2, ge=0, le=20)
    age_years: float = Field(default=0, ge=0)
    construction_quality: Literal["basic", "standard", "premium"] = "standard"
    amenities: list[str] = []
    currency: str = "INR"


class ValuationFactor(BaseModel):
    factor: str
    impact: Literal["positive", "negative", "neutral"]
    explanation: str


class ValuationResponse(BaseModel):
    currency: str
    estimated_value_low: float
    estimated_value_mid: float
    estimated_value_high: float
    price_per_sqft: float
    confidence: Literal["low", "medium", "high"]
    factors: list[ValuationFactor]
    assumptions: list[str]
    summary: str
    disclaimer: str = DISCLAIMER


# ---------- Planning ----------
class PlanningRequest(BaseModel):
    project_name: str = Field(min_length=2)
    project_type: Literal["residential", "commercial", "industrial", "infrastructure", "renovation"] = "residential"
    location: str
    built_up_area_sqft: float = Field(gt=0)
    floors: int = Field(default=1, ge=1, le=100)
    budget: Optional[float] = Field(default=None, gt=0)
    duration_months: Optional[int] = Field(default=None, gt=0)
    currency: str = "INR"
    notes: str = ""


class Phase(BaseModel):
    name: str
    duration_weeks: int
    activities: list[str]
    deliverables: list[str]


class Material(BaseModel):
    item: str
    quantity: float
    unit: str
    estimated_cost: float


class LaborRole(BaseModel):
    role: str
    count: int


class Risk(BaseModel):
    risk: str
    severity: Level
    mitigation: str


class PlanningResponse(BaseModel):
    currency: str
    total_estimated_cost: float
    total_duration_weeks: int
    phases: list[Phase]
    materials: list[Material]
    labor: list[LaborRole]
    risks: list[Risk]
    summary: str
    disclaimer: str = DISCLAIMER


# ---------- Daily site assistant ----------
class AssistantRequest(BaseModel):
    site_name: str = "Main site"
    tasks: list[str] = Field(min_length=1)
    notes: str = ""
    city: Optional[str] = None


class PrioritizedTask(BaseModel):
    task: str
    priority: Level
    reason: str


class AssistantResponse(BaseModel):
    priorities: list[PrioritizedTask]
    checklist: list[str]
    safety_reminders: list[str]
    coordination_tips: list[str]
    summary: str
    disclaimer: str = DISCLAIMER


# ---------- Weather ----------
class WeatherRequest(BaseModel):
    city: str = Field(min_length=2)
    activity: str = "general site work"


class DayForecast(BaseModel):
    date: str
    condition: str
    temp_max_c: float
    temp_min_c: float
    precipitation_mm: float
    wind_max_kmh: float


class WeatherSnapshot(BaseModel):
    city: str
    temperature_c: float
    humidity_pct: float
    wind_kmh: float
    precipitation_mm: float
    condition: str
    forecast: list[DayForecast]
    source: str = "open-meteo"


class Advisory(BaseModel):
    activity: str
    recommendation: str
    reason: str


class AdvisoryOut(BaseModel):
    work_suitability: Literal["good", "caution", "unsuitable"]
    advisories: list[Advisory]
    precautions: list[str]
    summary: str


class WeatherResponse(AdvisoryOut):
    weather: WeatherSnapshot
    disclaimer: str = DISCLAIMER


# ---------- Knowledge ----------
class KnowledgeRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1500)
    context: str = ""


class KnowledgeResponse(BaseModel):
    answer: str
    key_points: list[str]
    references: list[str]
    related_questions: list[str]
    confidence: Literal["low", "medium", "high"]
    disclaimer: str = DISCLAIMER
