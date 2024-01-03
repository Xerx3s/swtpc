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
    <h5>Activated Alumina Adsorption Dosage Recommendation</h5>
    <p>
        For more information on the treatment method, see the <a href="https://wiki.sustainable-water.de/en/methods/aaa" target="_blank" rel="noreferrer">knowledge base entry</a>.
    </p>
    <p>
        Please input the fluoride concentration present in your water and select your desired contact time.<br />
    </p>
</div>

{#if advanced}
    <Advanced_input />
{:else}
    <Simple_input />
{/if}