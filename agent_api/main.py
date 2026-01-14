from fastapi import FastAPI, Query, HTTPException
from models import Prerequisites, AskLeetCodeRequest, AskCodeForcesRequest
from llm_client import get_llm_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Prerequisite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # or ["http://localhost:3000"] for frontend-only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = get_llm_client()

@app.get('/')
async def health_check():
    return "Welcome to the Code Buddy Agent API"

@app.post("/askleetcode", response_model=Prerequisites)
async def ask_leetcode(payload: AskLeetCodeRequest):
    prompt = f"""
    For the following LeetCode problem, list all prerequisite topics,
    algorithms, and techniques required to solve it.

    Sort them from EASY to HARD.

    LeetCode Question:
    {payload.question}
    """
    print(payload.question)
    try:
        response = client.create(
            response_model=Prerequisites,
            messages=[{"role": "user", "content": prompt}]
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/askcodeforces", response_model=Prerequisites)
async def ask_codeforces(payload: AskCodeForcesRequest):
    with open("topics.txt", "r") as f:
        topics = f.read()
    prompt = f"""
    For the following CodeForces problem, list all prerequisite topics,
    algorithms, and techniques required to solve it.

    Sort them from EASY to HARD.

    CodeForces Question:
    {payload.problem}
    
    Solution:
    {payload.solution if payload.solution else "N/A"}

    Here is a list of topics. Do not include any topics outside of this list:
    {topics}
    """
    # print(payload.solution)
    try:
        response = client.create(
            response_model=Prerequisites,
            messages=[{"role": "user", "content": prompt}]
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))