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
    <h5>Flocculation Prediction</h5>
    <p>
        For more information on the treatment method, see the <a href="http://192.168.178.69:3000/en/methods/flocculation" target="_blank" rel="noreferrer">knowledge base entry</a>.
    </p>
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