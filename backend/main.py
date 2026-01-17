from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import json
import httpx
import models
import db
import logging
import helper

app = FastAPI()

class LogAndValidateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            body_bytes = await request.body()

            # Log raw body
            try:
                body_json = json.loads(body_bytes)
                print("🔹 Raw request body:", body_json)
            except Exception:
                print("🔹 Raw request body (non-JSON):", body_bytes)

            # Re-inject body so FastAPI can read it again
            async def receive():
                return {
                    "type": "http.request",
                    "body": body_bytes,
                }

            request._receive = receive

        response = await call_next(request)
        return response
app.add_middleware(LogAndValidateMiddleware)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Constants ----------
# ML_SERVICE_URL = "http://127.0.0.1:9000/"
ML_SERVICE_URL = "https://agent-api-1046850164238.asia-south1.run.app/"
leetcodeUrl = "askleetcode"
codeforcesUrl = "askcodeforces"
logger = logging.getLogger("uvicorn")
# ---------- Routes ----------
@app.get("/test")
async def root():
    print(1)
    return {"status": "ok"}


# to analyse the problem
@app.post("/analyze", response_model=list[models.Tag])
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
        
        print(data.url)
        res = ml_response.json();

        parts = data.url.split("/")
        num = ""
        if(parts[-2]=="problem"):
            num = parts[-3]
        else:
            num = parts[-2]

        problem_id = num+parts[-1]
        handle = data.handle

        if handle:
            known_tags = set(
                tag.strip().lower()
                for tag in await db.get_user_tags(handle=handle)
            )
        else:
            known_tags = set()

        tags: list[models.Tag] = [
            models.Tag(
                tag=p["topic"].strip().lower(),
                known=p["topic"].strip().lower() in known_tags
            )
            for p in res.get("prerequisites", [])
        ]

        problem = models.Problem(
            problem_id=problem_id,
            tags=tags
        )

        await db.add_problem(problem)
        print(tags)
        return tags

    except httpx.RequestError as e:
        print("ML service request failed:", repr(e))
        raise HTTPException(
            status_code=503,
            detail="ML service unreachable"
        )

# to add tags to the user
@app.post("/verify_solution")
async def verify_solution(data: models.VerifySolutionRequest):
    print("solution added in queue")

    parts = data.problemUrl.split("/")
    num = ""
    if(parts[-2]=="problem"):
       num = parts[-3]
    else:
        num = parts[-2]
    problem_id = num + parts[-1]; 

    submission = await helper.wait_for_accepted(
        data.handle,
        problem_id,
        steps=7
    )

    print(submission)
    if not submission:
        return {"sumbission": submission,}
    
    print(submission["verdict"])
    tags = await db.get_problem_tags(problem_id=problem_id);
    print(tags)
    await db.add_user_tags(
        data.handle,
        tags
    )

    return {
        "status": "verified",
        "verdict": submission["verdict"],
        "tags_added": tags
    }