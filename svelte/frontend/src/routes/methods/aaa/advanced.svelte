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
    import Map from '$lib/leafletmap/Map.svelte';
    import Slider from "@smui/slider";
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
    import { coords_store } from "/opt/svelte/frontend/src/stores/stores";
    import Tooltip, { Wrapper } from '@smui/tooltip';
    
    let map_component;

    let location = {
        "city": "Darmstadt",
        "country": "Deutschland"
    }

    let sun = {
        "rise": 0,
        "set": 24
    }

    let data = {
        "latitude": 49.87334845778753,
        "longitude": 8.65687138520094,
        "starting_hour": 8,
        "water_temperature": 18,
        "target_logdis": 4
    }

    coords_store.subscribe(value => {
        data.latitude = value.lat
        data.longitude = value.lng
        location.city = value.city
        location.country = value.country
    })

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
        scales: {
            xAxes: [
                {
                    position: "bottom",
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                }
            ],
            yAxes: [
                {
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                }
            ],
        },
    }
        
    async function owm_sunriseset() {
        let key = "a9c05d43e3817e2b68f4f0f305504cf7"
        let url = `https://api.openweathermap.org/data/2.5/weather?lat=${data.latitude}&lon=${data.longitude}&exclude=hourly,daily&appid=${key}`
        let res = await fetch(url)
        const response = await res.json()

        // Werte ändern sich erst nach zweimaligem Ausführen...
        let utcrise = new Date(response.sys.sunrise * 1000)
        let utcset = new Date(response.sys.sunset * 1000)
        sun.rise = new Date(utcrise.getTime() + (response.timezone+3600) * 1000).getUTCHours() //+60 min sonst ist die Radiation noch 0...
        sun.set = new Date(utcset.getTime() + response.timezone * 1000).getUTCHours()
        data.starting_hour = await sun.rise + 1
    } 

    async function setNewLocation() {
        let coords = await map_component.newlocation(location.city, location.country)
        data.latitude = coords.lat
        data.longitude = coords.lng
        owm_sunriseset()
    }
    
    function handleClick() {
        graph_data = sodis_forecast()
        show_results = true
    }

</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:40em">
        <Content style="display:flex; flex-direction:column; margin:0em">
            <Map bind:this={map_component}/>
        </Content>
    </Paper>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Location</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <div style="display:flex; flex-direction:row">
                <Wrapper>
                    <Textfield type="text" bind:value={location.city} label="City" style="flex-grow:1; margin-bottom:0.5em"/>
                    <Tooltip>Enter the city name of your location</Tooltip>
                </Wrapper>
                <Wrapper>
                    <Button on:click={setNewLocation} style="flex-grow:0.5; margin-top:0.75em">Search</Button>
                    <Tooltip>
                        Click this button after entering city and country.
                        You can click multiple times to skip through all cities of the same name.
                    </Tooltip>
                </Wrapper>
            </div>
            <br />
            <Wrapper>
                <Textfield type="text" bind:value={location.country} label="Country" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the country name of your location</Tooltip>
            </Wrapper>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Initial Values</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Slider bind:value={data.starting_hour} min={sun.rise} max={sun.set} step={1} style="min-width:10em"/>
                <Textfield type="number" input$step=1 input$min={sun.rise} input$max={sun.set} bind:value={data.starting_hour} label="Starting Hour" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    Either use the slider or enter a value to define the starting hour.
                    It is assumed that at the selected time the bottles filled with water are placed in direct sunlight.
                </Tooltip>
            </Wrapper>
            <br />
            <!--
            <Textfield type="number" input$step=1 bind:value={data.water_temperature} label="Water Temperature" suffix="°C" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            -->
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.target_logdis} label="Target Logarithmic Disinfection" suffix="" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    A value of 1 corresponds to a pathogen reduction of 90 %, 2 of 99 %, etc.
                    The actual reduction required always depends on the raw water used, but a value of 4 should not be undercut if possible.</Tooltip>
            </Wrapper>
            <br />
        </Content>
    </Paper>
</div>

<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={handleClick}>Predict</Button>
</Group>

{#if show_results}
    <div style="display:flex; flex-direction:column; justify-content:center; align-items:stretch">
        <Paper style="margin:1em; flex-grow:1; min-width:20em">
            <Title>Prediction</Title>
            <Content style="display:flex; flex-direction:column; margin:1em">
                {#await graph_data}
                    <LinearProgress indeterminate />
                {:then graph_data}
                    {message} <br />
                    <DataTable table$aria-label="Results" style="max-width: 100%;">
                        <Head>
                        <Row>
                            <Cell>Description</Cell>
                            <Cell numeric>Value</Cell>
                        </Row>
                        </Head>
                        <Body>
                            <Row>
                                <Cell>Final log disinfection</Cell>
                                <Cell numeric>{final_logdis}</Cell>
                            </Row>
                            <Row>
                                <Cell>Duration (in h)</Cell>
                                <Cell numeric>{duration}</Cell>
                            </Row>
                        </Body>
                    </DataTable>
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