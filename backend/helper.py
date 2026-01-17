import httpx
import asyncio

CODEFORCES_STATUS_API = "https://codeforces.com/api/user.status"

async def fetch_latest_submission(handle: str, problem_id: str):
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(
            CODEFORCES_STATUS_API,
            params={"handle": handle, "count": 5}
        )
        res.raise_for_status()

    data = res.json()
    if data["status"] != "OK":
        return None

    for sub in data["result"]:
        pid = f"{sub['problem']['contestId']}{sub['problem']['index']}"
        if pid == problem_id:
            return sub

    return None

async def wait_for_accepted(handle: str, problem_id: str, steps=5):
    delay = 1

    for _ in range(steps):
        submission = await fetch_latest_submission(handle, problem_id)
        if submission and submission.get("verdict") == "OK":
            return submission

        await asyncio.sleep(delay)
        delay *= 2

    return None
