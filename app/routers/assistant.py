import httpx
from fastapi import APIRouter
from .. import mocks
from ..llm import generate
from ..prompts import PROMPTS
from ..schemas import AssistantRequest, AssistantResponse
from ..weather_client import get_weather

router = APIRouter(prefix="/assistant", tags=["Daily site assistant"])


@router.post("/daily", response_model=AssistantResponse)
def daily(req: AssistantRequest):
    weather_note = "not provided"
    if req.city:
        try:
            w = get_weather(req.city)
            weather_note = f"{w.condition}, {w.temperature_c} C, wind {w.wind_kmh} km/h, rain {w.precipitation_mm} mm"
        except (LookupError, httpx.HTTPError):
            weather_note = "unavailable"
    text = f"Site: {req.site_name}\nTasks: {req.tasks}\nNotes: {req.notes or 'none'}\nWeather: {weather_note}"
    return generate(PROMPTS["assistant"], text, AssistantResponse, mocks.assistant(req.tasks))
