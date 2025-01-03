document.addEventListener('DOMContentLoaded', () => {
    const mapElement = document.getElementById('map');

    // Initialize map
    const map = new google.maps.Map(mapElement, {
        zoom: 7,
        center: { lat: 7.8731, lng: 80.7718 }, // Center of Sri Lanka
    });

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    // Fetch route data
    fetch('/get_route')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            // Calculate and display route
            const request = {
                origin: data.start,
                destination: data.end,
                travelMode: 'DRIVING',
            };
            directionsService.route(request, (result, status) => {
                if (status === 'OK') {
                    directionsRenderer.setDirections(result);
                } else {
                    console.error('Directions request failed:', status);
                }
            });
        })
        .catch(error => console.error('Error fetching route data:', error));
});
