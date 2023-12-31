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
    
    import { onMounted, ref } from 'vue';

    let pages;
    const options = ref([]);
    const formData = ref([]);
    //const notifs = ref(2);
    const currentPageNum = ref(0);
	const isNewUser = ref(window.localStorage.getItem('newUserCreateVacancy') === 'true');


    // get company name
    let session = window.localStorage.getItem('session') ?? '{}'
    const { CompanyName: cn = false, PhoneNumber: phone = false, Email: em = false } = JSON.parse(session);
    const email = ref(em);
    const companyName = ref(cn);
    const phoneNumber = ref(phone);

    onMounted(async () => {
        pages = document.querySelectorAll('.form-page-container');

        const response = await api({
            method: 'get',
            url: '/v1/vacancies/tags',
            responseType: 'json',
        }).catch(apiCatchError);

        options.value = response?.data ?? options.value;
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
        window.localStorage.removeItem('newUserCreateVacancy');
        isNewUser.value = false;
    }

</script>

<template>
    <!-- <EmployerNavbar page='newVacancy' :numNotifs='notifs' /> -->
    <EmployerNavbar page='newVacancy' />

    <main class='container'>
        <div class='header'>
            <h1 class='title'>{{ (companyName ? `${ companyName } - ` : '') + 'New Vacancy' }}</h1>
            <hr />
        </div>
    </main>

    <nav class='form-progress'>
        <FormStepper :stepNum='currentPageNum' />
    </nav>

    <form class='form-pane'>
        <div class='form-page-container'>
            <BasicDetailsForm @next='changePage(1)' :companyName='companyName' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <MoreDetailsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ContactDetailsForm :email='email' :phoneNumber='phoneNumber' @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <LogisticsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <TagsForm :options='options' @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ReviewForm :formData='formData' :options='options' @next='changePage(1)' @back='changePage(-1)' />
        </div>
        
    </form>


	<TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Create new vacancy</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    You can create a new vacancy by completing this form.                
                </p>
                <p class='desc'>
                    Notice you can always go to the previous step by clicking the back button, which will be shown after the first step.
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
