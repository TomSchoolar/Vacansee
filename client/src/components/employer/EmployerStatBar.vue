<template>
    <div class='stat-bar'>
        <h1 class='title'>{{ user }}</h1>
        <hr />
        <div class='stat-boxes'>
            <div class='stat-box' v-for='[key, value] of Object.entries(stats)' :key='key'>
                <h4 class='stat-title'>{{ labels[key] }}:</h4>
                <h1 class='stat'>{{ value }}</h1>
            </div>
        </div>
    </div>
    
</template>

<script setup>
    const props = defineProps(['user', 'stats']);
    
    const labels = {
        newApplications: 'New Applications',
        activeAdverts: 'Active Adverts',
        totalApplications: 'Total Applications Received',
        rejectedApplications: 'Rejected Applications',
        acceptedApplications: 'Accepted Applications'
    };
</script>

<style scoped>
    .stat {
        color: #08415c;
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
        margin: 15px 0 50px 0;
    }

    .stat-title {
        font-size: 18px;
        margin: 8px 0;
    }
    

</style>