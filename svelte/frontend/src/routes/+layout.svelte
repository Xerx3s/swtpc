<script lang="ts">
    import TopAppBar, { Row, Section, Title } from "@smui/top-app-bar"
    import IconButton from "@smui/icon-button"
    import Checkbox from "@smui/checkbox"
    import Drawer, { AppContent, Scrim, Header, Subtitle, Content } from "@smui/drawer"
    import List, { Item, Text } from '@smui/list';
	  import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Label } from "@smui/button"
    import Switch from "@smui/switch"

    let advanced = false;

    let open = false;
    let active = 'Gray Kittens';

    function setActive(value: string) {
        active = value;
        open = false;
    }

    advanced_view.subscribe(value => {
		advanced = value;
    })

    function set_advanced_view() {
        advanced_view.set(advanced)
    }

    set_advanced_view();
</script>

<header style="margin-bottom:1em">
  <TopAppBar variant="static" dense>
      <Row>
          <Section>
              <IconButton class="material-icons" on:click={() => (open = !open)} >menu</IconButton>
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

<div class="drawer-container">
  <Drawer variant="modal" fixed={false} bind:open>
    <Header>
      <Title>Super Drawer</Title>
      <Subtitle>It's the best drawer.</Subtitle>
    </Header>
    <Content>
      <List>
        <Item
          href="javascript:void(0)"
          on:click={() => setActive('Gray Kittens')}
          activated={active === 'Gray Kittens'}
        >
          <Text>Gray Kittens</Text>
        </Item>
        <Item
          href="javascript:void(0)"
          on:click={() => setActive('A Space Rocket')}
          activated={active === 'A Space Rocket'}
        >
          <Text>A Space Rocket</Text>
        </Item>
        <Item
          href="javascript:void(0)"
          on:click={() => setActive('100 Pounds of Gravel')}
          activated={active === '100 Pounds of Gravel'}
        >
          <Text>100 Pounds of Gravel</Text>
        </Item>
        <Item
          href="javascript:void(0)"
          on:click={() => setActive('All of the Shrimp')}
          activated={active === 'All of the Shrimp'}
        >
          <Text>All of the Shrimp</Text>
        </Item>
        <Item
          href="javascript:void(0)"
          on:click={() => setActive('A Planet with a Mall')}
          activated={active === 'A Planet with a Mall'}
        >
          <Text>A Planet with a Mall</Text>
        </Item>
      </List>
    </Content>
  </Drawer>
  <main class="main-content">
      <Scrim fixed={false} />
      <AppContent class="app-content">
          <slot />
      </AppContent>
  </main>
</div>

<footer>
    <div class="grid">
        <a href="/" role="button" class="outline">Motivation</a>
        <a href="/" role="button" class="outline">Treatment Methods</a>
        <a href="/" role="button" class="outline">Knowledge Base</a>
    </div>
</footer>

