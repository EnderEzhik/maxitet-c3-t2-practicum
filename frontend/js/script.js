const API_BASE = "http://localhost:8000";

const modCardsContainer = document.getElementById("cardsContainer");
const versionSelect = document.getElementById("versionSelect");
const categoryCheckboxesContainer = document.querySelector(".filter-checkboxes");

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/** @param {string} title @param {string} description @param {string[]|string} versions @param {string[]|string} categories */
function createModCard(title, description, versions, categories) {
    const article = document.createElement("article");
    article.className = "mod-card";

    const vList = Array.isArray(versions) ? versions : String(versions).split(/[\s,;]+/).filter(Boolean);
    const cList = Array.isArray(categories) ? categories : String(categories).split(/[\s,;]+/).filter(Boolean);

    const versionChips = vList.map((v) => `<span class="mod-chip" role="listitem">${escapeHtml(v.version)}</span>`).join("");
    const categoryChips = cList.map((c) => `<span class="mod-chip" role="listitem">${escapeHtml(c.category)}</span>`).join("");

    article.innerHTML = `
        <h3 class="mod-card__title">${escapeHtml(title)}</h3>
        <p class="mod-card__desc">${escapeHtml(description)}</p>
        <div class="mod-card__section">
            <div class="mod-card__label">Версии</div>
            <div class="mod-card__chips" role="list">${versionChips}</div>
        </div>
        <div class="mod-card__section">
            <div class="mod-card__label">Категории</div>
            <div class="mod-card__chips" role="list">${categoryChips}</div>
        </div>
    `;
    return article;
}

async function fetchMods() {
    try {
        const response = await fetch(`${API_BASE}/mods`, {
            method: "GET"
        });

        if (!response.ok) {
            console.error(response.status);
            console.error(await response.json());
            alert("Ошибка загрузки модов");
        }

        const data = await response.json();
        const mods = data.data;

        Array.from(mods).forEach(mod => {
            const modCard = createModCard(mod.name, mod.description, mod.versions, mod.categories);
            modCardsContainer.appendChild(modCard);
        });
    }
    catch (error) {
        console.error(error);
    }
}

async function fetchVersions() {
    try {
        const response = await fetch(`${API_BASE}/versions`, { method: "GET" });

        if (!response.ok) {
            console.error(response.status);
            console.error(await response.json());
            alert("Ошибка загрузки версий");
            return;
        }

        const data = await response.json();
        const versions = data.data;

        for (const v of versions) {
            const opt = document.createElement("option");
            opt.value = v.version;
            opt.textContent = v.version;
            versionSelect.appendChild(opt);
        }
    } catch (error) {
        console.error(error);
    }
}

async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`, { method: "GET" });

        if (!response.ok) {
            console.error(response.status);
            console.error(await response.json());
            alert("Ошибка загрузки категорий");
            return;
        }

        const data = await response.json();
        const categories = data.data;

        categoryCheckboxesContainer.replaceChildren();

        for (const c of categories) {
            const label = document.createElement("label");
            label.className = "form-check";

            const input = document.createElement("input");
            input.type = "checkbox";
            input.className = "form-check-input";
            input.name = "category";
            input.value = c.category;

            label.appendChild(input);
            label.appendChild(document.createTextNode(c.category));

            categoryCheckboxesContainer.appendChild(label);
        }
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await Promise.all([fetchMods(), fetchVersions(), fetchCategories()]);
});
