document.addEventListener("DOMContentLoaded", () => {

  loadAllDoctors();

  document.getElementById("searchBtn")
    .addEventListener("click", searchDoctors);

  document.getElementById("confirmBookingBtn")
    .addEventListener("click", confirmBooking);

});


let selectedDoctorId = null;


// ================= LOAD ALL DOCTORS =================
function loadAllDoctors() {

  fetch("/appointments/api/doctors")
    .then(res => res.json())
    .then(res => {

      if (!res.success) return;

      renderDoctors(res.data, "doctorList");

    })
    .catch(err => console.error(err));
}


// ================= SEARCH AVAILABLE DOCTORS =================
function searchDoctors() {

  const query = document.getElementById("searchInput").value.trim();

  if (!query) return;

  fetch(`/appointments/api/doctors/search?q=${query}`)
    .then(res => res.json())
    .then(res => {

      const container = document.getElementById("availableDoctorList");

      if (!res.success || res.data.length === 0) {
        container.innerHTML = "<p>No available doctors found</p>";
        return;
      }

      renderDoctors(res.data, "availableDoctorList");

    })
    .catch(err => console.error(err));
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
    .catch(err => console.error(err));
}


// ================= CONFIRM BOOKING =================
function confirmBooking() {

  const time = document.getElementById("appointmentTime").value;
  const agreed = document.getElementById("policyAgree").checked;

  if (!time) {
    alert("Please select time");
    return;
  }

  if (!agreed) {
    alert("You must agree to consultation policy");
    return;
  }

  fetch("/appointments/api/book", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      employee_id: selectedDoctorId,
      datetime: time
    })
  })
  .then(res => res.json())
  .then(res => {

    if (!res.success) {
      alert(res.error);
      return;
    }

    closeModal();
    openSuccessModal();

  })
  .catch(err => console.error(err));
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