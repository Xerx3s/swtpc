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
    <h5>Online Water Analysis Tool</h5>
    <p>
        You are at the Online Water Analysis Tools.<br />
        Please fill in the form below and click the analysis button.<br />
        Afterwards a combination of treatment methods will be suggested to you.
    </p>
</div>

{#if advanced}
    <Advanced_input />
{:else}
    <Simple_input />
{/if}