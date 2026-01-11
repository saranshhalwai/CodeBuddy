from pydantic import BaseModel
from typing import List

class Prerequisite(BaseModel):
    level: str
    topic: str
    description: str

class LeetCodePrerequisites(BaseModel):
    prerequisites: List[Prerequisite]
