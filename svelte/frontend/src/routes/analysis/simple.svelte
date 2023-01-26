<script lang="ts">
	import { selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Slider from "@smui/slider"
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label } from "@smui/list"
    import Checkbox from "@smui/checkbox"

    let data = {
        "turbidity": 0,
        "organic_material": false,
        "heavy_metals": false,
        "nitrate": false,
        "coliforms": false,
        "arsenic": false,
        "fluoride": false
    }

    let methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false //activated alumina adsorption
    }

    let results = ""

    function set_selected_methods() {
        selected_methods.set(methods)
    }

    function selectmethods() {
        methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false
        }
        let intro = "To reduce "
        let outro = " following concept has to be realised: "

        //problems
        let problems_list: String[] = []

        if (data.turbidity > 0) {
            problems_list.push(`<a href="/">Turbidity</a>`)
        }
        if (data.organic_material) {
            problems_list.push(`<a href="/">Organic Material</a>`)
        }
        if (data.heavy_metals) {
            problems_list.push(`<a href="/">Heavy Metals</a>`)
        }
        if (data.nitrate) {
            problems_list.push(`<a href="/">Nitrate</a>`)
        }
        if (data.coliforms) {
            problems_list.push(`<a href="/">Coliform Bacteria</a>`)
        }
        if (data.arsenic) {
            problems_list.push(`<a href="/">Arsenic</a>`)
        }
        if (data.fluoride) {
            problems_list.push(`<a href="/">Fluoride</a>`)
        }
        let problems_string = problems_list.join(", ")

        //methods
        let methods_list: String[] = []

        if (data.turbidity > 1 || data.heavy_metals) {
            methods.flocculation = true
            methods_list.push(`<a href="/">Flocculation</a>`)
        }
        if (data.turbidity == (1 || 2) || data.organic_material || data.nitrate || data.arsenic) {
            methods.bsf = true
            if (!data.arsenic) {
                methods_list.push(`<a href="/">Biosand Filtration</a>`)
            }
            else{
                methods_list.push(`<a href="/">modified Biosand Filtration</a>`)
            }
        }
        if (data.fluoride) {
            methods.aaa = true
            methods_list.push(`<a href="/">Activated Alumina Adsorption</a>`)
        }
        if (data.coliforms) {
            methods.sodis = true
            methods_list.push(`<a href="/">SODIS</a>`)
        }
        let methods_string = methods_list.join(", ")

        set_selected_methods()
        results = intro + problems_string + outro + methods_string
    }

</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1">
        <Title>Turbidity</Title>
        <Content>
            <Slider bind:value={data.turbidity} min={0} max={3} step={1} discrete style="min-width:10em"/>
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
    <Paper style="margin:1em; flex-grow:1">
        <Title>Taste or Smell</Title>
        <Content>
            <List checkList>
                <Item>
                    <Label>Earthy or Musty</Label>
                    <Meta>
                        <Checkbox bind:checked={data.organic_material} />
                    </Meta>
                </Item>
                <Item>
                    <Label>Metallic</Label>
                    <Meta>
                        <Checkbox bind:checked={data.heavy_metals} />
                    </Meta>
                </Item>
            </List>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Anomalies</Title>
        <Content>
            <List checkList>
                <Item>
                    <Label>Strong Algae Formation</Label>
                    <Meta>
                        <Checkbox bind:checked={data.nitrate} />
                    </Meta>
                </Item>
                <Item>
                    <Label>Cases of Diarrhea or Stomach Pain</Label>
                    <Meta>
                        <Checkbox bind:checked={data.coliforms} />
                    </Meta>
                </Item>
                <Item>
                    <Label>Excessive Hornification of Skin</Label>
                    <Meta>
                        <Checkbox bind:checked={data.arsenic} />
                    </Meta>
                </Item>
                <Item>
                    <Label>Discoloration of Teeth and/or frequent bone fractures</Label>
                    <Meta>
                        <Checkbox bind:checked={data.fluoride} />
                    </Meta>
                </Item>
            </List>
        </Content>
    </Paper>
</div>
<Group style="display: flex; justify-content: strech; margin-bottom:1em">
    <Button variant="unelevated" style="width: 50%; margin: auto;" on:click={selectmethods}>Analyze</Button>
</Group>
{#if results != ""}
    <div style="display:flex; margin-bottom:1em">
        <Paper style="flex-grow:1;">
            <Title>Results</Title>
            <Content>
                {@html results}
            </Content>
        </Paper>
    </div>
{/if}