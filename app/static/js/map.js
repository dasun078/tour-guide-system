// Initialize Google Map
function initMap(trips = []) {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: { lat: 7.8731, lng: 80.7718 }, // Centered on Sri Lanka
    });

    // Add markers for trips
    trips.forEach(trip => {
        new google.maps.Marker({
            position: { lat: trip.lat, lng: trip.lng },
            map: map,
            title: trip.title,
        });
    });
}

// Modal Controls
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}
