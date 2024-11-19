<script>
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();
	
	export let colors = []
	export let paletteColor
	export let background = '#fff'
</script>

<section>
	<div>
		{#each colors as color}
		<button 
			class:active={paletteColor === color}
			on:click={() => {
				dispatch('color', { color })
				paletteColor = color
			}}
			style:background={color}>
			<span class="visually-hidden">
				Select the color {color}
			</span>
		</button>
		{/each}
	</div>
	
	<button 
		class="eraser"
		class:active={paletteColor === background}
		on:click={() => {
			dispatch('color', { color: background })
			paletteColor = background
		}}>
		<span class="visually-hidden">
			Eraser
		</span>
		🧹
	</button>
</section>

<style>
	section {
		background: #2a2a2a;
		padding: 0.5rem;
		display: flex;
		align-items: center;
		gap: 0 1rem;
		height: 60px;
		box-sizing: border-box;
	}
	
	section > div {
		flex-grow: 1;
		display: flex;
		gap: 0.5rem;
		overflow-x: auto;
		padding: 0.25rem;
	}
	
	button {
		width: 2rem;
		height: 2rem;
		border-radius: 4px;
		cursor: pointer;
		border: 2px solid transparent;
		padding: 0;
		transition: transform 0.1s;
	}
	
	button:hover {
		transform: scale(1.1);
	}
	
	button.active {
		border-color: #fff;
		box-shadow: 0 0 10px rgba(255,255,255,0.5);
	}
	
	.eraser {
		background: #fff;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 1.2rem;
	}
	
	div::-webkit-scrollbar {
		height: 0.25rem;
	}

	div::-webkit-scrollbar-track {
		background: #1a1a1a;
		border-radius: 0.125rem;
	}

	div::-webkit-scrollbar-thumb {
		background: #4a4a4a;
		border-radius: 0.125rem;
	}
	
	div::-webkit-scrollbar-thumb:hover {
		background: #5a5a5a;
	}
</style>