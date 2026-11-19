"""Sample responses used when no API key is configured (MOCK mode)."""
from .schemas import PlanningRequest, ValuationRequest

SAFETY = {
    "overall_risk": "high", "safety_score": 58, "ppe_compliance": False,
    "ppe_findings": ["Two workers without safety helmets", "No high-visibility vests on upper deck", "Safety boots present"],
    "hazards": [
        {"type": "Fall from height", "severity": "high", "description": "Open slab edge without guard rails.",
         "recommendation": "Install edge protection and toe boards; enforce harness use."},
        {"type": "Housekeeping", "severity": "medium", "description": "Loose rebar offcuts on walkway.",
         "recommendation": "Clear walkways and designate a scrap collection area."},
    ],
    "immediate_actions": ["Stop work near the slab edge until guard rails are fitted", "Issue helmets and vests before work resumes"],
    "summary": "[MOCK] Moderate-to-high risk site. Fall protection and PPE enforcement need immediate attention.",
}
CRACKS = {
    "crack_detected": True, "crack_type": "Diagonal crack", "severity": "medium", "estimated_width_mm": 1.5,
    "structural_risk": "medium",
    "probable_causes": ["Differential settlement", "Shrinkage and thermal movement"],
    "recommended_actions": ["Mark crack ends with dated pencil lines", "Have a structural engineer inspect the foundation"],
    "repair_methods": ["Epoxy injection for non-moving cracks", "Polymer-modified mortar patching after stabilisation"],
    "monitoring_advice": "Fit tell-tales and re-measure width every 2 weeks for 3 months.",
    "summary": "[MOCK] Diagonal crack near a wall opening, likely settlement-related. Monitor before repairing.",
}
WEATHER = {
    "work_suitability": "caution",
    "advisories": [
        {"activity": "Concrete pouring", "recommendation": "Pour in the morning and cure with wet burlap", "reason": "High afternoon temperature accelerates setting."},
        {"activity": "Crane operations", "recommendation": "Pause if gusts exceed 35 km/h", "reason": "Wind limits for safe lifting."},
    ],
    "precautions": ["Provide drinking water and shaded rest areas", "Cover cement and sand stocks"],
    "summary": "[MOCK] Workable with precautions. Schedule heat-sensitive tasks early.",
}
KNOWLEDGE = {
    "answer": "[MOCK] M25 concrete has a characteristic compressive strength of 25 N/mm² at 28 days and is commonly used for RCC in residential buildings. Mix design should follow IS 10262 and durability needs follow IS 456.",
    "key_points": ["M25 = 25 MPa at 28 days", "Typical nominal mix 1:1:2", "Curing for at least 7 days"],
    "references": ["IS 456:2000", "IS 10262:2019"],
    "related_questions": ["What is the difference between M20 and M25?", "How long should slabs be cured?"],
    "confidence": "medium",
}


def assistant(tasks: list[str]) -> dict:
    levels = ["high", "medium", "low"]
    return {
        "priorities": [{"task": t, "priority": levels[min(i, 2)], "reason": "[MOCK] Ordered by listed sequence and dependencies."} for i, t in enumerate(tasks)],
        "checklist": ["Toolbox talk at start of shift", "Verify PPE for all workers", "Inspect scaffolding and lifting gear", "Log material deliveries"],
        "safety_reminders": ["Keep walkways clear", "No work at height without harness"],
        "coordination_tips": ["Confirm material arrival with the store before noon"],
        "summary": "[MOCK] Start with the highest-priority task and finish safety checks first.",
    }


def valuation(r: ValuationRequest) -> dict:
    rate = {"basic": 4500, "standard": 6500, "premium": 9500}[r.construction_quality]
    rate *= max(0.6, 1 - 0.01 * r.age_years) * (1 + 0.02 * len(r.amenities))
    mid = rate * r.area_sqft
    return {
        "currency": r.currency, "estimated_value_low": round(mid * 0.9), "estimated_value_mid": round(mid),
        "estimated_value_high": round(mid * 1.1), "price_per_sqft": round(rate), "confidence": "low",
        "factors": [
            {"factor": "Construction quality", "impact": "positive" if r.construction_quality == "premium" else "neutral", "explanation": f"{r.construction_quality} finish assumed."},
            {"factor": "Property age", "impact": "negative" if r.age_years > 10 else "neutral", "explanation": f"{r.age_years:g} years old."},
        ],
        "assumptions": ["[MOCK] Generic rate card, not live market data"],
        "summary": f"[MOCK] Indicative value for {r.area_sqft:g} sqft in {r.location}.",
    }


def planning(r: PlanningRequest) -> dict:
    cost = r.built_up_area_sqft * 1800 * r.floors ** 0.1
    weeks = r.duration_months * 4 if r.duration_months else max(24, int(r.built_up_area_sqft / 60))
    names = ["Site preparation", "Foundation", "Structure", "Masonry and MEP", "Finishing", "Handover"]
    share = [0.08, 0.17, 0.30, 0.20, 0.20, 0.05]
    return {
        "currency": r.currency, "total_estimated_cost": round(cost), "total_duration_weeks": weeks,
        "phases": [{"name": n, "duration_weeks": max(1, round(weeks * s)), "activities": [f"{n} works"], "deliverables": [f"{n} sign-off"]} for n, s in zip(names, share)],
        "materials": [
            {"item": "Cement", "quantity": round(r.built_up_area_sqft * 0.4), "unit": "bags", "estimated_cost": round(r.built_up_area_sqft * 0.4 * 400)},
            {"item": "Steel", "quantity": round(r.built_up_area_sqft * 4), "unit": "kg", "estimated_cost": round(r.built_up_area_sqft * 4 * 65)},
        ],
        "labor": [{"role": "Mason", "count": 8}, {"role": "Helper", "count": 12}, {"role": "Site engineer", "count": 1}],
        "risks": [{"risk": "Monsoon delay", "severity": "medium", "mitigation": "Complete foundation before rainy season"}],
        "summary": f"[MOCK] Indicative plan for {r.project_name}.",
    }
