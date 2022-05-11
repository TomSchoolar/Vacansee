<script setup>
    import Joi from 'joi';
    import api, { apiCatchError } from '@/assets/js/api';
    import Footer from '@/components/partials/Footer.vue';
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import FormStepper from '@/components/employer/newVacancy/FormStepper.vue';
    import TutorialModal from '../../components/employer/tutorial/TutorialModal.vue';


    // form pages
    import BasicDetailsForm from '@/components/employer/newVacancy/BasicDetailsForm.vue';
    import MoreDetailsForm from '@/components/employer/newVacancy/MoreDetailsForm.vue';
    import ContactDetailsForm from '@/components/employer/newVacancy/ContactDetailsForm.vue';
    import LogisticsForm from '@/components/employer/newVacancy/LogisticsForm.vue';
    import TagsForm from '@/components/employer/newVacancy/TagsForm.vue';
    import ReviewForm from '@/components/employer/newVacancy/ReviewForm.vue';
    
    import { onMounted, onBeforeUnmount, ref } from 'vue';

    let pages;
    const notifs = ref(2);
    const formData = ref([]);
    const vacancyData = ref({});
    const currentPageNum = ref(0);
	const isNewUser = ref(window.localStorage.getItem('newUserEditVacancy') === 'true');


    // get company name
    let session = window.localStorage.getItem('session') ?? '{}'
    const { CompanyName: cn = false } = JSON.parse(session);
    const companyName = ref(cn);

    onMounted(async () => {
        pages = document.querySelectorAll('.form-page-container');

        let id = window.location.pathname.split('/').pop()

        const vacancy = await api({
            url: `/v1/e/vacancies/${ id }/edit/`,
            method: 'get',
            responseType: 'json'
        }).catch(apiCatchError);

        if(!vacancy.data)
            window.location.href = '/e/vacancy';

        vacancyData.value = vacancy.data;
    });

    const changePage = (incr) => {
        try {
        const maxPage = pages.length;
        const oldPage = currentPageNum.value;
        const newPage = currentPageNum.value + incr;

        if(newPage > maxPage || newPage < 0)
            return;

        if(newPage < maxPage) {
            pages[oldPage].classList.add('form-page-container-hidden');
            pages[newPage].classList.remove('form-page-container-hidden');
        }

        if(newPage == pages.length - 1) {
            // review page, get form data
            const form = document.querySelector('form');
            formData.value = new FormData(form);
        }

        currentPageNum.value += incr;
        } catch(e) {
            console.error(e)
        }
    }

    const finishTutorial = () => {
        window.localStorage.removeItem('newUserEditVacancy');
        isNewUser.value = false;
    }

    onBeforeUnmount(() => {})

</script>

<template>
    <EmployerNavbar :numNotifs='notifs' />

    <main class='container'>
        <div class='header'>
            <h1 class='title'>{{ (companyName ? `${ companyName } - ` : '') + `Edit ${ vacancyData.VacancyName ? vacancyData.VacancyName : 'Vacancy' }` }}</h1>
            <hr />
        </div>
    </main>

    <nav class='form-progress'>
        <FormStepper :stepNum='currentPageNum' v-if='vacancyData' />
    </nav>

    <form class='form-pane'>
        <div class='form-page-container'>
            <BasicDetailsForm @next='changePage(1)' :companyName='companyName' :title='vacancyData.VacancyName' :salary='vacancyData.Salary' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <MoreDetailsForm @next='changePage(1)' @back='changePage(-1)' :description='vacancyData.Description' :expectSkillsValue='true' :skills='vacancyData.SkillsRequired' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ContactDetailsForm @next='changePage(1)' @back='changePage(-1)' :email='vacancyData.Email' :phoneNumber='vacancyData.PhoneNumber' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <LogisticsForm @next='changePage(1)' @back='changePage(-1)' :expectExperienceValue='true' :experience='vacancyData.ExperienceRequired' :city='vacancyData.Location' :timezone='vacancyData.TimeZone' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <TagsForm @next='changePage(1)' @back='changePage(-1)' :tags='vacancyData.Tags' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ReviewForm :formData='formData' @next='changePage(1)' @back='changePage(-1)' :edit='true' />
        </div>
        
    </form>


    <TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Edit vacancy</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    On this page you can edit a vacancy by completing the same form you used to create it.           
                </p>
                <p class='desc'>
                    Except this time the form is pre-populated with vacancy data.    
                </p>
            </div>

        </template>
    </TutorialModal>

    <Footer></Footer>

</template>

<style scoped>
    *:deep(.invalid-input) {
        border: 3px solid var(--red) !important;
    }

    hr {
        width: 100%;
        margin: 8px 0 12px 0;
        border: 0;
        border-top: 2px solid #555;
    } 

    .container {
        width: calc(100vw - 80px);
        padding: 0 40px;
    }

    .form-page-container-hidden {
        visibility: hidden;
        position: absolute;
        top: 0;
        left: 0;
    }

    .form-pane {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 280px;
        margin: 70px auto;
        min-height: 100px;
    }
 
    .header {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .title {
        margin: 0;
        font-size: 32px;
        position: relative;
        left: 5px;
        font-weight: 400;
    }
    
</style>
