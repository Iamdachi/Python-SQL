import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from .models import Student, Room

class BaseReader(ABC):
    @abstractmethod
    def read(self, filepath: Path) -> list[Union[Student, Room]]:
        pass

class JSONReader(BaseReader):
    def read(self, filepath: Path) -> list[Union[Student, Room]]:
        with filepath.open("r", encoding="utf-8") as file:
            return json.load(file)
