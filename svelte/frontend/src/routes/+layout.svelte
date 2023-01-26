<script lang="ts">
    import TopAppBar, { Row, Section, Title } from "@smui/top-app-bar"
    import IconButton from "@smui/icon-button"
    import Menu from "@smui/menu"
    import List, {Item, Separator, Text } from "@smui/list"
	  import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Label } from "@smui/button"
    import Switch from "@smui/switch"

    let advanced = false;
    let menu: Menu;
    let clicked = "nothing yet."

    advanced_view.subscribe(value => {
		advanced = value;
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
        <Button href="/analysis">
          <Label>Analysis</Label>
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
                  <Switch bind:checked={advanced} on:SMUISwitch:change={set_advanced_view}/>
          </Section>
      </Row>
  </TopAppBar>
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
  <Button variant="unelevated" style="flex-grow:1; margin: 1em;" href="http://192.168.178.69:3000/">
    <Label>Knowledge Base</Label>
  </Button>
</footer>

