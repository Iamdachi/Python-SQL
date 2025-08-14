"""TypedDict definitions for database entities."""

from typing import TypedDict

class Room(TypedDict):
    id: int
    name: str

class Student(TypedDict):
    id: int
    name: str
    birthday: str  # ISO format date string: YYYY-MM-DD
    sex: str  # 'M' or 'F'
    room: int  # Foreign key to Room.id

