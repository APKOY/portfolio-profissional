// ==============================
//      ADMIN – Tabs
// ==============================
document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".admin-tab-button");
    const panels = document.querySelectorAll(".admin-panel");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            panels.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            document.querySelector(btn.dataset.target).classList.add("active");
        });
    });

    loadProjects();
    loadSkills();
    loadExperiences();

    // Botões de reset
    const pfReset = document.querySelector("#project-form-reset");
    if (pfReset) pfReset.addEventListener("click", () => clearForm("project-form"));

    const sfReset = document.querySelector("#skill-form-reset");
    if (sfReset) sfReset.addEventListener("click", () => clearForm("skill-form"));

    const efReset = document.querySelector("#experience-form-reset");
    if (efReset) efReset.addEventListener("click", () => clearForm("experience-form"));
});

// ==============================
//      HELPERS
// ==============================
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) form.reset();
    const hidden = document.querySelector(`#${formId} input[type='hidden']`);
    if (hidden) hidden.value = "";
}

async function apiRequest(url, method = "GET", body = null, isJson = false) {
    const options = { method };

    if (body) {
        if (isJson) {
            options.headers = { "Content-Type": "application/json" };
            options.body = JSON.stringify(body);
        } else {
            options.body = body;
        }
    }

    const response = await fetch(url, options);

    if (!response.ok) {
        const text = await response.text();
        console.error("Erro na API:", text);
        alert("Erro na operação.");
        return null;
    }

    try {
        return await response.json();
    } catch {
        return {};
    }
}

// ==============================
//      PROJECTS
// ==============================
async function loadProjects() {
    const data = await apiRequest("/api/projects");
    if (!data) return;

    const tbody = document.querySelector("#projects-table tbody");
    tbody.innerHTML = "";

    data.forEach(p => {
        const row = `
        <tr>
            <td>${p.title}</td>
            <td>${p.technologies || ""}</td>
            <td>${p.date || ""}</td>
            <td>${p.status || ""}</td>
            <td>
                <button class="btn small" onclick="editProject(${p.id})">Editar</button>
                <button class="btn small outline" onclick="deleteProject(${p.id})">Excluir</button>
            </td>
        </tr>`;
        tbody.insertAdjacentHTML("beforeend", row);
    });
}

async function editProject(id) {
    const p = await apiRequest(`/api/projects/${id}`);
    if (!p) return;

    document.querySelector("#project-id").value = p.id;
    document.querySelector("#project-title").value = p.title;
    document.querySelector("#project-description").value = p.description;
    document.querySelector("#project-technologies").value = p.technologies || "";
    document.querySelector("#project-github").value = p.github_url || "";
    document.querySelector("#project-demo").value = p.demo_url || "";
    document.querySelector("#project-date").value = p.date || "";
    document.querySelector("#project-status").value = p.status || "";

    document.querySelector("[data-target='#admin-projects']").click();
}

document.querySelector("#project-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = document.querySelector("#project-id").value;

    const body = {
        title: document.querySelector("#project-title").value,
        description: document.querySelector("#project-description").value,
        technologies: document.querySelector("#project-technologies").value,
        github_url: document.querySelector("#project-github").value,
        demo_url: document.querySelector("#project-demo").value,
        date: document.querySelector("#project-date").value,
        status: document.querySelector("#project-status").value,
    };

    const url = id ? `/api/projects/${id}` : `/api/projects`;
    const method = id ? "PUT" : "POST";

    const res = await apiRequest(url, method, body, true);
    if (res) {
        clearForm("project-form");
        loadProjects();
    }
});

async function deleteProject(id) {
    if (!confirm("Tem certeza que deseja excluir?")) return;

    const res = await apiRequest(`/api/projects/${id}`, "DELETE");
    if (res) loadProjects();
}

// ==============================
//      SKILLS
// ==============================
async function loadSkills() {
    const data = await apiRequest("/api/skills");
    if (!data) return;

    const tbody = document.querySelector("#skills-table tbody");
    tbody.innerHTML = "";

    data.forEach(s => {
        const row = `
        <tr>
            <td>${s.name}</td>
            <td>${s.level || ""}</td>
            <td>${s.category || ""}</td>
            <td>
                <button class="btn small" onclick="editSkill(${s.id})">Editar</button>
                <button class="btn small outline" onclick="deleteSkill(${s.id})">Excluir</button>
            </td>
        </tr>`;
        tbody.insertAdjacentHTML("beforeend", row);
    });
}

async function editSkill(id) {
    const s = await apiRequest(`/api/skills/${id}`);
    if (!s) return;

    document.querySelector("#skill-id").value = s.id;
    document.querySelector("#skill-name").value = s.name;
    document.querySelector("#skill-level").value = s.level || "";
    document.querySelector("#skill-category").value = s.category || "";

    document.querySelector("[data-target='#admin-skills']").click();
}

document.querySelector("#skill-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = document.querySelector("#skill-id").value;

    const body = {
        name: document.querySelector("#skill-name").value,
        level: document.querySelector("#skill-level").value,
        category: document.querySelector("#skill-category").value,
    };

    const url = id ? `/api/skills/${id}` : `/api/skills`;
    const method = id ? "PUT" : "POST";

    const res = await apiRequest(url, method, body, true);
    if (res) {
        clearForm("skill-form");
        loadSkills();
    }
});

async function deleteSkill(id) {
    if (!confirm("Excluir habilidade?")) return;

    const res = await apiRequest(`/api/skills/${id}`, "DELETE");
    if (res) loadSkills();
}

// ==============================
//      EXPERIENCES
// ==============================
async function loadExperiences() {
    const data = await apiRequest("/api/experiences");
    if (!data) return;

    const tbody = document.querySelector("#experiences-table tbody");
    tbody.innerHTML = "";

    data.forEach(exp => {
        const period = `${exp.start_date || ""} - ${exp.end_date || ""}`;
        const row = `
        <tr>
            <td>${exp.role}</td>
            <td>${exp.company || ""}</td>
            <td>${period}</td>
            <td>
                <button class="btn small" onclick="editExperience(${exp.id})">Editar</button>
                <button class="btn small outline" onclick="deleteExperience(${exp.id})">Excluir</button>
            </td>
        </tr>`;
        tbody.insertAdjacentHTML("beforeend", row);
    });
}

async function editExperience(id) {
    const exp = await apiRequest(`/api/experiences/${id}`);
    if (!exp) return;

    document.querySelector("#experience-id").value = exp.id;
    document.querySelector("#experience-role").value = exp.role;
    document.querySelector("#experience-company").value = exp.company || "";
    document.querySelector("#experience-location").value = exp.location || "";
    document.querySelector("#experience-start").value = exp.start_date || "";
    document.querySelector("#experience-end").value = exp.end_date || "";
    document.querySelector("#experience-current").checked = exp.current || false;
    document.querySelector("#experience-description").value = exp.description || "";

    document.querySelector("[data-target='#admin-experiences']").click();
}

document.querySelector("#experience-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = document.querySelector("#experience-id").value;

    const body = {
        role: document.querySelector("#experience-role").value,
        company: document.querySelector("#experience-company").value,
        location: document.querySelector("#experience-location").value,
        start_date: document.querySelector("#experience-start").value,
        end_date: document.querySelector("#experience-end").value,
        current: document.querySelector("#experience-current").checked,
        description: document.querySelector("#experience-description").value,
    };

    const url = id ? `/api/experiences/${id}` : `/api/experiences`;
    const method = id ? "PUT" : "POST";

    const res = await apiRequest(url, method, body, true);
    if (res) {
        clearForm("experience-form");
        loadExperiences();
    }
});

async function deleteExperience(id) {
    if (!confirm("Excluir experiência?")) return;

    const res = await apiRequest(`/api/experiences/${id}`, "DELETE");
    if (res) loadExperiences();
}
