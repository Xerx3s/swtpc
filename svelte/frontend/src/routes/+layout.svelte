<script lang="ts">
    import TopAppBar, { Row, Section, Title } from "@smui/top-app-bar"
    import IconButton from "@smui/icon-button"
    import Checkbox from "@smui/checkbox"
    //import "@picocss/pico"
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
    <TopAppBar variant="static" dense>
        <Row>
            <Section>
                <IconButton class="material-icons">menu</IconButton>
                <Title>SWTPC</Title>
            </Section>
            <Section align="end" toolbar>
                    {#if advanced}
                        Advanced View
                    {:else}
                        Simple View
                    {/if}
                    <Checkbox bind:checked={advanced} on:change={set_advanced_view}/>
            </Section>
        </Row>
    </TopAppBar>
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