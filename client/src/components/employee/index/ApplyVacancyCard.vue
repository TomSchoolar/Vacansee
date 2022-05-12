<script setup>  
    import api, { apiCatchError } from '@/assets/js/api';

    import { computed, onMounted, ref, watch } from 'vue';    

    const props = defineProps(['vacancy', 'tags', 'favourited', 'cardAction']);
    const emit = defineEmits(['update']);

    const favourite = async (vID) => {
        await api({
            url: `/v1/vacancies/${ vID }/favourite/`,
            method: 'post',
            responseType: 'json'
        }).catch(apiCatchError);

        emit('update');
    }

    const unfavourite = async (vID) => {
        await api({
            url: `/v1/vacancies/${ vID }/unfavourite/`,
            method: 'delete',
            responseType: 'json'
        }).catch(apiCatchError);

        emit('update');
    }

    const apply = async (vID) => {
        await api({
            url: `/v1/vacancies/${ vID }/apply/`,
            method: 'post',
            responseType: 'json'
        }).catch(apiCatchError);

        emit('update');
    }

    const reject = async (vID) => {
        await api({
            url: `/v1/vacancies/${ vID }/reject/`,
            method: 'post',
            responseType: 'json'
        }).catch(apiCatchError);

        emit('update');
    }


    watch(props, () => {
        const vacancyId = props?.vacancy?.VacancyId ?? '-1';

        if(props.cardAction == null) {
            return;
        } else if(props.cardAction == 'apply') {
            apply(vacancyId);
        } else if(props.cardAction == 'favourite') {
            favourite(vacancyId);
        } else if(props.cardAction == 'reject') {
            reject(vacancyId);
        }
    });

    
    let tagsLim = ref(6);
    let extraTags = computed(() => {
        let extraTags = '';

        if(!props?.vacancy?.tags || !props?.tags)
            return;

        if(props.vacancy.tags.length > tagsLim.value) {

            props.vacancy.tags.slice(tagsLim.value,-1).forEach((tag) => {
                extraTags += `${ props.tags[tag].text }, `;
            });

            extraTags += props.tags[props.vacancy.tags.length - 1].text;
        }   

        return (extraTags ? extraTags : false);
    })
</script>

<template>
    <div class='card'>
        <div class='company-info'>
            <div class='company-name'>{{ vacancy.CompanyName }}<i id='favourite' class='fas fa-star' title='favourited' v-if='vacancy.Favourited'></i></div>
            <p class='job-title'>{{ vacancy?.VacancyName }}{{ vacancy?.Salary ? ` - ${ vacancy.Salary }` : '' }}</p>
            <p class='location' v-if='vacancy.Location'>Based in {{ vacancy.Location }}</p>
        </div>
        <div class='description' v-if='vacancy.Description'>
            <p>{{ vacancy.Description }}</p>
        </div>
        <span class='card-section' v-if='vacancy.SkillsRequired'>Necessary Skills:</span>
        <div class='skills'>
            <table>
                <tr v-for='(skill, index) in vacancy.SkillsRequired' :key='`skill-${ index }`'>
                    <th>> {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span v-if='vacancy?.ExperienceRequired' class='card-section'>Experience:</span>
        <div class='experience' v-if='vacancy?.ExperienceRequired'>
            <div class='exp-container' v-for='(xp, index) in vacancy.ExperienceRequired' :key='`xp-${ index }`'>
                <span class='exp-position'>> {{ xp.split('&&')[0] }}</span>
                <span class='exp-time' v-if='xp.split("&&").length > 1'>{{ xp.split('&&')[1] }}</span>
            </div>
        </div>
        <span class='card-section' v-if='vacancy?.tags?.length > 0'>Tags:</span>
        <div v-if='vacancy?.tags?.length > 0'>
            <i class='tag' v-for='tag in vacancy.tags.slice(0, tagsLim)' :key='tag.id' :class='tags[tag-1]?.icon' :title='tags[tag-1]?.text'></i>
            <th v-if='extraTags' class='tag tags-overflow' :title='extraTags'>
                <div class='tags-num' ref='extra-tags'>+{{ vacancy.tags.length - tagsLim }}</div>
                <i class='fa-solid fa-tags'></i>
            </th>
        </div>
        <div class='spacing-block'></div>
        <div class='apply-buttons'>
            <div class='divider'><hr /></div>
            <button aria-label='reject' type='button' class='reject' @click='reject(vacancy.VacancyId)'><i class='fas fa-multiply'></i></button>
            <button aria-label='unfavourite' class='favourite' @click='unfavourite(vacancy.VacancyId)' v-if='favourited == true'><i class='fas fa-star'></i></button>
            <button aroa-label='favourite' class='favourite' @click='favourite(vacancy.VacancyId)' v-if="favourited == false"><i class='far fa-star'></i></button>
            <button aria-label='apply' class='apply' @click='apply(vacancy.VacancyId)'><i class='fas fa-check'></i></button>
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
        width: 80% !important;
        max-width: 380px;
        min-width: 310px;
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

    .exp-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .exp-time {
        color: var(--slate);
        font-style: italic;
        font-size: 13px;
    }

    .experience {
        width: 100%;
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
        padding-top: 15px;
        padding-left: 220px;
        font-size: 45px;
        color: var(--red)
    }
</style>