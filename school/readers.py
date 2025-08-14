import json
from abc import ABC, abstractmethod
from typing import Union
from .models import Student, Room

class BaseReader(ABC):
    @abstractmethod
    def read(self, filepath: str) -> list[Union[Student, Room]]:
        pass

class JSONReader(BaseReader):
    def read(self, filepath: str) -> list[Union[Student, Room]]:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
