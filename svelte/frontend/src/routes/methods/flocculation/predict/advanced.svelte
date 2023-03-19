<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';


    let data = {
        "surface_water": "model suspension",
        "initial_pH": 8.2,
        "initial_EC": 450,
        "initial_turbidity": 130,
        "flocculant": "Moringa",
        "floc_concentration": 20,
        "floc_saline_Molarity": 0.3,
        "floc_dose": 200,
        "floc_cactus_share": 0,
        "stirring_speed_coagulation_phase": 100,
        "duration_coagulation_phase": 1,
        "stirring_speed_flocculation_phase": 20,
        "duration_flocculation_phase": 15,
        "duration_sedimentation_phase": 45,
        "print_assessment": false,
        "load_pipe": false}

    let pred_ftur = 0.0
    let pred_fpH = 0.0
    let pred_fEC = 0.0
    let flocculants = get_flocculants()
    let show_results = false

    async function get_flocculants() {
        let url = "http://localhost:3001/floc/"

        let res = await fetch(url, {
            mode: "cors",
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        let res2 = await res.json()

        let flocs:String[] = []
        res2.forEach((element: string[]) => {
            //flocculants.push({id: element[0], name: element[0]})
            flocs.push(element[0])
        });
        return flocs
    }

    async function predict_tur() {
        let url = "http://localhost:3001/tur/"

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
    }

    async function predict_ph() {
        let url = "http://localhost:3001/ph/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()
    
        pred_fpH = res2["final_pH"]
        }

    async function predict_ec() {
        let url = "http://localhost:3001/ec/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()
        
        pred_fEC = res2["final_EC"].toFixed(0)
        }
    
    function handleClick() {
        predict_tur()
        predict_ph()
        predict_ec()
        show_results = true
        }
</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Indicator Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Textfield type="number" input$step=0.1 bind:value={data.initial_pH} label="Initial pH" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.initial_EC} label="Initial EC" suffix="µS/cm" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.initial_turbidity} label="Initial Turbidity" suffix="NTU" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Flocculant Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            {#await flocculants}
                <LinearProgress indeterminate />
            {:then flocculants}
                <Select bind:value={data.flocculant} label="Flocculant" style="flex-grow:1; margin-bottom:0.5em">
                    {#each flocculants as flocculant}
                        <Option value={flocculant}>{flocculant}</Option>
                    {/each}
                </Select>
            {/await}
                <br />
                <Textfield type="number" input$step=1 bind:value={data.floc_concentration} label="Flocculant Concentration in Base Solution" suffix="g/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
                <Textfield type="number" input$step=0.1 bind:value={data.floc_saline_Molarity} label="Saline Molarity of Flocculant Base Solution" suffix="mol/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
                <Textfield type="number" input$step=1 bind:value={data.floc_cactus_share} label="Cactus Share in Flocculant Base Solution" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
                <Textfield type="number" input$step=1 bind:value={data.floc_dose} label="Flocculant Dosage" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Flocculation Process Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Textfield type="number" input$step=1 bind:value={data.stirring_speed_coagulation_phase} label="Stirring Speed during Coagulation Phase" suffix="RPM" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.duration_coagulation_phase} label="Duration of Coagulation Phase" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.stirring_speed_flocculation_phase} label="Stirring Speed during Flocculation Phase" suffix="RPM" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.duration_flocculation_phase} label="Duration of Flocculation Phase" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step=1 bind:value={data.duration_sedimentation_phase} label="Duration of Sedimentation Phase" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
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
                <Textfield type="number" input$step=0.1 bind:value={pred_fpH} label="Final pH" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
                <Textfield type="number" input$step=1 bind:value={pred_fEC} label="Final EC" suffix="µS/cm" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
                <Textfield type="number" input$step=1 bind:value={pred_ftur} label="Final Turbidity" suffix="NTU" style="flex-grow:1; margin-bottom:0.5em"/>
                <br />
            </Content>
        </Paper>
    </div>
{/if}