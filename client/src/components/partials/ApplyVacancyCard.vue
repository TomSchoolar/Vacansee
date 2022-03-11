<script setup>  
    
    const props = defineProps(['companyName', 'jobTitle', 'location', 'description', 'skills', 'experience', 'tags'])

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
        <div class='company-info'>
            <div class='company-name'>{{ companyName }}<i id='favourite' class='fas fa-star' v-if="favourited === 'True'"></i></div>
            <p class='job-title'>{{ jobTitle }}</p>
            <p class='location'>Based in {{ location }}</p>
        </div>
        <div class='description'>
            <p>{{ description }}</p>
        </div>
        <span style='font-weight: bold;'>Necessary Skills:</span>
        <div class='skills' v-for='skill in skills' v-bind:key='skill'>
            <table>
                <tr>
                    <th>- {{skill}}</th>
                </tr>
            </table>
        </div>
        <span style='font-weight: bold;'>Experience:</span>
        <div class='experience' v-for='xp in experience' v-bind:key='xp'>
            <table>
                <tr>
                    <th>- {{xp}}</th>
                </tr>
            </table>
        </div>
        <span style='font-weight: bold;'>Requirements:</span>
        <table>
        <tr>
            <th class='tags' v-for='tag in tags' v-bind:key='tag.id'>
                <i :class=tag.icon></i>
            </th>
        </tr>
        </table>
        <div class='divider'><hr /></div>
        <div class='apply-buttons'>
            <button type='button' class='reject' @click='reject'><i class='fas fa-multiply'></i></button>
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
        height: 50px;
        padding-top: 5px;
        padding-bottom: 5px;
    }

    .divider hr {
        margin: 5px;
    }

    .job-title {
        font-style: italic;
    }

    .location {
        font-style: italic;
    }

    .skills {
        font-weight: normal;
    }

    .tags {
        font-size: 250%;
        padding-left: 15px;
        padding-top: 0px;
        padding-right: 10px;
        padding-bottom: 0px;;
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
        color: var(--red)
    }
</style>