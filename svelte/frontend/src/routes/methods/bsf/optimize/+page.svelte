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
        let url = "http://localhost:3001/bsf_bounds/"

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
                name: "Filter Parameter",
                param: [
                    {
                        id: "diameter",
                        description: "Diameter (in cm)", 
                        unit: "cm",
                        bounds: [bounds.diameter[0], bounds.diameter[1]],
                        minmax: [20, 30],
                        step: 1,
                        minRange: 1,
                    },
                    {
                        id: "material_height",
                        description: "Material Height (in cm)", 
                        unit: "cm",
                        bounds: [bounds.material_height[0], bounds.material_height[1]],
                        minmax: [5, 25],
                        step: 0.5,
                        minRange: 1,
                    },
                    {
                        id: "mean_grain_diameter",
                        description: "Mean Grain Diameter (in mm)",
                        unit: "mm",
                        bounds: [bounds.mean_grain_diameter[0], bounds.mean_grain_diameter[1]],
                        minmax: [0.15, 0.2],
                        step: 0.01,
                        minRange: 0.05,
                    }
                ]
            },
            { 
                name: "Filtration Process Parameter",
                param: [
                    {
                        id: "mean_flow",
                        description: "Mean Flow (in l/h)",
                        unit: "l/h",
                        bounds: [bounds.mean_flow[0], bounds.mean_flow[1]],
                        minmax: [1, 100],
                        step: 0.01,
                        minRange: 5,
                    },
                    {
                        id: "mean_pause",
                        description: "Mean Pause Periode (in h)",
                        unit: "h",
                        bounds: [bounds.mean_pause[0], bounds.mean_pause[1]],
                        minmax: [10, 24],
                        step: 0.1,
                        minRange: 0.5,
                    },
                    {
                        id: "time_schmutzdecke",
                        description: "Time since last Scraping of Schmutzdecke (in d)",
                        unit: "d",
                        bounds: [bounds.time_schmutzdecke[0], bounds.time_schmutzdecke[1]],
                        minmax: [10, 20],
                        step: 1,
                        minRange: 5,
                    }
                ]
            },
        ]
        return param_sets
    }

    async function optimize() {
        let data = {
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
        
        let url = "http://localhost:3001/opt_bsf/"
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

<div>
    <h5>Biosand Filtration Optimization</h5>
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