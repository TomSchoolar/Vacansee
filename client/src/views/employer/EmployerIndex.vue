<script setup>
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerStatBar from '@/components/employer/EmployerStatBar.vue';

    import relativeTime from 'dayjs/plugin/relativeTime';
    import dayjs from 'dayjs';
    import { ref } from 'vue';

    dayjs.extend(relativeTime);

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
            accepted: 2000,
            rejected: 1100,
            listed: new Date(2022, 2, 1),
            isOpen: true
        },
        {
            id: 1,
            title: 'Accountant',
            new: 6,
            accepted: 8,
            rejected: 34,
            listed: new Date(2022, 1, 19),
            isOpen: true
        },
        {
            id: 2,
            title: 'This is an unreasonably long job title that doesn\'t fit the template, like seriously who does this',
            new: 0,
            accepted: 2,
            rejected: 11,
            listed: new Date(2022, 0, 3),
            isOpen: false
        }
    ];

    vacancies.forEach((vacancy) => {
        vacancy.listedAgo = dayjs(vacancy.listed).fromNow();
        vacancy.formattedDate = dayjs(vacancy.listed).format('DD/MM/YYYY');
    });

    let notifs = ref(2); 
    
    const closeVacancy = () => {
        alert('are you sure you want to close this vacancy?');
    }

    const deleteVacancy = () => {
        alert('are you sure you want to delete this vacancy?');
    }
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
                        <div class='vacancy-listed' :title='vacancy.formattedDate'>Listed {{ vacancy.listedAgo }}</div>
                        <button class='vacancy-button vacancy-button-red' @click='closeVacancy' v-if='vacancy.isOpen'>Close Applications</button>
                        <button class='vacancy-button vacancy-button-red' @click='deleteVacancy' v-else>Delete</button>
                        <router-link :to='`/e/review/${ vacancy.id }`' class='vacancy-button vacancy-button-blue' v-if='vacancy.new'>Review Applications</router-link>
                        <router-link :to='`/e/review/${ vacancy.id }`' class='vacancy-button vacancy-button-grey' v-else>Reread Applications</router-link>
                        
                    </div>
                </div>
            </div>
        </section>
    </main>

    <button @click='notifs++'>Add notification</button>
    <button @click='notifs < 1 ? 0 : notifs--'>Remove Notification</button>

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
        margin: 0;
        font-size: 32px;
        position: relative;
        left: 5px;
        font-weight: 400;
    }

    .vacancy {
        height: 50px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 25px;
    }

    .vacancy-button {
        font-weight: 500; /* required for some reason */
        border-radius: 15px;
        color: #fff;
        border: 2.2px solid #333;
        width: 150px;
        height: 32px;
        margin-left: 15px;
        font-size: 13px;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
    }

    .vacancy-button-blue {
        background: #08415c;
    }

    .vacancy-button-blue:hover, .vacancy-button-blue:focus, .vacancy-button-blue:active {
        background: #0a567a; /* 8% lighter */
        cursor: pointer;
  } 

    .vacancy-button-grey {
        background: #6b818c;
    }

    .vacancy-button-grey:hover, .vacancy-button-grey:focus, .vacancy-button-grey:active {
        background: #627680; /* 8% darker */
        cursor: pointer;
  } 

    .vacancy-button-red {
        background: #cc2936;
    }

    .vacancy-button-red:hover, .vacancy-button-red:focus, .vacancy-button-red:active {
        background: #bb2531; /* 8% darker */
        cursor: pointer;
    } 

    .vacancy-decisions {
        width: 250px;
        text-align: center;
        margin-right: 20px;
    }

    .vacancy-left {
        width: 40%;
        display: flex;
        align-items: center;
        flex-grow: 1;
    }

    .vacancy-listed {
        width: 180px;
        text-align: center;
        margin-right: 5px;
        cursor: default;
    }

    .vacancy-right {
        display: flex;
        align-items: center;
        flex-grow: 1;
        justify-content: flex-end;
    }

    .vacancy-new {
        font-size: 16px;
        width: 200px;
        text-align: center;
    }

    .vacancy-title {
        font-size: 18px;
        cursor: default;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        text-align: left;
        margin-right: 30px;
        width: calc(100% - 230px);
        font-weight: 500;
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