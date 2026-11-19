from fastapi import APIRouter
from .. import mocks
from ..llm import generate
from ..prompts import PROMPTS
from ..schemas import PlanningRequest, PlanningResponse

router = APIRouter(prefix="/planning", tags=["Project planning"])


@router.post("/generate", response_model=PlanningResponse)
def generate_plan(req: PlanningRequest):
    text = f"Create a construction plan for this project:\n{req.model_dump_json(indent=2)}"
    return generate(PROMPTS["planning"], text, PlanningResponse, mocks.planning(req))
