<script>
	import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";
    import Simple_input from "./simple.svelte"
    import Advanced_input from "./advanced.svelte"

    let advanced = false

    advanced_view.subscribe(value => {
        advanced = value;
    })
</script>

<div>
    <h5>Solar Disinfection Prediction</h5>
    <p>
        Please indicate your location. To do so, please click on the map or enter the city and country below. <br />
        Please also select the time at which the disinfection will be started.
    </p>
</div>

{#if advanced}
    <Advanced_input />
{:else}
    <Simple_input />
{/if}