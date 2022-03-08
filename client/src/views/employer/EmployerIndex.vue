<script setup>
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerStatBar from '@/components/employer/EmployerStatBar.vue';

    import relativeTime from 'dayjs/plugin/relativeTime';
    import dayjs from 'dayjs';
    import { ref, watch } from 'vue';

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
    let filter = ref('all');
    let limit = ref(10);
    let sort = ref('newApps');
    let page = ref(3);
    let numPages = ref(5);

    watch(filter, (filterValue) => {
        alert(`showing ${ filterValue } adverts`);
    });

    watch(limit, (newLimit) => {
        alert(`showing ${ newLimit } articles per page`);
    });

    watch(sort, (sortParam) => {
        alert(`sorted by ${ sortParam }`);
    });

    watch(page, (newPage, oldPage) => {
        alert(`moved from page ${ oldPage } to page ${ newPage }`);
    });
    
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
            <div class='title-bar'>
                <h1 class='title'>Listed Vacancies</h1>
                <div class='title-bar-right'>
                    <div class='select-group'>
                        <label for='filter' class='select-label select-label-hidden'>filter:</label>
                        <select v-model='filter' aria-label='filter vacancies' id='filter'>
                            <option value='all' selected>show all adverts</option>
                            <option value='active'>show active adverts</option>
                            <option value='closed'>show closed adverts</option>
                        </select>
                    </div>


                    <div class='select-group'>
                        <label for='limit' class='select-label select-label-hidden'>page limit:</label>
                        <select v-model='limit' aria-label='set page size' id='limit'>
                            <option value=5>5 per page</option>
                            <option value=10 selected>10 per page</option>
                            <option value=20>20 per page</option>
                            <option value=50>50 per page</option>
                        </select>
                    </div>


                    <div class='select-group'>
                        <label for='sort' class='select-label'>sort by:</label>
                        <select v-model='sort' aria-label='sort vacancies' id='sort'>
                            <option value='newApps' selected>new applications</option>
                            <option value='dateDesc'>latest first</option>
                            <option value='dateAsc'>oldest first</option>
                            <option value='titleAsc'>title (a-z)</option>
                            <option value='titleDesc'>title (z-a)</option>
                        </select>
                    </div>

                </div>
            </div>

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

            <div class='pagination'>
                <div class='pag-block pag-start' @click='page=1'><i class="fa-solid fa-angles-left"></i></div>
                <div class='pag-block' @click='page > 1 ? page-- : page'><i class="fa-solid fa-angle-left"></i></div>
                <div class='pag-block' @click='page=i' v-for='i in 5' :key='i' :class='i == page ? "pag-active" : ""'>{{ i }}</div>
                <div class='pag-block' @click='page < numPages ? page++ : page'><i class="fa-solid fa-angle-right"></i></div>
                <div class='pag-block pag-end' @click='page=numPages'><i class="fa-solid fa-angles-right"></i></div>
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

    .pagination {
        display: flex;
        width: 100%;
        justify-content: center;
        margin: 15px 0 30px 0;
    }

    .pag-active {
        background: var(--blue) !important; /* important removes background color hover change */
        color: white;
    }


    .pag-block {
        padding: 3px 6px;
        border: 1px solid var(--jet);
        border-left-width: 0;
        min-width: 20px;
    }

    .pag-end {
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }

    .pag-block:hover, .pag-block:focus, .pag-block:active {
        cursor: pointer;
        background: rgba(85, 85, 85, 0.1);
    }

    .pag-start {
        border-width: 1px;
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
    }

    .select-group {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: 10px;
    }

    .select-label {
        font-size: 12px;
        position: relative;
        left: 2px;
    }

    .select-label-hidden {
        color: white;
    }

    .title, div /deep/ .title {
        margin: 0;
        font-size: 32px;
        position: relative;
        left: 5px;
        font-weight: 400;
    }

    .title-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }

    .title-bar-right {
        display: flex;
        align-items: center;
        position: relative;
        right: 5px;
        /* top: 2px; */
    }

    .title-bar-right select {
        padding: 4px 6px;
        font-family: var(--fonts);
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
        background: var(--blue);
    }

    .vacancy-button-blue:hover, .vacancy-button-blue:focus, .vacancy-button-blue:active {
        background: var(--blue-focus);
        cursor: pointer;
  } 

    .vacancy-button-grey {
        background: var(--slate);
    }

    .vacancy-button-grey:hover, .vacancy-button-grey:focus, .vacancy-button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
  } 

    .vacancy-button-red {
        background: var(--red);
    }

    .vacancy-button-red:hover, .vacancy-button-red:focus, .vacancy-button-red:active {
        background: var(--red-focus);
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