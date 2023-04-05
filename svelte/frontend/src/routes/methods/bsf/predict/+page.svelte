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
    <h5>Biosand Filtration Prediction</h5>
    <p>
        Please enter the required parameters. <br />
        You will then be presented with the expected final values that are possible based on the treatment method and the entered input parameters.
    </p>
</div>

{#if advanced}
    <Advanced_input />
{:else}
    <Simple_input />
{/if}