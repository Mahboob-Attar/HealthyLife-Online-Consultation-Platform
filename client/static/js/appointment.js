document.addEventListener("DOMContentLoaded", () => {

  loadDoctors();

  document.getElementById("searchBtn")
    .addEventListener("click", searchDoctors);

  document.getElementById("confirmBookingBtn")
    .addEventListener("click", confirmBooking);

});

let selectedDoctorId = null;


// ================= LOAD AVAILABLE DOCTORS =================
function loadDoctors() {

  fetch("/appointments/api/doctors")
    .then(res => res.json())
    .then(res => {

      if (!res.success || !res.available || res.available.length === 0) {
        showMessage("availableDoctorList", "No doctors available at this time");
        return;
      }

      renderDoctors(res.available, "availableDoctorList");

    })
    .catch(() => showMessage("availableDoctorList", "Server error"));
}


// ================= SEARCH DOCTORS =================
function searchDoctors() {

  const query = document.getElementById("searchInput").value.trim();

  if (!query) {
    loadDoctors();
    return;
  }

  fetch(`/appointments/api/doctors/search?q=${encodeURIComponent(query)}`)
    .then(res => res.json())
    .then(res => {

      if (!res.success || !res.available || res.available.length === 0) {
        showMessage("availableDoctorList", "No active doctors found");
        return;
      }

      renderDoctors(res.available, "availableDoctorList");

    })
    .catch(() => showMessage("availableDoctorList", "Search error"));
}


// ================= RENDER DOCTOR CARDS =================
function renderDoctors(doctors, containerId) {

  const container = document.getElementById(containerId);
  container.innerHTML = "";

  doctors.forEach(doc => {

    const card = `
      <div class="doctor-card">

        <h3>${doc.name}</h3>
        <p>${doc.specialization}</p>
        <p>${doc.experience} years experience</p>

        <button onclick="openBookingModal('${doc.employee_id}')">
          Book Appointment
        </button>

      </div>
    `;

    container.innerHTML += card;

  });

}


// ================= SHOW MESSAGE =================
function showMessage(containerId, msg) {
  document.getElementById(containerId).innerHTML = `<p>${msg}</p>`;
}


// ================= OPEN MODAL =================
function openBookingModal(employeeId) {

  selectedDoctorId = employeeId;
  document.getElementById("bookingModal").style.display = "flex";

  loadAvailability(employeeId);
}


// ================= CLOSE MODAL =================
function closeModal() {
  document.getElementById("bookingModal").style.display = "none";
}


// ================= LOAD AVAILABILITY =================
function loadAvailability(employeeId) {

  fetch(`/appointments/api/availability/${employeeId}`)
    .then(res => res.json())
    .then(res => {

      const list = document.getElementById("availabilityList");
      list.innerHTML = "";

      if (!res.success || res.data.length === 0) {
        list.innerHTML = "<p>No available slots</p>";
        return;
      }

      res.data.forEach(slot => {
        list.innerHTML += `
          <div>
            ${formatDate(slot.start_datetime)} → ${formatDate(slot.end_datetime)}
          </div>
        `;
      });

    })
    .catch(() => {
      document.getElementById("availabilityList").innerHTML = "<p>Error loading slots</p>";
    });
}


// ================= CONFIRM BOOKING =================
function confirmBooking() {

  const btn = document.getElementById("confirmBookingBtn");
  btn.disabled = true;

  const time = document.getElementById("appointmentTime").value;
  const agreed = document.getElementById("policyAgree").checked;

  if (!time) {
    alert("Please select time");
    btn.disabled = false;
    return;
  }

  if (!agreed) {
    alert("You must agree to consultation policy");
    btn.disabled = false;
    return;
  }

  fetch("/appointments/api/book", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    employee_id: selectedDoctorId,
    datetime: time,
    policy_agreed: agreed   
  })
})
  .then(res => res.json())
  .then(res => {

    btn.disabled = false;

    if (!res.success) {
      alert(res.error || "Booking failed");
      return;
    }

    closeModal();
    openSuccessModal();

  })
  .catch(() => {
    btn.disabled = false;
    alert("Server error during booking");
  });
}


// ================= SUCCESS MODAL =================
function openSuccessModal() {
  document.getElementById("successModal").style.display = "flex";
}

function closeSuccessModal() {
  document.getElementById("successModal").style.display = "none";
}


// ================= FORMAT DATE =================
function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleString();
}


