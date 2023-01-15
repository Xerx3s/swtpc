import {writable} from "svelte/store"

export const advanced_view = writable(false);

export const selected_methods = writable({
    "flocculation": false,
    "bsf": false,
    "sodis": false
});