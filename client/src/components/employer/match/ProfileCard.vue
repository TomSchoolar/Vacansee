<script setup>  

    const profile = defineProps(['profile']);
    const p = profile.profile;
</script>

<template>
    <div class='card'>
        <div class='info'>
            <p class='name'>{{ p.FirstName }} <span v-if='p.Pronouns' class='pronouns'>({{ p.Pronouns }})</span></p>
            <p class='location' v-if='p.Location'>Based in {{ p.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ p.TopicSentence }}</p>
        </div>
        <span class='card-section' v-if='p.NotableSkills'>Notable Skills:</span>
        <div class='skills block'>
            <table>
                <tr v-for='skill in p.NotableSkills' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span class='card-section' v-if='p.Experience'>Experience:</span>
        <div class='experience block'>
            <table>
                <tr v-for='xp in p.Experience' v-bind:key='xp'>
                    <!-- <th class='table-title'>- {{ xp.Title }}</th> 
                    <th><span class='table-date'>{{ xp.StartDate }} - {{ xp.EndDate }}</span></th> -->
                    <th class='table-title'>> {{ xp }} </th>
                </tr>
            </table>
        </div>
        <span class='card-section' v-if='p.Qualifications'>Qualifications:</span>
        <div class='qualifications'>
            <table>
                <tr v-for='qual in p.Qualifications' v-bind:key='qual'>
                    <th>- {{ qual }}</th>
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

    .block {
        margin-bottom: 10px;
    }

    .card {
        font-weight: normal;
        height: 500px;
        width: 400px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        align-items: center;
        text-align: left;
        justify-content: space-between;
        padding-left: 20px;
        padding-right: 20px;
        padding-top: 5px;
        background: white;
    }

    .card-section {
        font-weight: bold;
    }

    .description p {
        height: 50px;
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .info p {
        margin: 0px;
    }

    .name { 
        font-weight: bold;
        font-size: 24px;
        margin: 0px;
        padding: 10px 0px 0px 0px;
    }

    .job-title {
        font-style: italic;
    }

    .location {
        font-style: italic;
    }
    
    .pronouns {
        font-weight: normal;
        font-size: 16px;
        font-style: italic;
        color: var(--slate);
    }

    .skills {
        font-weight: normal;
    }

    .table-date {
        font-style: italic;
        color: var(--slate);
        font-size: 14px;
        white-space: nowrap;
    }

    .table-title {
        width: 99%;
    }

    .tags {
        font-size: 250%;
        padding-left: 15px;
        padding-top: 0px;
        padding-right: 10px;
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
    }
</style>