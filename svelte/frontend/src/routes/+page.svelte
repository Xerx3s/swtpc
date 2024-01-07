<script lang="ts">
	import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";

    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"

    let advanced: boolean;
    advanced_view.subscribe(value => {
		advanced = value;
    })
</script>

<h1 style="font-size:8vw;">Welcome</h1>
<p>This is the online tool for automated conceptual design of sustainable drinking water treatment plants from low-tech.</p>
<p>Based on simple input parameters, various treatment methods are selected and combined to produce the cleanest drinking water possible.
    This online tool focuses exclusively on low-tech methods in order to provide as many people as possible with access to clean water by the simplest means.</p>

<Group style="display: flex; justify-content: strech;">
    <Button variant="unelevated" style="width: 50%; margin: auto;" href="/analysis">Start Analysis</Button>
</Group>

<p>
    For a more accurate result, use the switch in the Top Navigation Bar.
    If you set it to "Advanced View", you will get access to more sophisticated ways to perform the analysis.
    However, this also requires more precise input parameters. <br /> <br />
    A <a href="https://wiki.sustainable-water.de/" target="_blank" rel="noreferrer">knowledge base</a> is available for more background information on the individual technologies.
</p>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    <Paper style="flex-grow:1; margin:1em">
        <Title>Currently supported treatment methods</Title>
        <Content>
            <ul>
                <li><a href="https://wiki.sustainable-water.de/en/methods/aaa" target="_blank" rel="noreferrer">Activated Alumina Adsorption</a></li>
                <li><a href="https://wiki.sustainable-water.de/en/methods/biosand-filtration" target="_blank" rel="noreferrer">Biosand Filtration</a></li>
                <li><a href="https://wiki.sustainable-water.de/en/methods/flocculation" target="_blank" rel="noreferrer">Flocculation</a></li>
                <li><a href="https://wiki.sustainable-water.de/en/methods/sodis" target="_blank" rel="noreferrer">SODIS</a></li>
            </ul>
        </Content>
    </Paper>
    <Paper style="flex-grow:1; margin:1em">
        <Title>Additional treatment methods</Title>
        <Content>
            <ul>
                <li><a href="https://wiki.sustainable-water.de/en/methods/boiling" target="_blank" rel="noreferrer">Boiling</a></li>
                <li><a href="https://wiki.sustainable-water.de/en/methods/ceramic-pot-filtration" target="_blank" rel="noreferrer">Ceramic Pot Filtration</a></li>
                <li><a href="https://wiki.sustainable-water.de/en/methods/chlorination" target="_blank" rel="noreferrer">Chlorination</a></li>
                <li><a href="https://wiki.sustainable-water.de/en/methods/membrane-filtration" target="_blank" rel="noreferrer">Membrane Filtration</a></li>
            </ul>
        </Content>
    </Paper>
</div>

<p>
    <b>Disclaimer:</b> <br />
    This website does not store any user data.
    All data entered is only used for analysis and then immediately discarded. <br />
    When using external APIs, care has been taken to ensure that they are handled in an equally compliant manner.
    The privacy policies of <a href="https://openweather.co.uk/privacy-policy" target="_blank" rel="noreferrer">OpenWeatherMap</a> and <a href="https://www.fossgis.de/datenschutzerkl%C3%A4rung/" target="_blank" rel="noreferrer">OpenStreetMap</a> can be viewed on the respective official pages.
    <br /> <br />
    The content of this page runs under the <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noreferrer">Creative Commons Attribution-ShareAlike License</a> and may therefore be remixed, adapted and build upon even for commercial purposes.
    However projects based on this work must give credit to it and carry the same license under the identical terms.
    This license is often compared to “copyleft” free and open source software licenses.
    All new works will carry the same license, so any derivatives will also allow commercial use.
</p>