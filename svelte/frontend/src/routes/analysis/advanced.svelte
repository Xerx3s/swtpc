<script lang="ts">
	import { selected_methods, show_selected_methods } from "/opt/svelte/frontend/src/stores/stores";
    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"
    import List, {Item, Meta, Label } from "@smui/list"
    import Checkbox from "@smui/checkbox"
    import Textfield from "@smui/textfield"

    let data = {
        "turbidity": 130,
        "ec": 400,
        "ph": 7.5,
        "nitrate": 0.0,
        "arsenic": 0.0,
        "iron": 0.0,
        "fluoride": 0.0,
        "tvc": 0,
        "coliforms": 0,
        "ecoli": 0
    }

    let limits = {
        "turbidity": ["NTU", 5],
        "ec": ["µS/cm", null],
        "ph": ["", 6.5, 8.5],
        "nitrate": ["mg/l", 50],
        "arsenic": ["mg/l", 0.01],
        "iron": ["mg/l", 0.3],
        "fluoride": ["mg/l", 1.5],
        "tvc": ["cfu/100ml", 0],
        "coliforms": ["1/100ml", 0],
        "ecoli": ["1/100ml", 0]
    }

    let methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false
    }

    let results = ""

    function set_selected_methods() {
        selected_methods.set(methods)
        show_selected_methods.set(true)
    }

    function selectmethods() {
        methods = {
        "flocculation": false,
        "bsf": false,
        "sodis": false,
        "aaa": false
        }
        let intro = "To reduce or adjust "
        let outro = " following concept has to be realised: "

        //problems
        let problems_list: String[] = []

        if (data.turbidity > limits.turbidity[1]) {
            problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/turbidity" target="_blank" rel="noreferrer">Turbidity</a>`)
        }
        //if (data.ph < limits.ph[1] || data.ph > limits.ph[2]) {
        //    problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/ph" target="_blank" rel="noreferrer">pH</a>`)
        //}
        if (data.nitrate > limits.nitrate[1]) {
            problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/nitrate" target="_blank" rel="noreferrer">Nitrate</a>`)
        }
        if (data.arsenic > limits.arsenic[1]) {
            problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/arsenic" target="_blank" rel="noreferrer">Arsenic</a>`)
        }
        if (data.iron > limits.iron[1]) {
            problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/iron" target="_blank" rel="noreferrer">Iron</a>`)
        }
        if (data.fluoride > limits.fluoride[1]) {
            problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/fluoride" target="_blank" rel="noreferrer">Fluoride</a>`)
        }
        if (data.tvc > limits.tvc[1]) {
            problems_list.push(`tvc`)
        }
        if (data.coliforms > limits.coliforms[1]) {
            problems_list.push(`<a href="http://192.168.178.69:3000/en/contaminants/coliform-bacteria" target="_blank" rel="noreferrer">Coliform Bacteria</a>`)
        }
        if (data.ecoli > limits.ecoli[1]) {
            problems_list.push(`ecoli`)
        }
        let problems_string = problems_list.join(", ")

        //methods
        let methods_list: String[] = []

        if (data.turbidity > limits.turbidity[1] || data.iron > limits.iron[1]) {
            methods.flocculation = true
            methods_list.push(`<a href="http://192.168.178.69:3000/en/methods/flocculation" target="_blank" rel="noreferrer">Flocculation</a>`)
        }
        if (data.turbidity > (20 * limits.turbidity[1]) || data.tvc > limits.tvc[1] || data.nitrate > limits.nitrate[1] || data.arsenic > limits.arsenic[1]) {
            methods.bsf = true
            if (data.arsenic < limits.arsenic[1]) {
                methods_list.push(`<a href="http://192.168.178.69:3000/en/methods/biosand-filtration" target="_blank" rel="noreferrer">Biosand Filtration</a>`)
            }
            else{
                methods_list.push(`<a href="http://192.168.178.69:3000/en/methods/biosand-filtration" target="_blank" rel="noreferrer">modified Biosand Filtration</a>`)
            }
        }
        if (data.fluoride > limits.fluoride[1]) {
            methods.aaa = true
            methods_list.push(`<a href="http://192.168.178.69:3000/en/methods/aaa" target="_blank" rel="noreferrer">Activated Alumina Adsorption</a>`)
        }
        if (data.tvc > limits.tvc[1] || data.coliforms > limits.coliforms[1] || data.ecoli > limits.ecoli[1]) {
            methods.sodis = true
            methods_list.push(`<a href="http://192.168.178.69:3000/en/methods/sodis" target="_blank" rel="noreferrer">SODIS</a>`)
        }
        let methods_string = methods_list.join(", ")

        set_selected_methods()
        if (methods.aaa || methods.bsf || methods.flocculation || methods.sodis) {
            results = intro + problems_string + outro + methods_string
        } else {
            results = "Please select matching inputs first."
        }

    }
</script>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="margin:1em; flex-grow:1">
        <Title>Indicator Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <Textfield type="number" bind:value={data.turbidity} label="Turbidity" suffix="NTU"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.ph} label="pH-Value" suffix=""  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" bind:value={data.ec} label="Electrical Conductivity" suffix="µS/cm"  style="flex-grow:1; margin-bottom:0.5em"/>
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Anorganic Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <Textfield type="number" input$step="0.1" bind:value={data.nitrate} label="Nitrate" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.01" bind:value={data.arsenic} label="Arsenic" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.iron} label="Iron" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <Textfield type="number" input$step="0.1" bind:value={data.fluoride} label="Flouride" suffix="mg/l"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
        </Content>
    </Paper>
    <Paper style="margin:1em; flex-grow:1">
        <Title>Organic Parameters</Title>
        <Content style="display:flex; flex-direction:column">
            <!--<Textfield type="number" bind:value={data.tvc} label="Total Viable Count" suffix="cfu/ml"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />-->
            <Textfield type="number" bind:value={data.coliforms} label="Coliform Bacteria" suffix="1/100ml"  style="flex-grow:1; margin-bottom:0.5em"/>
            <br />
            <!--<Textfield type="number" bind:value={data.ecoli} label="E.Coli" suffix="1/100ml"  style="flex-grow:1; margin-bottom:0.5em"/>-->
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