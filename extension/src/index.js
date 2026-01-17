import { extractCodeforcesProblem } from "./content/extractor.js";
import { fetchPrerequisites } from "./content/api.js";
import { injectSidebarUI, renderPrerequisites } from "./content/uiInjector.js";
import { initSubmitListener } from "./listeners/submissionListener.js";
import { getUserHandle } from "./content/submissionExtractor.js";

initSubmitListener();
injectSidebarUI(async () => {
  const problem = extractCodeforcesProblem();
  if (!problem) return;

  renderPrerequisites({
    prerequisites: ["Analyzing..."],
    difficulty: ""
  });
  const handle = getUserHandle();
  console.log(handle)
  const payload = {
    ...problem,
    ...(handle ? { handle } : {})
  };
  const result = await fetchPrerequisites(payload);
  renderPrerequisites(result);
});