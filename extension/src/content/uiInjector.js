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
      <div style="
        display:flex;
        align-items:center;
        gap:6px;
      ">
        <span style="
          font-size:14px;
          color:#3B5998;
        ">→</span>

        <span style="
          font-size:14px;
          font-weight:600;
          color:#3B5998;
        ">
          Prerequisites
        </span>
      </div>

      <span id="cf-prereq-toggle" style="
        width:12px;
        height:12px;
        display:inline-block;
      "></span>
    </div>

    <div style="
      border-top:1px solid #e0e0e0;
      margin:6px 0;
    "></div>

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

  // inject SVG AFTER element exists
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

  if (!result || !Array.isArray(result.prerequisites)) {
    box.innerHTML = `
      <div style="font-size:11px; color:red;">
        Invalid response format
      </div>
    `;
    return;
  }

  const bgColor = {
    EASY: "#f5f5f5",
    MEDIUM: "#e6e6e6",
    HARD: "#d6d6d6"
  };

  box.innerHTML = `
    <div style="
      display:flex;
      flex-direction:column;
      gap:4px;
      margin-top:4px;
    ">
      ${result.prerequisites
        .map(p => `
          <div style="
            display:inline-block;
            width:fit-content;
            padding:3px 7px;
            font-size:11px;
            border-radius:3px;
            background:${bgColor[p.level] || "#f5f5f5"};
            border:1px solid #b9b9b9;
            color:black;
          ">
            ${p.topic}
          </div>
        `)
        .join("")}
    </div>
  `;
}
