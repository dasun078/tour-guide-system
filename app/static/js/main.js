/* main.js */

// Wait for the DOM to load before executing scripts
document.addEventListener("DOMContentLoaded", function () {
    /**
     * Multi-select functionality for activities field
     */
    const activitiesSelect = document.getElementById("activities");
    if (activitiesSelect) {
        activitiesSelect.addEventListener("change", function () {
            const selectedActivities = Array.from(activitiesSelect.selectedOptions).map(option => option.text.trim());
            console.log("Selected activities:", selectedActivities);

            // Fetch AI recommendations based on selected activities
            fetchRecommendations({ activities: selectedActivities });
        });
    }

    /**
     * Validate the budget input to ensure it's a positive number
     */
    const budgetInput = document.getElementById("budget");
    if (budgetInput) {
        budgetInput.addEventListener("input", function () {
            const budgetValue = parseFloat(budgetInput.value);
            if (isNaN(budgetValue) || budgetValue < 0) {
                alert("Budget must be a positive number.");
                budgetInput.value = ""; // Clear invalid input
            }

            // Fetch AI recommendations based on updated budget
            fetchRecommendations({ budget: budgetValue });
        });
    }

    /**
     * Validate the destination input to ensure it's not empty
     */
    const destinationInput = document.getElementById("destination");
    if (destinationInput) {
        destinationInput.addEventListener("blur", function () {
            if (destinationInput.value.trim() === "") {
                alert("Destination cannot be empty.");
            }
        });
    }

    /**
     * Handle form submission validation for better UX
     */
    const tripForm = document.querySelector(".trip-form");
    if (tripForm) {
        tripForm.addEventListener("submit", function (e) {
            if (destinationInput && destinationInput.value.trim() === "") {
                e.preventDefault();
                alert("Please provide a valid destination.");
            }
            if (budgetInput && (isNaN(parseFloat(budgetInput.value)) || budgetInput.value < 0)) {
                e.preventDefault();
                alert("Please enter a valid positive budget.");
            }
        });
    }

    /**
     * Add hover effects for featured attractions
     */
    const attractionItems = document.querySelectorAll(".attraction-item");
    if (attractionItems.length) {
        attractionItems.forEach(item => {
            item.addEventListener("mouseover", function () {
                item.style.transform = "scale(1.05)";
                item.style.transition = "transform 0.3s ease";

                // Play sound effect on hover
                const soundSrc = item.getAttribute("data-sound");
                if (soundSrc) {
                    const audio = new Audio(soundSrc);
                    audio.play();
                }
            });

            item.addEventListener("mouseout", function () {
                item.style.transform = "scale(1)";
            });
        });
    }

    /**
     * Fetch AI-powered recommendations dynamically
     * @param {Object} filters - Filters to send to the server
     */
    async function fetchRecommendations(filters = {}) {
        try {
            const response = await fetch(`/recommend_destinations?budget=${filters.budget || ''}&activities=${filters.activities || ''}`);
            const recommendations = await response.json();

            // Update recommendations section dynamically
            const recommendationsList = document.getElementById("recommendations-list");
            if (recommendationsList) {
                recommendationsList.innerHTML = recommendations.map(dest => `<li>${dest}</li>`).join("");
            }
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        }
    }

    /**
     * Real-time ML-enhanced text suggestions for destinations
     */
    const destinationSuggestions = document.getElementById("destination-suggestions");
    if (destinationInput && destinationSuggestions) {
        destinationInput.addEventListener("input", async function () {
            try {
                const query = destinationInput.value.trim();
                if (query.length > 2) {
                    const response = await fetch(`/destination_suggestions?query=${query}`);
                    const suggestions = await response.json();

                    // Update suggestions dropdown
                    destinationSuggestions.innerHTML = suggestions
                        .map(suggestion => `<option value="${suggestion}">${suggestion}</option>`)
                        .join("");
                }
            } catch (error) {
                console.error("Error fetching destination suggestions:", error);
            }
        });
    }
});
