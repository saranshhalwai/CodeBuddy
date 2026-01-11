(function () {
  const data = window.extractCodeforcesProblem();
  if (!data) return;
  console.log("CF_PROBLEM_EXTRACTED", data);
})();