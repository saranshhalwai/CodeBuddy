import { getUserHandle } from "./submissionExtractor.js";

const API_URL = "http://127.0.0.1:8000/analyze";
const SUBMIT_URL = "http://127.0.0.1:8000/verify_solution"

export async function fetchPrerequisites(problemData) {
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(problemData)
    });
    if (!res.ok) {
      throw new Error("Backend error");
    }
    return await res.json();
  } catch (err) {
    console.error("API ERROR:", err);
    return {
      error: true,
      message: "Failed to analyze problem"
    };
  }
}

export async function sendSubmissionEvent() {
  const handle = getUserHandle();
  if (!handle) return;
  fetch(SUBMIT_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      handle: handle,
      problemUrl: location.href,
    })
  });
}