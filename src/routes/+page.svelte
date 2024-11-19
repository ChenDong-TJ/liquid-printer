<script>
	import Canvas from './Canvas.svelte'
	
	const color = '#000000'
	const background = '#FFFFFF'
</script>

<main>
	<Canvas {color} {background} />
</main>

<style>	
	:global(body) {
		margin: 0;
		padding: 0;
		height: 100vh;
		display: flex;
		justify-content: center;
		align-items: center;
		background: #1a1a1a;
		overflow: hidden;
	}
	
	main {
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>