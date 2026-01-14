import { extractCodeforcesProblem } from "./content/extractor.js";
import { fetchPrerequisites } from "./content/api.js";
import { injectSidebarUI, renderPrerequisites } from "./content/uiInjector.js";

injectSidebarUI(async () => {
  const problem = extractCodeforcesProblem();
  if (!problem) return;

  renderPrerequisites({
    prerequisites: ["Analyzing..."],
    difficulty: ""
  });

  const result = await fetchPrerequisites(problem);
  renderPrerequisites(result);
});
