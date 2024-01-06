<script lang="ts">
    import Slider from "@smui/slider"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import Textfield from "@smui/textfield"
    import Button, { Group } from "@smui/button"
    import Select, { Option } from "@smui/select"
    import LinearProgress from '@smui/linear-progress';

    let data = {
        "turbidity": 0,
        "flocculant": "Moringa"
    }
    let flocculants = get_flocculants()
    
    async function get_flocculants() {
        let url = "https://api.sustainable-water.de/floc/"

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

</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1">
        <Title>Turbidity</Title>
        <Content>
            <Slider bind:value={data.turbidity} min={0} max={3} step={1} style="min-width:10em"/>
            <center>
            {#if data.turbidity === 0}
                none
            {:else if data.turbidity === 1}
                low
            {:else if data.turbidity === 2}
                medium
            {:else if data.turbidity === 3}
                high
            {/if}
            </center>
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
        </Content>
    </Paper>
</div>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1; min-width:20em">
        <Title>Prediction</Title>
        <Content style="display:flex; flex-direction:column; margin:1em">
            {#if data.turbidity == 0}
                No treatment to reduce turbidity is necessary.
            {:else if data.flocculant == "Moringa"}
                Based on the indication of turbidity, a dose of {100 * data.turbidity} mg/l flocculant should be sufficient.
                The amount corresponds to about {data.turbidity / 2} dried and ground Moringa seed per liter of water.
            {:else if data.flocculant == "MoringaKaktus"}
                {#if data.turbidity > 2}
                    Dried and ground cactus clatodes can support flocculation with Moringa and increase flocculation activity.
                    A combination of the two flocculants is particularly suitable for low to medium turbidity.
                {:else}
                    Based on the indication of turbidity, a dose of {50 * data.turbidity} mg/l Moringa flocculant should be sufficient.
                    The amount corresponds to about {data.turbidity / 4} Moringa seed per liter of water.
                    In addition, about 50 mg/l of Cactus flocculant should be added to increase flocculation activity.
                {/if}
            {:else if data.flocculant == "Kaktus"}
                {#if data.turbidity < 3}
                    Dried and ground cactus clatodes are an effective flocculant only when turbidity is high. 
                {:else}
                    Based on the indication of turbidity, a dose of 100 mg/l flocculant should be sufficient.
                {/if}
            {/if}
        </Content>
    </Paper>
</div>