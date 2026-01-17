from fastapi import HTTPException
import firebase_admin
from firebase_admin import credentials, firestore
import models

cred = credentials.Certificate("firebase-service-account.json")

firebase_app = firebase_admin.initialize_app(cred)

instance = firestore.client()

# create a new user
async def add_user(user: models.User):
    try:
        ref = instance.collection("users").document(user.handle)

        if ref.get().exists:
            return

        ref.set(user.dict())
        return {"id": ref.id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create user: {str(e)}"
        )

# add new tages to an existing user
async def add_user_tags(handle: str, tags: list[str]):
    try:
        ref = instance.collection("users").document(handle)

        doc = ref.get()
        if not doc.exists:
            ref.set({"id": handle, "tags": tags })
            return {"status": "created", "tags": tags}
        
        ref.update({"tags": firestore.ArrayUnion(tags)})
        return {"status": "updated"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update user tags: {str(e)}"
        )
    
async def get_user_tags(handle: str) -> list[str]:
    try:
        ref = instance.collection("users").document(handle)
        doc = ref.get()

        if not doc.exists:
            return []

        data = doc.to_dict()
        return data.get("tags", [])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch user tags: {str(e)}"
        )

# add a new problem along with its tags
async def add_problem(problem: models.Problem):
    try:
        ref = instance.collection("problems").document(problem.problem_id)

        tags_as_strings = [tag.tag for tag in problem.tags]

        if ref.get().exists:
            return {"status": "exists"}

        ref.set({
            "problem_id": problem.problem_id,
            "tags": tags_as_strings
        })
        return {"id": ref.id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add problem: {str(e)}"
        )


# update tags of an existing problem
async def update_problem_tags(problem_id: str, tags: list[models.Tag]):
    try:
        ref = instance.collection("problems").document(problem_id)

        if not ref.get().exists:
            raise HTTPException(
                status_code=404,
                detail="Problem not found"
            )

        tags_as_strings = [tag.tag for tag in tags]

        ref.update({"tags": tags_as_strings})
        return {"status": "updated"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update problem tags: {str(e)}"
        )

async def get_problem_tags(problem_id: str) -> list[str]:
    try:
        ref = instance.collection("problems").document(problem_id)
        doc = ref.get()

        if not doc.exists:
            return []

        data = doc.to_dict()
        tags: list[str] = data.get("tags", [])

        return tags

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch problem tags: {str(e)}"
        )
    