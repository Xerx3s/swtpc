<script lang="ts">
    let data = {
        "surface_water": "model suspension",
        "initial_pH": 8.5,
        "initial_EC": 400,
        "initial_turbidity": 130,
        "flocculant": "Moringa",
        "floc_concentration": 20,
        "floc_saline_Molarity": 0.3,
        "floc_dose": 200,
        "floc_cactus_share": 0,
        "stirring_speed_coagulation_phase": 100,
        "duration_coagulation_phase": 1,
        "stirring_speed_flocculation_phase": 20,
        "duration_flocculation_phase": 15,
        "duration_sedimentation_phase": 45,
        "print_assessment": false,
        "load_pipe": false}
    let pred_ftur = 0.0
    let pred_fpH = 0.0
    let pred_fEC = 0.0
    let flocculants: string[] = []

    get_flocculants()

    async function get_flocculants() {
        let url = "http://localhost:3001/floc/"

        let res = await fetch(url, {
            mode: "cors",
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        let res2 = await res.json()

        flocculants = []
        res2.forEach((element: string[]) => {
            //flocculants.push({id: element[0], name: element[0]})
            flocculants.push(element[0])
        });

        console.log(flocculants)
        return flocculants
    }

    async function predict_tur() {
        let url = "http://localhost:3001/tur/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()

        pred_ftur = res2["final_turbidity"]
    }

    async function predict_ph() {
        let url = "http://localhost:3001/ph/"

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

    async function predict_ec() {
        let url = "http://localhost:3001/ec/"

        let res = await fetch(url, {
            mode: "cors",
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        let res2 = await res.json()
        
        pred_fEC = res2["final_EC"]
        }
    
    async function doPost() {
        predict_tur()
        predict_ph()
        predict_ec()
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
        <label for="initial_turbidity">
            <strong>Turbidity</strong> (in NTU)
            <input type="number" id="initial_EC" name="initial_EC" bind:value={data.initial_turbidity} required>
        </label>
        <label for="initial_pH">
            <strong>pH value</strong>
            <input type="number" id="initial_pH" name="initial_pH" bind:value={data.initial_pH} step="0.1" required>
        </label>
        <label for="initial_EC">
            <strong>Electrical conductivity</strong> (in µS/cm)
            <input type="number" id="initial_EC" name="initial_EC" bind:value={data.initial_EC} required>
        </label>
        <label for="flocculant">
            <strong>Flocculant</strong>
            <select id="flocculant" name="flocculant" bind:value={data.flocculant}>
                <option value="" disabled selected>Select one</option>
                {#each flocculants as flocculant}
                    <option value="{flocculant}">{flocculant}</option>
                {/each}
            </select>
        </label>
        <label for="floc_concentration">
            <strong>Flocculant base solution concentration</strong> (in g/l)
            <input type="number" id="floc_concentration" name="floc_concentration" bind:value={data.floc_concentration} required>
        </label>
        <label for="floc_saline_Molarity">
            <strong>saline molarity of base solution</strong> (in mol/l)
            <input type="number" step="0.1" id="floc_saline_Molarity" name="floc_saline_Molarity" bind:value={data.floc_saline_Molarity} required>
        </label>
        <label for="floc_dose">
            <strong>applied flocculant dosage</strong> (in mg/l)
            <input type="number" id="floc_dose" name="floc_dose" bind:value={data.floc_dose} required>
        </label>
        <label for="floc_cactus_share">
            <strong>flocculant cactus share</strong> (in %)
            <input type="number" min=0 max=100 step=1 id="floc_cactus_share" name="floc_cactus_share" bind:value={data.floc_cactus_share} required>
        </label>
        <label for="stirring_speed_coagulation_phase">
            <strong>stirring speed during coagulation phase</strong> (in rpm)
            <input type="number" id="stirring_speed_coagulation_phase" name="stirring_speed_coagulation_phase" bind:value={data.stirring_speed_coagulation_phase} required>
        </label>
        <label for="duration_coagulation_phase">
            <strong>duration of coagulation phase</strong> (in min)
            <input type="number" id="duration_coagulation_phase" name="duration_coagulation_phase" bind:value={data.duration_coagulation_phase} required>
        </label>
        <label for="stirring_speed_flocculation_phase">
            <strong>stirring speed during flocculation phase</strong> (in rpm)
            <input type="number" id="stirring_speed_flocculation_phase" name="stirring_speed_flocculation_phase" bind:value={data.stirring_speed_flocculation_phase} required>
        </label>
        <label for="duration_flocculation_phase">
            <strong>duration of flocculation phase</strong> (in min)
            <input type="number" id="duration_flocculation_phase" name="duration_flocculation_phase" bind:value={data.duration_flocculation_phase} required>
        </label>
        <label for="duration_sedimentation_phase">
            <strong>duration of sedimentation phase</strong> (in min)
            <input type="number" id="duration_sedimentation_phase" name="duration_sedimentation_phase" bind:value={data.duration_sedimentation_phase} required>
        </label>

        <button type="submit" on:click={doPost}>Senden</button>

        <label for="pred_ftur">
            <strong>predicted final turbidity</strong> (in NTU)
            <input type="number" id="pred_ftur" name="pred_ftur" bind:value={pred_ftur} readonly>
        </label>

        <label for="pred_fpH">
            <strong>predicted final pH</strong>
            <input type="number" id="pred_fpH" name="pred_fpH" bind:value={pred_fpH} readonly>
        </label>

        <label for="pred_fEC">
            <strong>predicted final EC</strong> (in µS/cm)
            <input type="number" id="pred_fEC" name="pred_fEC" bind:value={pred_fEC} readonly>
        </label>
    </div>
</form>