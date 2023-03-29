import {writable} from "svelte/store"

export const advanced_view = writable(false);

export const selected_methods = writable({
    "flocculation": false,
    "bsf": false,
    "sodis": false,
    "aaa": false
});

export const coords_store = writable({
    "lat": 0.0,
    "lng": 0.0,
    "city": "Darmstadt",
    "country": "Deutschland"
})