<script lang="ts">
	import { advanced_view } from "/opt/svelte/frontend/src/stores/stores";

    import Button, { Group } from "@smui/button"
    import Paper, { Title, Subtitle, Content } from "@smui/paper"

    let advanced: boolean;
    advanced_view.subscribe(value => {
		advanced = value;
    })
</script>

<h1>Welcome</h1>
<p>This is the online tool for automated conceptual design of sustainable drinking water treatment plants from low-tech.</p>
<p>Based on simple input parameters, different treatment methods can be selected and combined to produce the cleanest drinking water possible.
    This online tool focuses exclusively on low-tech methods in order to provide as many people as possible with access to clean water by the simplest means.</p>

<Group style="display: flex; justify-content: strech;">
    <Button variant="unelevated" style="width: 50%; margin: auto;" href="/analysis">Start Analysis</Button>
</Group>

<div style="display:flex;">
    <div class="paper-container" style="width:50%; padding:1em">
        <Paper>
            <Title>Currently supported treatment methods</Title>
            <Content>
                <ul>
                    <li>Flocculation</li>
                    <li>Biosand Filtration</li>
                    <li>SODIS</li>
                    <li>(Flouride Termination)</li>
                </ul>
            </Content>
        </Paper>
    </div>
    <div class="paper-container" style="width:50%; padding:1em">
        <Paper>
            <Title>Additional treatment methods</Title>
            <Content>
                <ul>
                    <li>Boiling</li>
                    <li>Chlorination</li>
                    <li>Membrane Filtration</li>
                    <li>Ceramic Pot Filtration</li>
                </ul>
            </Content>
        </Paper>
    </div>
</div>

Bullets werden noch zu wiki verlinkt!
<br />
<br />