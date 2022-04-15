<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import FormStepper from '@/components/employee/profile/FormStepper.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    
    // form pages
    import PersonalDetailsForm from '@/components/employee/profile/PersonalDetailsForm.vue';
    import ContactDetailsForm from '@/components/employee/profile/ContactDetailsForm.vue';
    import LocationForm from '@/components/employee/profile/LocationForm.vue';
    import SoftSkillsForm from '@/components/employee/profile/SoftSkillsForm.vue';
    import ExperienceForm from '@/components/employee/profile/ExperienceForm.vue';
    import QualificationsForm from '@/components/employee/profile/QualificationsForm.vue';
    import ReviewForm from '@/components/employee/profile/ReviewForm.vue';

    import { onMounted, ref } from 'vue';

    let pages;
    const formData = ref([]);
    const notifs = ref(2);
    const currentPageNum = ref(0);

    onMounted(() => {
        pages = document.querySelectorAll('.form-page-container');
    });

    const changePage = (incr) => {
        const maxPage = pages.length - 1;
        const oldPage = currentPageNum.value;
        const newPage = currentPageNum.value + incr;

        if(newPage > maxPage || newPage < 0)
            return;

        pages[oldPage].classList.add('form-page-container-hidden');
        pages[newPage].classList.remove('form-page-container-hidden');

        currentPageNum.value += incr;

        if(newPage == pages.length - 1) {
            // review page, get form data
            const form = document.querySelector('form');
            formData.value = new FormData(form);
        }
    }

    


</script>

<template>
    <EmployeeNavbar page='home' :numNotifs='notifs'> </EmployeeNavbar>

    
    <div class= 'container'>
        <h1 class ='title'> User Profile SetUp </h1>

        <nav class='form-progress'>
            <FormStepper :stepNum='currentPageNum' />
        </nav>

    </div>

    <form class='form-pane'>
        <div class='form-page-container'>
            <PersonalDetailsForm @next='changePage(1)' :companyName='companyName' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ContactDetailsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <LocationForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <SoftSkillsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ExperienceForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <QualificationsForm @next='changePage(1)' @back='changePage(-1)' />
        </div>
        <div class='form-page-container form-page-container-hidden'>
            <ReviewForm :formData='formData' @back='changePage(-1)' />
        </div>
        
    </form>

</template>

<style scoped>
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
        align: left;
        text-align: left;  
        margin-top:0; 
        border-bottom: 1px solid;
    }
    
</style>