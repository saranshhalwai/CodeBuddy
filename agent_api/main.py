from fastapi import FastAPI, Query, HTTPException
from models import LeetCodePrerequisites, AskLeetCodeRequest
from llm_client import get_llm_client

app = FastAPI(title="LeetCode Prerequisite API")

client = get_llm_client()

@app.get('/')
async def health_check():
    return "Welcome to the Code Buddy Agent API"

@app.post("/askleetcode", response_model=LeetCodePrerequisites)
async def ask_leetcode(payload: AskLeetCodeRequest):
    prompt = f"""
    For the following LeetCode problem, list all prerequisite topics,
    algorithms, and techniques required to solve it.

    Sort them from EASY to HARD.

    LeetCode Question:
    {payload.question}
    """

    try:
        response = client.create(
            response_model=LeetCodePrerequisites,
            messages=[{"role": "user", "content": prompt}]
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
