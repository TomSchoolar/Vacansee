<script setup>
    import axios from 'axios';
    import EmptyCard from '@/components/employer/review/EmptyCard.vue';
    import MatchCard from '@/components/employer/review/MatchCard.vue';
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import ApplyProfileCard from '@/components/employer/review/ApplyProfileCard';
    
    import { ref, onMounted } from 'vue';
    import { getJwt } from '@/assets/js/jwt';


    const url = window.location.pathname;
    const vacancyId = url.substring(url.lastIndexOf('/') + 1);

    const jwt = getJwt();
    const notifs = ref(2);
    const jwtRef = ref(jwt);
    const matches = ref([]);
    const currentProfile = ref({});
    const currentApplication = ref({});    

    onMounted(async () => {
        if(!jwt)
            return;

        const response = await axios({
            url: `/e/review/${ vacancyId }/`,
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            method: 'get',
            headers: {
                Authorization: `Bearer: ${ jwt }`
            },
            responseType: 'json',
            timeout: 4000
        }).catch((err) => {
            try {
                let { message = err.message, status = err.status } = err.response.data;
                console.error(`oops: ${ status }: ${ message }`);

                if(status === 401) {
                    alert('Your auth token has likely expired, please login again');
                }
            } catch {
                console.error(`uh oh: ${ err }`);
            }
        });

        if(!response)
            return;

        const { matches: apiMatches = [], new: newApp = {} } = response.data;

        matches.value = apiMatches;

        if(newApp){
            let { application = {}, profile = {}} = newApp;
            currentApplication.value = application;
            currentProfile.value = profile;
        }
    });


    const onMatch = (application, nextApplication, nextProfile) => {
        matches.value.push(application);
        currentProfile.value = nextProfile;
        currentApplication.value = nextApplication;
    }

    const updateCard = (nextApplication, nextProfile) => {
        currentProfile.value = nextProfile;
        currentApplication.value = nextApplication;
    }

    const download_button = () => {
        alert('downloading all applications');
    }
</script>



<template>
    <EmployerNavbar :numNotifs='notifs'></EmployerNavbar>

    <div class='container'>
        <div class='col col-left'>
            <div class='col-header'> 
                <h3 class='col-title'>Matches ({{ matches.length }})</h3>
                <div class='header-right'>
                    <button type='button' class='application-button application-button-grey' id= 'download_button' @click= download_button>Download Applications</button>
                    <div class='search-group'>
                        <i class="fas fa-search search-icon"></i>
                        <input class='search' placeholder='search' type='text'> 
                    </div>
                </div>
            </div>

            <hr class='slim-hr'/>

            <div class='applications'>
                <MatchCard v-for='match in matches' :key='match.id' :stats='match' />
            </div>
        </div>

        <div class='col col-right'>
            <div class='col-header'> 
                <h3 class='col-title'>Strat Security Co. - Customer Service Representative</h3>
            </div>

            <hr class='slim-hr' />

            <main class='card-container'>
                <ApplyProfileCard 
                    v-if='Object.keys(currentApplication).length !== 0'
                    class='card' 
                    :application='currentApplication' 
                    :profile='currentProfile' 
                    :vacancyId='vacancyId' 
                    :jwt='jwtRef'
                    @match='onMatch'
                    @defer='updateCard'
                    @reject='updateCard'
                />

                <EmptyCard v-else />
            </main>
        </div>
    </div>

</template>



<style scoped>
    table {
        border: 1px solid;
        height: 100%;
        width: 100%;
    }

    .applications {
        overflow-y: scroll;
        height: calc(100% - 47px);
        overflow-x: hidden;
    }

    .application-button {
        font-weight: 500; /* required for some reason */
        border-radius: 7px;
        color: #fff;
        border: 2.2px solid #333;
        min-width: 150px;
        font-size: 12px;
        text-decoration: none;
        padding: 2px 4px;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
    }

    .application-button-grey {
        background: var(--slate);
    }

    .application-button-grey:hover, .application-button-grey:focus, .application-button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
    }

    .card {
        position: relative;
        top: -30px;
    }

    .card-container {
        height: calc(100% - 48px);
        width: 100%;
        background: var(--background-blue);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .container {
        display: flex;
    }

    .col {
        height: calc(100vh - 100px);
        margin-top: -30px;
        padding-top: 30px;
    }

    .col-header {
        display: flex;
        padding: 0 20px 7px 20px;
        justify-content: space-between;
        align-items: center;
        margin-top: -10px;
    }

    .col-left {
        flex-grow: 0.3;
        min-width: 550px;
        border-right: 1px solid #9a9a9a;
    }

    .col-right {
        flex-grow: 3;
    }

    .col-title {
        margin: 0;
        font-weight: 500;
        font-size: 21px;
    }

    .header-right {
        display: flex;
    }

    .search {
        border-radius: 7px;
        padding: 2px 4px 2px 22px;
        margin-left: 8px;
        width: 120px;
    }

    .search-icon {
        position: absolute;
        left: 12px;
        top: 6px;
    }

    .search-group {
        position: relative;
    }

    .slim-hr {
        margin-bottom: 0;
    }
</style>