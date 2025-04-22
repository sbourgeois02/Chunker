# file_handlers/pdf_handler.py

from file_handlers.base_handler import BaseFileHandler
import fitz  # PyMuPDF

class PdfFileHandler(BaseFileHandler):
    def load_text(self, filepath: str) -> str:
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
