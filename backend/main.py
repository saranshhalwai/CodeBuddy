from dataclasses import Field
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel, Field
from typing_extensions import Annotated


app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Constants ----------
ML_SERVICE_URL = "http://127.0.0.1:9000/"
leetcodeUrl = "askleetcode"
codeforcesUrl = "askcodeforces"

# ---------- Models ----------
class InputData(BaseModel):
    platform: str
    url: str
    title: str
    timeLimit: str
    memoryLimit: str
    statement: str
    examples: str 

class AskCodeForcesRequest(BaseModel):
    problem: str = Field(min_length=1)
    solution: Optional[str] = Field(min_length=1)  

class AskLeetCodeRequest(BaseModel):
    question: str = Field(min_length=1)

class Prerequisite(BaseModel):
    level: str
    topic: str
    description: str

class Prerequisites(BaseModel):
    prerequisites: list[Prerequisite]

# ---------- Routes ----------
@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/analyze", response_model=Prerequisites)
async def analyze(data: InputData):
    try:
        if data.platform.lower() == "codeforces":
            url = ML_SERVICE_URL + codeforcesUrl

            payload = AskCodeForcesRequest(
                problem=f"""
                Title: {data.title}

                Statement:
                {data.statement}

                Examples:
                {data.examples}
                """.strip(),
                    solution="solution not available"
            ).dict()

        elif data.platform.lower() == "leetcode":
            url = ML_SERVICE_URL + leetcodeUrl

            payload = AskLeetCodeRequest(
                question=f"""
                    Title: {data.title}

                    Statement:
                    {data.statement}

                    Examples:
                    {data.examples}
                    """.strip()
                ).dict()
        else:
            raise HTTPException(status_code=400, detail="Unsupported platform")

        async with httpx.AsyncClient(timeout=10.0) as client:
            ml_response = await client.post(url, json=payload)

        if ml_response.status_code != 200:
            raise HTTPException(status_code=502, detail="ML service error")

        return ml_response.json()

    except httpx.RequestError as e:
        print("ML service request failed:", repr(e))
        raise HTTPException(
            status_code=503,
            detail="ML service unreachable"
        )


