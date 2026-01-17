import { extractCodeforcesProblem } from "./content/extractor.js";
import { fetchPrerequisites } from "./content/api.js";
import { injectSidebarUI, renderPrerequisites } from "./content/uiInjector.js";
import { initSubmitListener } from "./listeners/submissionListener.js";

injectSidebarUI(async () => {
  const problem = extractCodeforcesProblem();
  if (!problem || !problem.title) return;

  initSubmitListener();
  console.log("Hi")
  renderPrerequisites({
    prerequisites: ["Analyzing..."],
    difficulty: ""
  });

  const result = await fetchPrerequisites(problem);
  renderPrerequisites(result);
});
