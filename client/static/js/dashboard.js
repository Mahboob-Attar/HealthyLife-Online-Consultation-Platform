/* DASHBOARD MAIN INIT */

document.addEventListener("DOMContentLoaded", () => {
  initDashboard();
  initDoctorApproval();
});

/* =====================================================
   DASHBOARD DATA (Charts + Stats)
===================================================== */

async function initDashboard() {
  try {
    const res = await fetch("/dashboard/data", {
      credentials: "include",
    });

    const result = await res.json();

    if (!result.success) {
      console.error("Dashboard error:", result.message);
      return;
    }

    const { data, role } = result;

    renderTotalDoctors(data);
    renderSpecializationChart(data);
    renderFeedbackChart(data);

    if (role === "admin") {
      console.log("Admin loaded dashboard");
    }
  } catch (err) {
    console.error("Dashboard JS Error:", err);
  }
}

/* ---------- TOTAL DOCTORS ---------- */
function renderTotalDoctors(data) {
  const el = document.getElementById("totalDoctors");
  if (el && data.stats) {
    el.textContent = data.stats.total_doctors || 0;
  }
}

/* ---------- SPECIALIZATION CHART ---------- */
function renderSpecializationChart(data) {
  if (!data.stats?.specializations) return;

  const canvas = document.getElementById("specializationChart");
  if (!canvas) return;

  new Chart(canvas.getContext("2d"), {
    type: "doughnut",
    data: {
      labels: data.stats.specializations.map((s) => s.specialization),
      datasets: [
        {
          data: data.stats.specializations.map((s) => s.count),
          backgroundColor: [
            "#1da1f2",
            "#00ffcc",
            "#ff6384",
            "#ff9f40",
            "#36a2eb",
            "#9966ff",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#ffffff",
            font: { size: 14 },
          },
        },
      },
    },
  });
}

/* ---------- FEEDBACK CHART ---------- */
function renderFeedbackChart(data) {
  if (!data.ratings?.feedback_ratings) return;

  const canvas = document.getElementById("feedbackChart");
  if (!canvas) return;

  const ratings = ["1", "2", "3", "4", "5"];
  const ratingCounts = ratings.map(
    (r) => data.ratings.feedback_ratings[r] || 0
  );
  const totalRatings = ratingCounts.reduce((a, b) => a + b, 0);

  const totalText = document.getElementById("totalRatingsText");
  if (totalText) totalText.textContent = `Total Ratings: ${totalRatings}`;

  new Chart(canvas.getContext("2d"), {
    type: "bar",
    data: {
      labels: ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
      datasets: [
        {
          data: ratingCounts,
          backgroundColor: [
            "rgba(255,77,79,0.9)",
            "rgba(255,136,56,0.9)",
            "rgba(255,219,50,0.9)",
            "rgba(110,207,57,0.9)",
            "rgba(54,207,201,0.95)",
          ],
          borderColor: "rgba(255,255,255,0.3)",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { display: false }, grid: { display: false } },
        x: { ticks: { color: "#b1c7ff" }, grid: { display: false } },
      },
    },
  });
}

/* =====================================================
   DOCTOR APPROVAL SECTION
===================================================== */

let currentDoctorId = null;

function initDoctorApproval() {
  const filter = document.getElementById("statusFilter");
  if (!filter) return;

  filter.addEventListener("change", () => loadDoctors(filter.value));

  loadDoctors();
  loadApprovalStats();
}

function getStatusClass(status) {
  if (status === "approved") return "status-approved";
  if (status === "rejected") return "status-rejected";
  return "status-pending";
}

/* ---------- LOAD DOCTORS ---------- */
async function loadDoctors(status = "pending") {
  const tableBody = document.getElementById("doctorTableBody");
  if (!tableBody) return;

  try {
    const res = await fetch(`/dashboard/admin/doctors?status=${status}`);
    const data = await res.json();

    tableBody.innerHTML = "";

    if (!data.doctors?.length) {
      tableBody.innerHTML = `<tr><td colspan="5">No doctors found</td></tr>`;
      return;
    }

    data.doctors.forEach((doc) => {
      const row = `
        <tr>
          <td>${doc.name}</td>
          <td>${doc.email}</td>
          <td>${doc.location}</td>
          <td><span class="status-badge ${getStatusClass(doc.status)}">${doc.status}</span></td>
          <td>
            <button onclick="viewDoc(${doc.id})">👁</button>
            ${
              doc.status === "pending"
                ? `<button onclick="approveDoc(${doc.id})">✔</button>
                   <button onclick="openRejectModal(${doc.id})">✖</button>`
                : ""
            }
          </td>
        </tr>
      `;
      tableBody.insertAdjacentHTML("beforeend", row);
    });
  } catch (err) {
    console.error("Load doctors error:", err);
  }
}

/* ---------- APPROVE ---------- */
async function approveDoc(id) {
  await fetch(`/dashboard/admin/doctors/${id}/approve`, { method: "POST" });
  loadDoctors(document.getElementById("statusFilter").value);
  loadApprovalStats();
}

/* ---------- REJECT ---------- */
function openRejectModal(id) {
  currentDoctorId = id;
  document.getElementById("rejectReason").value = "";
  document.getElementById("rejectModal").style.display = "flex";
}

async function submitReject() {
  const reason = document.getElementById("rejectReason").value.trim();
  if (!reason) return alert("Enter reason");

  await fetch(`/dashboard/admin/doctors/${currentDoctorId}/reject`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reason }),
  });

  closeRejectModal();
  loadDoctors(document.getElementById("statusFilter").value);
  loadApprovalStats();
}

function closeRejectModal() {
  document.getElementById("rejectModal").style.display = "none";
}

function viewDoc(id) {
  window.open(`/dashboard/admin/doctors/${id}/pdf`, "_blank");
}

/* ---------- STATS ---------- */
async function loadApprovalStats() {
  const res = await fetch("/dashboard/admin/doctors/stats");
  const data = await res.json();

  document.getElementById("totalCount").textContent = data.total || 0;
  document.getElementById("pendingCount").textContent = data.pending || 0;
  document.getElementById("approvedCount").textContent = data.approved || 0;
  document.getElementById("rejectedCount").textContent = data.rejected || 0;
}
