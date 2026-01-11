import { extractCodeforcesProblem } from "./content/extractor.js";

(function () {
  const data = extractCodeforcesProblem();
  if (!data) return;
  console.log("CF_PROBLEM_EXTRACTED", data);
})();
