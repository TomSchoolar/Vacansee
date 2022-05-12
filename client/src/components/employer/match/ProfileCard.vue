<script setup>  

    const props = defineProps(['profile']);
</script>

<template>
    <div class='card'>
        <div class='info'>
            <p class='name'>{{ profile.FirstName }} <span v-if='profile.Pronouns' class='pronouns'>({{ profile.Pronouns }})</span></p>
            <p class='location' v-if='profile.Location'>Based in {{ profile.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ profile.TopicSentence }}</p>
        </div>
        <span class='card-section' v-if='profile.NotableSkills'>Notable Skills:</span>
        <div class='skills block'>
            <table>
                <tr v-for='(skill, index) in profile.NotableSkills' v-bind:key='`skill-${ index }`'>
                    <th>> {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span class='card-section' v-if='profile.Experience'>Experience:</span>
        <div class='experience block'>
            <table>
                <tr v-for='(xp, index) in profile.Experience' v-bind:key='`xp-${ index }`'>
                    <!-- <th class='table-title'>- {{ xprofile.Title }}</th> 
                    <th><span class='table-date'>{{ xprofile.StartDate }} - {{ xprofile.EndDate }}</span></th> -->
                    <th class='table-title'>> {{ xp.split('&&')[0] }} </th>
                    <th v-if='xp.split("&&").length > 1'><span class='table-date'>{{ xp.split('&&')[1] }}</span></th>
                </tr>
            </table>
        </div>
        <span class='card-section' v-if='profile.Qualifications'>Qualifications:</span>
        <div class='qualifications'>
            <table>
                <tr v-for='(qual, index) in profile.Qualifications' v-bind:key='`qual-${ index }`'>
                    <th>> {{ qual }}</th>
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

    div.card {
        font-weight: normal;
        min-height: 400px;
        max-height: 600px;
        overflow-y: hidden;
        width: 370px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        align-items: center;
        text-align: left;
        justify-content: space-between;
        padding: 20px;
        background: white;
    }

    .card-section {
        font-weight: bold;
    }

    .description p {
        min-height: 10px;
        max-height: 60px;
        text-overflow: ellipsis;
        padding-top: 5px;
        padding-bottom: 5px;
        margin: 10px auto;
    }

    .info p {
        margin: 0px;
    }

    .name { 
        font-weight: bold;
        font-size: 24px;
        margin: 0px;
        display: flex;
        align-items: center;
        gap: 6px;
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
        color: var(--slate-focus);
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