import {writable} from "svelte/store"

export const advanced_view = writable(false);
export const show_selected_methods = writable(false);

export const selected_methods = writable({
    "flocculation": false,
    "bsf": false,
    "sodis": false,
    "aaa": false
});

export const coords_store = writable({
    "lat": 49.87334845778753,
    "lng": 8.65687138520094,
    "city": "Darmstadt",
    "country": "Deutschland"
})