const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor");
const doctorForm = document.getElementById("doctorForm");

const verifyBtn = document.getElementById("verifyLicenseBtn");
const licenseInput = document.getElementById("licenseInput");
const licenseStatus = document.getElementById("licenseStatus");

const successPopup = document.getElementById("successPopup");
const closeSuccess = document.getElementById("closeSuccess");
const successMessage = document.getElementById("successMessage");

let licenseVerified = false;


// ===== FUNCTIONS =====

// Open doctor modal
function openDoctorModal() {
  doctorPopup.classList.add("active");
  document.body.classList.add("popup-open");
}

// Close doctor modal
function closeDoctorModal() {
  doctorPopup.classList.remove("active");
}

// Open success popup WITH DIM
function openSuccessPopup() {
  successPopup.classList.add("show");
  document.body.classList.add("popup-open");
}

// Close success popup + remove dim
function closeSuccessPopup() {
  successPopup.classList.remove("show");
  document.body.classList.remove("popup-open");
}


// ===== OPEN =====
doctorBtn?.addEventListener("click", openDoctorModal);

// ===== CLOSE FORM =====
closeDoctor?.addEventListener("click", () => {
  doctorPopup.classList.remove("active");
  document.body.classList.remove("popup-open");
});


// ===== VERIFY LICENSE =====
verifyBtn?.addEventListener("click", async () => {

  const email = licenseInput.value.trim();

  if (!email) {
    licenseStatus.textContent = "Enter license email first";
    licenseStatus.style.color = "red";
    return;
  }

  licenseStatus.innerHTML = '<span class="spinner"></span> Verifying...';
  licenseStatus.style.color = "orange";

  try {

    const response = await fetch("/doctors/verify-license", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ license: email })
    });

    const result = await response.json();

    if (response.ok && result.success) {
      licenseStatus.textContent = "✔ License verified";
      licenseStatus.style.color = "green";
      licenseVerified = true;
    } else {
      licenseStatus.textContent = result.message || "Invalid license";
      licenseStatus.style.color = "red";
      licenseVerified = false;
    }

  } catch (err) {
    licenseStatus.textContent = "Server error";
    licenseStatus.style.color = "red";
    licenseVerified = false;
  }

});


// ===== SUBMIT =====
doctorForm?.addEventListener("submit", async (e) => {

  e.preventDefault();

  if (!licenseVerified) {
    alert("Please verify license before submitting");
    return;
  }

  const agree = document.getElementById("doctorAgreement");
  if (!agree?.checked) {
    alert("Please accept agreement");
    return;
  }

  const formData = new FormData(doctorForm);

  try {

    const response = await fetch("/doctors/register", {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    if (response.ok && result.success) {

      doctorForm.reset();
      licenseStatus.textContent = "";
      licenseVerified = false;

      // Close doctor modal
      doctorPopup.classList.remove("active");

      // Set message
      successMessage.innerText =
        "✅ Registration submitted successfully.\n\n" +
        "We have received your request and our team will review it shortly.\n" +
        "If you need any help or want to make changes, please contact support.\n\n" +
        "You will receive updates via email — please check your inbox.";

      // Open success popup with dim
      openSuccessPopup();

    } else {

      alert(result.message || "Registration failed");

    }

  } catch (err) {

    console.error(err);
    alert("Server error");

  }

});


// ===== CLOSE SUCCESS =====
closeSuccess?.addEventListener("click", closeSuccessPopup);
