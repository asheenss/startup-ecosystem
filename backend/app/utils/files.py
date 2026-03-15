from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

ALLOWED_PDF_MIME_TYPES = {"application/pdf", "application/x-pdf"}


def build_safe_upload_path(base_dir: Path, upload_file: UploadFile) -> Path:
    suffix = Path(upload_file.filename or "upload.pdf").suffix.lower()
    if suffix != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")

    if upload_file.content_type not in ALLOWED_PDF_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid content type for pitch deck upload")

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{uuid4()}{suffix}"
