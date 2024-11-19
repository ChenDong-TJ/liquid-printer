<script>
	import { onMount } from 'svelte'
	
	export let color = '#000'
	export let background = '#fff'
	
	let canvas
	let context
	let isDrawing = false
	const CANVAS_SIZE = 600
	const PIXEL_SIZE = 20 // 30x30 pixels (600/20)
	
	onMount(() => {
		context = canvas.getContext('2d')
		canvas.width = CANVAS_SIZE
		canvas.height = CANVAS_SIZE
		
		context.fillStyle = background
		context.fillRect(0, 0, canvas.width, canvas.height)
	})
	
	const drawPixel = (x, y) => {
		const pixelX = Math.floor(x / PIXEL_SIZE) * PIXEL_SIZE
		const pixelY = Math.floor(y / PIXEL_SIZE) * PIXEL_SIZE
		
		if (pixelX >= canvas.width || pixelY >= canvas.height || pixelX < 0 || pixelY < 0) return
		
		context.fillStyle = color
		context.fillRect(pixelX, pixelY, PIXEL_SIZE, PIXEL_SIZE)
	}
	
	const handleStart = (e) => {
		isDrawing = true
		const { offsetX, offsetY } = getCoordinates(e)
		drawPixel(offsetX, offsetY)
	}
	
	const handleMove = (e) => {
		if (!isDrawing) return
		const { offsetX, offsetY } = getCoordinates(e)
		drawPixel(offsetX, offsetY)
	}
	
	const handleEnd = () => {
		isDrawing = false
	}
	
	const getCoordinates = (e) => {
		if (e.type.startsWith('touch')) {
			const rect = canvas.getBoundingClientRect()
			const touch = e.touches[0]
			const scale = canvas.width / rect.width
			return {
				offsetX: (touch.clientX - rect.left) * scale,
				offsetY: (touch.clientY - rect.top) * scale
			}
		}
		const rect = canvas.getBoundingClientRect()
		const scale = canvas.width / rect.width
		return {
			offsetX: e.offsetX * scale,
			offsetY: e.offsetY * scale
		}
	}

	const saveImage = async () => {
		const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
		const link = document.createElement('a')
		link.download = `pixel-art-${timestamp}.png`
		link.href = canvas.toDataURL()
		link.click()

		// 添加对后端的调用
		try {
			const response = await fetch('/api/process-image', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					imageData: canvas.toDataURL().split(',')[1], // 移除前缀
					timestamp: timestamp
				})
			})
			
			if (!response.ok) {
				throw new Error('后端处理失败')
			}
			
			const result = await response.json()
			console.log('Python脚本执行结果:', result)
		} catch (error) {
			console.error('调用后端出错:', error)
			alert('处理图片时出错')
		}
	}
</script>

<div class="canvas-container">
	<canvas
		bind:this={canvas}
		style:background
		on:mousedown={handleStart}
		on:mousemove={handleMove}
		on:mouseup={handleEnd}
		on:mouseleave={handleEnd}
		on:touchstart|preventDefault={handleStart}
		on:touchmove|preventDefault={handleMove}
		on:touchend|preventDefault={handleEnd}
	/>
	<button class="save-button" on:click={saveImage}>Save Image</button>
</div>

<style>
	.canvas-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
	}
	
	canvas {
		image-rendering: pixelated;
		image-rendering: crisp-edges;
		cursor: crosshair;
		width: 600px;
		height: 600px;
		box-shadow: 0 0 20px rgba(0,0,0,0.3);
	}

	.save-button {
		padding: 0.5rem 1rem;
		background: #4CAF50;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 1rem;
	}

	.save-button:hover {
		background: #45a049;
	}
</style>