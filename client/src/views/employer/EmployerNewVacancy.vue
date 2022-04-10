<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import FormStepper from '@/components/employer/newVacancy/FormStepper.vue';
    
    // form pages
    import BasicDetailsForm from '@/components/employer/newVacancy/BasicDetailsForm.vue';
    import MoreDetailsForm from '@/components/employer/newVacancy/MoreDetailsForm.vue';

    
    import { onMounted, ref } from 'vue';

    const notifs = ref(2);
    const currentPageNum = ref(0);
    const pages = ['basic details', 'more details'];

    // get company name
    let session = window.localStorage.getItem('session') ?? '{}'
    const { CompanyName: cn = 'Vacancy Stats' } = JSON.parse(session);
    const companyName = ref(cn);


    const changePage = (incr) => {
        const maxPage = pages.length - 1;
        const newPage = currentPageNum.value + incr;

        if(newPage > maxPage || newPage < 0)
            return;

        currentPageNum.value += incr;
    }

</script>

<template>
    <EmployerNavbar page='newVacancy' :numNotifs='notifs' />

    <main class='container'>
        <div class='header'>
            <h1 class='title'>{{ companyName }}</h1>
            <hr />
        </div>
    </main>

    <nav class='form-progress'>
        <FormStepper :stepNum='currentPageNum' />
    </nav>

    <form class='form-pane'>
        <BasicDetailsForm @next='changePage(1)' :companyName='companyName' v-if='pages[currentPageNum] == "basic details"' />
        <MoreDetailsForm @next='changePage(1)' @back='changePage(-1)' v-if='pages[currentPageNum] == "more details"' />
        
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