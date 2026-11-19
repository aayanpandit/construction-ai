from fastapi import APIRouter
from ..llm import generate
from ..mocks import KNOWLEDGE
from ..prompts import PROMPTS
from ..schemas import KnowledgeRequest, KnowledgeResponse

router = APIRouter(prefix="/knowledge", tags=["Knowledge assistant"])


@router.post("/ask", response_model=KnowledgeResponse)
def ask(req: KnowledgeRequest):
    text = f"Question: {req.question}\nContext: {req.context or 'none'}"
    return generate(PROMPTS["knowledge"], text, KnowledgeResponse, KNOWLEDGE)
