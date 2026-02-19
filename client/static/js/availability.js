document.addEventListener("DOMContentLoaded", function () {

    const openBtn = document.getElementById("doctoravailabilityBtn");
    const popup = document.getElementById("availabilityPopup");
    const closeBtn = document.getElementById("closeAvailability");

    const dateInput = document.getElementById("availabilityDate");
    const startTime = document.getElementById("startTime");
    const endTime = document.getElementById("endTime");

    function setMinTime() {

        const selectedDate = dateInput.value;
        const today = new Date().toISOString().split("T")[0];

        if (selectedDate === today) {

            const now = new Date();
            const hours = String(now.getHours()).padStart(2, "0");
            const minutes = String(now.getMinutes()).padStart(2, "0");

            const currentTime = `${hours}:${minutes}`;

            startTime.min = currentTime;

            // if user selected earlier time reset
            if (startTime.value < currentTime) {
                startTime.value = currentTime;
            }

        } else {
            startTime.min = "00:00";
        }
    }

    //  OPEN POPUP
    openBtn?.addEventListener("click", () => {

        popup.classList.add("active");

        const now = new Date();

        const today = now.toISOString().split("T")[0];
        dateInput.value = today;
        dateInput.min = today;

        const hours = String(now.getHours()).padStart(2, "0");
        const minutes = String(now.getMinutes()).padStart(2, "0");

        const currentTime = `${hours}:${minutes}`;

        startTime.value = currentTime;
        startTime.min = currentTime;

        const endHour = String(now.getHours() + 1).padStart(2, "0");
        endTime.value = `${endHour}:${minutes}`;

    });

    // CLOSE BUTTON
    closeBtn?.addEventListener("click", () => {
        popup.classList.remove("active");
    });

    // DATE CHANGE
    dateInput?.addEventListener("change", setMinTime);

});
