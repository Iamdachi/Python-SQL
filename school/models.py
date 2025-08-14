from typing import TypedDict

class Room(TypedDict):
    id: int
    name: str

class Student(TypedDict):
    birthday: str
    id: int
    name: str
    room: int
    sex: str
