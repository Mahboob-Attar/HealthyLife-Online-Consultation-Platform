document.addEventListener("DOMContentLoaded", function () {

    const openBtn = document.getElementById("doctoravailabilityBtn");
    const popup = document.getElementById("availabilityPopup");
    const closeBtn = document.getElementById("closeAvailability");

    const dateInput = document.getElementById("availabilityDate");
    const startTime = document.getElementById("startTime");
    const endTime = document.getElementById("endTime");

    const form = document.getElementById("availabilityForm");
    const submitBtn = form?.querySelector("button[type='submit']");
    const shiftInfo = document.getElementById("shiftInfo");

    function setMinTime() {

        const selectedDate = dateInput.value;
        const today = new Date().toISOString().split("T")[0];

        if (selectedDate === today) {

            const now = new Date();
            const hours = String(now.getHours()).padStart(2, "0");
            const minutes = String(now.getMinutes()).padStart(2, "0");

            const currentTime = `${hours}:${minutes}`;

            startTime.min = currentTime;

            if (startTime.value < currentTime) {
                startTime.value = currentTime;
            }

        } else {
            startTime.min = "00:00";
        }
    }

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

        updateShiftInfo();
    });

    closeBtn?.addEventListener("click", () => {
        popup.classList.remove("active");
    });

    dateInput?.addEventListener("change", setMinTime);

    function isSameTime() {
        return startTime.value === endTime.value;
    }

    function isOvernight() {
        return endTime.value < startTime.value;
    }

    // ⭐ SHIFT DURATION PREVIEW
    function updateShiftInfo() {

        if (!startTime.value || !endTime.value) {
            shiftInfo.innerText = "";
            return;
        }

        let start = new Date(`1970-01-01T${startTime.value}:00`);
        let end = new Date(`1970-01-01T${endTime.value}:00`);

        if (end <= start) {
            end.setDate(end.getDate() + 1);
        }

        let diffMs = end - start;
        let hours = Math.floor(diffMs / (1000 * 60 * 60));
        let minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

        shiftInfo.innerText = `Shift duration: ${hours}h ${minutes}m`;
    }

    startTime.addEventListener("change", updateShiftInfo);
    endTime.addEventListener("change", updateShiftInfo);

    // SINGLE SUBMIT HANDLER
    form?.addEventListener("submit", async function (e) {

        e.preventDefault();

        if (isSameTime()) {
            alert("Start and end time cannot be same");
            return;
        }

        if (isOvernight()) {
            if (!confirm("Overnight shift detected. End time will be considered next day. Continue?")) {
                return;
            }
        }

        const formData = new FormData(form);

        try {

            submitBtn.disabled = true;
            submitBtn.innerText = "Saving...";

            const response = await fetch("/availability/save", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            alert(data.message);

            if (data.success) {
                form.reset();
                shiftInfo.innerText = "";
                popup.classList.remove("active");
            }

        } catch (error) {

            console.error("Error:", error);
            alert("Something went wrong. Please try again.");

        } finally {

            submitBtn.disabled = false;
            submitBtn.innerText = "Save";

        }

    });

});
sus