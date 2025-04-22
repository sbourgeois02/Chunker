# utils/detect_filetype.py

from file_handlers.txt_handler import TxtFileHandler
from file_handlers.pdf_handler import PdfFileHandler
from file_handlers.docx_handler import DocxFileHandler

def get_handler_for_file(filename: str):
    if filename.endswith(".txt"):
        return TxtFileHandler()
    elif filename.endswith(".pdf"):
        return PdfFileHandler()
    elif filename.endswith(".docx"):
        return DocxFileHandler()
    else:
        raise ValueError(f"Unsupported file type: {filename}")