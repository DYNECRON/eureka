<script lang="ts">
	import Results from "$lib/components/results.svelte";
	import Searchbar from "$lib/components/search-bar.svelte";
</script>

<div class="container max-w-[1024px] space-y-4 py-20">
	<h1
		class="bg-gradient-to-b from-white to-white/20 bg-clip-text text-center text-7xl font-bold tracking-tighter text-transparent"
	>
		Eureka
	</h1>
	<Searchbar />
	<Results />
</div>
