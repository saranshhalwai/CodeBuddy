import { sendSubmissionEvent } from "../content/api.js";

export function initSubmitListener() {
  document.addEventListener("submit", (e) => {
    const form = e.target;
    if (!form || !form.action) return;
    if (form.action.includes("/submit")) {
      sendSubmissionEvent();
    }
  });
}
