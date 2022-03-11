<script setup>  
    const props = defineProps(['firstName', 'pronouns', 'location', 'topicSentence', 'skills', 'experience', 'qualifications']);

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
            <p class='name'>{{ firstName }} <span class='pronouns'>({{ pronouns }})</span></p>
            <p class='location'>Based in {{ location }}</p>
        </div>
        <div class='description'>
            <p>{{ topicSentence }}</p>
        </div>
        <span class='card-section'>Notable Skills:</span>
        <div class='skills' v-for='skill in skills' v-bind:key='skill'>
            <table>
                <tr>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span class='card-section'>Experience:</span>
        <div class='experience' v-for='xp in experience' v-bind:key='xp'>
            <table>
                <tr>
                    <th>- {{ xp.title }}</th>
                    <th><span class='date'>{{ xp.startDate }} - {{ xp.endDate }}</span></th>
                </tr>
            </table>
        </div>
        <span class='card-section'>Qualifcations:</span>
        <div class='qualifications' v-for='qual in qualifications' v-bind:key='qual'>
            <table>
                <tr>
                    <th>- {{qual}}</th>
                </tr>
            </table>
        </div>
        <div class='divider'><hr /></div>
        <div class='apply-buttons'>
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

    .apply-buttons button:active i {
        font-size: 14px;
    }

    .apply-buttons i {
        font-size: 20px;
    }

    .apply-buttons .apply {
        background: #66E355;
    }

    .apply-buttons .favourite {
        background: #ffbf00
    }

    .apply-buttons .reject {
        background: #FF8582
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
        padding-left: 20px;
        padding-right: 20px;
        padding-top: 5px;
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
        margin: 5px;
    }

    .experience .date {
        font-style: italic;
        color: var(--slate);
        font-size: 14px;
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