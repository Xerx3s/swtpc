<script lang="ts">
    import Textfield from "@smui/textfield"
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';
    import Tooltip, { Wrapper } from '@smui/tooltip';
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';
    import Checkbox from '@smui/checkbox';
    import FormField from '@smui/form-field';

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
        "load_pipe": true}

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

        if (data.flocculant == "Kaktus") {
            data.floc_cactus_share = 100
        } else if (data.flocculant == "Moringa") {
            data.floc_cactus_share = 0
        }

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

        return true
        }
    
    function handleClick() {
        predict_tur()
            .then(() => predict_ph())
            .then(() => predict_ec())
        //predict_ph()
        //show_results = predict_ec()
        show_results = true
        }
</script>

<div style="color:red;">
    <b>Development tools:</b>
    <FormField>
      <Checkbox bind:checked={data.load_pipe} />
      <span slot="label">load pipe</span>
    </FormField>
    <FormField>
      <Checkbox bind:checked={data.print_assessment} />
      <span slot="label">print assessment</span>
    </FormField>
</div>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Indicator Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" input$step=0.1 bind:value={data.initial_pH} label="Initial pH" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Initial pH of the raw water used</Tooltip>
            </Wrapper>
                <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.initial_EC} label="Initial EC" suffix="µS/cm" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Initial electrical conductivity of the raw water used</Tooltip>
            </Wrapper>
                <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.initial_turbidity} label="Initial Turbidity" suffix="NTU" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Initial turbidity of the raw water used</Tooltip>
            </Wrapper>
                <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Flocculant Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            {#await flocculants}
                <LinearProgress indeterminate />
            {:then flocculants}
                <Wrapper>
                    <Select bind:value={data.flocculant} label="Flocculant" style="flex-grow:1; margin-bottom:0.5em">
                        {#each flocculants as flocculant}
                            <Option value={flocculant}>{flocculant}</Option>
                        {/each}
                    </Select>
                    <Tooltip>Select the flocculant you want to use</Tooltip>
                </Wrapper>
            {/await}
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.floc_concentration} label="Flocculant Concentration in Base Solution" suffix="g/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the amount of flocculant (usually powder form) that you wish to use to prepare the concentrated base solution.</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=0.1 bind:value={data.floc_saline_Molarity} label="Saline Molarity of Flocculant Base Solution" suffix="mol/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the amount of salt you want to use to prepare the stock solution. Common salt (NaCl) has a molar mass of about 58 g/mol.</Tooltip>
            </Wrapper>
            <br />
            {#if data.flocculant == "MoringaKaktus"}
                <Wrapper>
                    <Textfield type="number" input$step=1 bind:value={data.floc_cactus_share} label="Cactus Share in Flocculant Base Solution" suffix="%" style="flex-grow:1; margin-bottom:0.5em"/>
                    <Tooltip>Enter the percentage of cactus in the flocculant</Tooltip>
                </Wrapper>
                <br />
            {/if}
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.floc_dose} label="Flocculant Dosage" suffix="mg/l" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>Enter the amount of flocculant you want to use to flocculate one liter of raw water</Tooltip>
            </Wrapper>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Flocculation Process Parameter</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.stirring_speed_coagulation_phase} label="Stirring Speed during Coagulation Phase" suffix="RPM" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    Specify the stirring speed at the beginning of the flocculation process.
                    This should be quite high during the coagulation phase.
                </Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.duration_coagulation_phase} label="Duration of Coagulation Phase" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    Specify the stirring time at the beginning of the flocculation process.
                    This should be quite short during the coagulation phase.
                    Normally a stirring time around a minute or two should be enough.
                </Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.stirring_speed_flocculation_phase} label="Stirring Speed during Flocculation Phase" suffix="RPM" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    Specify the stirring speed during the flocculation phase of the process.
                    This should not be too high.
                </Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.duration_flocculation_phase} label="Duration of Flocculation Phase" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    Specify the stirring time during the flocculation phase of the process.
                    This shouldn't be too short.
                    Wait until visibly larger flocs have formed before proceeding to the next phase.</Tooltip>
            </Wrapper>
            <br />
            <Wrapper>
                <Textfield type="number" input$step=1 bind:value={data.duration_sedimentation_phase} label="Duration of Sedimentation Phase" suffix="min" style="flex-grow:1; margin-bottom:0.5em"/>
                <Tooltip>
                    Specify the sedimentation time at the end of the flocculation process.
                    This should be quite long.
                    Wait until all the flocs have settled.
                    Longer standing times rarely have negative effects.
                </Tooltip>
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
                Based on the values entered above, a final pH of {pred_fpH} and an EC of {pred_fEC} µS/cm should result.
                The residual turbidity is approximately {pred_ftur} NTU.
                <br />
                {#if pred_ftur > 5}
                    <p>
                        Since the residual turbidity is still above the WHO guideline value of 5 NTU, it is recommended to integrate another treatment stage for turbidity reduction.
                        For example, <a href="http://192.168.178.69:3000/en/methods/biosand-filtration" target="_blank" rel="noreferrer">biosand filtration</a> can be useful for this.
                    </p>
                {/if}
                    <DataTable table$aria-label="Results" style="max-width: 100%;">
                        <Head>
                        <Row>
                            <Cell>Description</Cell>
                            <Cell numeric>Value</Cell>
                        </Row>
                        </Head>
                        <Body>
                        <!--    <Row>
                                <Cell>Final pH</Cell>
                                <Cell numeric>{pred_fpH}</Cell>
                            </Row>
                        -->
                            <Row>
                                <Cell>Final EC (in µS/cm)</Cell>
                                <Cell numeric>{pred_fEC}</Cell>
                            </Row>
                            <Row>
                                <Cell>Final turbidity (in NTU)</Cell>
                                <Cell numeric>{pred_ftur}</Cell>
                            </Row>
                        </Body>
                    </DataTable>
                {/await}
            </Content>
        </Paper>
    </div>
{/if}