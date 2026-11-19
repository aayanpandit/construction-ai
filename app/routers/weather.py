import httpx
from fastapi import APIRouter, HTTPException
from ..llm import generate
from ..mocks import WEATHER
from ..prompts import PROMPTS
from ..schemas import AdvisoryOut, WeatherRequest, WeatherResponse
from ..weather_client import get_weather

router = APIRouter(prefix="/weather", tags=["Weather advisory"])


@router.post("/advisory", response_model=WeatherResponse)
def advisory(req: WeatherRequest):
    try:
        snapshot = get_weather(req.city)
    except LookupError:
        raise HTTPException(404, f"City '{req.city}' was not found. Check the spelling or add the country.")
    except httpx.HTTPError:
        raise HTTPException(502, "Weather service is unreachable. Try again in a moment.")
    text = f"Planned activity: {req.activity}\nWeather data:\n{snapshot.model_dump_json(indent=2)}"
    out = generate(PROMPTS["weather"], text, AdvisoryOut, WEATHER)
    return WeatherResponse(weather=snapshot, **out.model_dump())
