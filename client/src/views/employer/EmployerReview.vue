<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import Footer from '@/components/partials/Footer.vue';
    import MatchCard from '@/components/employer/match/MatchCard.vue';
    import EmptyCard from '@/components/employer/review/EmptyCard.vue';
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import ProfileCard from '@/components/employer/match/ProfileCard.vue';
    import ApplyProfileCard from '@/components/employer/review/ApplyProfileCard';
    import TutorialModal from '../../components/employer/tutorial/TutorialModal.vue';

    
    import { ref, onMounted } from 'vue';    


    const url = window.location.pathname;
    const vacancyId = url.substring(url.lastIndexOf('/') + 1);

    const notifs = ref(2);
    const matches = ref([]);
    const vacancy = ref({});
    const showDeck = ref(true);
    const matchProfile = ref({});
    const currentProfile = ref({});
    const currentApplication = ref({});
	const isNewUser = ref(window.localStorage.getItem('newUserReview') === 'true');
    

    const searchValue = ref("");

    const getApplicants = async () => {
        const response = await api({
            url: `/v1/e/vacancies/${ vacancyId }/review/`,
            method: 'get',
            responseType: 'json',
            params: {
                'searchValue': searchValue.value
            }
        }).catch(apiCatchError);

        if(!response?.data)
            return;

        const { matches: apiMatches = [], new: newApp = {}, vacancy: apiVacancy = {} } = response.data;

        matches.value = apiMatches;
        vacancy.value = apiVacancy;

        if(newApp){
            let { application = {}, profile = {}} = newApp;
            currentApplication.value = application;
            currentProfile.value = profile;
        }
    }

    onMounted(async () => {
        getApplicants();
    });

    const showMatchApplication = (nextProfile) => {
        matchProfile.value = nextProfile.value;
        showDeck.value = false;
    }

    const onUnmatch = async (match) => {
        showDeck.value = true;
        matches.value = { };
        getApplicants();
    }

    const onMatch = (application, nextApplication, nextProfile) => {
        matches.value.push(application);
        currentProfile.value = nextProfile;
        currentApplication.value = nextApplication;
    }

    const updateCard = (nextApplication, nextProfile) => {
        currentProfile.value = nextProfile;
        currentApplication.value = nextApplication;
    }

    //download button
    /*
    const download_button = () => {
        alert('downloading all applications');
    }*/

    const finishTutorial = () => {
        window.localStorage.setItem('newUserReview', false);
        isNewUser.value = false;
    }

    const searchBarValueUpdated = (value) => {
        searchValue.value = value;

        getApplicants();
    }
</script>



<template>
    <!-- <EmployerNavbar :numNotifs='notifs'></EmployerNavbar> -->
    <EmployerNavbar ></EmployerNavbar>

    <div class='container'>
        <div class='col col-left'>
            <div class='col-header'> 
                <h3 class='col-title'>Matches ({{ matches.length }})</h3>
                <div class='header-right'>
                    <!-- download button -->
                    <!-- <button type='button' class='application-button application-button-grey' id= 'download_button' @click= download_button>Download Applications</button> -->
                    
                    <div class='search-group'>
                        <i class="fas fa-search search-icon"></i>
                        <input class='search' v-model='searchbar' @change='searchBarValueUpdated(searchbar)' placeholder='search' type='text'> 
                    </div>
                </div>
            </div>

            <hr class='slim-hr'/>

            <div class='applications'>
                <MatchCard v-for='match in matches' 
                    :key='match.id' 
                    :stats='match'
                    :vacancyName='vacancy.VacancyName'
                    :showingThis='!showDeck && matchProfile.UserId == match?.profile?.UserId'
                    @unmatch='onUnmatch(match)'
                    @showApplication='showMatchApplication'
                    @hideApplication='showDeck = true'
                 />
            </div>
        </div>

        <div class='col col-right'>
            <div class='col-header'> 
                <h3 class='col-title'>
                    {{ vacancy.CompanyName }}
                    <span v-if='vacancy.CompanyName && vacancy.VacancyName'> - </span>
                    {{ vacancy.VacancyName }}
                </h3>
            </div>

            <hr class='slim-hr' />

            <main class='card-container'>
                <ApplyProfileCard 
                    v-if='Object.keys(currentApplication).length !== 0 && showDeck'
                    class='card' 
                    :application='currentApplication' 
                    :profile='currentProfile' 
                    :vacancyId='vacancyId' 
                    @match='onMatch'
                    @defer='updateCard'
                    @reject='updateCard'
                />

                <ProfileCard
                    v-else-if='!showDeck'
                    class='card'
                    :profile='matchProfile'
                />

                <EmptyCard v-else />
            </main>
        </div>
    </div>

    
	<TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Review applications</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    On this page you can review all the applications made to a vacancy one by one on the right.
                </p>
                <p class='desc'>
                    You can either reject the current application, skip it, or match with it by clicking the green (left), yellow (up) or red (right) buttons at the bottom of the card or by using the relevant (arrow keys).
                </p>
                <p class='desc'>
                    A rejection will prevent the same applicant from appearing again and notify the applicant, while skipping puts them to the bottom of the deck.
                </p>
                <p class='desc'>
                    Accepting an application will form a match, which will be displayed along with existing matches on the left.
                </p>
            </div>

        </template>
    </TutorialModal>


    <Footer></Footer>

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
        display: flex;
        gap: 6px;
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
