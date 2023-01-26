<script lang="ts">
    import SvelteMarkdown from "svelte-markdown"
    import { marked } from "marked"

    let result = ""

    async function getArticle() {
        let url = "http://localhost:1337/api/articles/1"

        let res = await fetch(url, {
            mode: "cors",
            method: "GET",
            headers: {
                'Content-Type': 'application/json'
            }
        })
        
        let res2 = await res.json()
        result = marked.parse(res2.data.attributes.main)
    }

    getArticle()
</script>
<div style="margin:1em">
    {@html result}
</div>