from pydantic import BaseModel, Field
from typing import List


class Prerequisite(BaseModel):
    level: str
    topic: str
    description: str

class AskLeetCodeRequest(BaseModel):
    question: str = Field(min_length=1)

class LeetCodePrerequisites(BaseModel):
    prerequisites: List[Prerequisite]
