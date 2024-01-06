<script>
    import Button, { Group, Label } from "@smui/button"
    import { show_selected_methods, selected_methods } from "/opt/svelte/frontend/src/stores/stores";

    let methods;

    selected_methods.subscribe(value => {
      methods = value;
    })
</script>

<p>
  <b>Required treatment methods:</b>
  <Group variant="unelevated" style="display: flex; justify-content: stretch;">
    {#if methods.flocculation}
      <Button variant="outlined" color="secondary" style="flex-grow:1" href="/methods/flocculation/predict">
        <Label>Flocculation</Label>
      </Button>
    {/if}
    {#if methods.bsf}
      <Button variant="outlined" color="secondary" style="flex-grow:1" href="/methods/bsf/predict">
        <Label>BSF</Label>
      </Button>
    {/if}
    {#if methods.aaa}
      <Button variant="outlined" color="secondary" style="flex-grow:1" href="/methods/aaa/predict">
        <Label>AAA</Label>
      </Button>
    {/if}
    {#if methods.sodis}
      <Button variant="outlined" color="secondary" style="flex-grow:1" href="/methods/sodis/predict">
        <Label>SODIS</Label>
      </Button>
    {/if}
    {#if methods.ro}
      <Button variant="outlined" color="secondary" style="flex-grow:1" href="https://wiki.sustainable-water.de/en/methods/reverse-osmosis" target="_blank" rel="noreferrer">
        <Label>RO</Label>
      </Button>
    {/if}
    <Button variant="outlined" color="secondary" style="flex-grow:1; color:red" on:click={() => show_selected_methods.set(false)}>
      <Label>Reset</Label>
    </Button>
  </Group>
</p>