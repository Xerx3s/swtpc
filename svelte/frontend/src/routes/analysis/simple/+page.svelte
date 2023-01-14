<script>
    let data = {
        "turbidity": 0,
        "organic_material": false,
        "heavy_metals": false,
        "nitrate": false,
        "coliformes": false,
        "arsenic": false
        //Methode, um Flouride zu identifizieren?
    }

</script>

<div>
    Input Parameters
    <div class="grid">
        <article>
            <header>Turbidity</header>
            <input type="range" min="0" max="3" bind:value={data.turbidity}>
            {#if data.turbidity === 0}
                none
            {:else if data.turbidity === 1}
                low
            {:else if data.turbidity === 2}
                medium
            {:else if data.turbidity === 3}
                high
            {/if}
        </article>
        <article>
            <header>Taste or Smell</header>
            <label><input type="checkbox" bind:checked={data.organic_material}> Earthy or Musty</label>
            <label><input type="checkbox" bind:checked={data.heavy_metals}> Metallic</label>
            
        </article>
        <article>
            <header>Anomalies</header>
            <label><input type="checkbox" bind:checked={data.nitrate}> Strong Algae Formation</label>
            <label><input type="checkbox" bind:checked={data.coliformes}> Cases of Diarrhea or Stomach Pain</label>
            <label><input type="checkbox" bind:checked={data.arsenic}> Excessive Hornification of Skin</label>
        </article>
    </div>
</div>