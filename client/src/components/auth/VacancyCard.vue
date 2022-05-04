<script setup>  
    import { ref } from 'vue';

    const { vacancy = {} } = defineProps(['vacancy']);
    const { jobTitle, position, description } = vacancy;

</script>

<template>
    <div class='card'>
        <div class='top'>
        </div>
        <div class='mid'>
            <div class='company-name'>{{ jobTitle }}</div>
        </div>
        <div class='description'>
            <p class='job-title'>{{ position }}</p>

            <p>{{ description }}</p>
        </div>
    
    </div>
</template>

<style scoped>

    .card {
        background-color: white;
        color: #08415c;
        font-weight: normal;
        height: 250px;
        width: 200px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 20px 0;
        align-items: center;
        text-align: left;
        justify-content: space-between;
        margin: 5px;
    }

    .description{
        padding: 0 20px;
        font-size: 10px;
    }

    .mid {
        background-color: #cc2936;
        color: white;
        text-align: center;
        padding:0px;

    }

    .top{
        padding: 0px;
    }


</style>