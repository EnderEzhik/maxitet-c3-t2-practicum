const modCardsContainer = document.getElementById("cardsContainer");

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
        const response = await fetch("http://localhost:8000/mods", {
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

document.addEventListener("DOMContentLoaded", async () => {
    await fetchMods();
});
