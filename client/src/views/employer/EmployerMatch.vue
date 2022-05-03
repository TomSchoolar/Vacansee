<script setup>
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import ProfileCard from '@/components/employer/match/ProfileCard.vue';
    import MatchesColumn from '@/components/employer/match/MatchesColumn.vue';
    import VacanciesColumn from '@/components/employer/match/VacanciesColumn.vue';
    import TutorialModal from '../../components/employer/tutorial/TutorialModal.vue'

    
    import { ref } from 'vue';

    document.title = 'Matches | Vacansee';

    const updateCard = (nextProfile) => {
        currentProfile.value = nextProfile;
    }
    
    const notifs = ref(2);
    const currentProfile = ref();
    const selectedVacancy = ref();
    const selectedVacancyName = ref();
	const isNewUser = ref(window.localStorage.getItem('newUserEmployerMatch') == null);


    const updateVacancyId = (vacancy) => {
        selectedVacancy.value = vacancy.VacancyId;
        selectedVacancyName.value = vacancy.VacancyName;
    };

    let session = window.localStorage.getItem('session') ?? '{}'
    const { CompanyName: cn = 'Vacancy Stats' } = JSON.parse(session);
    const companyName = ref(cn);

    const finishTutorial = () => {
        window.localStorage.setItem('newUserEmployerMatch', false);
        isNewUser.value = false;
    }
</script>

<template>
    <EmployerNavbar page='matches' :numNotifs='notifs'></EmployerNavbar>

    <header class='header'>
        <h1 class='title'>{{companyName}} - Matches</h1>
    </header>

    <main class='container'>
        <VacanciesColumn @selectVacancy='updateVacancyId' />

        <MatchesColumn  :selectedVacancy='selectedVacancy' :selectedVacancyName='selectedVacancyName' @show-application='updateCard' />

        <section class='profile-column'>
            <div class='card' v-for='profile in currentProfile' :key='profile'>
                <ProfileCard class='card' :profile='profile' />
            </div>
        </section>
    </main>

    <TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Employer Match</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    On this page you can view all of the matches made on every vacancy you have listed. 
                </p>
                <p class='desc'>
                    If you have any matches, you can select a vacancy in the first column, and an applicant in the second to view their profile card.
                </p>
            </div>

        </template>
    </TutorialModal>
</template>

<style scoped>
    .card {
        position: relative;
        margin-left : auto; 
        margin-right : auto;
        bottom: 20px;
        min-width: 350px;
    }
    
    .container {
        display: flex;
        justify-content: stretch;
        padding: 0;
        width: calc(100vw - 80px);
        width: 100vw;
    }

    .header {
        width: calc(100vw - 80px);
        margin: -10px 0 0 0;
        padding: 0 40px 20px 40px;
        display: flex;
        justify-content: flex-start;
        border-bottom: 1px solid var(--jet);
    }

    .profile-column {
        background-color: var(--background-blue);
        width: 33vw;
        min-width: 450px;
        flex-grow: 0;
        display: flex;
        align-items: center;
    }

    *:deep(.search) {
        font-size: 14px;
        border-radius: 5px;
        padding-left: 5px;
        width: 150px;
        padding: 1.5px 4px 1.5px 22px;
    }

    *:deep(.search-group) {
        position: relative;
    }

    *:deep(.search-icon) {
        position: absolute;
        left: 5px;
        top: 6px;
        font-size: 14px;
    }

    *:deep(.select-label) {
        font-size: 12px;
    }

    *:deep(.select-group) {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: auto;
    }

    *:deep(.sort) {
        width: 155px;
        font-size: 13px;
        font-family: var(--font);
    }

    .title {
        display: inline-block;
        margin: 0;
        font-size: 30px;
        position: relative;
        left: 5px;
        font-weight: 500;
    }
</style>