<script setup>  
    const props = defineProps(['companyName', 'jobTitle', 'location', 'description', 'skills', 'experience', 'tags', 'favourited']);
</script>

<template>
    <div class='card'>
        <div class='company-info'>
            <div class='company-name'>{{ companyName }}<i id='favourite' class='fas fa-star' v-show="favourited === 'True'"></i></div>
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
        margin: 0;
        padding-top: 5px;
        padding-bottom: 5px;
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
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
        color: var(--red);
    }

</style>