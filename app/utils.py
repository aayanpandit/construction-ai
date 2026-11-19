from fastapi import HTTPException, UploadFile
from .config import settings

ALLOWED = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def read_image(file: UploadFile) -> tuple[bytes, str]:
    """Validate an uploaded image and return (bytes, media_type)."""
    if file.content_type not in ALLOWED:
        raise HTTPException(400, "Unsupported file type. Upload a JPG, PNG, WEBP or GIF image.")
    data = file.file.read()
    if not data:
        raise HTTPException(400, "The uploaded file is empty.")
    if len(data) > settings.max_image_mb * 1024 * 1024:
        raise HTTPException(413, f"Image is larger than {settings.max_image_mb} MB. Upload a smaller photo.")
    return data, file.content_type
