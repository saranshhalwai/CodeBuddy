export function extractCodeforcesProblem() {
  const root = document.querySelector(".problem-statement");
  if (!root) return null;

  const title = root.querySelector(".header .title")?.innerText.trim();
  const timeLimit = root.querySelector(".time-limit")?.innerText.trim();
  const memoryLimit = root.querySelector(".memory-limit")?.innerText.trim();
  const statement = root.innerText.trim();
  const examples = root.querySelector(".sample-tests")?.innerText.trim() || null;
  const editorialLink = document
    .querySelector("#sidebar .sidebar-menu ul li:nth-child(2) a")
    ?.href || null;

  return {
    platform: "Codeforces",
    url: location.href,
    title,
    timeLimit,
    memoryLimit,
    statement,
    examples,
    editorialLink
  };
}
