<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group, Label } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';
    import Dialog, { Actions } from '@smui/dialog';
    //import LeafletMap from '$lib/LeafletMap.svelte';
    

    let data = {
        "location_city": "Darmstadt",
        "location_country": "Deutschland",
        "starting_hour": 8,
        "water_temperature": 18,
        "target_logdis": 4
    }

    let duration = 0.0
    let message = ""
    let show_results = false
    let final_logdis = 0.0

    async function sodis_forecast() {
        let url = "http://localhost:3001/sodis/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()
        duration = res2["duration"].toFixed(1)
        message = res2["message"]
        final_logdis = res2["result"]["Log Dis"][res2["result"]["Log Dis"].length -1].toFixed(1)
        
        return true
    }

    function handleClick() {
        show_results = sodis_forecast()
        }
</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Location</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Textfield type="text" bind:value={data.location_city} label="City" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="text" bind:value={data.location_country} label="Country" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Initial Values</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Textfield type="number" input$step=1 bind:value={data.starting_hour} label="Starting Hour" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
</div>

<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={handleClick}>Predict</Button>
</Group>

{#if show_results}
    <div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
        <Paper style="margin:1em; flex-grow:1; min-width:20em">
            <Title>Prediction</Title>
            <Content style="display:flex; flex-direction:column; margin:1em">
                {#await show_results}
                    <LinearProgress indeterminate />
                {:then show_results}
                    {message}
                    <br />
                    <Textfield type="number" input$step=0.01 bind:value={final_logdis} label="Final logarithmic Disinfection" suffix="" style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                    <Textfield type="number" input$step=0.01 bind:value={duration} label="Duration" suffix="h" style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                {/await}
            </Content>
        </Paper>
    </div>
{/if}