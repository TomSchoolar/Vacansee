<script setup>
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import EmployeeStatBar from '@/components/employee/EmployeeStatBar.vue';

    import axios from 'axios';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import { jwtGetId } from '@/assets/js/jwt';
    import dayjs from 'dayjs';
    import { ref, watch } from 'vue';

    dayjs.extend(relativeTime);

   // vars init
    const stats = ref({
        totalApplications: '...',
        pendingApplications: '...',
        matches: '...',
    });

    const vacancies = ref (null);

    
    let filter = ref('all');
    let limit = ref(10);
    let sort = ref('dateDesc');

    let page = ref(1);
    let numPages = ref(5);

    document.title = 'Applications | VacanSee'

    // api request function
    const getVacancies = async (options) => {
        const { count = 5, pageNum = 1, sort = 'newApps', filter = 'all' } = options;

        const uID = jwtGetId();

        if(!uID)
            return;

        const response = await axios({
            method: 'get',
            url: '/e/vacancy/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            params: {
                uID,
                sort,
                count,
                filter,
                pageNum
            }
        }).catch((err) => {
            try {
                let { message = err.message, status = err.status } = err.response.data;
                console.error(`oops: ${ status }: ${ message }`);
            } catch {
                console.error(`uh oh: ${ err }`);
                alert('Error: Server may not be running');
            }

        });

        if(!response || !response.data)
            return false;

        const { data } = response;


        if(!data)
            return false;

        return true;
    }


    // vacancy api request
    onMounted(async () => {
        const result = await getApplications({ });

        if(!result) {
            return;
        }
    });



    // get vacancies in new order
    const sortApps = async (sortParam) => {
        const result = await getApplications({ sort: sortParam, count: limit.value, pageNum: page.value, filter: filter.value });
        
        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }


    // change page
    const changePage = async (newPage) => {
        const result = await getApplications({ sort: sort.value, count: limit.value, pageNum: newPage, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        page.value = newPage;   
    }



    watch(filter, async (filterValue) => {
        // change which vacancies are display based on isOpen
        const result = await getApplications({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filterValue });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        filter.value = filterValue;
    });


    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        while((page.value - 1) * limit.value >= numApps.value) page.value--;

        if(page.value < 0)
            page.value = 0;

        const result = await getApplications({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        limit.value = newLimit;
    });

    watch(sort, sortApps);

    
    // vacancy button actions

    const closeVacancy = () => {
        alert('are you sure you want to close this vacancy?');
    }

    const deleteVacancy = () => {
        alert('are you sure you want to delete this vacancy?');
    }

    watch(page, (newPage, oldPage) => {
        alert(`moved from page ${ oldPage } to page ${ newPage }`);
    });
    
    const cancelApplication = () => {
        alert('are you sure you want to cancel this application?');
    }

    const deleteApplication = () => {
        alert('are you sure you want to delete this application?');
    }
</script>



<template>
    <EmployeeNavbar page='applications' :numNotifs='notifs'></EmployeeNavbar>

    <main class='container'>
        <section class='vacancies-section'>
            <div class='title-bar'>
                <h1 class='title'>Applications</h1>
                <div class='title-bar-right'>
                    <div class='select-group'>
                        <label for='filter' class='select-label select-label-hidden'>filter:</label>
                        <select v-model='filter' aria-label='filter vacancies' id='filter'>
                            <option value='all' selected>show all applications</option>
                            <option value='matched'>show matched applications</option>
                            <option value='pending'>show pending applications</option>
                            <option value='rejected'>show rejected applications</option>
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
                            <option value='dateDesc'>latest first</option>
                            <option value='dateAsc'>oldest first</option>
                        </select>
                    </div>

                </div>
            </div>

            <EmployeeStatBar :stats='stats' />

            <hr />

            <div class='vacancies' v-for='vacancy in applications' :key='application.id'>
                <div class='vacancy'>
                    <div class='vacancy-left'>
                        <h5 class='vacancy-title' :title='vacancy.title'>{{ vacancy.title }}</h5>
                        <h5 class='vacancy-company'>{{ vacancy.company }}</h5>
                        <h5 class='vacancy-status' v-if='vacancy.isAccepted'>Matched!</h5>
                        <h5 class='vacancy-status' v-else-if='vacancy.isReviewed && !vacancy.isAccepted'>Rejected</h5>
                        <h5 class='vacancy-status' v-else>Application sent!</h5>
                    </div>
                    <div class='vacancy-right'>
                        <div class='vacancy-applied' :title='vacancy.updated'>Applied {{ vacancy.appliedDate }}<br />Updated {{ vacancy.updatedDate }}</div>
                        <button class='vacancy-button vacancy-button-grey' @click='deleteApplication' v-if='vacancy.isReviewed && !vacancy.isAccepted'>Delete Application</button>
                        <button class='vacancy-button vacancy-button-red' @click='cancelApplication' v-else>Cancel Application</button>
                        <router-link :to='`/applications/${ vacancy.id }`' class='vacancy-button vacancy-button-blue' v-if='vacancy.isAccepted'>Match Details</router-link>
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
    hr, div:deep(hr) {
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
        background: var(--red) !important; /* important removes background color hover change */
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

    .title, div:deep(.title) {
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

    .vacancy-applied {
        width: 200px;
        text-align: center;
        margin-right: 20px;
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

    .vacancy-company {
        font-size: 16px;
        width: 300px;
        text-align: center;
    }

    .vacancy-left {
        width: 60%;
        display: flex;
        align-items: center;
        flex-shrink: 1;
    }

    .vacancy-right {
        display: flex;
        align-items: center;
        flex-grow: 1;
        justify-content: flex-end;
    }

    .vacancy-status {
        font-size: 16px;
        width: 300px;
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

    .vacancy-updated {
        width: 180px;
        text-align: center;
        margin-right: 5px;
        cursor: default;
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