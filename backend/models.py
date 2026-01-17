from pydantic import BaseModel, Field
from pydantic.types import StringConstraints
from typing_extensions import Annotated
from typing import Optional

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)]

class InputData(BaseModel):
    platform: str
    url: str
    title: str
    timeLimit: str
    memoryLimit: str
    statement: str
    examples: str 

class AskCodeForcesRequest(BaseModel):
    problem: str
    solution: Optional[str]

class AskLeetCodeRequest(BaseModel):
    question: str

class Prerequisite(BaseModel):
    level: str
    topic: str
    description: str

class Prerequisites(BaseModel):
    prerequisites: list[Prerequisite]
    
class User(BaseModel):
    handle: str
    tags: list[str]

class Problem(BaseModel):
    problem_id: str
    tags: list[str]
