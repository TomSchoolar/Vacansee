<script setup>
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerStatBar from '@/components/employer/EmployerStatBar.vue';

    import { ref } from 'vue';

    const stats = {
        newApplications: 19,
        activeAdverts: 2,
        totalApplications: 96,
        rejectedApplications: 65,
        acceptedApplications: 12
    };

    const vacancies = [
        {
            id: 0,
            title: 'Customer Service Representative',
            new: 13,
            accepted: 2,
            rejected: 11,
            listed: new Date('1st March 2022'),
            isOpen: true
        },
        {
            id: 1,
            title: 'Accountant',
            new: 6,
            accepted: 8,
            rejected: 34,
            listed: new Date('19th February 2022'),
            isOpen: true
        },
        {
            id: 2,
            title: 'This is an unreasonably long job title that doesn\'t fit the template, like seriously who does this',
            new: 0,
            accepted: 2,
            rejected: 11,
            listed: new Date('3rd January 2022'),
            isOpen: false
        }
    ];

    vacancies.forEach((vacancy) => {
        vacancy.listedAgo = dayjs(vacancy.listed).from(dayjs.now())
    });

    let notifs = ref(2);    
</script>



<template>
    <EmployerNavbar page='home' :numNotifs='notifs'></EmployerNavbar>

    <main class='container'>
        <EmployerStatBar user='Strat Security Co.' :stats='stats' />

        <section class='vacancies-section'>
            <h1 class='title'>Listed Vacancies</h1>
            <hr />

            <div class='vacancies' v-for='vacancy in vacancies' :key='vacancy.id'>
                <div class='vacancy'>
                    <div class='vacancy-left'>
                        <h5 class='vacancy-title' :title='vacancy.title'>{{ vacancy.title }}</h5>
                        <h5 class='vacancy-new' v-if='vacancy.new'>{{ vacancy.new }} New Applications!</h5>
                        <p class='vacancy-new' v-else>No New Applications</p>
                    </div>
                    <div class='vacancy-right'>
                        <div class='vacancy-decisions'>{{ vacancy.accepted }} Accepted / {{ vacancy.rejected }} Rejected</div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- <button @click='notifs++'>Add notification</button> -->
    <!-- <button @click='notifs < 1 ? 0 : notifs--'>Remove Notification</button> -->

</template>



<style scoped>
    hr, div /deep/ hr {
        width: 100%;
        margin: 8px 0 12px 0;
        border: 0;
        border-top: 2px solid #555;
    }

    .container {
        padding: 0 40px;
        width: calc(100vw - 80px);
    }

    .title, div /deep/ .title {
        font-weight: 500;
        margin: 0;
        font-size: 32px;
        position: relative;
        left: 5px;
    }

    .vacancy {
        height: 60px;
        border: 2px solid #555;
        border-radius: 10px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 25px;
    }

    .vacancy-left {
        width: 40%;
        display: flex;
        align-items: center;
    }

    .vacancy-new {
        font-size: 16px;
        width: 200px;
        text-align: center;
    }

    .vacancy-title {
        font-weight: 500;
        font-size: 18px;
        cursor: default;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        text-align: left;
        margin-right: 30px;
        width: calc(100% - 230px);
    }

    .vacancies {
        width: calc(100% - 10px);;
        padding: 0 5px;
        display: block;
    }

    .vacancies-section {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
</style>