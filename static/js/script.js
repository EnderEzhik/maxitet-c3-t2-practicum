const modCardsContainer = document.getElementById("cardsContainer");
const totalCount = document.getElementById("totalCount");
const filtersForm = document.getElementById("filtersForm");
const versionSelect = document.getElementById("versionSelect");
const categoryCheckboxesContainer = document.querySelector(".filter-checkboxes");
const prevPageButton = document.getElementById("prevPage");
const nextPageButton = document.getElementById("nextPage");
const pageNumbersContainer = document.getElementById("pageNumbers");
const pageInfo = document.getElementById("pageInfo");
const modDetailsModalElement = document.getElementById("modDetailsModal");
const modDetailsTitle = document.getElementById("modDetailsTitle");
const modDetailsDescription = document.getElementById("modDetailsDescription");
const modDetailsDownloads = document.getElementById("modDetailsDownloads");
const modDetailsModal = window.bootstrap ? new window.bootstrap.Modal(modDetailsModalElement) : null;

const modUploadModalElement = document.getElementById("modUploadModal");
const modUploadModal = window.bootstrap ? new window.bootstrap.Modal(modUploadModalElement) : null;

const modUploadTitle = document.getElementById("modUploadTitle");

const modUploadNameSection = document.getElementById("modUploadNameSection");
const modUploadDescriptionSection = document.getElementById("modUploadDescriptionSection");
const modUploadCategoriesSection = document.getElementById("modUploadCategoriesSection");

const modUploadNameInput = document.getElementById("modUploadNameInput");
const modUploadDescriptionInput = document.getElementById("modUploadDescriptionInput");
const modUploadVersionSelect = document.getElementById("modUploadVersionSelect");
const modUploadCategoryCheckboxes = document.getElementById("modUploadCategoryCheckboxes");
const modUploadFileInput = document.getElementById("modUploadFileInput");
const modUploadError = document.getElementById("modUploadError");
const modUploadSubmitBtn = document.getElementById("modUploadSubmitBtn");

const openModUploadFromDetailsBtn = document.getElementById("openModUploadFromDetailsBtn");
const openUploadCreateBtn = document.querySelector('button[upload-mod-tooltip="Загрузить мод"]');

const MODS_PER_PAGE = 9;
let allMods = [];
let currentPage = 1;

let modUploadMode = /** @type {"create"|"upload"|null} */ (null);
let modUploadTargetModId = null;
let lastOpenedModId = null;

/** @type {Array<{id:number, version:string}>} */
let versionsCache = [];
/** @type {Array<{id:number, category:string}>} */
let categoriesCache = [];

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/** @param {string} value */
function tokenizeVersion(value) {
    const tokens = String(value).match(/\d+|[a-zA-Z]+/g);
    return tokens ?? [];
}

/**
 * Сравнение версий Minecraft: от новой к старой.
 * @param {string} left
 * @param {string} right
 * @returns {number}
 */
function compareMinecraftVersionsDesc(left, right) {
    const leftTokens = tokenizeVersion(left);
    const rightTokens = tokenizeVersion(right);
    const maxLength = Math.max(leftTokens.length, rightTokens.length);

    for (let index = 0; index < maxLength; index += 1) {
        const leftToken = leftTokens[index];
        const rightToken = rightTokens[index];

        if (leftToken === undefined) {
            return 1;
        }
        if (rightToken === undefined) {
            return -1;
        }

        const leftNumber = Number(leftToken);
        const rightNumber = Number(rightToken);
        const leftIsNumber = Number.isInteger(leftNumber);
        const rightIsNumber = Number.isInteger(rightNumber);

        if (leftIsNumber && rightIsNumber && leftNumber !== rightNumber) {
            return rightNumber - leftNumber;
        }

        if (leftIsNumber !== rightIsNumber) {
            return leftIsNumber ? -1 : 1;
        }

        if (leftToken !== rightToken) {
            return rightToken.localeCompare(leftToken, "ru");
        }
    }

    return 0;
}

/** @param {Array<{id: number, version: string}>} versions */
function sortVersionsDesc(versions) {
    return [...versions].sort((left, right) => compareMinecraftVersionsDesc(left.version, right.version));
}

/** @param {string} title @param {string} description @param {string[]|string} versions @param {string[]|string} categories */
function createModCard(title, description, versions, categories) {
    const article = document.createElement("article");
    article.className = "mod-card";
    article.tabIndex = 0;
    article.role = "button";

    const vList = Array.isArray(versions)
        ? sortVersionsDesc(versions)
        : String(versions).split(/[\s,;]+/).filter(Boolean);
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

/** @param {{ id: number, name: string, description: string, versions: Array<{id: number, version: string}> }} mod */
function openModDetails(mod) {
    if (!modDetailsModal) {
        return;
    }

    modDetailsTitle.textContent = mod.name;
    modDetailsDescription.textContent = mod.description;
    lastOpenedModId = mod.id;
    if (openModUploadFromDetailsBtn) {
        openModUploadFromDetailsBtn.dataset.modId = String(mod.id);
    }
    modDetailsDownloads.replaceChildren();

    const versions = Array.isArray(mod.versions) ? sortVersionsDesc(mod.versions) : [];
    if (versions.length === 0) {
        const emptyState = document.createElement("p");
        emptyState.className = "mod-details-empty";
        emptyState.textContent = "Для этого мода пока нет доступных версий для скачивания.";
        modDetailsDownloads.appendChild(emptyState);
        modDetailsModal.show();
        return;
    }

    for (const version of versions) {
        const link = document.createElement("a");
        link.className = "mod-download-link";
        link.href = `/mods/${mod.id}/download?version=${version.version}`;
        link.textContent = `Скачать для Minecraft ${version.version}`;
        modDetailsDownloads.appendChild(link);
    }

    modDetailsModal.show();
}

function resetModUploadForm() {
    modUploadError.textContent = "";

    modUploadNameInput.value = "";
    modUploadDescriptionInput.value = "";

    modUploadVersionSelect.value = "";
    modUploadFileInput.value = "";

    for (const checkbox of modUploadCategoryCheckboxes.querySelectorAll("input[name='categories']")) {
        checkbox.checked = false;
    }
}

function openModUploadForCreateMode() {
    if (!modUploadModal) {
        return;
    }

    modUploadMode = "create";
    modUploadTargetModId = null;

    modUploadTitle.textContent = "Публикация мода";
    modUploadSubmitBtn.textContent = "Опубликовать";

    if (modUploadNameSection) modUploadNameSection.style.display = "";
    if (modUploadDescriptionSection) modUploadDescriptionSection.style.display = "";
    if (modUploadCategoriesSection) modUploadCategoriesSection.style.display = "";

    resetModUploadForm();

    // В режиме создания все версии доступны
    for (const opt of modUploadVersionSelect.options) {
        opt.disabled = false;
    }

    modUploadModal.show();
}

/**
 * @param {{ id:number, versions?: Array<{version:string}> }} mod
 */
function openModUploadForUploadMode(mod) {
    if (!modUploadModal) {
        return;
    }

    modUploadMode = "upload";
    modUploadTargetModId = mod.id;

    modUploadTitle.textContent = "Добавление версии мода";
    modUploadSubmitBtn.textContent = "Загрузить";

    if (modUploadNameSection) modUploadNameSection.style.display = "none";
    if (modUploadDescriptionSection) modUploadDescriptionSection.style.display = "none";
    if (modUploadCategoriesSection) modUploadCategoriesSection.style.display = "none";

    resetModUploadForm();

    const existingVersions = new Set(Array.isArray(mod.versions) ? mod.versions.map((v) => v.version) : []);
    for (const opt of modUploadVersionSelect.options) {
        if (!opt.value) continue;
        opt.disabled = existingVersions.has(opt.value);
    }

    // Подбираем первую активную версию, если выбранная отключена/не выбрана
    if (!modUploadVersionSelect.value) {
        const firstEnabled = Array.from(modUploadVersionSelect.options).find((o) => o.value && !o.disabled);
        if (firstEnabled) modUploadVersionSelect.value = firstEnabled.value;
    } else {
        const selectedOpt = modUploadVersionSelect.selectedOptions[0];
        if (selectedOpt && selectedOpt.disabled) {
            const firstEnabled = Array.from(modUploadVersionSelect.options).find((o) => o.value && !o.disabled);
            if (firstEnabled) modUploadVersionSelect.value = firstEnabled.value;
        }
    }

    modUploadModal.show();
}

async function submitModUpload() {
    const file = modUploadFileInput.files?.[0];
    const selectedVersion = modUploadVersionSelect.value;

    if (!selectedVersion) {
        modUploadError.textContent = "Выберите версию Minecraft.";
        return;
    }

    if (!file) {
        modUploadError.textContent = "Выберите файл .jar.";
        return;
    }

    try {
        if (modUploadMode === "create") {
            const name = modUploadNameInput.value.trim();
            const description = modUploadDescriptionInput.value.trim();
            const selectedCategories = Array.from(
                modUploadCategoryCheckboxes.querySelectorAll("input[name='categories']:checked"),
                (checkbox) => checkbox.value
            );

            if (!name) {
                modUploadError.textContent = "Название мода обязательно.";
                return;
            }
            if (!description) {
                modUploadError.textContent = "Описание мода обязательно.";
                return;
            }
            if (selectedCategories.length === 0) {
                modUploadError.textContent = "Выберите хотя бы одну категорию.";
                return;
            }

            const formData = new FormData();
            formData.append("name", name);
            formData.append("description", description);
            formData.append("version", selectedVersion);
            for (const category of selectedCategories) {
                formData.append("categories", category);
            }
            formData.append("mod_file", file);

            const response = await fetch("/mods", { method: "POST", body: formData });
            if (!response.ok) {
                const err = await response.json().catch(() => null);
                throw new Error(err?.detail ? String(err.detail) : `HTTP ${response.status}`);
            }

            const createdMod = await response.json();
            lastOpenedModId = createdMod.id;
            modUploadModal.hide();
            await fetchMods(getFiltersState());
            const refreshedMod = allMods.find((m) => m.id === createdMod.id);
            openModDetails(refreshedMod || createdMod);
            return;
        }

        if (modUploadMode === "upload") {
            if (!modUploadTargetModId) {
                throw new Error("Не задан mod_id для загрузки версии.");
            }

            const formData = new FormData();
            formData.append("mod_file", file);

            const url = `/mods/${modUploadTargetModId}/upload-file?version_number=${encodeURIComponent(selectedVersion)}`;
            const response = await fetch(url, { method: "POST", body: formData });
            if (!response.ok) {
                const err = await response.json().catch(() => null);
                throw new Error(err?.detail ? String(err.detail) : `HTTP ${response.status}`);
            }

            modUploadModal.hide();
            await fetchMods(getFiltersState());

            const refreshedMod = allMods.find((m) => m.id === modUploadTargetModId);
            if (refreshedMod) {
                openModDetails(refreshedMod);
            }
        }
    } catch (error) {
        console.error(error);
        modUploadError.textContent = error instanceof Error ? error.message : "Ошибка загрузки мода.";
    }
}

/**
 * @typedef {Object} FiltersState
 * @property {string} title
 * @property {string} versionId
 * @property {string[]} categories
 */

/** @returns {FiltersState} */
function getFiltersState() {
    const titleInput = filtersForm.elements.title;
    const versionInput = filtersForm.elements.version_id;
    const checkedCategories = filtersForm.querySelectorAll("input[name='categories']:checked");

    return {
        title: titleInput.value.trim(),
        versionId: versionInput.value,
        categories: Array.from(checkedCategories, (checkbox) => checkbox.value)
    };
}

/**
 * @param {FiltersState} filters
 * @returns {string}
 */
function buildModsQueryString(filters) {
    const params = new URLSearchParams();

    if (filters.title) {
        params.append("title", filters.title);
    }

    if (filters.versionId) {
        params.append("version_id", filters.versionId);
    }

    for (const category of filters.categories) {
        params.append("categories", category);
    }

    return params.toString();
}

function renderPagination() {
    const totalPages = Math.max(1, Math.ceil(allMods.length / MODS_PER_PAGE));
    pageNumbersContainer.replaceChildren();

    for (let page = 1; page <= totalPages; page += 1) {
        const pageButton = document.createElement("button");
        pageButton.type = "button";
        pageButton.className = `page-btn btn btn-outline-secondary btn-sm${page === currentPage ? " active" : ""}`;
        pageButton.dataset.page = String(page);
        pageButton.textContent = String(page);
        pageNumbersContainer.appendChild(pageButton);
    }

    prevPageButton.disabled = currentPage <= 1;
    nextPageButton.disabled = currentPage >= totalPages;
    pageInfo.textContent = `Страница ${currentPage} из ${totalPages}`;
}

function renderCurrentPageMods() {
    const start = (currentPage - 1) * MODS_PER_PAGE;
    const end = start + MODS_PER_PAGE;
    const pageMods = allMods.slice(start, end);

    modCardsContainer.replaceChildren();
    for (const mod of pageMods) {
        const modCard = createModCard(mod.name, mod.description, mod.versions, mod.categories);
        modCard.addEventListener("click", () => {
            openModDetails(mod);
        });
        modCardsContainer.appendChild(modCard);
    }
}

function setPage(nextPage) {
    const totalPages = Math.max(1, Math.ceil(allMods.length / MODS_PER_PAGE));
    currentPage = Math.min(Math.max(nextPage, 1), totalPages);
    renderCurrentPageMods();
    renderPagination();
}

/** @param {FiltersState} filters */
async function fetchMods(filters = { title: "", versionId: "", categories: [] }) {
    try {
        const queryString = buildModsQueryString(filters);
        const url = queryString ? `/mods?${queryString}` : `/mods`;
        const response = await fetch(url, {
            method: "GET"
        });

        if (!response.ok) {
            console.error(response.status);
            console.error(await response.json());
            alert("Ошибка загрузки модов");
        }

        const data = await response.json();
        const mods = data.data;
        const count = data.count;

        allMods = Array.isArray(mods) ? mods : [];
        currentPage = 1;
        renderCurrentPageMods();
        renderPagination();

        totalCount.textContent = `Найдено модов: ${count}`;
    }
    catch (error) {
        console.error(error);
    }
}

async function fetchVersions() {
    try {
        const response = await fetch(`/versions`, { method: "GET" });

        if (!response.ok) {
            console.error(response.status);
            console.error(await response.json());
            alert("Ошибка загрузки версий");
            return;
        }

        const data = await response.json();
        versionsCache = sortVersionsDesc(data.data);

        // Фильтры (value = version.id)
        versionSelect.replaceChildren();
        const anyOpt = document.createElement("option");
        anyOpt.value = "";
        anyOpt.textContent = "Любая";
        versionSelect.appendChild(anyOpt);

        for (const v of versionsCache) {
            const opt = document.createElement("option");
            opt.value = String(v.id);
            opt.textContent = v.version;
            versionSelect.appendChild(opt);
        }

        // Модал (value = version.version)
        modUploadVersionSelect.replaceChildren();
        const modalDefaultOpt = document.createElement("option");
        modalDefaultOpt.value = "";
        modalDefaultOpt.textContent = "Выберите версию";
        modUploadVersionSelect.appendChild(modalDefaultOpt);

        for (const v of versionsCache) {
            const opt = document.createElement("option");
            opt.value = v.version;
            opt.textContent = v.version;
            modUploadVersionSelect.appendChild(opt);
        }
    } catch (error) {
        console.error(error);
    }
}

async function fetchCategories() {
    try {
        const response = await fetch(`/categories`, { method: "GET" });

        if (!response.ok) {
            console.error(response.status);
            console.error(await response.json());
            alert("Ошибка загрузки категорий");
            return;
        }

        const data = await response.json();
        categoriesCache = data.data;

        // Фильтры (чекбоксы в сайдбаре)
        categoryCheckboxesContainer.replaceChildren();
        for (const c of categoriesCache) {
            const label = document.createElement("label");
            label.className = "form-check";

            const input = document.createElement("input");
            input.type = "checkbox";
            input.className = "form-check-input";
            input.name = "categories";
            input.value = c.category;

            label.appendChild(input);
            label.appendChild(document.createTextNode(c.category));
            categoryCheckboxesContainer.appendChild(label);
        }

        // Модал (чекбоксы выбора категорий)
        modUploadCategoryCheckboxes.replaceChildren();
        for (const c of categoriesCache) {
            const label = document.createElement("label");
            label.className = "form-check";

            const input = document.createElement("input");
            input.type = "checkbox";
            input.className = "form-check-input";
            input.name = "categories";
            input.value = c.category;

            label.appendChild(input);
            label.appendChild(document.createTextNode(c.category));
            modUploadCategoryCheckboxes.appendChild(label);
        }
    } catch (error) {
        console.error(error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    await Promise.all([fetchVersions(), fetchCategories()]);
    await fetchMods();

    prevPageButton.addEventListener("click", () => {
        setPage(currentPage - 1);
    });

    nextPageButton.addEventListener("click", () => {
        setPage(currentPage + 1);
    });

    pageNumbersContainer.addEventListener("click", (event) => {
        const target = event.target;
        if (!(target instanceof HTMLButtonElement)) {
            return;
        }

        if (!target.dataset.page) {
            return;
        }

        setPage(Number(target.dataset.page));
    });

    filtersForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        await fetchMods(getFiltersState());
    });

    filtersForm.addEventListener("reset", async () => {
        setTimeout(async () => {
            await fetchMods();
        }, 0);
    });

    if (openUploadCreateBtn) {
        openUploadCreateBtn.addEventListener("click", () => {
            openModUploadForCreateMode();
        });
    }

    if (openModUploadFromDetailsBtn) {
        openModUploadFromDetailsBtn.addEventListener("click", () => {
            const modId = Number(openModUploadFromDetailsBtn.dataset.modId || lastOpenedModId);
            const mod = allMods.find((m) => m.id === modId);
            if (!mod) {
                return;
            }
            openModUploadForUploadMode(mod);
        });
    }

    modUploadSubmitBtn?.addEventListener("click", () => {
        submitModUpload();
    });
});
