# utils/detect_filetype.py

from file_handlers.txt_handler import TxtFileHandler

def get_handler_for_file(filename: str):
    if filename.endswith(".txt"):
        return TxtFileHandler()
    else:
        raise ValueError(f"Unsupported file type: {filename}")