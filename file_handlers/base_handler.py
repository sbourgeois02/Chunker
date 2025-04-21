# file_handlers/base_handler.py

from abc import ABC, abstractmethod

class BaseFileHandler(ABC):
    @abstractmethod
    def load_text(self, filepath: str) -> str:
        pass