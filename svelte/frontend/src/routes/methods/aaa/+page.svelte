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
        For more information on the treatment method, see the <a href="http://192.168.178.69:3000/en/methods/sodis" target="_blank" rel="noreferrer">knowledge base entry</a>.
    </p>
    <p>
        Select your location. To do so, please click on the map or enter the city and country below. <br />
        Please also select the time at which the disinfection will be started. <br />
        {#if advanced}
            Optionally, select the desired logarithmic disinfection.
            A value of 1 corresponds to a pathogen reduction of 90 %, 2 of 99 %, etc.
            The actual reduction required always depends on the raw water used, but a value of 4 should not be undercut if possible.
        {/if}
    </p>
</div>

{#if advanced}
    <Advanced_input />
{:else}
    <Simple_input />
{/if}