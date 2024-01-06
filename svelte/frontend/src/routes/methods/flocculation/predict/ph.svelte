<script lang="ts">
    let data = {
        "initial_pH": 8.5,
        "floc_concentration": 20,
        "floc_saline_Molarity": 0.3,
        "floc_dose": 200,
        "print_assessment": false,
        "load_pipe": false}
    let pred_fpH = 0

    async function doPost() {
        let url = "https://api.sustainable-water.de/ph/"

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
</script>

<form>
    <div class="container-fluid">
        <strong>Options:</strong><br/>
        <div class="grid">
            <label for="print_assessment">
                print assessment of pipe
                <input type="checkbox" id="print_assessment" name="print_assessment" bind:checked={data.print_assessment}>
            </label>
            <label for="load_pipe">
                load pipe
                <input type="checkbox" id="load_pipe" name="load_pipe" bind:checked={data.load_pipe} disabled>
            </label>
        </div>
    </div>
    <div class="container-fluid">
        <label for="initial_pH">
            <strong>pH value</strong>
            <input type="number" id="initial_pH" name="initial_pH" bind:value={data.initial_pH} step="0.1" required>
        </label>
        <label for="floc_concenctration">
            <strong>Flocculant base solution concentration</strong> (in g/l)
            <input type="number" id="floc_concenctration" name="floc_concenctration" bind:value={data.floc_concentration} required>
        </label>
        <label for="floc_saline_Molarity">
            <strong>saline molarity of base solution</strong> (in mol/l)
            <input type="number" step="0.1" id="floc_saline_Molarity" name="floc_saline_Molarity" bind:value={data.floc_saline_Molarity} required>
        </label>
        <label for="floc_dose">
            <strong>applied flocculant dosage</strong> (in mg/l)
            <input type="number" id="floc_dose" name="floc_dose" bind:value={data.floc_dose} required>
        </label>

        <button type="submit" on:click={doPost}>Senden</button>

        <label for="pred_fpH">
            <strong>predicted final pH</strong>
            <input type="number" id="pred_fpH" name="pred_fpH" placeholder="0" bind:value={pred_fpH}>
        </label>
    </div>
</form>