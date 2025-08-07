import io
from typing import List
from pypdf import PdfReader
from docx import Document as DocxDocument
from pyzmail import PyzMessage
# We no longer need to import get_body or pyzmail.text

def extract_text_from_pdf(file: bytes) -> str:
    reader = PdfReader(io.BytesIO(file))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file: bytes) -> str:
    doc = DocxDocument(io.BytesIO(file))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_eml(file: bytes) -> str:
    """
    Extracts the text content from an email file using the modern pyzmail36 approach.
    """
    message = PyzMessage.from_bytes(file)
    
    # The simplest and most reliable way is to access the text_part directly.
    if message.text_part is not None:
        # The payload of the part contains the body as bytes.
        payload = message.text_part.get_payload()
        if isinstance(payload, bytes):
            # We must decode the bytes into a string.
            # Use the part's specified charset, or fall back to 'utf-8'.
            return payload.decode(message.text_part.charset or 'utf-8', errors='ignore')
            
    # If there is no plain text part, return an empty string.
    return ""

def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> List[str]:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks