<script setup> 
    const { application = {} } = defineProps(['application']);
    const { firstName, pronouns, location, topicSentence, skills, experience, qualifications } = application;
    
    const favourite = () => {
        alert('favourited!');
    }

    const apply = () => {
        alert('applied!');
    }

    const reject = () => {
        alert('rejected!');
    }
</script>

<template>
    <div class='card'>
        <div class='info'>
            <p class='name'>{{ firstName }} <span class='pronouns' v-if='pronouns'>({{ pronouns }})</span></p>
            <p class='location' v-if='location'>Based in {{ location }}</p>
        </div>
        <div class='description'>
            <p>{{ topicSentence }}</p>
        </div>
        <span v-if='skills' class='card-section'>Notable Skills:</span>
        <div class='skills block' >
            <table>
                <tr v-for='skill in skills' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span v-if='experience' class='card-section'>Experience:</span>
        <div class='experience block'>
            <table>
                <tr v-for='xp in experience' v-bind:key='xp'>
                    <th class='table-title'>- {{ xp.title }}</th>
                    <th><span class='table-date'>{{ xp.startDate }} - {{ xp.endDate }}</span></th>
                </tr>
            </table>
        </div>
        <span v-if='qualifications' class='card-section'>Qualifications:</span>
        <div class='qualifications' v-for='qual in qualifications' v-bind:key='qual'>
            <table>
                <tr>
                    <th>- {{qual}}</th>
                </tr>
            </table>
        </div>
        <div class='apply-buttons'>
            <div class='divider'><hr /></div>
            <button class='reject' @click='reject'><i class='fas fa-multiply'></i></button>
            <button class='favourite' @click='favourite'><i class='fas fa-star'></i></button>
            <button class='apply' @click='apply'><i class='fas fa-check'></i></button>
        </div>
    </div>
</template>

<style scoped>
    th {
        font-weight: normal;
        padding-bottom: 0px;
        padding-top: 0px;
    }

    .apply-buttons {
        position: absolute;
        bottom: 10px;
        width: calc(100% - 40px);
    }

    .apply-buttons button {
        width: 32%;
        height: 30px;
        border: 2px solid;
        border-radius: 15px;
        cursor: pointer;
        margin: 2px;
        text-align: center;
        transition-duration: 0.4s;
    }

    .apply-buttons i {
        font-size: 20px;
    }

    .apply-buttons .apply {
        background: #66E355;
    }

    .apply:active, .apply:focus, .apply:hover {
        background: #38d623; /* 20% darker */
    }

    .apply-buttons .favourite {
        background: #ffbf00;
    }

    .favourite:active, .favourite:focus, .favourite:hover {
        background: #eaaf00; /* 8% darker */
    }

    .apply-buttons .reject {
        background: #ff8582
    }

    .reject:active, .reject:focus, .reject:hover {
        background: #ff6663; /* 8% darker */
    }

    .block {
        margin-bottom: 10px;
    }

    .card {
        font-weight: normal;
        height: 550px;
        width: 400px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        align-items: center;
        text-align: left;
        justify-content: space-between;
        padding: 5px 20px;
        position: relative;
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

    .divider hr {
        margin: 10px 5px;
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
        white-space: nowrap;
        font-style: italic;
        color: var(--slate);
        font-size: 14px;
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