// ===================== INFO POPUPS =====================

// About Popup
const aboutLink = document.querySelector('a[href="#about"]');
if (aboutLink) {
  aboutLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("aboutPopup")?.classList.add("active");
  });
}

// FAQ Popup
const faqLink = document.querySelector('a[href="#faq"]');
if (faqLink) {
  faqLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("faqPopup")?.classList.add("active");
  });
}

// Support Popup
const supportLink = document.querySelector('a[href="#contact"]');
if (supportLink) {
  supportLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("supportPopup")?.classList.add("active");
  });
}

// Close Info Popups
document.querySelectorAll(".close-info").forEach((btn) => {
  btn.addEventListener("click", () => {
    const popupId = btn.getAttribute("data-close");
    document.getElementById(popupId)?.classList.remove("active");
  });
});

// ===================== AUTH POPUP HANDLING =====================

document.addEventListener("DOMContentLoaded", () => {
  const menuIcon = document.querySelector(".menu-icon");
  const authPopup = document.getElementById("authMasterPopup");

  if (menuIcon && authPopup) {
    menuIcon.addEventListener("click", () => {
      authPopup.style.display = "flex";

      // show role box safely (auth.js handles this)
      if (typeof showRoleBox === "function") {
        showRoleBox();
      }
    });

    authPopup.addEventListener("click", (e) => {
      if (e.target === authPopup) {
        authPopup.style.display = "none";
      }
    });
  }
});

