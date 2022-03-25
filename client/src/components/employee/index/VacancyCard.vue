<script setup>  
    import { ref } from 'vue';

    const { vacancy = {} } = defineProps(['vacancy']);

    let tagsLim = ref(6);
    let extraTags = ref('');

    const tags = [
        {
            id: 0,
            icon: 'fa-solid fa-book'
        },
        {
            id: 1,
            icon: 'fa-solid fa-code'
        },
        {
            id: 2,
            icon: 'fa-brands fa-python'
        },
        {
            id: 3,
            icon: 'fa-solid fa-school'
        },
        {
            id: 4,
            icon: 'fa-solid fa-briefcase'
        },
        {
            id: 5,
            icon: 'fa-solid fa-database'
        },
    ]

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
            <div class='company-name'>{{ vacancy.CompanyName }}<i id='favourite' class='fas fa-star' title='favourited' v-if="vacancy.Favourited"></i></div>
            <p class='job-title'>{{ vacancy.VacancyName }} - {{ vacancy.Salary }}</p>
            <p class='location' v-if='vacancy.Location'>Based in {{ vacancy.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ vacancy.Description }}</p>
        </div>
        
        <span v-if='vacancy.SkillsRequired' class='card-section'>Necessary Skills:</span>
        <div class='skills'>
            <table>
                <tr v-for='skill in vacancy.SkillsRequired' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>

        <span v-if='vacancy.ExperienceRequired' class='card-section'>Experience:</span>
        <div class='experience'>
            <table>
                <tr v-for='xp in vacancy.ExperienceRequired' v-bind:key='xp'>
                    <th>- {{ xp }}</th>
                </tr>
            </table>
        </div>
        <span v-if='tags' class='card-section'>Requirements:</span>
        <table>
            <tr>
                <th class='tags' v-for='tag in tags.slice(0,tagsLim)' v-bind:key='tag.id'>
                    <i :class='tag.icon' :title='tag.title'></i>
                </th>
                <th v-if='tags.length > 6' class='tags tags-overflow' :title='extraTags'>
                    <div class='tags-num' ref='extra-tags'>+{{ tags.length - tagsLim }}</div>
                    <i class='fa-solid fa-tags'></i>
                </th>
            </tr>
        </table>
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

    .tags i {
        font-size: 32px;
    }

    .tag {
        font-size: 25px;
        margin: 10px;
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
        color: var(--red);
    }

</style>