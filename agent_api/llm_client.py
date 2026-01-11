import os
import instructor
import google.genai as genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

DEV_MODE = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"

def get_llm_client():
    if DEV_MODE:
        # -------- GROQ (Development) --------
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise RuntimeError("GROQ_API_KEY not found")

        groq_client = Groq(api_key=groq_api_key)

        return instructor.from_groq(
            groq_client,
            model="llama-3.3-70b-versatile"
        )

    else:
        # -------- GEMINI (Production) --------
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY not found")

        genai.configure(api_key=gemini_api_key)

        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        return instructor.from_gemini(
            model,
            mode=instructor.Mode.GEMINI_JSON
        )
