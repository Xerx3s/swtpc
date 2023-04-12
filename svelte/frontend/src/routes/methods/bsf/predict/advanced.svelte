<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';
    import Tooltip, { Wrapper } from '@smui/tooltip';
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';


    let data = {
        "diameter": 40,
        "material_height": 50,
        "mean_grain_diameter": 0.2,
        "mean_flow": 20,
        "mean_pause": 12,
        "time_schmutzdecke": 14,
        "initial_turbidity": 30,
        "initial_tvc": 1000,
        "print_assessment": false,
        "load_pipe": false}

    let pred_ftur = 0.0
    let pred_tvc = 0.0
    let show_results = false

    async function predict_bsf() {
        let url = "http://localhost:3001/bsf/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        console.log(JSON.stringify(data))
        let res2 = await res.json()
        pred_ftur = res2["final_turbidity"].toFixed(0)

        return true
    }

    function handleClick() {
        show_results = predict_bsf()
        pred_tvc = ((1 - 0.90) * data.initial_tvc).toFixed(0)
        }
</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Indicator Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.initial_turbidity} label="Initial Turbidity" suffix="NTU" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Initial turbidity of the raw water used</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.initial_tvc} label="Initial Total Viable Count" suffix="cfu/100ml" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Indicator for the pathogen load of the raw water</Tooltip>
            </Wrapper>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Filter Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.diameter} label="Diameter" suffix="cm" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Diameter of the bucket used for the construction of the biosand filter.</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=0.1 bind:value={data.material_height} label="Material Height" suffix="cm" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Height of the filled sand layer</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=0.05 bind:value={data.mean_grain_diameter} label="Mean Grain Diameter" suffix="mm" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>mean grain diameter of the sand used</Tooltip>
            </Wrapper>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Filtration Process Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.mean_flow} label="Mean Flow" suffix="l/h" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>mean flow rate when using the filter.</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.mean_pause} label="Duration of daily Pause Time" suffix="h/d" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Total pause time over one day of use.</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.time_schmutzdecke} label="Time since last Scraping of Schmutzdecke" suffix="d" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Days that the schmutzdecke could develop again since the last surface scraping.</Tooltip>
            </Wrapper>
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
                    <p>
                        Based on the given input parameters, a residual turbidity of {pred_ftur} NTU is expected after treatment of the water by biosand filtration.
                        Pathogens should have been reduced to a total viable count of {pred_tvc} cfu/100ml.
                        {#if pred_tvc > 99}
                            This is still a high value considering that the WHO guidelines set a value of 0 cfu/100ml.
                            If problems that can be attributed to pathogens continue to occur, another disinfection step such as <a href="http://192.168.178.69:3000/en/methods/sodis" target="_blank" rel="noreferrer">SODIS</a> or <a href="http://192.168.178.69:3000/en/methods/chlorination" target="_blank" rel="noreferrer">chlorination</a> should be integrated.
                        {/if}
                    </p>
                    <DataTable table$aria-label="Results" style="max-width: 100%;">
                        <Head>
                        <Row>
                            <Cell>Description</Cell>
                            <Cell numeric>Value</Cell>
                        </Row>
                        </Head>
                        <Body>
                            <Row>
                                <Cell>Final turbidity (in NTU)</Cell>
                                <Cell numeric>{pred_ftur}</Cell>
                            </Row>
                            <Row>
                                <Cell>Final total viable count (in cfu/100ml)</Cell>
                                <Cell numeric>{pred_tvc}</Cell>
                            </Row>
                        </Body>
                    </DataTable>
                {/await}
            </Content>
        </Paper>
    </div>
{/if}