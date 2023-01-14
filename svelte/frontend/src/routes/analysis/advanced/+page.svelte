<script lang="ts">
    let data = {
        "turbidity": 130,
        "ec": 400,
        "ph": 8.5,
        "nitrate": 0.0,
        "arsenic": 0.0,
        "iron": 0.0,
        "flouride": 0.0, //Methode, um Flouride zu identifizieren
        "tvc": 0,
        "coliforms": 0,
        "ecoli": 0
    }

    function selectmethods() {
        return null
    }
</script>

<div>
    Input Parameters
    <div class="grid">
        <article>
            <header>Indicator Parameters</header>
            <label>
                Turbidity (in NTU)
                <input type="number" step=1 bind:value={data.turbidity}/>
            </label>
            <label>
                pH-Value ( )
                <input type="number" step=0.1 bind:value={data.ph}/>
            </label>
            <label>
                EC (in µS/cm)
                <input type="number" step=1 bind:value={data.ec}/>
            </label>
        </article>
        <article>
            <header>Anorganic Parameters</header>
            <label>
                Nitrate (in mg/l)
                <input type="number" step=0.1 bind:value={data.nitrate}/>
            </label>
            <label>
                Arsenic (in mg/l)
                <input type="number" step=0.1 bind:value={data.arsenic}/>
            </label>
            <label>
                Iron (in mg/l)
                <input type="number" step=0.1 bind:value={data.iron}/>
            </label>
            <label>
                Flouride (in mg/l)
                <input type="number" step=0.1 bind:value={data.flouride}/>
            </label>
        </article>
        <article>
            <header>Organic Parameters</header>
            <label>
                Total Viable Count (in cfu/ml)
                <input type="number" step=0.1 bind:value={data.tvc}/>
            </label>
            <label>
                Coliforms (in 1/100ml)
                <input type="number" step=0.1 bind:value={data.coliforms}/>
            </label>
            <label>
                E.Coli (in 1/100ml)
                <input type="number" step=0.1 bind:value={data.ecoli}/>
            </label>
        </article>
    </div>
    <button on:click={selectmethods}>Analyze</button>
</div>