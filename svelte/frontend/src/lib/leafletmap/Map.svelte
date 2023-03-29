<script>
    import L from 'leaflet'
    import 'leaflet/dist/leaflet.css'
    import { coords_store } from "/opt/svelte/frontend/src/stores/stores";

    let marker;

    function initMap(node) {
        const map = L.map(node).setView([51.505, -0.09], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        map.on('click', (event) => onClick(event, map))
    }

    function onClick(event, map) {
        reverseGeocode(event.latlng.lat, event.latlng.lng).then( (rev) => {
            coords_store.set({
                "lat": event.latlng.lat,
                "lng": event.latlng.lng,
                "city": rev.city,
                "country": rev.country
            })
        })
        
        if (marker) { // check
            map.removeLayer(marker); // remove
        }
        
        marker = new L.marker([event.latlng.lat, event.latlng.lng]).addTo(map)
            //.bindPopup('success')
            .openPopup();
    }

    async function reverseGeocode(lat, lon) {
        const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;
        const response = await fetch(url);
        const data = await response.json();

        return {
            city: data.address.city || data.address.town,
            country: data.address.country,
        };
}


</script>

<div use:initMap></div>

<style>
    div {
        height: 300px;
    }
</style>