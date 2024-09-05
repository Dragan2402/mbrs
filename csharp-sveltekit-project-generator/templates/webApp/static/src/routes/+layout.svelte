<script>
	import '../app.css';
</script>

<div class="app">
	<slot />
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		height: 100vh;
	}
</style>
