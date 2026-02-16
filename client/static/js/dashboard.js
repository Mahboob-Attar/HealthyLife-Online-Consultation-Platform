document.addEventListener("DOMContentLoaded", async () => {
  try {
    // 🔥 Single API Call (role-based backend)
    const res = await fetch("/dashboard/data", {
      credentials: "include"
    });

    const result = await res.json();

    if (!result.success) {
      console.error("Dashboard error:", result.message);
      return;
    }

    const data = result.data;
    const role = result.role;

    /*  TOTAL DOCTORS*/
    if (data.stats) {
      document.getElementById("totalDoctors").textContent =
        data.stats.total_doctors || 0;
    }

    /*  SPECIALIZATION CHART */
    if (data.stats && data.stats.specializations) {
      const specCanvas = document.getElementById("specializationChart");

      if (specCanvas) {
        new Chart(specCanvas.getContext("2d"), {
          type: "doughnut",
          data: {
            labels: data.stats.specializations.map((s) => s.specialization),
            datasets: [{
              data: data.stats.specializations.map((s) => s.count),
              backgroundColor: [
                "#1da1f2",
                "#00ffcc",
                "#ff6384",
                "#ff9f40",
                "#36a2eb",
                "#9966ff"
              ],
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: "bottom",
                labels: {
                  color: "#ffffff",
                  font: { size: 14 }
                }
              }
            }
          }
        });
      }
    }

    /* FEEDBACK RATINGS CHART */
    if (data.ratings && data.ratings.feedback_ratings) {
      const feedbackCanvas = document.getElementById("feedbackChart");

      if (feedbackCanvas) {
        const ratings = ["1", "2", "3", "4", "5"];
        const ratingCounts = ratings.map(
          r => data.ratings.feedback_ratings[r] || 0
        );

        const totalRatings = ratingCounts.reduce((a, b) => a + b, 0);

        const totalText = document.getElementById("totalRatingsText");
        if (totalText)
          totalText.textContent = `Total Ratings: ${totalRatings}`;

        new Chart(feedbackCanvas.getContext("2d"), {
          type: "bar",
          data: {
            labels: [
              "1 Star",
              "2 Stars",
              "3 Stars",
              "4 Stars",
              "5 Stars"
            ],
            datasets: [{
              data: ratingCounts,
              backgroundColor: [
                "rgba(255,77,79,0.9)",
                "rgba(255,136,56,0.9)",
                "rgba(255,219,50,0.9)",
                "rgba(110,207,57,0.9)",
                "rgba(54,207,201,0.95)"
              ],
              borderColor: "rgba(255,255,255,0.3)",
              borderWidth: 2,
              barPercentage: 0.45,
              categoryPercentage: 0.55
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: false }
            },
            scales: {
              y: {
                beginAtZero: true,
                ticks: { display: false },
                grid: { display: false }
              },
              x: {
                ticks: { color: "#b1c7ff" },
                grid: { display: false }
              }
            }
          }
        });
      }
    }

    /* ADMIN ONLY SECTION (optional)*/
    if (role === "admin" && data.users) {
      console.log("Admin Users:", data.users);
      // Later you can render users table here
    }

  } catch (err) {
    console.error("Dashboard JS Error:", err);
  }
});
