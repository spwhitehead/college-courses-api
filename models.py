from enum import Enum
from pydantic import BaseModel


class DepartmentName(Enum):
    COMPUTER_SCIENCE = "Computer Science"
    HISTORY = "History"
    MATHEMATICS = "Mathematics"
    BIOLOGY = "Biology"


class Course(BaseModel):
    name: str
    level: int
    semester: str


class Department(BaseModel):
    name: DepartmentName
    courses: list[Course]
