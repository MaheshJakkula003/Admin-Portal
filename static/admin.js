const API_BASE = "http://127.0.0.1:5000/api";

function showToast(msg) {
    const toast = document.getElementById('toast');
    const text = document.getElementById('toastMsg');

    if (!toast || !text) return;

    text.textContent = msg;
    toast.classList.add('show');

    setTimeout(() => toast.classList.remove('show'), 3000);
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showDashboard() {
    document.getElementById('authWrapper').style.display = 'none';
    document.getElementById('dashboardWrapper').classList.add('active');

    if (typeof showSection === "function") {
        showSection('dashboard');
    }

    loadOpportunities();
}

window.addEventListener('load', async () => {
    try {
        const res = await fetch(`${API_BASE}/check-session`, {
            credentials: "include"
        });

        if (res.ok) {
            showDashboard();
        }
    } catch {
        console.log("Not logged in");
    }
});

async function handleLogout() {
    try {
        await fetch(`${API_BASE}/logout`, {
            method: "GET",
            credentials: "include"
        });

        document.getElementById('dashboardWrapper').classList.remove('active');
        document.getElementById('authWrapper').style.display = 'flex';

        showToast("Logged out");

    } catch {
        showToast("Logout failed");
    }
}

document.getElementById('loginForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    const remember = document.getElementById('loginRemember').checked;

    if (!isValidEmail(email)) return showToast("Invalid email");
    if (!password) return showToast("Enter password");

    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ email, password, remember })
        });

        const data = await res.json();

        if (!res.ok) return showToast(data.error);

        showToast("Login successful");
        setTimeout(showDashboard, 800);

    } catch {
        showToast("Server error");
    }
});

document.getElementById('signupForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const full_name = document.getElementById('signupName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value.trim();
    const confirm_password = document.getElementById('signupConfirmPassword').value.trim();

    if (!full_name) return showToast("Enter name");
    if (!isValidEmail(email)) return showToast("Invalid email");
    if (password.length < 8) return showToast("Password must be 8+ chars");
    if (password !== confirm_password) return showToast("Passwords mismatch");

    try {
        const res = await fetch(`${API_BASE}/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ full_name, email, password, confirm_password })
        });

        const data = await res.json();

        if (!res.ok) return showToast(data.error);

        showToast("Account created! Please login.");

        setTimeout(() => {
            if (typeof showPage === "function") {
                showPage('loginPage');
            }
        }, 800);

    } catch {
        showToast("Server error");
    }
});

async function loadOpportunities() {
    try {
        const res = await fetch(`${API_BASE}/opportunities`, {
            credentials: "include"
        });

        if (!res.ok) return;

        const result = await res.json();
        const data = result.data;

        const grid = document.querySelector('.opportunities-grid');
        if (!grid) return;

        grid.innerHTML = "";

        if (data.length === 0) {
            grid.innerHTML = "<p>No opportunities found.</p>";
            return;
        }

        data.forEach(op => {
            const card = document.createElement('div');
            card.className = 'opportunity-card';

            const skills = op.skills ? op.skills.split(',') : [];
            const skillTags = skills.map(s =>
                `<span class="skill-tag">${escapeHtml(s)}</span>`
            ).join("");

            card.innerHTML = `
                <h5>${escapeHtml(op.title)}</h5>
                <div><b>Description:</b> ${escapeHtml(op.description)}</div>
                <div><b>Duration:</b> ${escapeHtml(op.duration)}</div>
                <div><b>Start:</b> ${op.start_date}</div>
                <div><b>End:</b> ${op.end_date || '-'}</div>
                <span>${escapeHtml(op.category)}</span>
                <div class="skills-tags">${skillTags}</div>
                <div class="card-actions">
                    <button class="edit-btn">Edit</button>
                    <button class="delete-btn">Delete</button>
                </div>
            `;

            card.querySelector('.edit-btn').onclick = () => editOpportunity(op);
            card.querySelector('.delete-btn').onclick = () => deleteOpportunity(op.id);

            grid.appendChild(card);
        });

    } catch (err) {
        console.error(err);
    }
}

function editOpportunity(op) {
    document.getElementById('oppId').value = op.id;
    document.getElementById('oppName').value = op.title;
    document.getElementById('oppDuration').value = op.duration;
    document.getElementById('oppStartDate').value = op.start_date;
    document.getElementById('oppEndDate').value = op.end_date || '';
    document.getElementById('oppDescription').value = op.description;
    document.getElementById('oppSkills').value = op.skills;
    document.getElementById('oppCategory').value = op.category;
    document.getElementById('oppFuture').value = op.future_opportunities;
    document.getElementById('oppMaxApplicants').value = op.max_applicants;

    document.getElementById('modalTitle').innerText = "Edit Opportunity";
    openOpportunityModal();
}

async function deleteOpportunity(id) {
    if (!confirm("Delete this opportunity?")) return;

    try {
        const res = await fetch(`${API_BASE}/opportunities/${id}`, {
            method: "DELETE",
            credentials: "include"
        });

        const data = await res.json();

        if (!res.ok) return showToast(data.error);

        showToast("Deleted");
        loadOpportunities();

    } catch {
        showToast("Server error");
    }
}

document.getElementById('opportunityForm')?.addEventListener('submit', async function (e) {
    e.preventDefault();

    const id = document.getElementById('oppId').value;

    const payload = {
        title: document.getElementById('oppName').value.trim(),
        duration: document.getElementById('oppDuration').value.trim(),
        start_date: document.getElementById('oppStartDate').value,
        end_date: document.getElementById('oppEndDate').value,
        description: document.getElementById('oppDescription').value.trim(),
        skills: document.getElementById('oppSkills').value.trim(),
        category: document.getElementById('oppCategory').value,
        future_opportunities: document.getElementById('oppFuture').value.trim(),
        max_applicants: document.getElementById('oppMaxApplicants').value
    };

    if (!payload.title || !payload.duration || !payload.start_date || !payload.description) {
        return showToast("Fill required fields");
    }

    try {
        const res = await fetch(
            id ? `${API_BASE}/opportunities/${id}` : `${API_BASE}/opportunities`,
            {
                method: id ? "PUT" : "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(payload)
            }
        );

        const data = await res.json();

        if (!res.ok) return showToast(data.error);

        showToast(id ? "Updated!" : "Created!");

        closeOpportunityModal();
        this.reset();
        loadOpportunities();

    } catch {
        showToast("Server error");
    }
});