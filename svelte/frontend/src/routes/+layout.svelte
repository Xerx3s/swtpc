<script lang="ts">
    import "@picocss/pico"
</script>

<header>
    <nav class="container-fluid">
        <ul>
            <li>swtpc</li>
        </ul>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/">One</a></li>
            <li><a href="/">Two</a></li>
            
        </ul>
    </nav>
</header>

<main class="container">
    <slot />
</main>

<footer class="container-fluid">
    <div class="grid">
        <a href="/about" role="button" class="outline">About</a>
        <a href="/analytic/simple" role="button" class="outline">simple</a>
        <a href="/predict/ec" role="button" class="outline">predict EC</a>
    </div>
</footer>