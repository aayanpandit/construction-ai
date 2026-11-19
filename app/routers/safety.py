from fastapi import APIRouter, File, Form, UploadFile
from ..llm import generate
from ..mocks import SAFETY
from ..prompts import PROMPTS
from ..schemas import SafetyResponse
from ..utils import read_image

router = APIRouter(prefix="/safety", tags=["Safety monitoring"])


@router.post("/analyze", response_model=SafetyResponse)
def analyze(image: UploadFile = File(...), notes: str = Form("")):
    img = read_image(image)
    text = f"Analyze this construction site photo for safety. Site notes: {notes or 'none'}."
    return generate(PROMPTS["safety"], text, SafetyResponse, SAFETY, img)
