export async function getUserHandle() {
  const profileLink = document.querySelector('a[href^="/profile/"]');
  if (!profileLink) return null;
  return profileLink.textContent.trim();
}

export async function getProblemMeta() {
  const parts = location.pathname.split("/");

  if (location.pathname.includes("/problemset/problem/")) {
    return {
      contestId: parts[3],
      index: parts[4]
    };
  }

  if (location.pathname.includes("/contest/")) {
    return {
      contestId: parts[2],
      index: parts[4]
    };
  }

  return null;
}