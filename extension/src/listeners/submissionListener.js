import { sendSubmissionEvent } from "../content/api.js";

let listenerInitialized = false;

export function initSubmitListener() {
  if (listenerInitialized) return;
  listenerInitialized = true;

  console.log("[CF-EXT] initSubmitListener");

  const attach = () => {
    const btn = document.getElementById("sidebarSubmitButton");
    if (!btn) return false;
    btn.addEventListener("click", () => {
      console.log("[CF-EXT] Submit clicked");
      sendSubmissionEvent();
    });

    return true;
  };
  if (attach()) return;
  const observer = new MutationObserver(() => {
    if (attach()) observer.disconnect();
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}
