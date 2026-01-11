from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
from uuid import UUID

app = FastAPI()

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL")

# -------- Request / Response Models --------

class InputData(BaseModel):
    platform: str
    url: str
    title: str
    timeLimit: str
    memoryLimit: str
    statement: str
    examples: str   


class PredictionResponse(BaseModel):
    prerequisites: list[str]


# -------- API Endpoints --------

@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/analyze", response_model=PredictionResponse)
async def analyze(data: InputData):
    try:
        print(data)
        # async with httpx.AsyncClient(timeout=10.0) as client:
        #     ml_response = await client.post(
        #         ML_SERVICE_URL,
        #         json=data.dict()
        #     )

        # if ml_response.status_code != 200:
        #     raise HTTPException(
        #         status_code=502,
        #         detail="ML service error"
        #     )
        # return ml_response.json()

        return data

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="ML service unreachable"
        )
