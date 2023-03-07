<script lang="ts">
	import { selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label, Separator } from "@smui/list"
    import Checkbox from "@smui/checkbox"
    import Textfield from "@smui/textfield"
    import Slider from '@smui/slider';
    import LinearProgress from '@smui/linear-progress';

    let param_sets = get_bounds()
    let result = optimize()
    let show_result = false

    async function get_bounds() {
        let url = "http://localhost:3001/floc_bounds/"

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
            load_pipe: false,
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
        
        let url = "http://localhost:3001/opt_tur/"

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
            if (!(isNaN(value))) {
                if (key == "initial_pH" || key == "floc_saline_Molarity") {
                let rounded = value.toFixed(1)
                res3.push({ 
                    id: key,
                    opt: rounded })
                } else {
                    let rounded = value.toFixed(0)
                    res3.push({ 
                        id: key,
                        opt: rounded })
                }
            } else {
                res3.push({ 
                id: key,
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
                {#each result as r}
                    <Content style="display:flex; flex-direction:column; margin:1em">
                    <Textfield bind:value={r.opt} bind:label={r.id} style="flex-grow:1; margin-bottom:0.5em"/>
                    <br />
                    </Content>
                    <Separator />
                {/each}
            {/await}
        </Paper>
    </div>
{/if}