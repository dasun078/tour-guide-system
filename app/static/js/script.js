// Initialize Google Map
function initMap() {
    const map = new google.maps.Map(document.getElementById("route-map"), {
        zoom: 7,
        center: { lat: 7.8731, lng: 80.7718 }, // Centered on Sri Lanka
    });

    // Example destination markers
    const destinations = [
        { lat: 6.9271, lng: 79.8612, title: "Colombo" },
        { lat: 7.2906, lng: 80.6337, title: "Kandy" },
    ];

    destinations.forEach(dest => {
        new google.maps.Marker({
            position: { lat: dest.lat, lng: dest.lng },
            map: map,
            title: dest.title,
        });
    });
}

// Fetch real-time weather data
async function fetchWeather() {
    try {
        const response = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?q=Colombo,lk&units=metric&appid=AIzaSyBVvQRYauv9Afgcla7nlWxjNbm-NJA2ddY`
        );
        const weatherData = await response.json();

        const weatherDiv = document.getElementById("weather");
        weatherDiv.innerHTML = `
            <p><strong>City:</strong> ${weatherData.name}</p>
            <p><strong>Temperature:</strong> ${weatherData.main.temp}°C</p>
            <p><strong>Condition:</strong> ${weatherData.weather[0].description}</p>
        `;
    } catch (error) {
        console.error("Error fetching weather data:", error);
        const weatherDiv = document.getElementById("weather");
        weatherDiv.innerHTML = "<p>Unable to fetch weather data. Please try again later.</p>";
    }
}

// Modal controls
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// Fetch AI-recommended destinations
async function fetchRecommendations() {
    const userBudget = document.getElementById("budget").value;
    const activities = Array.from(document.getElementById("activities").selectedOptions).map(opt => opt.value);

    try {
        const response = await fetch(`/recommend_destinations?budget=${userBudget}&activities=${activities.join(',')}`);
        const recommendations = await response.json();

        const recommendationsList = document.getElementById("recommendations-list");
        recommendationsList.innerHTML = recommendations.map(dest => `<li>${dest}</li>`).join('');
    } catch (error) {
        console.error("Error fetching recommendations:", error);
    }
}

// Event listeners
document.addEventListener("DOMContentLoaded", () => {
    // Initialize map and fetch weather data
    if (document.getElementById("route-map")) initMap();
    if (document.getElementById("weather")) fetchWeather();

    // Attach event listeners for dynamic recommendations
    const budgetInput = document.getElementById("budget");
    const activitiesSelect = document.getElementById("activities");

    if (budgetInput && activitiesSelect) {
        budgetInput.addEventListener("change", fetchRecommendations);
        activitiesSelect.addEventListener("change", fetchRecommendations);
    }
});
