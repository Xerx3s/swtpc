<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group, Label } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';
    import Dialog, { Actions } from '@smui/dialog';
    import { onMount } from 'svelte';
    import { Line } from 'svelte-chartjs';
    import 'chart.js/auto';

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
    let graph_data = sodis_forecast()

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

        let x_data = res2["result"]["time"].map(function(v) {return v.slice(11, 16) })
        let graph_data = [
            {
                labels: x_data,
                datasets: [
                    {
                        label: "logarithmic Disinfection",
                        data: res2["result"]["Log Dis"],
                        borderColor: "purple",
                    },
                ],
            },
            {
                labels: x_data,
                datasets: [
                    {
                        label: "Radiation",
                        data: res2["result"]["actual Radiation"],
                        borderColor: "red",
                    },
                ],
            },
            {
                labels: x_data,
                datasets: [
                    {
                        label: "ambient Temperature",
                        data: res2["result"]["Air Temp"],
                        borderColor: "green",
                    },
                ],
            },
            {
                labels: x_data,
                datasets: [
                    {
                        label: "Water Temperature",
                        data: res2["result"]["Water Temp"],
                        borderColor: "blue",
                    },
                ],
            },
            {
                labels: x_data,
                datasets: [
                    {
                        label: "total Cloud Coverage",
                        data: res2["result"]["total Clouds"],
                        borderColor: "grey",
                    },
                ],
            }
        ];

        return graph_data
    }

    let options: {
        title: {
            display: true,
            text: 'Chart.js Line Chart'
        },
        },
        interaction: {
            mode: 'index',
            intersect: false
        },
        scales: {
            x: {
                display: true,
                title: {
                display: true,
                text: 'Month'
                }
            },
            y: {
                display: true,
                title: {
                display: true,
                text: 'Value'
                }
            }
        }
    
    function handleClick() {
        graph_data = sodis_forecast()
        show_results = true
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
            <Textfield type="number" input$step=1 bind:value={data.starting_hour} label="Starting" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.water_temperature} label="Water Temperature" suffix="°C" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.target_logdis} label="Target Logarithmic Disinfection" suffix="" style="flex-grow:1; margin-bottom:0.5em"/>
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
                {#await graph_data}
                    <LinearProgress indeterminate />
                {:then graph_data}
                    {message}
                    <br />
                    <Textfield type="number" input$step=0.01 bind:value={final_logdis} label="Final Logarithmic Disinfection" suffix="" style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                    <Textfield type="number" input$step=0.01 bind:value={duration} label="Duration" suffix="h" style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                {/await}
            </Content>
        </Paper>
        <Paper style="margin:1em; flex-grow:1; min-width:20em">
            <Title>Graph</Title>
            <Content style="display:flex; flex-direction:column; margin:1em">
                {#await graph_data}
                    <LinearProgress indeterminate />
                {:then graph_data}
                    <Line data={graph_data[0]} options={options} width={100} height={25} />
                    (y-axis: log dis; x-axis: hh:mm) 
                    <Line data={graph_data[1]} options={options} width={100} height={25} />
                    (y-axis: W/m²; x-axis: hh:mm)
                    <Line data={graph_data[2]} options={options} width={100} height={25} />
                    (y-axis: °C; x-axis: hh:mm)
                    <!--
                    <Line data={graph_data[3]} options={options} width={100} height={25} />
                    (y-axis: °C; x-axis: hh:mm)
                    -->
                    <Line data={graph_data[4]} options={options} width={100} height={25} />
                    (y-axis: %; x-axis: hh:mm)
                {/await}
            </Content>
        </Paper>
    </div>
{/if}