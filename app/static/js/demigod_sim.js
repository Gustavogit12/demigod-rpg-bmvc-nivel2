document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("sim-form");
    const titleInput = document.getElementById("title");
    const godSelect = document.getElementById("godly_parent");
    const levelInput = document.getElementById("level");
    const abilitySelect = document.getElementById("ability_index");
    const previewBox = document.getElementById("sim-preview");
    const formError = document.getElementById("form-error");

    const classTable = {
        Zeus: { atk: 24, mults: [1.8, 1.2] },
        Poseidon: { atk: 20, mults: [1.6, 1.9] },
        Hades: { atk: 26, mults: [1.5, 2.1] }
    };

    function updatePreview() {
        if (!godSelect || !levelInput || !previewBox) return;
        const god = godSelect.value;
        const lvl = Math.max(1, Math.min(20, parseInt(levelInput.value) || 1));
        const idx = abilitySelect ? (parseInt(abilitySelect.value) || 0) : 0;

        if (classTable[god]) {
            const c = classTable[god];
            const atk = c.atk + (lvl - 1) * 4;
            const mult = c.mults[idx] || c.mults[0];
            const raw = (atk * mult).toFixed(1);
            previewBox.innerHTML = `Dano bruto estimado: <strong>${raw}</strong> (ATQ ${atk} × ${mult}x no nível ${lvl})`;
        } else {
            previewBox.textContent = "Selecione linhagem e nível para prévia rápida.";
        }
    }

    if (godSelect && levelInput) {
        godSelect.addEventListener("change", updatePreview);
        levelInput.addEventListener("input", updatePreview);
        if (abilitySelect) abilitySelect.addEventListener("change", updatePreview);
        updatePreview();
    }

    if (form) {
        form.addEventListener("submit", (e) => {
            const title = titleInput.value.trim();
            const god = godSelect.value;
            const lvl = parseInt(levelInput.value);

            if (title.length < 3) {
                e.preventDefault();
                formError.textContent = "O título deve ter pelo menos 3 caracteres.";
                formError.classList.remove("hidden");
                titleInput.focus();
                return;
            }

            if (!god) {
                e.preventDefault();
                formError.textContent = "Selecione uma linhagem divina.";
                formError.classList.remove("hidden");
                godSelect.focus();
                return;
            }

            if (isNaN(lvl) || lvl < 1 || lvl > 20) {
                e.preventDefault();
                formError.textContent = "O nível deve ser um número entre 1 e 20.";
                formError.classList.remove("hidden");
                levelInput.focus();
            }
        });
    }

    const filterInput = document.getElementById("filter-input");
    const items = document.querySelectorAll(".sim-item");
    if (filterInput) {
        filterInput.addEventListener("input", () => {
            const q = filterInput.value.toLowerCase().trim();
            items.forEach((el) => {
                const text = el.getAttribute("data-filter") || "";
                el.style.display = text.includes(q) ? "flex" : "none";
            });
        });
    }

    document.querySelectorAll(".delete-form").forEach((delForm) => {
        delForm.addEventListener("submit", (e) => {
            const t = delForm.getAttribute("data-title");
            if (!confirm(`Excluir a simulação "${t}"?`)) {
                e.preventDefault();
            }
        });
    });
});