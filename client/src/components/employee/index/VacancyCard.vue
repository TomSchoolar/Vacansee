<script setup>  
    import { computed, ref, watch } from 'vue';

    const props = defineProps(['vacancy', 'tags']);



    let tagsLim = ref(6);
    let effectiveLim = ref(tagsLim.value);
    let extraTags = computed(() => {
        let extraTags = '';

        if(!props?.vacancy?.tags || !props?.tags)
            return;

        if(props.vacancy.tags.length > tagsLim.value) {
            effectiveLim.value = tagsLim.value - 1;

            props.vacancy.tags.slice(effectiveLim.value,-1).forEach((tag) => {
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
                <div v-for='(skill, index) in vacancy?.SkillsRequired' :key='`skill-${ index }`'>
                    > {{ skill }}
                </div>
            </div>
        </div>

        <span v-if='vacancy?.ExperienceRequired' class='card-section'>Experience:</span>
        <div class='experience'>
            <div class='exp-container' v-for='(xp, index) in vacancy?.ExperienceRequired' :key='`xp-${ index }`'>
                <span class='exp-position'>> {{ xp.split('&&')[0] }}</span>
                <span class='exp-time' v-if='xp.split("&&").length > 1'>{{ xp.split('&&')[1] }}</span>
            </div>
        </div>
        <span class='card-section' v-if='vacancy?.tags?.length > 0'>Tags:</span>
        <div class='tags-row' v-if='vacancy?.tags?.length > 0'>
            <i class='tag' v-for='tag in vacancy.tags.slice(0, effectiveLim)' :key='tag.id' :class='tags[tag-1].icon' :title='tags[tag-1].text'></i>
            <th v-if='extraTags' class='tag tags-overflow' :title='extraTags'>
                <div class='tags-num' ref='extra-tags'>+{{ vacancy.tags.length - effectiveLim }}</div>
                <i class='fa-solid fa-tags'></i>
            </th>
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
        min-height: 400px;
        width: calc(100% / 3 - 56px);
        max-width: 380px;
        min-width: 310px;
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
        margin: 5px 0 5px 0;
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
        align-items: center;
    }

    .tags-overflow {
        position: relative;
        cursor: help;
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
        color: var(--red);
    }

</style>