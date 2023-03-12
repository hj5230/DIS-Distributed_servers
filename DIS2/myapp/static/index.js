const placement = document.querySelector("#placement");

const getGroupHTML = (topic) =>
  `<span class="badge bg-secondary">${topic}</span>
  <div class='card-group'>`;

const getCardHTML = (title, text, timestamp) =>
  `<div class='card'>
    <div class="card-header note-title" data-title="${title}">${title}</div>
      <div class="card-body">
        <p class="card-text">${text}</p>
        <small class="card-text">${timestamp}</small>
      </div>
  </div>`;

const renderNotes = async () => {
  const pro = await fetch(`http://localhost:8000/loadnotes/`);
  const res = await pro.json();
  const notesHTML = res.map((t) => {
    let group = getGroupHTML(t.name);
    const cardsHTML = t.notes.map((n) =>
      getCardHTML(n.name, n.text, n.timestamp)
    );
    group += cardsHTML.join("");
    group += "</div>";
    return group;
  });
  placement.innerHTML = notesHTML.join("");

  const noteTitles = document.querySelectorAll(".note-title");
  noteTitles.forEach((title) => {
    title.addEventListener("click", async () => {
      const searchTerm = title.dataset.title;
      const wikiPro = await fetch(
        `https://en.wikipedia.org/api/rest_v1/page/summary/${searchTerm}`
      );
      const wikiRes = await wikiPro.json();
      const extractHTML = wikiRes.extract_html;
      const tooltipHTML = `<div class="collapse" id="collapse-${searchTerm}">
                            <div class="card card-body">${extractHTML}</div>
                          </div>`;
      if (title.getAttribute("data-bs-toggle") !== "collapse") {
        title.setAttribute("data-bs-toggle", "collapse");
        title.setAttribute("data-bs-target", `#collapse-${searchTerm}`);
        title.insertAdjacentHTML("afterend", tooltipHTML);
        const tooltipCollapse = new bootstrap.Collapse(
          document.getElementById(`collapse-${searchTerm}`)
        );
        tooltipCollapse.show();
      } else {
        const tooltipCollapse = bootstrap.Collapse.getInstance(
          document.getElementById(`collapse-${searchTerm}`)
        );
        tooltipCollapse.hide();
      }
    });
  });
};

document.querySelector("#create").onclick = async () => {
  const topic = document.querySelector("#topic").value;
  const title = document.querySelector("#title").value;
  const text = document.querySelector("#text").value;
  const formData = new FormData();
  formData.append("topic", topic);
  formData.append("title", title);
  formData.append("text", text);
  const pro = await fetch(`http://localhost:8000/savenote/`, {
    method: "POST",
    body: formData,
  });
  if (pro.statusText === "OK") {
    placement.innerHTML = "";
    renderNotes();
  }
};

(() => {
  renderNotes();
})();
