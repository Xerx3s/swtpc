<script lang="ts">
	import { selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label } from "@smui/list"
    import Checkbox from "@smui/checkbox"
    import Textfield from "@smui/textfield"

    let data = {
        "turbidity": 130,
        "ec": 400,
        "ph": 8.5,
        "nitrate": 0.0,
        "arsenic": 0.0,
        "iron": 0.0,
        "flouride": 0.0,
        "tvc": 0,
        "coliforms": 0,
        "ecoli": 0
    }

    let methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false
    }

    let results = ""

    function set_selected_methods() {
        selected_methods.set(methods)
    }

    function selectmethods() {
        results = "blubb"

        return null
    }
</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1">
        <Title>Indicator Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <Textfield type="number" bind:value={data.turbidity} label="Turbidity" suffix="NTU"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.ph} label="pH-Value" suffix=""  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" bind:value={data.ec} label="Electrical Conductivity" suffix="µS/cm"  style="flex-grow:1; margin-bottom:0.5em"/>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Anorganic Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <Textfield type="number" input$step="0.1" bind:value={data.nitrate} label="Nitrate" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.arsenic} label="Arsenic" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.iron} label="Iron" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.flouride} label="Flouride" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Organic Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <Textfield type="number" bind:value={data.tvc} label="Total Viable Count" suffix="cfu/ml"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" bind:value={data.coliforms} label="Coliform Bacteria" suffix="1/100ml"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" bind:value={data.ecoli} label="E.Coli" suffix="1/100ml"  style="flex-grow:1; margin-bottom:0.5em"/>
        </Content>
    </Paper>
</div>
<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={selectmethods}>Analyze</Button>
</Group>
{#if results != ""}
    <div style="display:flex; margin-bottom:1em">
        <Paper style="flex-grow:1;">
            <Title>Results</Title>
            <Content>
                {@html results}
            </Content>
        </Paper>
    </div>
{/if}