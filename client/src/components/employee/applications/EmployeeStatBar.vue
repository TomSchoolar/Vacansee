<script setup>
    const props = defineProps(['stats']);
    
    const labels = {
        total: 'Total Applications',
        new: 'Applications Pending',
        matches: 'Matches'
    };
</script>



<template>
    <div class='stat-bar'>
        <div class='stat-boxes'>
            <div class='stat-box' v-for='[key, value] of Object.entries(stats)' :key='key'>
                <h1 class='stat-title'>{{ labels[key] }}:</h1>
                <h1 class='stat'>{{ value }}</h1>
            </div>
        </div>
    </div>
    
</template>



<style scoped>
    .stat {
        color: var(--red);
        font-size: 50px;
        margin: 0;
    }

    .stat-bar {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .stat-boxes {
        width: 100%;
        display: flex;
        justify-content: space-evenly;
        margin: 15px 0 30px 0;
    }

    .stat-title {
        font-size: 18px;
        margin: 8px 0;
    }
    

</style>