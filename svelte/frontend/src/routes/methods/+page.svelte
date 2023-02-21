<script lang="ts">
    import Card, { Content, PrimaryAction, Media, MediaContent, Actions, ActionButtons, ActionIcons } from '@smui/card';
    import Button, { Label } from '@smui/button';

    let methods = [
        {
            id: "flocculation",
            name: "Flocculation",
            image: "card-media-flocculation",
            description: "Treatment Process to remove small particles and colloides from water."
        },
        { 
            id: "bsf",
            name: "Bio-Sand Filtration",
            image: "card-media-bsf",
            description: "Treatment Process to reduce pathogens and nitrate concentration in water."
        },
        { 
            id: "sodis",
            name: "SODIS",
            image: "card-media-sodis",
            description: "Treatment Process reduce pathogens in water."
        },
        {
            id: "aaa",
            name: "Activated Alumina Adsorption",
            image: "card-media-aaa",
            description: "Treatment Process to remove fluoride concentration in water."
        }
    ]

</script>

<style>
    * :global(.card-media-flocculation) {
      background-image: url("/flocculation.png");
    }
    * :global(.card-media-bsf) {
      background-image: url("https://practicalsurvivalist.com/wp-content/uploads/2016/10/bio-sand-water-purifier-700x394.jpg");
    }
    * :global(.card-media-sodis) {
      background-image: url("https://upload.wikimedia.org/wikipedia/commons/6/67/Indonesia-sodis-gross.jpg");
    }
    * :global(.card-media-aaa) {
      background-image: url("https://upload.wikimedia.org/wikipedia/commons/c/c8/Active_Al2O3.jpg");
    }
</style>

<div style="display:flex; flex-wrap:wrap; justify-content:center; align-items:stretch">
    {#each methods as method}
        <Card style="margin:1em; flex-grow:1; justify-content:flex-end">
            <Media class={method.image} aspectRatio="16x9">
            <MediaContent>
                <div
                style="color: black; position: absolute; bottom: 16px; left: 16px;"
                >
                <h2 style="margin: 0; color: black; text-shadow: 0 0 3px white, 0 0 5px grey">
                    {method.name}
                </h2>
                </div>
            </MediaContent>
            </Media>
            <Content class="mdc-typography--body2">
                {method.description}
            </Content>
            <Actions>
            <ActionButtons>
                <Button href="/methods/{method.id}/predict">
                <Label>Predict</Label>
                </Button>
                <Button href="/methods/{method.id}/optimize">
                <Label>Optimize</Label>
                </Button>
            </ActionButtons>
            </Actions>
        </Card>
    {/each}
</div>