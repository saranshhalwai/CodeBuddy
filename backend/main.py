from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import models
import db


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

# ---------- Routes ----------
@app.get("/test")
async def root():
    try:
        return {"status": "ok"}
    except httpx.RequestError as e:
        print("ML service request failed:", repr(e))
        raise HTTPException(
            status_code=503,
            detail="ML service unreachable"
        )


@app.post("/analyze", response_model=models.Prerequisites)
async def analyze(data: models.InputData):
    try:
        if data.platform.lower() == "codeforces":
            url = ML_SERVICE_URL + codeforcesUrl

            payload = models.AskCodeForcesRequest(
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

            payload = models.AskLeetCodeRequest(
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
        
        data = ml_response.json();
        problem_id = "test_id"
        tags = list({
            p["topic"].strip().lower()
            for p in data.get("prerequisites", [])
        })

        problem = models.Problem(
            problem_id=problem_id,
            tags=tags
        )

        await db.add_problem(problem)
        return data

    except httpx.RequestError as e:
        print("ML service request failed:", repr(e))
        raise HTTPException(
            status_code=503,
            detail="ML service unreachable"
        )
