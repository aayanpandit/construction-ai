from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import llm
from .config import settings
from .routers import assistant, cracks, knowledge, planning, safety, valuation, weather

app = FastAPI(title="Construction Intelligence Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


@app.exception_handler(llm.LLMError)
async def llm_error_handler(_: Request, exc: llm.LLMError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.get("/api/health")
def health():
    return {"status": "ok", "llm_mode": llm.mode(), "model": settings.model}


for r in (safety, cracks, valuation, planning, assistant, weather, knowledge):
    app.include_router(r.router, prefix="/api")
