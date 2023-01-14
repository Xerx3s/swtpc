<script lang="ts">
    import "@picocss/pico"
	import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";

    let advanced = false

    set_advanced_view()

    advanced_view.subscribe(value => {
		advanced = value;
    })

    function set_advanced_view() {
        advanced_view.set(advanced)
    }
</script>

<header>
    <nav class="container-fluid">
        <ul>
            <li><a href="/"><strong>SWTPC</strong></a></li>
        </ul>
        <ul>
            <li>
                <label for="switch">
                    {#if advanced}
                        Advanced Mode
                    {:else}
                        Simple Mode
                    {/if}
                    <input type="checkbox" id="switch" name="switch" role="switch" bind:checked={advanced} on:change={set_advanced_view}>
                </label>
            </li>
        </ul>
    </nav>
</header>

<main class="container">
    <slot />
</main>

<footer class="container-fluid">
    <div class="grid">
        <a href="/" role="button" class="outline">Motivation</a>
        <a href="/" role="button" class="outline">Treatment Methods</a>
        <a href="/" role="button" class="outline">Knowledge Base</a>
    </div>
</footer>