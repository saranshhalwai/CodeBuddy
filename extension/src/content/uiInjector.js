let container;
let collapsed = false;

export function injectSidebarUI(onAnalyzeClick) {
  if (container) return;

  const sidebar = document.querySelector("#sidebar");
  if (!sidebar) return;

  const boxes = sidebar.querySelectorAll(".roundbox.sidebox");
  if (boxes.length < 1) return;

  container = document.createElement("div");
  container.className = "roundbox sidebox borderTopRound";
  container.style.padding = "6px 8px";

  container.innerHTML = `
    <div id="cf-prereq-header" style="
      display:flex;
      align-items:center;
      justify-content:space-between;
      cursor:pointer;
      user-select:none;
    ">
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="font-size:14px; color:#3B5998;">→</span>
        <span style="font-size:14px; font-weight:600; color:#3B5998;">
          Prerequisites
        </span>
      </div>
      <span id="cf-prereq-toggle"
        style="width:12px; height:12px; display:inline-block;">
      </span>
    </div>

    <div style="border-top:1px solid #e0e0e0; margin:6px 0;"></div>

    <button id="cf-analyze-btn"
      style="
        width:fit-content;
        padding:3px 8px;
        font-size:11px;
        background:#f8f8f8;
        border:1px solid #b9b9b9;
        border-radius:3px;
        cursor:pointer;
        color:#000;
      ">
      Analyze
    </button>

    <div id="cf-prereq-result" style="margin-top:6px;"></div>
  `;

  boxes[0].after(container);

  const arrow = container.querySelector("#cf-prereq-toggle");

  arrow.innerHTML = `
    <svg viewBox="0 0 320 512"
         width="12"
         height="12"
         style="fill:#777; display:block; transition:transform 0.15s ease;">
      <path d="M96 96l128 160-128 160"/>
    </svg>
  `;

  container.querySelector("#cf-analyze-btn").onclick = onAnalyzeClick;

  container.querySelector("#cf-prereq-header").onclick = () => {
    collapsed = !collapsed;

    container.querySelector("#cf-prereq-result").style.display =
      collapsed ? "none" : "block";

    arrow.firstElementChild.style.transform =
      collapsed ? "rotate(0deg)" : "rotate(90deg)";
  };
}

export function renderPrerequisites(result) {
  const box = document.getElementById("cf-prereq-result");
  if (!box) return;

  let tags;
  if (Array.isArray(result)) {
    tags = result;
  } else if (Array.isArray(result?.tags)) {
    tags = result.tags;
  } else {
    box.innerHTML = `
      <div style="font-size:11px; color:red;">
        Invalid response format
      </div>
    `;
    return;
  }

  const knownTags = tags.filter(t => t.known === true);
  const unknownTags = tags.filter(t => t.known !== true);

  unknownTags.sort((a, b) => a.tag.localeCompare(b.tag));

  const grayShades = ["#f5f5f5", "#ececec", "#e2e2e2", "#d8d8d8"];

  box.innerHTML = `
    <div style="
      display:flex;
      flex-direction:column;
      gap:4px;
      margin-top:4px;
    ">

      <!-- ✅ Known tags on top -->
      ${knownTags.map(t => `
        <div style="
          display:inline-flex;
          align-items:center;
          gap:6px;
          width:fit-content;
          padding:3px 7px;
          font-size:11px;
          border-radius:3px;
          background:#ffffff;
          border:1px solid #34a853;
          color:#137333;
          font-weight:600;
        ">
          ✓ ${t.tag}
        </div>
      `).join("")}

      <!-- ⏳ Unknown tags with increasing gray -->
      ${unknownTags.map((t, idx) => {
        const bg = grayShades[idx % grayShades.length];
        return `
          <div style="
            display:inline-flex;
            align-items:center;
            gap:6px;
            width:fit-content;
            padding:3px 7px;
            font-size:11px;
            border-radius:3px;
            background:${bg};
            border:1px solid #b9b9b9;
            color:#000;
          ">
            ${t.tag}
          </div>
        `;
      }).join("")}

    </div>
  `;
}

