<script lang="ts">
	import { selected_methods, show_selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label } from "@smui/list"
    import Checkbox from "@smui/checkbox"
    import Textfield from "@smui/textfield"
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
    import { afterUpdate, tick } from 'svelte';

    let data = {
        "turbidity": 4,
        "ec": 400,
        "ph": 7.5,
        "tds": 200,
        "nitrate": 0.0,
        "arsenic": 0.0,
        "iron": 0.0,
        "fluoride": 0.0,
        "tvc": 0,
        "coliforms": 0,
        "ecoli": 0
    }

    let limits = {
        "turbidity": ["NTU", 5],
        "ec": ["µS/cm", null],
        "ph": ["", 6.5, 8.5],
        "tds": ["mg/l", 600],
        "nitrate": ["mg/l", 50],
        "arsenic": ["mg/l", 0.01],
        "iron": ["mg/l", 0.3],
        "fluoride": ["mg/l", 1.5],
        "tvc": ["cfu/100ml", 0],
        "coliforms": ["1/100ml", 0],
        "ecoli": ["1/100ml", 0]
    }

    let methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false,
        "ro": false,
    }

    let results = ""

    function autoScroll() {
        const el = document.getElementById("results");
        if (!el) return;
        el.scrollIntoView({
            behavior: 'smooth'
        });
    }

    afterUpdate(() => {
        autoScroll()
    });

    function set_selected_methods() {
        selected_methods.set(methods)
        show_selected_methods.set(true)
    }

    function selectmethods() {
        methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false,
        "ro": false
        }
        let intro = "To reduce or adjust "
        let outro = " following concept has to be realised: "

        //problems
        let problems_list: String[] = []

        if (data.turbidity > limits.turbidity[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/turbidity" target="_blank" rel="noreferrer">Turbidity</a>`)
        }
        //if (data.ph < limits.ph[1] || data.ph > limits.ph[2]) {
        //    problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/ph" target="_blank" rel="noreferrer">pH</a>`)
        //}
        if (data.nitrate > limits.nitrate[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/nitrate" target="_blank" rel="noreferrer">Nitrate</a>`)
        }
        if (data.tds > limits.tds[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/salinity" target="_blank" rel="noreferrer">Salinity</a>`)
        }
        if (data.arsenic > limits.arsenic[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/arsenic" target="_blank" rel="noreferrer">Arsenic</a>`)
        }
        if (data.iron > limits.iron[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/iron" target="_blank" rel="noreferrer">Iron</a>`)
        }
        if (data.fluoride > limits.fluoride[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/fluoride" target="_blank" rel="noreferrer">Fluoride</a>`)
        }
        if (data.tvc > limits.tvc[1] || data.coliforms > limits.coliforms[1] || data.ecoli > limits.ecoli[1]) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/coliform-bacteria" target="_blank" rel="noreferrer">Pathogens</a>`)
        }
        let problems_string = problems_list.join(", ")

        //methods
        let methods_list: String[] = []

        if (data.turbidity > (10 * limits.turbidity[1])) {
                methods.flocculation = true
                methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/flocculation" target="_blank" rel="noreferrer">Flocculation</a>`)
            }
        if (data.tds > limits.tds[1]) {
            methods.ro = true
            methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/reverse-osmosis" target="_blank" rel="noreferrer">Reverse Osmosis</a>`)
        } else {
            if (data.turbidity > limits.turbidity[1] || data.nitrate > limits.nitrate[1] || data.arsenic > limits.arsenic[1]) {
                methods.bsf = true
                if (data.arsenic < limits.arsenic[1]) {
                    methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration" target="_blank" rel="noreferrer">Biosand Filtration</a>`)
                }
                else{
                    methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration#arsenic-removal" target="_blank" rel="noreferrer">modified Biosand Filtration</a>`)
                }
            }
            if (data.fluoride > limits.fluoride[1]) {
                methods.aaa = true
                methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/aaa" target="_blank" rel="noreferrer">Activated Alumina Adsorption</a>`)
            }
            if (data.tvc > limits.tvc[1] || data.coliforms > limits.coliforms[1] || data.ecoli > limits.ecoli[1]) {
                methods.sodis = true
                methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/sodis" target="_blank" rel="noreferrer">SODIS</a>`)
            }
        }
        let methods_string = methods_list.join(", ")

        set_selected_methods()
        if (methods.aaa || methods.bsf || methods.flocculation || methods.sodis || methods.ro) {
            results = intro + problems_string + outro + methods_string
        } else {
            results = "No treatment required."
        }

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
            <br />
            <Textfield type="number" bind:value={data.tds} label="Total dissolved Solids" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Anorganic Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <Textfield type="number" input$step="0.1" bind:value={data.nitrate} label="Nitrate" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.01" bind:value={data.arsenic} label="Arsenic" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <!--<Textfield type="number" input$step="0.1" bind:value={data.iron} label="Iron" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />-->
            <Textfield type="number" input$step="0.1" bind:value={data.fluoride} label="Fluoride" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
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
    <div style="display:flex; margin-bottom:1em" id="results">
        <Paper style="flex-grow:1;">
            <Title>Results</Title>
            <Content>
                {@html results}
                <br />
                To obtain the best possible treatment result, the sequence of treatment steps should correspond to the following table: 
                <br /><br />
                <DataTable table$aria-label="Results" style="width: 100%;">
                    <Head>
                        <Row>
                            <Cell numeric>Order</Cell>
                            <Cell style="white-space:normal;">Treatment Method</Cell>
                            <Cell style="white-space:normal;">Further Information</Cell>
                        </Row>
                    </Head>
                    <Body>
                        {#if methods.flocculation}
                            <Row>
                                <Cell numeric>1</Cell>
                                <Cell><a href="/methods/flocculation/predict">Flocculation</a></Cell>
                                <Cell><a href="https://wiki.sustainable-water.de/en/methods/flocculation" target="_blank" rel="noreferrer">Wiki</a></Cell>
                            </Row>
                        {/if}
                        {#if methods.ro}
                            <Row>
                                <Cell numeric>2</Cell>
                                <Cell style="white-space:normal;">Reverse Osmosis</Cell>
                                <Cell><a href="https://wiki.sustainable-water.de/en/methods/reverse-osmosis" target="_blank" rel="noreferrer">Wiki</a></Cell>
                            </Row>
                        {/if}
                        {#if methods.bsf}
                            <Row>
                                <Cell numeric>2</Cell>
                                <Cell>
                                    {#if data.arsenic}
                                        <a href="/methods/bsf/predict" style="white-space:normal;">modified Biosand Filtration</a>
                                    {:else}
                                        <a href="/methods/bsf/predict" style="white-space:normal;">Biosand Filtration</a>
                                    {/if}
                                </Cell>
                                <Cell>
                                    {#if data.arsenic}
                                        <a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration#arsenic-removal" target="_blank" rel="noreferrer">Wiki</a>
                                    {:else}
                                        <a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration" target="_blank" rel="noreferrer">Wiki</a>
                                    {/if}
                                </Cell>
                            </Row>
                        {/if}
                        {#if methods.aaa}
                            <Row>
                                <Cell numeric>3</Cell>
                                <Cell><a href="/methods/aaa/predict" style="white-space:normal;">Activated Alumina Adsorption</a></Cell>
                                <Cell><a href="https://wiki.sustainable-water.de/en/methods/aaa" target="_blank" rel="noreferrer">Wiki</a></Cell>
                            </Row>
                        {/if}
                        {#if methods.sodis}
                            <Row>
                                <Cell numeric>4</Cell>
                                <Cell><a href="/methods/sodis/predict">SODIS</a></Cell>
                                <Cell><a href="https://wiki.sustainable-water.de/en/methods/sodis" target="_blank" rel="noreferrer">Wiki</a></Cell>
                            </Row>
                        {/if}
                    </Body>
                </DataTable>
                <br /> <br />
                A new row below the top navigation bar is now visible.
                It contains all required treatment steps in the correct order.
                You can click on the individual methods to go to the respective prediction models.
            </Content>
        </Paper>
    </div>
{/if}