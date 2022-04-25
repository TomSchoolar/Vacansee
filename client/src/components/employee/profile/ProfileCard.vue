<script setup>  
    import { ref } from 'vue';

    const { profile = {} } = defineProps(['profile']);

</script>

<template>
    <div class='card'>
        <div class='personal-info'>
            <div class='name'> <b> {{ profile.FirstName }} {{ profile.LastName }} </b> <i> ({{profile.Pronouns}}) </i></div>
            <p class='location' v-if='profile.Location'>Based in {{ profile.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ profile.TopicSentence }}</p>
        </div>
        
        <span class='card-section'>Notable Skills:</span>
        <div class='skills'>
            <table>
                <tr v-if='profile.skill1'> - {{profile.skill1}} </tr>
                <tr v-if='profile.skill2'> - {{profile.skill2}} </tr>
                <tr v-if='profile.skill3'> - {{profile.skill3}} </tr>
            </table>
        </div>

        <span class='card-section'>Experience:</span>
        <div class='experience'>
            <table>
                <tr v-if='profile.position1'>
                    <th> - {{profile.position1}} </th>
                    <th> ({{profile.position1start}} - {{profile.position1end}}) </th>
                </tr>
                <tr v-if='profile.position2'>
                    <th> - {{profile.position2}} </th>
                    <th> ({{profile.position2start}} - {{profile.position2end}}) </th>
                </tr>
                <tr v-if='profile.position3'>
                    <th> - {{profile.position3}} </th>
                    <th> ({{profile.position3start}} - {{profile.position3end}}) </th>
                </tr>
            </table>
        </div>
        
        <span class='card-section'>Qualifications:</span>
        <div class='qualification'>
            <table>
                <tr v-if='profile.qualification1'>
                    <div v-if='profile.number1'>
                        <th> - {{profile.number1}} {{profile.qualification1}} </th>
                        <th> ({{profile.highgrade1}} - {{profile.lowgrade1}}) </th>
                    </div>
                    <div v-if='profile.subject1'>
                        <th> - {{profile.type1}} {{profile.subject1}} ({{profile.classification1}})</th>
                    </div>
                </tr>
                <tr v-if='profile.qualification2'>
                    <div v-if='profile.number2'>
                        <th> - {{profile.number2}} {{profile.qualification2}} </th>
                        <th> ({{profile.highgrade2}} - {{profile.lowgrade2}}) </th>
                    </div>
                    <div v-if='profile.subject2'>
                        <th> - {{profile.type2}} {{profile.subject2}} ({{profile.classification2}})</th>
                    </div>
                </tr>
                <tr v-if='profile.qualification3'>
                    <div v-if='profile.number3'>
                        <th> - {{profile.number3}} {{profile.qualification3}} </th>
                        <th> ({{profile.highgrade3}} - {{profile.lowgrade3}}) </th>
                    </div>
                    <div v-if='profile.subject3'>
                        <th> - {{profile.type3}} {{profile.subject3}} ({{profile.classification3}}) </th>
                    </div>
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
        padding: 30px 20px 15px 20px;
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