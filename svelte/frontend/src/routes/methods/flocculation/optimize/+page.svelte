<script lang="ts">
	import { selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label, Separator } from "@smui/list"
    import Checkbox from "@smui/checkbox"
    import Textfield from "@smui/textfield"
    import Slider from '@smui/slider';
    import LinearProgress from '@smui/linear-progress';
    import DataTable, { Head, Body, Row, Cell } from '@smui/data-table';

    let param_sets = get_bounds()
    let result = optimize()
    let show_result = false

    let description = {
        initial_pH: "Initial pH-Value",
        initial_EC: "Initial EC (in µS/cm)",
        initial_turbidity: "Initial Turbidity (in NTU)",
        flocculant: "Flocculant", 
        floc_concentration: "Flocculant Concentration in Base Solution (in g/l)", 
        floc_saline_Molarity: "Saline Molarity of Flocculant Base Solution (in mol/l)",
        floc_cactus_share: "Cactus Share in Flocculant Base Solution (in %)",
        floc_dose: "Flocculant Dosage (in mg/l)",
        stirring_speed_coagulation_phase: "Stirring Speed during Coagulation Phase (in RPM)",
        duration_coagulation_phase: "Duration of Coagulation Phase (in minutes)",
        stirring_speed_flocculation_phase: "Stirring Speed during Flocculation Phase (in RPM)",
        duration_flocculation_phase: "Duration of Flocculation Phase (in minutes)",
        duration_sedimentation_phase: "Duration of Sedimentation Phase (in minutes)",
        final_turbidity: "Final Turbidity (in NTU)"
        }

    async function get_bounds() {
        let url = "https://api.sustainable-water.de/floc_bounds/"

        let res = await fetch(url, {
            mode: "cors",
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        let bounds = await res.json()
        let param_sets = [
            {
                name: "Indicator Parameter",
                param: [
                    {
                        id: "initial_pH",
                        description: "Initial pH-Value",
                        unit: "",
                        bounds: [bounds.initial_pH[0], bounds.initial_pH[1]],
                        minmax: [8, 9],
                        step: 0.1,
                        minRange: 0.2,
                    },
                    {
                        id: "initial_EC",
                        description: "Initial EC (in µS/cm)",
                        unit: "µS/cm",
                        bounds: [bounds.initial_EC[0], bounds.initial_EC[1]],
                        minmax: [400, 600],
                        step: 0.1,
                        minRange: 0.2,
                    },
                    {
                        id: "initial_turbidity",
                        description: "Initial Turbidity (in NTU)", 
                        unit: "NTU",
                        bounds: [bounds.initial_turbidity[0], bounds.initial_turbidity[1]],
                        minmax: [80, 120],
                        step: 1,
                        minRange: 10,
                    },
                ]
            },
            {
                name: "Flocculant Parameter",
                param: [
                    {
                        id: "floc_concentration",
                        description: "Flocculant Concentration in Base Solution (in g/l)", 
                        unit: "g/l",
                        bounds: [bounds.floc_concentration[0], bounds.floc_concentration[1]],
                        minmax: [20, 30],
                        step: 1,
                        minRange: 1,
                    },
                    {
                        id: "floc_saline_Molarity",
                        description: "Saline Molarity of Flocculant Base Solution (in mol/l)",
                        unit: "mol/l",
                        bounds: [bounds.floc_saline_Molarity[0], bounds.floc_saline_Molarity[1]],
                        minmax: [0.1, 0.5],
                        step: 0.1,
                        minRange: 0.1,
                    },
                    {
                        id: "floc_cactus_share",
                        description: "Cactus Share in Flocculant Base Solution (in %)",
                        unit: "%",
                        bounds: [bounds.floc_cactus_share[0], bounds.floc_cactus_share[1]],
                        minmax: [0, 100],
                        step: 1,
                        minRange: 5,
                    },
                    {
                        id: "floc_dose",
                        description: "Flocculant Dosage (in mg/l)",
                        unit: "mg/l",
                        bounds: [bounds.floc_dose[0], bounds.floc_dose[1]],
                        minmax: [100, 300],
                        step: 1,
                        minRange: 25,
                    },
                ]
            },
            { 
                name: "Flocculation Process Parameter",
                param: [
                    {
                        id: "stirring_speed_coagulation_phase",
                        description: "Stirring Speed during Coagulation Phase (in RPM)",
                        unit: "RPM",
                        bounds: [bounds.stirring_speed_coagulation_phase[0], bounds.stirring_speed_coagulation_phase[1]],
                        minmax: [75, 125],
                        step: 5,
                        minRange: 5,
                    },
                    {
                        id: "duration_coagulation_phase",
                        description: "Duration of Coagulation Phase (in minutes)",
                        unit: "minutes",
                        bounds: [bounds.duration_coagulation_phase[0], bounds.duration_coagulation_phase[1]],
                        minmax: [1, 1.5],
                        step: 0.1,
                        minRange: 0.5,
                    },
                    {
                        id: "stirring_speed_flocculation_phase",
                        description: "Stirring Speed during Flocculation Phase (in RPM)",
                        unit: "RPM",
                        bounds: [bounds.stirring_speed_flocculation_phase[0], bounds.stirring_speed_flocculation_phase[1]],
                        minmax: [20, 30],
                        step: 5,
                        minRange: 5,
                    },
                    {
                        id: "duration_flocculation_phase",
                        description: "Duration of Flocculation Phase (in minutes)",
                        unit: "minutes",
                        bounds: [bounds.duration_flocculation_phase[0], bounds.duration_flocculation_phase[1]],
                        minmax: [10, 15],
                        step: 1,
                        minRange: 1,
                    },
                    {
                        id: "duration_sedimentation_phase", 
                        description: "Duration of Sedimentation Phase (in minutes)",
                        unit: "minutes",
                        bounds: [bounds.duration_sedimentation_phase[0], bounds.duration_sedimentation_phase[1]],
                        minmax: [30, 60],
                        step: 1,
                        minRange: 5,
                    },
                ]
            },
        ]
        return param_sets
    }

    async function optimize() {
        
        let data = {
            pred_type: "tur",
            flocculant: "Moringa",
            surface_water: "model suspension",
            load_pipe: true,
            print_assessment: false,
        };

        (await param_sets).forEach(set => {
            set.param.forEach(param => {
                let key_min = param.id + "_min";
                let key_max = param.id + "_max";
                Object.assign(data, { [key_min]: param.minmax[0] });
                Object.assign(data, { [key_max]: param.minmax[1] });
            })
        })
        
        let url = "https://api.sustainable-water.de/opt_tur/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()
        let res3 = []
        for (const [key, value] of Object.entries(res2)) {
            let name = description[key]
            if (!(isNaN(value))) {
                if (key == "initial_pH" || key == "floc_saline_Molarity") {
                let rounded = value.toFixed(1)
                res3.push({ 
                    id: key,
                    name: name,
                    opt: rounded })
                } else {
                    let rounded = value.toFixed(0)
                    res3.push({ 
                        id: key,
                        name: name,
                        opt: rounded })
                }
            } else {
                res3.push({ 
                id: key,
                name: name,
                opt: value })
            }
        }
        return res3
    }

    function handleClick() {
        result = optimize()
        show_result = true
    }
</script>

<div>
    <h5>Flocculation Optimization</h5>
    <p>
        For more information on the treatment method, see the <a href="https://wiki.sustainable-water.de/en/methods/flocculation" target="_blank" rel="noreferrer">knowledge base entry</a>.
    </p>
    <p>
        Define the possible areas where the necessary parameters are located by dragging the sliders.
        If you have specific values, narrow the selected range as much as possible.<br />
        As soon as you click the Optimize button, the processing will start and the results will be presented afterwards.<br />
        The results are the respective optimal parameters within the specified range.
        These have been selected with the aim of maximizing the cleaning performance.
    </p>
</div>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    {#await param_sets}
        <Paper style="margin:1em; flex-grow:1">
            <LinearProgress indeterminate />
        </Paper>
    {:then param_sets}
        {#each param_sets as set}
            <Paper style="margin:1em; flex-grow:1; min-width:20em">
                <Title>{set.name}</Title>
                {#each set.param as param}
                    <Content style="display:flex; flex-direction:column; margin:1em">
                        {param.description}
                        <Slider
                            range
                            bind:start={param.minmax[0]}
                            bind:end={param.minmax[1]}
                            min={param.bounds[0]}
                            max={param.bounds[1]}
                            step={param.step}
                            minRange={param.minRange}
                            discrete
                        />
                        Value: {param.minmax[0]} to {param.minmax[1]} {param.unit}
                        <br />
                    </Content>
                    <Separator />
                {/each}
            </Paper>
        {/each}
    {/await}
</div>
<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={handleClick}>Optimize</Button>
</Group>

{#if show_result}
    <div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
        <Paper style="margin:1em; flex-grow:1; min-width:20em">
            <Title>Results</Title>
            {#await result}
                <LinearProgress indeterminate />
            {:then result}
                <Content style="display:flex; flex-direction:column; margin:1em">
                    <p>
                        The following table shows the results of the optimization.
                        The optimum values for maximum cleaning performance were calculated in each case from the ranges given above.
                        As can be seen, the turbidity should reduce from {result[2].opt} NTU to {result[12].opt} NTU.
                    </p>
                    <DataTable table$aria-label="Results" style="max-width: 100%;">
                        <Head>
                          <Row>
                            <Cell>Description</Cell>
                            <Cell numeric>Value</Cell>
                          </Row>
                        </Head>
                        <Body>
                            {#each result as r}
                                <Row>
                                    <Cell>{r.name}</Cell>
                                    <Cell numeric>{r.opt}</Cell>
                                </Row>
                            {/each}
                        </Body>
                      </DataTable>
                </Content>
            {/await}
        </Paper>
    </div>
{/if}