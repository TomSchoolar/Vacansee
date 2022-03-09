<script setup>
    import { ref, watch, onMounted } from 'vue';
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerStatBar from '@/components/employer/EmployerStatBar.vue';
    
    import axios from 'axios';
    import dayjs from 'dayjs';
    import relativeTime from 'dayjs/plugin/relativeTime';
    
    dayjs.extend(relativeTime);

    
    // vars init
    const stats = ref({
        activeAdverts: 0,
        totalApplications: 0,
        newApplications: 0,
        acceptedApplications: 0,
        rejectedApplications: 0
    });

    const notifs = ref(2);
    const vacancies = ref(null);

    // dropdown values
    const filter = ref('all');
    const limit = ref(10);
    const sort = ref('newApps');

    // pagination
    const page = ref(3);
    const numPages = ref(5);

    document.title = 'Home | Vacansee';

    // api request
    onMounted(async () => {

        let { data = false } = await axios({
            method: 'get',
            url: '/e/vacancy/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
        }).catch((err) => {
            console.log(`oops: ${ err }`);
        });
        
        if(!data) {
            return;
        }

        let { vacancies: vs = [], stats: statsObj = false } = data;

        if(statsObj)
            stats.value = statsObj;

        // sort newest first
        vs.sort((a, b) => {
            const dateA = dayjs(a.Created);
            const  dateB = b.Created;

            if(dateA.isBefore(dateB))
                return 1;
            if(dateA.isSame(dateB))
                return 0;
            return -1;
        });
        
        vs.forEach((vacancy) => {
            vacancy.listedAgo = dayjs(vacancy.Created).fromNow();
        });

        vacancies.value = vs;
    });


    const getStats = (data) => {  
        // get combined stats data for all vacancies      
        data.forEach((vacancy) => {
            if(vacancy.IsOpen)
                stats.value.activeAdverts++;
            
            stats.value.totalApplications += vacancy.Applications;
            stats.value.newApplications += vacancy.NewApplications;
            stats.value.acceptedApplications += vacancy.AcceptedApplications;
            stats.value.rejectedApplications += vacancy.RejectedApplications;
        });
    }



    // dropdown watchers

    watch(filter, (filterValue) => {
        alert(`showing ${ filterValue } adverts`);
    });

    watch(limit, (newLimit) => {
        alert(`showing ${ newLimit } articles per page`);
    });

    watch(sort, (sortParam) => {
        alert(`sorted by ${ sortParam }`);
    });


    //pagination watcher

    watch(page, (newPage, oldPage) => {
        alert(`moved from page ${ oldPage } to page ${ newPage }`);
    });
    

    // vacancy button actions

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
                        <h5 class='vacancy-title' :title='vacancy.title'>{{ vacancy.VacancyName }}</h5>
                        <h5 class='vacancy-new' v-if='vacancy.NewApplications'>{{ vacancy.NewApplications }} New Applications!</h5>
                        <p class='vacancy-new' v-else>No New Applications</p>
                    </div>
                    <div class='vacancy-right'>
                        <div class='vacancy-decisions'>{{ vacancy.AcceptedApplications }} Accepted / {{ vacancy.RejectedApplications }} Rejected</div>
                        <div class='vacancy-listed' :title='vacancy.formattedDate'>Listed {{ vacancy.listedAgo }}</div>
                        <button class='vacancy-button vacancy-button-red' @click='closeVacancy' v-if='vacancy.IsOpen'>Close Applications</button>
                        <button class='vacancy-button vacancy-button-red' @click='deleteVacancy' v-else>Delete</button>
                        <router-link :to='`/e/review/${ vacancy.id }`' class='vacancy-button vacancy-button-blue' v-if='vacancy.NewApplications'>Review Applications</router-link>
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