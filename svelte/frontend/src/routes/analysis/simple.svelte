<script lang="ts">
	import { selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Card from "@smui/card"
    import Slider from "@smui/slider"
    import Button from "@smui/button"

    let data = {
        "turbidity": 0,
        "organic_material": false,
        "heavy_metals": false,
        "nitrate": false,
        "coliformes": false,
        "arsenic": false
        //Methode, um Flouride zu identifizieren?
    }

    let methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false
    }

    let results = ""

    function set_selected_methods() {
        
        selected_methods.set(methods)
    }

    function selectmethods() {
        methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false
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
        if (data.coliformes) {
            problems_list.push(`<a href="/">Coliformes</a>`)
        }
        if (data.arsenic) {
            problems_list.push(`<a href="/">Arsenic</a>`)
        }
        let problems_string = problems_list.join(", ")

        //methods
        let methods_list: String[] = []

        if (data.turbidity > 1 || data.heavy_metals) {
            methods.flocculation = true
            methods_list.push(`<a href="/">Flocculation</a>`)
        }
        if (data.turbidity == (1 || 2)|| data.organic_material || data.nitrate || data.arsenic) {
            methods.bsf = true
            if (!data.arsenic) {
                methods_list.push(`<a href="/">Biosand Filtration</a>`)
            }
            else{
                methods_list.push(`<a href="/">modified Biosand Filtration</a>`)
            }
        }
        if (data.coliformes) {
            methods.sodis = true
            methods_list.push(`<a href="/">SODIS</a>`)
        }
        let methods_string = methods_list.join(", ")


        results = intro + problems_string + outro + methods_string
    }

</script>

<div>
    <div class="card-display">
        <div class="card-container">
            <Card padded>
                Turbidity
                <Slider bind:value={data.turbidity} min={0} max={3} step={1} discrete />
                {#if data.turbidity === 0}
                    none
                {:else if data.turbidity === 1}
                    low
                {:else if data.turbidity === 2}
                    medium
                {:else if data.turbidity === 3}
                    high
                {/if}
            </Card>
        </div>
        <br />
        <div class="card-container">
            <Card padded>
                <header>Taste or Smell</header>
                <label><input type="checkbox" bind:checked={data.organic_material}> Earthy or Musty</label>
                <label><input type="checkbox" bind:checked={data.heavy_metals}> Metallic</label>
            </Card>
        </div>
        <br />
        <div class="card-container">
            <Card padded>
                <header>Anomalies</header>
                <label><input type="checkbox" bind:checked={data.nitrate}> Strong Algae Formation</label>
                <label><input type="checkbox" bind:checked={data.coliformes}> Cases of Diarrhea or Stomach Pain</label>
                <label><input type="checkbox" bind:checked={data.arsenic}> Excessive Hornification of Skin</label>
            </Card>
            </div>
    </div>
    <Button on:click={selectmethods}>Analyze</Button>
    {#if results != ""}
        <div class="card-display">
            <div class="card-container">
                <Card padded>
                    <header>Results</header>
                    {@html results}
                </Card>
            </div>
        </div>
    {/if}
</div>