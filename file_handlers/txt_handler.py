# file_handlers/txt_handler.py

from .base_handler import BaseFileHandler

class TxtFileHandler(BaseFileHandler):
    def load_text(self, filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()