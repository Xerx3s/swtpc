a<script lang="ts">
	import { show_selected_methods, selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Slider from "@smui/slider"
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label } from "@smui/list"
    import Checkbox from "@smui/checkbox"
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
    import { afterUpdate, tick } from 'svelte';

    let data = {
        "turbidity": 0,
        "organic_material": false,
        "heavy_metals": false,
        "salts": false,
        "nitrate": false,
        "coliforms": false,
        "arsenic": false,
        "fluoride": false
    }

    let methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false,
        "ro": false
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

        let intro = "To reduce "
        let outro = " following concept has to be realised: "

        //problems
        let problems_list: String[] = []

        if (data.turbidity > 0) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/turbidity" target="_blank" rel="noreferrer">Turbidity</a>`)
        }
        if (data.organic_material) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/organic-material" target="_blank" rel="noreferrer">Organic Material</a>`)
        }
        if (data.heavy_metals) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/heavy-metals" target="_blank" rel="noreferrer">Heavy Metals</a>`)
        }
        if (data.salts) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/salinity" target="_blank" rel="noreferrer">Salinity</a>`)
        }
        if (data.nitrate) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/nitrate" target="_blank" rel="noreferrer">Nitrate</a>`)
        }
        if (data.coliforms) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/coliform-bacteria" target="_blank" rel="noreferrer">Pathogens</a>`)
        }
        if (data.arsenic) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/arsenic" target="_blank" rel="noreferrer">Arsenic</a>`)
        }
        if (data.fluoride) {
            problems_list.push(`<a href="https://wiki.sustainable-water.de/en/contaminants/fluoride" target="_blank" rel="noreferrer">Fluoride</a>`)
        }
        let problems_string = problems_list.join(", ")

        //methods
        let methods_list: String[] = []

        if (data.salts) {
            if (data.turbidity > 0) {
                methods.flocculation = true
                methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/flocculation" target="_blank" rel="noreferrer">Flocculation</a>`)
            }
            methods.ro = true
            methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/reverse-osmosis" target="_blank" rel="noreferrer">Reverse Osmosis</a>`)

        } else {
            if (data.turbidity > 1 || data.heavy_metals) {
                methods.flocculation = true
                methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/flocculation" target="_blank" rel="noreferrer">Flocculation</a>`)
            }
            if (data.turbidity == (1 || 2) || data.organic_material || data.nitrate || data.arsenic) {
                methods.bsf = true
                if (data.arsenic) {
                    methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration#arsenic-removal" target="_blank" rel="noreferrer">modified Biosand Filtration</a>`)
                }
                else {
                    methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration" target="_blank" rel="noreferrer">Biosand Filtration</a>`)
                }
            }
            if (data.fluoride) {
                methods.aaa = true
                methods_list.push(`<a href="https://wiki.sustainable-water.de/en/methods/aaa" target="_blank" rel="noreferrer">Activated Alumina Adsorption</a>`)
            }
            if (data.coliforms) {
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
        <Title>Turbidity</Title>
        <Content>
            <Slider bind:value={data.turbidity} min={0} max={3} step={1} style="min-width:10em"/>
            <center>
            {#if data.turbidity === 0}
                none
            {:else if data.turbidity === 1}
                low
            {:else if data.turbidity === 2}
                medium
            {:else if data.turbidity === 3}
                high
            {/if}
            </center>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Taste or Smell</Title>
        <Content>
            <List checkList>
                <Item>
                    <Label style="white-space:normal;">Earthy or Musty</Label>
                    <Meta>
                        <Checkbox bind:checked={data.organic_material} />
                    </Meta>
                </Item>
                <!--<Item>
                    <Label>Metallic</Label>
                    <Meta>
                        <Checkbox bind:checked={data.heavy_metals} />
                    </Meta>
                </Item>-->
                <Item>
                    <Label style="white-space:normal;">Salty</Label>
                    <Meta>
                        <Checkbox bind:checked={data.salts} />
                    </Meta>
                </Item>
            </List>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Anomalies</Title>
        <Content>
            <List checkList>
                <Item>
                    <Label style="white-space:normal;">Blue Baby Syndrom</Label>
                    <Meta>
                        <Checkbox bind:checked={data.nitrate} />
                    </Meta>
                </Item>
                <Item>
                    <Label style="white-space:normal;">Cases of Diarrhea or Stomach Pain</Label>
                    <Meta>
                        <Checkbox bind:checked={data.coliforms} />
                    </Meta>
                </Item>
                <Item>
                    <Label style="white-space:normal;">Excessive Hornification of Skin</Label>
                    <Meta>
                        <Checkbox bind:checked={data.arsenic} />
                    </Meta>
                </Item>
                <Item>
                    <Label style="white-space:normal;">Discoloration of Teeth and/or frequent bone fractures</Label>
                    <Meta>
                        <Checkbox bind:checked={data.fluoride} />
                    </Meta>
                </Item>
            </List>
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