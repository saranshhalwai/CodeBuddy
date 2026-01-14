from pydantic import BaseModel, Field
from typing import List, Optional


class Prerequisite(BaseModel):
    level: str
    topic: str
    description: str

class AskLeetCodeRequest(BaseModel):
    question: str = Field(min_length=1)

class Prerequisites(BaseModel):
    prerequisites: List[Prerequisite]

class AskCodeForcesRequest(BaseModel):
    problem: str = Field(min_length=1)
    solution: Optional[str] = Field(min_length=1)