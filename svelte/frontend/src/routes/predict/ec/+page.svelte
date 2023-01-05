<script lang="ts">
    let json = {"initial_EC": 400, "floc_concentration": 20, "floc_saline_Molarity": 0.3, "floc_dose": 200}
    let pred_fEC = 0
    let result = "testing"

    async function doPost() {
        let url = "http://localhost:3001/ec/"

        console.log(JSON.stringify(json))
        const res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
        }) //hier weitermachen... json wie korrekt übergeben?
        
        console.log(JSON.stringify(res))
        const json2 = await res.json()
        
        console.log(json2)
        result = JSON.stringify(json2)
        pred_fEC = json2["final_EC"]
        console.log(pred_fEC)
        }
</script>

<form>
    <div class="container-fluid">
        <label for="initial_EC">
            <strong>Electrical conductivity</strong> (in µS/cm)
            <input type="number" id="initial_EC" name="initial_EC" placeholder="400" bind:value={json.initial_EC} required>
        </label>
        <label for="floc_concenctration">
            <strong>Flocculant base solution concentration</strong> (in g/l)
            <input type="number" id="floc_concenctration" name="floc_concenctration" placeholder="20" bind:value={json.floc_concentration} required>
        </label>
        <label for="floc_saline_Molarity">
            <strong>saline molarity of base solution</strong> (in mol/l)
            <input type="number" step="0.1" id="floc_saline_Molarity" name="floc_saline_Molarity" placeholder="0,3" bind:value={json.floc_saline_Molarity} required>
        </label>
        <label for="floc_dose">
            <strong>applied flocculant dosage</strong> (in mg/l)
            <input type="number" id="floc_dose" name="floc_dose" placeholder="200" bind:value={json.floc_dose} required>
        </label>

        <button type="submit" on:click={doPost}>Senden</button>

        <label for="pred_fEC">
            <strong>predicted final EC</strong> (in µS/cm)
            <input type="number" id="pred_fEC" name="pred_fEC" placeholder="0" bind:value={pred_fEC}>
        </label>
    </div>
</form>

<p>{result}</p>