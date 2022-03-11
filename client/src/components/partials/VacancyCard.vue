<script setup>  
    import { ref } from 'vue';

    const { vacancy = {} } = defineProps(['vacancy']);
    const { companyName, favourited, jobTitle, location, description, skills, experience, tags } = vacancy;

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
            <div class='company-name'>{{ companyName }}<i id='favourite' class='fas fa-star' title='favourited' v-if="favourited"></i></div>
            <p class='job-title'>{{ jobTitle }}</p>
            <p class='location' v-if='location'>Based in {{ location }}</p>
        </div>
        <div class='description'>
            <p>{{ description }}</p>
        </div>
        <span v-if='skills' class='card-section'>Necessary Skills:</span>
        <div class='skills'>
            <table>
                <tr v-for='skill in skills' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span v-if='experience' class='card-section'>Experience:</span>
        <div class='experience'>
            <table>
                <tr v-for='xp in experience' v-bind:key='xp'>
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
        font-weight: normal;
        height: 500px;
        width: 400px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        align-items: center;
        text-align: left;
        justify-content: space-between;
        padding: 0 20px;
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
        font-size: 40px;
        padding: 0 10px 0 15px;
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