from fastapi import APIRouter
from .. import mocks
from ..llm import generate
from ..prompts import PROMPTS
from ..schemas import ValuationRequest, ValuationResponse

router = APIRouter(prefix="/valuation", tags=["Real estate valuation"])


@router.post("/estimate", response_model=ValuationResponse)
def estimate(req: ValuationRequest):
    text = f"Estimate the market value of this property:\n{req.model_dump_json(indent=2)}"
    return generate(PROMPTS["valuation"], text, ValuationResponse, mocks.valuation(req))
