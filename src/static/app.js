document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();

  // ── Conversion Calculator ────────────────────────────────────────────────────

  // Tab switching
  document.querySelectorAll(".calc-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".calc-tab").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".calc-panel").forEach((p) => p.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    });
  });

  // Generic convert helper
  async function doConvert(endpoint, value, fromUnit, toUnit, resultDiv) {
    if (value.trim() === "" || isNaN(Number(value))) {
      resultDiv.textContent = "Please enter a valid number.";
      resultDiv.className = "calc-result error";
      resultDiv.classList.remove("hidden");
      return;
    }
    try {
      const url = `/${endpoint}?value=${encodeURIComponent(value)}&from_unit=${encodeURIComponent(fromUnit)}&to_unit=${encodeURIComponent(toUnit)}`;
      const response = await fetch(url);
      const data = await response.json();
      if (response.ok) {
        resultDiv.textContent = `${data.input_value} ${data.from_unit} = ${data.result} ${data.to_unit}`;
        resultDiv.className = "calc-result success";
      } else {
        resultDiv.textContent = data.detail || "Conversion failed.";
        resultDiv.className = "calc-result error";
      }
    } catch {
      resultDiv.textContent = "Error connecting to server.";
      resultDiv.className = "calc-result error";
    }
    resultDiv.classList.remove("hidden");
  }

  // Temperature
  document.getElementById("temp-convert-btn").addEventListener("click", () => {
    doConvert(
      "convert/temperature",
      document.getElementById("temp-value").value,
      document.getElementById("temp-from").value,
      document.getElementById("temp-to").value,
      document.getElementById("temp-result")
    );
  });

  // Distance
  document.getElementById("dist-convert-btn").addEventListener("click", () => {
    doConvert(
      "convert/distance",
      document.getElementById("dist-value").value,
      document.getElementById("dist-from").value,
      document.getElementById("dist-to").value,
      document.getElementById("dist-result")
    );
  });

  // Weight
  document.getElementById("weight-convert-btn").addEventListener("click", () => {
    doConvert(
      "convert/weight",
      document.getElementById("weight-value").value,
      document.getElementById("weight-from").value,
      document.getElementById("weight-to").value,
      document.getElementById("weight-result")
    );
  });
});
