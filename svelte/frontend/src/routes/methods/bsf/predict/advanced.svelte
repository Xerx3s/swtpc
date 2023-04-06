<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';


    let data = {
        "diameter": 40,
        "material_height": 50,
        "mean_grain_diameter": 0.2,
        "mean_flow": 20,
        "mean_pause": 12,
        "time_schmutzdecke": 14,
        "initial_turbidity": 30,
        "initial_tvc": 10000,
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
            <Textfield type="number" input$step=1 bind:value={data.initial_turbidity} label="Initial Turbidity" suffix="NTU" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.initial_tvc} label="Initial Total Viable Count" suffix="cfu/100ml" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Filter Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Textfield type="number" input$step=1 bind:value={data.diameter} label="Diameter" suffix="cm" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=0.1 bind:value={data.material_height} label="Material Height" suffix="cm" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=0.01 bind:value={data.mean_grain_diameter} label="Mean Grain Diameter" suffix="mm" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Filtration Process Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Textfield type="number" input$step=1 bind:value={data.mean_flow} label="Mean Flow" suffix="l/h" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.mean_pause} label="Duration of daily Pause Time" suffix="h/d" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.time_schmutzdecke} label="Time since last Scraping of Schmutzdecke" suffix="d" style="flex-grow:1; margin-bottom:0.5em"/>
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
                    <Textfield type="number" input$step=1 bind:value={pred_ftur} label="Final Turbidity" suffix="NTU" style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                    <Textfield type="number" input$step=1 bind:value={pred_tvc} label="Final Total Viable Count" suffix="cfu/100ml" style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                {/await}
            </Content>
        </Paper>
    </div>
{/if}