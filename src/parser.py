import fitz       # PyMuPDF
import docx
import io


def extract_text(file) -> str:
    """
    Extract plain text from an uploaded PDF or DOCX file.
    Returns an empty string if the file cannot be read.
    """
    filename = file.name.lower()

    try:
        if filename.endswith(".pdf"):
            return _extract_pdf(file)
        elif filename.endswith(".docx"):
            return _extract_docx(file)
        else:
            return ""
    except Exception:
        return ""


def _extract_pdf(file) -> str:
    text_parts = []
    raw = file.read()
    with fitz.open(stream=raw, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).strip()


def _extract_docx(file) -> str:
    raw = file.read()
    doc = docx.Document(io.BytesIO(raw))
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs).strip()
