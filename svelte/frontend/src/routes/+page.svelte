<script lang="ts">
	import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";

    let advanced: boolean;
    advanced_view.subscribe(value => {
		advanced = value;
    })
</script>

<hgroup>
    <h1>Welcome</h1>
    <h2>This is the online tool for automated conceptual design of sustainable drinking water treatment plants from low-tech.<h2>
</hgroup>
<p>Based on simple input parameters, different treatment methods can be selected and combined to produce the cleanest drinking water possible.
    This online tool focuses exclusively on low-tech methods in order to provide as many people as possible with access to clean water by the simplest means.</p>

<div class="grid">
    <a href="/analysis" role="button">Start Analysis</a>
</div>
<br />
<div class="grid">
    <div class="container-fluid">
        <b>Currently supported treatment methods:</b>
        <ul>
            <li>Flocculation</li>
            <li>Biosand Filtration</li>
            <li>SODIS</li>
            <li>(Flouride Termination)</li>
        </ul>
    </div>
    <div class="container-fluid">
        <b>Additional treatment methods:</b>
        <ul>
            <li>boiling</li>
            <li>Chlorination</li>
            <li>membrane filtration</li>
            <li>ceramic pot filtration</li>
        </ul>
    </div>
</div>

Bullets werden noch zu wiki verlinkt!
<br />
<br />