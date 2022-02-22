<script setup>
    import HomeView from '@/views/HomeView.vue';
    import { ref, onMounted } from 'vue';

    let str = ref("");

    onMounted(() => {
        str.value = process.env.VUE_APP_TEST;
    });
</script>

<template>
	<HomeView />
	<p>{{ str }}</p>
</template>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }
</style>
