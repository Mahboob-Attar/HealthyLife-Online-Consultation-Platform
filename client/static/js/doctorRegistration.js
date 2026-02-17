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


// ===== MODAL FUNCTIONS =====
function openDoctorModal() {
  doctorPopup.classList.add("active");
  document.body.classList.add("popup-open");
}

function closeDoctorModal() {
  doctorPopup.classList.remove("active");
  document.body.classList.remove("popup-open");
}

function openSuccessPopup() {
  successPopup.classList.add("show");
  document.body.classList.add("popup-open");

  // Professional styling
  successPopup.style.background = "linear-gradient(135deg, #e8f5e9, #ffffff)";
  successPopup.style.border = "2px solid #4caf50";
  successPopup.style.boxShadow = "0 10px 25px rgba(0,0,0,0.15)";
}

function closeSuccessPopup() {
  successPopup.classList.remove("show");
  document.body.classList.remove("popup-open");
}


// ===== OPEN =====
doctorBtn?.addEventListener("click", openDoctorModal);

// ===== CLOSE =====
closeDoctor?.addEventListener("click", closeDoctorModal);


// ===== VERIFY LICENSE =====
verifyBtn?.addEventListener("click", async () => {

  const email = licenseInput.value.trim();

  if (!email) {
    licenseStatus.textContent = "Enter license Id";
    licenseStatus.style.color = "#d32f2f";
    return;
  }

  // Show spinner
  licenseStatus.innerHTML = '<span class="spinner"></span> Verifying...';
  licenseStatus.style.color = "#ff9800";

  const startTime = Date.now();

  try {

    const response = await fetch("/doctors/verify-license", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ license: email })
    });

    const result = await response.json();

    // Ensure minimum spinner time
    const elapsed = Date.now() - startTime;
    const delay = Math.max(0, 2500 - elapsed);
    await new Promise(res => setTimeout(res, delay));

    if (response.ok && result.success) {
      licenseStatus.textContent = "✔ License verified";
      licenseStatus.style.color = "#2e7d32";
      licenseVerified = true;
    } else {
      licenseStatus.textContent = result.message || "Invalid license";
      licenseStatus.style.color = "#d32f2f";
      licenseVerified = false;
    }

  } catch (err) {

    await new Promise(res => setTimeout(res, 2500));

    licenseStatus.textContent = "Server error";
    licenseStatus.style.color = "#d32f2f";
    licenseVerified = false;
  }

});


// ===== SUBMIT FORM =====
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

      // Reset form
      doctorForm.reset();
      licenseStatus.textContent = "";
      licenseVerified = false;

      closeDoctorModal();

      // Success message styling
      successMessage.innerText =
       successMessage.innerText =
        "✅ Registration Submitted Successfully\n\n" +

        "Thank you for registering with our healthcare platform.\n" +
        "Your application has been received and is currently under review by our verification team.\n\n" +

        "📄 What happens next?\n" +
        "• We will verify your medical license and submitted details\n" +
        "• The review process may take 24–48 hours\n" +
        "• Once approved, your doctor account will be activated\n\n" +

        "🆔 Platform Access\n" +
        "After approval, you will receive your unique Platform ID.\n" +
        "This ID will allow you to log in to the Availability,\n" +
        "and update your daily availability schedule.\n\n" +

        "📞 Verification Process\n" +
        "Our team may contact you to verify your documents\n" +
        "and confirm your professional details if required.\n\n" +

        "📧 Notifications\n" +
        "You will receive updates via email regarding your approval status.\n" +
        "Please keep an eye on your inbox (and spam folder just in case).\n\n" +

        "💬 Need help?\n" +
        "If you have any questions or need to update your information,\n" +
        "please contact our support team.\n\n" +

        "We appreciate your interest in joining our platform 🙏";


      successMessage.style.color = "#1b5e20";
      successMessage.style.fontWeight = "500";
      successMessage.style.lineHeight = "1.6";

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
