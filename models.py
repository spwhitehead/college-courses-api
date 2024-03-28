from dataclasses import dataclass
from enum import Enum


class DepartmentName(Enum):
    COMPUTER_SCIENCE = "Computer Science"
    HISTORY = "History"
    MATHEMATICS = "Mathematics"
    BIOLOGY = "Biology"


@dataclass
class Course:
    name: str
    level: int
    semester: str


@dataclass
class Department:
    name: DepartmentName
    courses: list[Course]
