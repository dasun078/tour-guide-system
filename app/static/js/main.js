/* main.js */

// Wait for the DOM to load before executing scripts
document.addEventListener("DOMContentLoaded", function () {
    // Handle multi-select functionality for the activities field
    const activitiesSelect = document.getElementById("activities");
    if (activitiesSelect) {
        activitiesSelect.addEventListener("change", function () {
            const selectedOptions = Array.from(activitiesSelect.selectedOptions).map(option => option.text.trim());
            console.log("Selected activities:", selectedOptions);
        });
    }

    // Validate the budget input to ensure it is a positive number
    const budgetInput = document.getElementById("budget");
    if (budgetInput) {
        budgetInput.addEventListener("input", function () {
            const budgetValue = parseFloat(budgetInput.value);
            if (isNaN(budgetValue) || budgetValue < 0) {
                alert("Budget must be a positive number.");
                budgetInput.value = ""; // Clear invalid input
            }
        });
    }

    // Validate the destination input to ensure it is not empty
    const destinationInput = document.getElementById("destination");
    if (destinationInput) {
        destinationInput.addEventListener("blur", function () {
            if (destinationInput.value.trim() === "") {
                alert("Destination cannot be empty.");
            }
        });
    }

    // Handle form submission validation for better user experience
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

    // Add hover effects for featured attractions
    const attractionItems = document.querySelectorAll(".attraction-item");
    if (attractionItems.length) {
        attractionItems.forEach(item => {
            item.addEventListener("mouseover", function () {
                item.style.transform = "scale(1.05)";
                item.style.transition = "transform 0.3s ease";
            });
            item.addEventListener("mouseout", function () {
                item.style.transform = "scale(1)";
            });
        });
    }

    // Play sound effect when hovering over attraction items
    attractionItems.forEach(item => {
        item.addEventListener("mouseover", function () {
            const soundSrc = item.getAttribute("data-sound");
            if (soundSrc) {
                const audio = new Audio(soundSrc);
                audio.play();
            }
        });
    });
});
