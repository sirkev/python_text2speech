"""
Document Parser Service
Handles parsing of PDF, DOCX, and TXT files into plain text for RAG ingestion.
"""

import io
from typing import Tuple


def parse_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file using PyMuPDF."""
    import fitz  # pymupdf

    text_parts = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)


def parse_docx(file_bytes: bytes) -> str:
    """Extracts text from a DOCX file using python-docx."""
    from docx import Document

    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])


def parse_txt(file_bytes: bytes) -> str:
    """Decodes a plain text file."""
    return file_bytes.decode("utf-8")


SUPPORTED_TYPES = {
    "application/pdf": parse_pdf,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": parse_docx,
    "text/plain": parse_txt,
}


def parse_file(file_bytes: bytes, content_type: str, filename: str) -> Tuple[str, str]:
    """
    Routes to the correct parser based on content type.
    Returns (extracted_text, source_name).
    """
    # Fallback: detect by extension if content_type is generic
    if content_type == "application/octet-stream":
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        ext_map = {"pdf": "application/pdf", "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "txt": "text/plain"}
        content_type = ext_map.get(ext, content_type)

    parser = SUPPORTED_TYPES.get(content_type)
    if not parser:
        raise ValueError(
            f"Unsupported file type: {content_type}. "
            f"Supported: PDF, DOCX, TXT."
        )

    text = parser(file_bytes)
    return text, filename
