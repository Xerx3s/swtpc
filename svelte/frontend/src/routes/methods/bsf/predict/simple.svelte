<script lang="ts">
    import Slider from "@smui/slider"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Textfield from "@smui/textfield"
    import Button, { Group } from "@smui/button"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';
	import { selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import List, {Item, Meta, Label } from "@smui/list"
    import Checkbox from "@smui/checkbox"

    let param = {
        "turbidity": 0,
        "organic_material": false,
        "results": false
    }

    let data = {
        "diameter": 40, // cm
        "material_height": 50, // cm
        "mean_grain_diameter": 0.2, // mm
        "mean_flow": 20, // l/h
        "mean_pause": 12, // h/d
        "time_schmutzdecke": 14, // d
        "initial_turbidity": 30, // NTU
        "initial_tvc": 10000, // cfu/100ml
        "print_assessment": false,
        "load_pipe": false}

    let pred_ftur = 0.0

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
    }

    function handleclick() {
        param.results = true
        data.initial_turbidity = param.turbidity * 10
        predict_bsf()
    }

</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1">
        <Title>Turbidity</Title>
        <Content>
            <Slider bind:value={param.turbidity} min={0} max={3} step={1} style="min-width:10em"/>
            <center>
            {#if param.turbidity === 0}
                none
            {:else if param.turbidity === 1}
                low
            {:else if param.turbidity === 2}
                medium
            {:else if param.turbidity === 3}
                high
            {/if}
            </center>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Taste or Smell</Title>
        <Content>
            <List checkList>
                <Item>
                    <Label>Earthy or Musty</Label>
                    <Meta>
                        <Checkbox bind:checked={param.organic_material} />
                    </Meta>
                </Item>
            </List>
        </Content>
    </Paper>
</div>
<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={handleclick}>Analyze</Button>
</Group>
{#if param.results}
    <div style="display:flex; margin-bottom:1em">
        <Paper style="flex-grow:1;">
            <Title>Results</Title>
            <Content>
                Based on the given input parameters and the assumptions listed below,
                a residual turbidity of {pred_ftur} NTU is expected after treatment of the water by biosand filtration.
                {#if param.organic_material}
                    Any bacteria present in the water should have been reduced by at least 90 %.
                {/if}
                <br /> <br />
                Assumptions as follows: <br />
                 - Bucket (diameter 40 cm) filled with 50 cm of fine sand. <br />
                 - Last scraping of the schmutzdecke was 14 days ago
            </Content>
        </Paper>
    </div>
{/if}