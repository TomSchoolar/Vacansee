<script setup>  
    import { ref } from 'vue';
    import { jwtGetId } from '@/assets/js/jwt';

    const { tags = [], vacancy = {} } = defineProps(['vacancy', 'tags']);
    const { vID, companyName, jobTitle, favourited, location, description, skills, experience, tags } = vacancy;

    const favourite = () => {
        const uID = jwtGetId(window.localStorage.jwt);

        const response = axios({
            method: 'post',
            url: '/vacancy/favourite/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            params: {
                uID,
                vID
            }
        }).catch((err) => {
            console.log(`oops: ${ err }`);
        });
    }
    
    const apply = () => {
        const uID = jwtGetId(window.localStorage.jwt);

        const response = axios({
            method: 'post',
            url: '/vacancy/apply/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            params: {
                uID,
                vID
            }
        }).catch((err) => {
            console.log(`oops: ${ err }`);
        });
    }

    const reject = () => {
        alert('rejected!');
    }


    let tagsLim = ref(6);
    let extraTags = ref('');

    if(tags.length > 6) {
        tagsLim.value = 5;

        tags.slice(5,-1).forEach((tag) => {
            extraTags.value += `${ tag.title }, `;
        });

        extraTags.value += tags[tags.length - 1].title;
    }
</script>

<template>
    <div class='card'>
        <div class='company-info'>
            <div class='company-name'>{{ vacancy.CompanyName }}<i id='favourite' class='fas fa-star' title='favourited' v-if='vacancy.Favourited'></i></div>
            <p class='job-title'>{{ vacancy.VacancyName }}</p>
            <p class='location' v-if='vacancy.Location'>Based in {{ vacancy.Location }}</p>
        </div>
        <div class='description' v-if='vacancy.Description'>
            <p>{{ vacancy.Description }}</p>
        </div>
        <span class='card-section' v-if='vacancy.SkillsRequired'>Necessary Skills:</span>
        <div class='skills'>
            <table>
                <tr v-for='skill in vacancy.SkillsRequired' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span class='card-section' v-if='vacancy.ExperienceRequired'>Experience:</span>
        <div class='experience' v-for='xp in vacancy.ExperienceRequired' v-bind:key='xp'>
            <table>
                <tr>
                    <th>- {{ xp }}</th>
                </tr>
            </table>
        </div>
        <span class='card-section' v-if='vacancy.Tags'>Requirements:</span>
        <div v-if='vacancy.Tags'>
            <i class='tag' v-for='tag in vacancy.Tags.slice(0, tagsLim)' v-bind:key='tag.id' :class='tags[tag].icon' :title='tags[tag].title'></i>
            <th v-if='tags.length > 6' class='tag tags-overflow' :title='extraTags'>
                <div class='tags-num' ref='extra-tags'>+{{ tags.length - tagsLim }}</div>
                <i class='fa-solid fa-tags'></i>
            </th>
        </div>
        <div class='spacing-block'></div>
        <div class='apply-buttons'>
            <div class='divider'><hr /></div>
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

    .card {
        font-weight: normal;
        height: 550px;
        width: 400px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        align-items: center;
        text-align: left;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: space-between;
        padding: 0 20px 30px 20px;
        position: relative;
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
        margin: 10px 0;
    }

    .divider hr {
        margin: 10px 5px;
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

    .spacing-block {
        width: 1px;
        height: 25px;
    }

    .tag {
        font-size: 32px;
        margin-right: 18px;
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

    .tags-overflow {
        position: relative;
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
        color: var(--red)
    }
</style>