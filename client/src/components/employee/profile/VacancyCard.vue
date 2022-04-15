<script setup>  
    import { ref } from 'vue';

    const { vacancy = {} } = defineProps(['vacancy']);

</script>

<template>
    <div class='card'>
        <div class='personal-info'>
            <div class='name'>{{ vacancy.Name }} {{vacancy.pronouns}}</div>
            <p class='location' v-if='vacancy.Location'>Based in {{ vacancy.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ vacancy.Description }}</p>
        </div>
        
        <span v-if='vacancy.Skills' class='card-section'>Notable Skills:</span>
        <div class='skills'>
            <table>
                <tr v-for='skill in vacancy.Skills' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>

        <span v-if='vacancy.Experience' class='card-section'>Experience:</span>
        <div class='experience'>
            <table>
                <tr v-for='xp in vacancy.Experience' v-bind:key='xp'>
                    <th>- {{ xp }}</th>
                </tr>
            </table>
        </div>
        
        <span v-if='vacancy.Qualification' class='card-section'>Qualifications:</span>
        <div class='qualification'>
            <table>
                <tr v-for='q in vacancy.Qualification' v-bind:key='q'>
                    <th>- {{ q }}</th>
                </tr>
            </table>
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
        font-size: 16px;
        font-weight: normal;
        height: 500px;
        width: calc(100% / 3 - 56px);
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 6px;
        align-items: center;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 0 20px 15px 20px;
    }

    .card > * {
        width: 100%;
    }

    .card-section {
        font-weight: 600;
    }

    .company-info p {
        margin: 0px;
        padding: 5px 0px 0px 0px;
    }

    .company-name { 
        font-weight: bold;
        font-size: 24px;
        margin: 0px;
        padding: 10px 0px 0px 0px;
    }

    .description p {
        font-size: 16px;
        margin: 10px 0;
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