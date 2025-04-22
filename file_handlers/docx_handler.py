# file_handlers/docx_handler.py

from file_handlers.base_handler import BaseFileHandler
from docx import Document

class DocxFileHandler(BaseFileHandler):
    def load_text(self, filepath: str) -> str:
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
