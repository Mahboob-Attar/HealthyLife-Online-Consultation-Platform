document.addEventListener("DOMContentLoaded", () => {

  loadDoctors();

  document.getElementById("searchBtn")
    .addEventListener("click", searchDoctors);

});


// ===== LOAD DOCTORS =====
function loadDoctors() {

  fetch("/appointments/api/doctors")
    .then(res => res.json())
    .then(data => renderDoctors(data));

}


// ===== SEARCH =====
function searchDoctors() {

  const query = document.getElementById("searchInput").value;

  fetch(`/appointments/api/doctors?q=${query}`)
    .then(res => res.json())
    .then(data => renderDoctors(data));

}


// ===== RENDER CARDS =====
function renderDoctors(doctors) {

  const container = document.getElementById("doctorList");

  container.innerHTML = "";

  if (!doctors.length) {
    container.innerHTML = "<p>No doctors found</p>";
    return;
  }

  doctors.forEach(doc => {

    const card = `
      <div class="doctor-card">

        <img src="/uploads/doctors/${doc.photo_path}" />

        <h3>${doc.name}</h3>
        <p><strong>${doc.specialization}</strong></p>
        <p>${doc.experience} years</p>

        <button onclick="bookAppointment('${doc.employee_id}')">
          Book Appointment
        </button>

      </div>
    `;

    container.innerHTML += card;

  });

}


// ===== BOOK =====
function bookAppointment(employeeId) {

  const datetime = prompt("Enter date time YYYY-MM-DD HH:MM");

  if (!datetime) return;

  fetch("/appointments/api/book", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ employee_id: employeeId, datetime })
  })
  .then(res => res.json())
  .then(data => {

    if (data.error) {
      alert(data.error);
    } else {
      alert("Appointment booked!");
      window.open(data.meeting_link);
    }

  });

}