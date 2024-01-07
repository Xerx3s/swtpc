<script>
    import L from 'leaflet'
    import 'leaflet/dist/leaflet.css'
    import { coords_store } from "/opt/svelte/frontend/src/stores/stores";

    let marker;
    let coords;
    let map;
    let city_counter;

    var greenIcon = L.icon({
        iconUrl: 'http://leafletjs.com/examples/custom-icons/leaf-green.png',
        shadowUrl: 'http://leafletjs.com/examples/custom-icons/leaf-shadow.png',
        iconSize: [38, 95],
        shadowSize: [50, 64],
        iconAnchor: [22, 94],
        shadowAnchor: [4, 62],
        popupAnchor: [-3, -76],
    })

    coords_store.subscribe(value => {
        coords = value;
    })

    function initMap(node) {
        map = L.map(node).setView([49.87334845778753, 8.65687138520094], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        map.on('click', (event) => onClick(event))

        return map
    }

    function addmarker(lat, lng) {
        if (marker) { // check
            map.removeLayer(marker); // remove
        }
        
        marker = new L.marker([lat, lng], {icon: greenIcon}).addTo(map)
    }

    function onClick(event) {
        reverseGeocode(event.latlng.lat, event.latlng.lng).then( (rev) => {
            coords_store.set({
                "lat": event.latlng.lat,
                "lng": event.latlng.lng,
                "city": rev.city,
                "country": rev.country
            })
        })

        addmarker(event.latlng.lat, event.latlng.lng)
    }

    async function reverseGeocode(lat, lng) {
        const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`;
        const response = await fetch(url);
        const data = await response.json();

        return {
            city: data.address.city || data.address.town,
            country: data.address.country,
        };
    }

    export async function newlocation(city, country) {
        const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&city=${city}&country=${country}`;
        const response = await fetch(url);
        const loc = await response.json();

        if (city == coords.city && (city_counter < loc.length-1)) {
            city_counter += 1
        } else {
            city_counter = 0
        }
        
        coords_store.set({
            "lat": loc[city_counter].lat,
            "lng": loc[city_counter].lon,
            "city": city,
            "country": country
        })
        
        addmarker(loc[city_counter].lat, loc[city_counter].lon)
        var latlng = L.latLng(loc[city_counter].lat, loc[city_counter].lon);
        map.setView(latlng,13);

        return {
            "lat": loc[city_counter].lat,
            "lng": loc[city_counter].lon,
        }
    }
</script>

<div use:initMap></div>

<style>
    div {
        height: 300px;
        z-index: 0;
    }
</style>