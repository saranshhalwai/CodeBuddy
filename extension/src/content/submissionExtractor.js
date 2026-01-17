export function getUserHandle() {
  const link = document.querySelector(
    ".lang-chooser a[href^='/profile/']"
  );
  if (!link) return null;
  console.log(link.textContent)
  return link.textContent.trim();
}