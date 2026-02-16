/* GLOBAL HELPERS */
function showBox(boxId) {
  document
    .querySelectorAll(".auth-box")
    .forEach((b) => (b.style.display = "none"));
  document.getElementById(boxId).style.display = "flex";
}

function closeAuthPopup() {
  document.getElementById("authMasterPopup").style.display = "none";
}

function showRoleBox() {
  showBox("roleBox");
}
function selectRole(role) {
  if (role === "user") openSignup();
  else openAdminLogin();
}

/* NAVIGATION */
function openLogin() {
  showBox("userLoginBox");
}
function openForgotPassword() {
  showBox("forgotBox");
}
function openAdminLogin() {
  showBox("adminLoginBox");
}
function openSignup() {
  showBox("userSignupBox");
}

/* EMAIL VALIDATION*/
function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

/* OTP FIELD SETUP*/
function setupOtpField(emailId, buttonId) {
  const emailInput = document.getElementById(emailId);
  const sendBtn = document.getElementById(buttonId);
  if (!emailInput || !sendBtn) return;

  sendBtn.disabled = true;

  emailInput.addEventListener("input", () => {
    sendBtn.disabled = !validateEmail(emailInput.value.trim());
  });
}

/* API HELPER (UPDATED) */
async function api(url, method = "POST", data = {}) {
  try {
    const res = await fetch(url, {
      method,
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: method === "GET" ? null : JSON.stringify(data),
    });
    return await res.json();
  } catch {
    return { status: "error", msg: "Network error" };
  }
}

/* OTP STATE */
let otpVerified = false;

function showVerified(inputId) {
  otpVerified = true;
  const input = document.getElementById(inputId);
  if (!input) return;

  input.style.border = "2px solid #28a745";
  input.style.color = "#28a745";
  input.style.fontWeight = "bold";
}

/*SEND OTP */
async function sendOTP() {
  const signupVisible =
    document.getElementById("userSignupBox").style.display === "flex";

  const forgotVisible =
    document.getElementById("forgotBox").style.display === "flex";

  let email = "";
  let purpose = "signup";

  if (signupVisible) {
    email = u_email.value.trim();
    purpose = "signup";
  }

  if (forgotVisible) {
    email = fp_email.value.trim();
    purpose = "reset";
  }

  if (!validateEmail(email)) return alert("Enter valid email!");

  const res = await api("/auth/send-otp", "POST", {
    email,
    purpose,
  });

  alert(res.msg);
}

/* USER SIGNUP*/
async function userSignup() {
  const name = u_name.value.trim();
  const email = u_email.value.trim();
  const otp = u_otp.value.trim();
  const pass = u_pass.value;

  if (!name || !email || !otp || !pass) return alert("All fields required!");

  if (!otpVerified) {
    const v = await api("/auth/verify-otp", "POST", {
      email,
      otp,
      purpose: "signup",
    });

    if (v.status !== "success") return alert(v.msg);
    showVerified("u_otp");
  }

  const res = await api("/auth/signup", "POST", {
    name,
    email,
    password: pass,
  });

  alert(res.msg);
  if (res.status === "success") openLogin();
}

/* USER LOGIN */
async function userLogin() {
  const email = ul_email.value.trim();
  const pass = ul_pass.value;

  if (!email || !pass)
    return alert("Email & password required");

  const res = await api("/auth/login", "POST", {
    email,
    password: pass,
  });

  if (res.status !== "success") return alert(res.msg);

  localStorage.setItem("user_name", res.name);

  //  Redirect to common dashboard
  window.location.href = "/";
}


/* ADMIN LOGIN*/
async function adminLogin() {
  const res = await api("/admin/login", "POST", {
    email: a_email.value.trim(),
    password: a_pass.value,
  });

  if (res.status !== "success") return alert(res.msg);

  window.location.href = "/dashboard/";
}

/*  RESET PASSWORD */
async function resetPassword() {
  const email = fp_email.value.trim();
  const otp = fp_otp.value.trim();
  const pass = fp_pass.value;

  if (!email || !otp || !pass) return alert("All fields required!");

  const res = await api("/auth/reset", "POST", {
    email,
    otp,
    password: pass,
  });

  alert(res.msg);

  if (res.status === "success") {
    otpVerified = false;
    openLogin();
  }
}

/*  NAVBAR SESSION CHECK (FIXED)*/
async function initUserNavbar() {
  const menuIcon = document.getElementById("menuIcon");
  const userContainer = document.getElementById("navUserContainer");
  const avatar = document.getElementById("navUserAvatar");
  const dropdown = document.getElementById("userDropdown");

  if (!avatar) return;

  const res = await api("/auth/me", "GET");

  if (res.logged_in) {
    if (menuIcon) menuIcon.style.display = "flex";
    if (userContainer) userContainer.style.display = "flex";

    if (res.role === "admin") {
      avatar.innerText = "A";
    } else {
      const name = localStorage.getItem("user_name") || "U";
      avatar.innerText = name.charAt(0).toUpperCase();
    }
  } else {
    if (menuIcon) menuIcon.style.display = "flex";
    if (userContainer) userContainer.style.display = "none";
  }

  avatar.onclick = () => {
    dropdown.style.display =
      dropdown.style.display === "flex" ? "none" : "flex";
  };

  document.addEventListener("click", (e) => {
    if (userContainer && !userContainer.contains(e.target))
      dropdown.style.display = "none";
  });
}

/* LOGOUT (FIXED)*/
async function logoutUser() {
  await api("/auth/logout", "POST");
  localStorage.removeItem("user_name");
  window.location.href = "/";
}

/* INIT*/
document.addEventListener("DOMContentLoaded", () => {
  setupOtpField("u_email", "u_send_btn");
  setupOtpField("fp_email", "fp_send_btn");
  initUserNavbar();
});

async function goToDashboard() {
  const res = await api("/auth/me", "GET");
  window.location.href = "/dashboard/";
}


async function goToAppointment() {
  const res = await api("/auth/me", "GET");
  
  if (res.role === "admin") {
    alert("Admin cannot book appointments.");
    return;
  }
  // doctor or patient allowed
  window.location.href = "/appointments";
}
