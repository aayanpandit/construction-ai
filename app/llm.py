"""Multimodal LLM client with strict JSON validation, one automatic repair retry,
and a MOCK mode (no API key) so the whole platform runs offline."""
import base64
import json
import re
from typing import Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError

from .config import settings

T = TypeVar("T", bound=BaseModel)


class LLMError(Exception):
    pass


_client = None
if settings.anthropic_api_key:
    from anthropic import Anthropic

    _client = Anthropic(api_key=settings.anthropic_api_key)


def mode() -> str:
    return "live" if _client else "mock"


def _extract_json(text: str) -> dict:
    text = re.sub(r"```(?:json)?", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("No JSON object found in model reply")
    return json.loads(text[start : end + 1])


def generate(
    system: str,
    user_text: str,
    schema: Type[T],
    mock: dict,
    image: Optional[tuple[bytes, str]] = None,
) -> T:
    if _client is None:
        return schema(**mock)

    system_full = (
        f"{system}\n\nReturn ONLY one valid JSON object matching this JSON Schema. "
        f"No markdown, no commentary, no extra keys.\n{json.dumps(schema.model_json_schema())}"
    )
    content: list[dict] = []
    if image:
        data, media_type = image
        content.append(
            {"type": "image", "source": {"type": "base64", "media_type": media_type,
                                          "data": base64.b64encode(data).decode()}}
        )
    content.append({"type": "text", "text": user_text})

    last_error = ""
    for _ in range(2):  # first try + one repair retry
        parts = list(content)
        if last_error:
            parts.append({"type": "text", "text": f"Your previous reply was invalid ({last_error}). Return corrected JSON only."})
        try:
            resp = _client.messages.create(
                model=settings.model,
                max_tokens=settings.max_tokens,
                system=system_full,
                messages=[{"role": "user", "content": parts}],
            )
            raw = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            return schema(**_extract_json(raw))
        except (ValueError, ValidationError) as e:
            last_error = str(e)[:300]
        except Exception as e:  # network / auth / rate limit
            raise LLMError(f"LLM request failed: {e}") from e
    raise LLMError(f"Model returned invalid JSON twice: {last_error}")
