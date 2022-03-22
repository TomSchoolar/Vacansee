<script setup> 
    import axios from 'axios';

    const emit = defineEmits(['match', 'defer', 'reject'])

    const { application, jwt, profile, vacancyId } = defineProps(['application', 'jwt', 'profile', 'vacancyId']);

    const updateStatus = async (newStatus, applicationId) => {
        const response = await axios({
            url: `/e/review/${ vacancyId }/updatestatus/${ applicationId }/`,
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            method: 'put',
            timeout: 4000,
            headers: {
                Authorization: `Bearer: ${ jwt }`
            },
            data: {
                setStatus: newStatus
            },
            responseType: 'json'
        }).catch((err) => {
            try {
                let { message = err.message, status = err.status } = err.response.data;
                console.error(`oops: ${ status }: ${ message }`);

                if(status === 401) {
                    alert('Your auth token has likely expired, please login again');
                }

                if(message === 'server error getting next application') {
                    alert('Error getting the next application')
                    return {};
                }
            } catch {
                console.error(`uh oh: ${ err }`);
            }
        });

        if(!response) {
            return false;
        }

        const { data = {} } = response;

        return data;
    }


    const accept = async (applicationId) => {
        const response = await updateStatus('accept', applicationId);

        if(!response)
            return;

        const { application = {}, nextApplication = {}, nextProfile = {} } = response;

        emit('match', application, nextApplication, nextProfile);
    }

    const defer = async (applicationId) => {
        const response = await updateStatus('defer', applicationId);

        if(!response)
            return;

        const { nextApplication = {}, nextProfile = {} } = response;

        emit('defer', nextApplication, nextProfile);
    }

    const reject = async (applicationId) => {
        const response = await updateStatus('defer', applicationId);

        if(!response)
            return;

        const { nextApplication = {}, nextProfile = {} } = response;

        emit('reject', nextApplication, nextProfile);
    }
</script>

<template>
    <div class='card'>
        <div class='info'>
            <p class='name'>{{ profile.FirstName }} <span class='pronouns' v-if='profile.Pronouns'>({{ profile.Pronouns }})</span></p>
            <p class='location' v-if='profile.Location'>Based in {{ profile.Location }}</p>
        </div>
        <div class='description'>
            <p>{{ profile.TopicSentence }}</p>
        </div>
        <span v-if='profile.NotableSkills' class='card-section'>Notable Skills:</span>
        <div class='skills block' >
            <table>
                <tr v-for='skill in profile.NotableSkills' v-bind:key='skill'>
                    <th>- {{ skill }}</th>
                </tr>
            </table>
        </div>
        <span v-if='profile.Experience' class='card-section'>Experience:</span>
        <div class='experience block'>
            <table>
                <tr v-for='xp in profile.Experience' v-bind:key='xp'>
                    <th class='table-title'>- {{ xp }}</th>
                    <th><span class='table-date'>{{ xp.startDate }} - {{ xp.endDate }}</span></th>
                </tr>
            </table>
        </div>
        <span v-if='profile.Qualifications' class='card-section'>Qualifications:</span>
        <div class='qualifications' v-for='qual in profile.Qualifications' v-bind:key='qual'>
            <table>
                <tr>
                    <th>- {{ qual }}</th>
                </tr>
            </table>
        </div>
        <div class='apply-buttons'>
            <div class='divider'><hr /></div>
            <button title='reject applicant' class='reject' @click='reject(application.ApplicationId)'><i class='fas fa-multiply'></i></button>
            <button title='defer decision' class='favourite' @click='defer(application.ApplicationId)'><i class="fa-solid fa-arrow-rotate-left"></i></button>
            <button title='match with applicant' class='apply' @click='accept(application.ApplicationId)'><i class='fas fa-check'></i></button>
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