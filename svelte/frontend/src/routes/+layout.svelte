<script lang="ts">
    import TopAppBar, { Row, Section, Title } from "@smui/top-app-bar"
    import IconButton from "@smui/icon-button"
    import Menu from "@smui/menu"
    import List, {Item, Separator, Text } from "@smui/list"
	  import { advanced_view, show_selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Label } from "@smui/button"
    import Switch from "@smui/switch"
    import MethodsRow from '$lib/methodsrow/MethodsRow.svelte';

    let advanced = false;
    let show_methods = false;
    let menu: Menu;

    advanced_view.subscribe(value => {
		advanced = value;
    })

    show_selected_methods.subscribe(value => {
      show_methods = value;
    })

    function set_advanced_view() {
        advanced_view.set(advanced)
    }

    set_advanced_view();
</script>

<header style="margin-bottom:1em">
  <Menu bind:this={menu}>
    <List>
      <Item>
        <Button href="/">
          <Label>Home</Label>
        </Button>
      </Item>
      <Item>
        <Button href="/analysis">
          <Label>Analysis</Label>
        </Button>
      </Item>
      <Item>
        <Button href="/methods">
          <Label>Methods</Label>
        </Button>
      </Item>
    </List>
  </Menu>

  <TopAppBar variant="static">
      <Row>
          <Section>
              <IconButton class="material-icons" on:click={() => menu.setOpen(true)} >menu</IconButton>
              <Title>
                  <Button color="secondary" href="/" >
                      <Label>SWTPC</Label>
                  </Button>
              </Title>
          </Section>
          <Section align="end" toolbar>
                  {#if advanced}
                      Advanced View
                  {:else}
                      Simple View
                  {/if}
                  <Switch color="secondary" bind:checked={advanced} on:SMUISwitch:change={set_advanced_view} icons={false} />
          </Section>
      </Row>
  </TopAppBar>

  {#if show_methods}
    <MethodsRow />
  {/if}

</header>

<main class="main-content">
  <slot />
</main>

<footer style="display:flex; justify-content:stretch">
  <Button variant="unelevated" style="flex-grow:1; margin: 1em;" href="/">
    <Label>Motivation</Label>
  </Button>
  <Button variant="unelevated" style="flex-grow:1; margin: 1em;" href="/analysis">
    <Label>Analysis</Label>
  </Button>
  <Button variant="unelevated" style="flex-grow:1; margin: 1em;" href="http://192.168.178.69:3000/" target="_blank" rel="noreferrer">
    <Label>Knowledge Base</Label>
  </Button>
</footer>

