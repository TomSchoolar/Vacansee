<template>
    <div id="navbar">
        <div id="title">TINDEED</div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    
    let page = ref("");
    console.log(page);
</script>

<style>
    body {
        margin: 0;
    }

    #navbar {
        width: 100vw;
        height: 70px;
        margin-bottom: 30px;
        padding: 0 25%;
        display: flex;
        align-items: center;
        color: #ffffff;
        background: #08415c;
    }

    #title {
        font-weight: bold;
        font-size: 20px;
    }
</style>