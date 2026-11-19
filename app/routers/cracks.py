from fastapi import APIRouter, File, Form, UploadFile
from ..llm import generate
from ..mocks import CRACKS
from ..prompts import PROMPTS
from ..schemas import CrackResponse
from ..utils import read_image

router = APIRouter(prefix="/cracks", tags=["Crack detection"])


@router.post("/analyze", response_model=CrackResponse)
def analyze(image: UploadFile = File(...), element: str = Form(""), notes: str = Form("")):
    img = read_image(image)
    text = f"Analyze this image for cracks. Building element: {element or 'unknown'}. Notes: {notes or 'none'}."
    return generate(PROMPTS["cracks"], text, CrackResponse, CRACKS, img)
