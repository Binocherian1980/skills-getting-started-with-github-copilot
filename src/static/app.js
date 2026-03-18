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

  // --- Currency Converter ---
  const currencyForm = document.getElementById("currency-form");
  const conversionResult = document.getElementById("conversion-result");
  const fromCurrencySelect = document.getElementById("from-currency");
  const toCurrencySelect = document.getElementById("to-currency");

  async function loadSupportedCurrencies() {
    try {
      const response = await fetch("/currency/supported");
      const data = await response.json();
      data.currencies.forEach((code) => {
        [fromCurrencySelect, toCurrencySelect].forEach((sel) => {
          const option = document.createElement("option");
          option.value = code;
          option.textContent = code;
          sel.appendChild(option);
        });
      });
      // Sensible defaults
      fromCurrencySelect.value = "USD";
      toCurrencySelect.value = "EUR";
    } catch (error) {
      console.error("Error loading currencies:", error);
    }
  }

  currencyForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const fromCurrency = fromCurrencySelect.value;
    const toCurrency = toCurrencySelect.value;

    try {
      const response = await fetch(
        `/currency/convert?amount=${encodeURIComponent(amount)}&from_currency=${encodeURIComponent(fromCurrency)}&to_currency=${encodeURIComponent(toCurrency)}`
      );
      const result = await response.json();

      if (response.ok) {
        conversionResult.innerHTML = `
          <strong>${result.original_amount} ${result.from_currency}</strong>
          &nbsp;=&nbsp;
          <strong>${result.converted_amount} ${result.to_currency}</strong>
          <br/>
          <small>Exchange rate: 1 ${result.from_currency} = ${result.exchange_rate} ${result.to_currency}</small>
        `;
        conversionResult.className = "success";
      } else {
        conversionResult.textContent = result.detail || "Conversion failed";
        conversionResult.className = "error";
      }
      conversionResult.classList.remove("hidden");
    } catch (error) {
      conversionResult.textContent = "Failed to convert. Please try again.";
      conversionResult.className = "error";
      conversionResult.classList.remove("hidden");
      console.error("Error converting currency:", error);
    }
  });

  loadSupportedCurrencies();
});
