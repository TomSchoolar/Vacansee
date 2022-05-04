<script setup>  
    import { ref } from 'vue';

    const props = defineProps(['vacancy']);

</script>

<template>
    <div class='card'>
        <div class='company-info'>
            <div class='company-name'>{{ vacancy?.CompanyName }}<i id='favourite' class='fas fa-star' title='favourited' v-if="vacancy?.Favourited"></i></div>
            <p class='job-title'>{{ vacancy?.VacancyName }}{{ vacancy?.Salary ? ` - ${ vacancy.Salary }` : '' }}</p>
            <p class='location' v-if='vacancy?.Location'>Based in {{ vacancy?.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ vacancy?.Description }}</p>
        </div>
        
        <span v-if='vacancy?.SkillsRequired' class='card-section'>Necessary Skills:</span>
        <div class='skills'>
            <div>
                <div v-for='skill in vacancy?.SkillsRequired' v-bind:key='skill'>
                    - {{ skill }}
                </div>
            </div>
        </div>

        <span v-if='vacancy?.ExperienceRequired' class='card-section'>Experience:</span>
        <div class='experience'>
            <div class='exp-container' v-for='xp in vacancy?.ExperienceRequired' v-bind:key='xp'>
                <span class='exp-position'>- {{ xp.split('&&')[0] }}</span>
                <span class='exp-time' v-if='xp.split("&&").length > 1'>{{ xp.split('&&')[1] }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
    th {
        font-weight: normal;
        padding-bottom: 0px;
        padding-top: 0px;
    }

    .card {
        font-size: 18px;
        font-weight: normal;
        min-height: 500px;
        min-width: 380px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 10px;
        align-items: center;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 0 20px 15px 20px;
        background: #eee;
        color: var(--blue);
    }

    .card > * {
        width: 100%;
    }

    .card-section {
        font-weight: 600;
        margin: 5px 0 5px 0;
    }

    .company-info p {
        margin: 0px;
        padding: 5px 0px 0px 0px;
    }

    .company-name { 
        font-weight: bold;
        font-size: 26px;
        margin: 0px;
        padding: 10px 0px 0px 0px;
    }

    .description p {
        font-size: 18px;
        margin: 10px 0 5px 0;
    }
    
    .exp-container {
        display: flex;
        justify-content: space-between;
    }

    .exp-time {
        color: var(--slate);
        font-style: italic;
        font-size: 13px;
    }

    .job-title {
        font-size: 18px;
        font-style: italic;
    }

    .location {
        font-style: italic;
    }

    .skills {
        font-weight: normal;
    }

    .tag {
        font-size: 32px;
        margin-right: 18px !important;
    }

    .tags-num {
        position: absolute;
        background: var(--red);
        color: white;
        font-size: 12px;
        border-radius: 30%;
        bottom: 5px;
        right: 5px;
        padding: 2px 3px;
    }

    .tags-row {
        display: flex;
    }

    .tags-overflow {
        position: relative;
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
        color: var(--red);
    }

</style>