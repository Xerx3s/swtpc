<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group, Label } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';
    import Dialog, { Actions } from '@smui/dialog';
    import { onMount, afterUpdate, tick } from 'svelte';
    import { Line } from 'svelte-chartjs';
    import 'chart.js/auto';
    //import Map from '$lib/leafletmap/Map.svelte';
    import Slider from "@smui/slider";
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
    //import { coords_store } from "/opt/svelte/frontend/src/stores/stores";
    import Tooltip, { Wrapper } from '@smui/tooltip';

    let data = {
        "contact_time": 60.0,
        "concentration": 10.0,
        "concentration_chloride": 0.0,
        "concentration_sulfate": 0.0,
        "concentration_bicarbonate": 0.0,
        "concentration_hydrogen_phosphate": 0.0,
        "concentration_arsenic": 0.0,
    }

    let process_param = {
        "daily_water": 20.0,
        "volume": 10.0,
        "f_mass_v": 0.0,
        "aaa_mass_v": 0.0,
        "aaa_mass_d": 0.0,
    }

    let f_limit = 1.5
    let coverage = 0.0
    let show_results = false

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

    async function aaa_dosing() {
        let url = "https://api.sustainable-water.de/aaa/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()
        try {
            coverage = res2["coverage"].toFixed(2)
            process_param.f_mass_v = (data.concentration - f_limit) * process_param.volume
            process_param.aaa_mass_v = process_param.f_mass_v / coverage
            process_param.aaa_mass_d = process_param.daily_water / process_param.volume * process_param.aaa_mass_v
        } catch(error) {
            coverage = "error"
        }
    }

    function handleClick() {
        aaa_dosing()
        show_results = true
    }

</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Initial Values</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" bind:value={process_param.daily_water} label="Daily water needs" suffix="l/d" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the daily water needs</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" bind:value={data.concentration} label="Initial Fluoride Concentration" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the initial fluoride concentration</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" bind:value={data.contact_time} label="Contact Time" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the desired contact time for the adsorption process</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" bind:value={process_param.volume} label="Process Volume" suffix="l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the process volume</Tooltip>
            </Wrapper>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Competing Ions</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" bind:value={data.concentration_chloride} label="Chloride concentration" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the initial chloride concentration</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" bind:value={data.concentration_sulfate} label="Sulfate concentration" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the initial sulfate concentration</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" bind:value={data.concentration_bicarbonate} label="Bicarbonate concentration" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the initial bicarbonate concentration</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" bind:value={data.concentration_hydrogen_phosphate} label="Hydrogen Phosphate concentration" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the initial hydrogen phosphate concentration</Tooltip>
            </Wrapper>
            <Wrapper>
                <Textfield type="number" bind:value={data.concentration_arsenic} label="Arsenic concentration" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the initial arsenic concentration</Tooltip>
            </Wrapper>
        </Content>
    </Paper>
</div>

<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={handleClick}>Predict</Button>
</Group>

{#if show_results}
    <div style="display:flex;" id="results">
        <Paper style="flex-grow:1;">
            <Title>Prediction</Title>
            <Content>
                {#await coverage}
                    <LinearProgress indeterminate />
                {:then coverage}
                    <DataTable table$aria-label="Results" style="width: 100%;">
                        <Head>
                        <Row>
                            <Cell>Description</Cell>
                            <Cell numeric>Value</Cell>
                        </Row>
                        </Head>
                        <Body>
                            <Row>
                                <Cell style="white-space:normal;">Concentration (in mg/l)</Cell>
                                <Cell numeric>{data.concentration}</Cell>
                            </Row>
                            <Row>
                                <Cell style="white-space:normal;">Contact Time (in min)</Cell>
                                <Cell numeric>{data.contact_time}</Cell>
                            </Row>
                            <Row>
                                <Cell style="white-space:normal;">Coverage (in mg/g)</Cell>
                                <Cell numeric>{coverage}</Cell>
                            </Row>
                            <Row>
                                <Cell style="white-space:normal;">Used activated alumina per process (in g/{process_param.volume}l)</Cell>
                                <Cell numeric>{process_param.aaa_mass_v.toFixed(0)}</Cell>
                            </Row>
                            <Row>
                                <Cell style="white-space:normal;">Daily used activated alumina (in g/d)</Cell>
                                <Cell numeric>{process_param.aaa_mass_d.toFixed(0)}</Cell>
                            </Row>
                        </Body>
                    </DataTable>
                {/await}
            </Content>
        </Paper>
    </div>
{/if}