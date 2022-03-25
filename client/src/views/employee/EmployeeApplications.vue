<script setup>
    import axios from 'axios';
    import dayjs from 'dayjs';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import MatchModal from '@/components/employee/applications/MatchModal.vue';
    import EmployeeStatBar from '@/components/employee/applications/EmployeeStatBar.vue';

    import { getJwt } from '@/assets/js/jwt';
    import { ref, watch, onMounted } from 'vue';


   // vars init
    const stats = ref({
        total: '...',
        new: '...',
        matches: '...',
    });


    const page = ref(1);
    const limit = ref(5);
    const notifs = ref(2);
    const numPages = ref(1);
    const filter = ref('all');
    const modalStats = ref({});
    const applications = ref([]);
    const sort = ref('dateDesc');
    const displayModal = ref(false);


    document.title = 'Applications | Tindeed'

    // api request function
    const getApplications = async (options) => {
        const { count = 5, pageNum = 1, sort = 'dateDesc', filter = 'all' } = options;

        const jwt = getJwt();

        if(!jwt)
            return;

        const response = await axios({
            method: 'get',
            url: '/applications/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            headers: {
                authorization: `Bearer: ${ jwt }`
            },
            params: {
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

        const { applications: newApps = [], numPages: ps = 1 } = response.data;

        if(!newApps)
            return false;

        numPages.value = ps;
        applications.value = newApps;

        applications.value.forEach((application) => {
            application.formattedDate = dayjs(application.LastUpdated).format("DD/MM/YYYY")
        });

        return true;
    }


    // application api request
    onMounted(async () => {
        const result = await getApplications({ });

        if(!result) {
            return;
        }
    });


    // get stats
    onMounted(async () => {
        const jwt = getJwt();

        if(!jwt)
            return;

        const response = await axios({
            method: 'get',
            url: '/applications/stats/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            headers: {
                authorization: `Bearer: ${ jwt }`
            }
        }).catch((err) => {
            try {
                let { message = err.message, status = err.status } = err.response.data;
                console.error(`oops: ${ status }: ${ message }`);
            } catch {
                console.error(`uh oh: ${ err }`);
            }
        });

        if(!response || !response.data)
            return false;

        const { data: newStats = {} } = response;

        if(!newStats)
            return false;

        stats.value = newStats;

        return true;
    })



    // get applications in new order
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



    const showMatch = async (matchId) => {
        const jwt = getJwt();

        if(!jwt)
            return;

        const response = await axios({
            url: `/applications/${ matchId }/`,
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            method: 'get',
            responseType: 'json',
            timeout: 3000,
            headers: {
                authorization: `Bearer: ${ jwt }`
            }
        }).catch((err) => {
            try {
                let { message = err.message, status = err.status } = err.response.data;
                console.error(`oops: ${ status }: ${ message }`);
            } catch {
                console.error(`uh oh: ${ err }`);
            }
        });

        const { data: newStats = false } = response;

        if(!stats)
            return;
        console.log(newStats)
        modalStats.value = newStats;
        displayModal.value = true;

    }



    watch(filter, async (filterValue) => {
        // change which applications are display based on isOpen
        const result = await getApplications({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filterValue });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        filter.value = filterValue;
    });


    watch(limit, async (newLimit) => {
        // change number of applications per page
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

    
    // application button actions
    
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
        <section class='applications-section'>
            <div class='title-bar'>
                <h1 class='title'>Applications</h1>
                <div class='title-bar-right'>
                    <div class='select-group'>
                        <label for='filter' class='select-label select-label-hidden'>filter:</label>
                        <select v-model='filter' aria-label='filter applications' id='filter'>
                            <option value='all' selected>show all applications</option>
                            <option value='matched'>show matched applications</option>
                            <option value='pending'>show pending applications</option>
                            <option value='rejected'>show rejected applications</option>
                        </select>
                    </div>


                    <div class='select-group'>
                        <label for='limit' class='select-label select-label-hidden'>page limit:</label>
                        <select v-model='limit' aria-label='set page size' id='limit'>
                            <option value=5 selected>5 per page</option>
                            <option value=10>10 per page</option>
                            <option value=20>20 per page</option>
                            <option value=50>50 per page</option>
                        </select>
                    </div>


                    <div class='select-group'>
                        <label for='sort' class='select-label'>sort by:</label>
                        <select v-model='sort' aria-label='sort applications' id='sort'>
                            <option value='dateDesc'>latest first</option>
                            <option value='dateAsc'>oldest first</option>
                        </select>
                    </div>

                </div>
            </div>

            <EmployeeStatBar :stats='stats' />

            <hr />

            <MatchModal :display='displayModal' :stats='modalStats' @close='displayModal = false' />

            <div class='applications' v-for='application in applications' :key='application.id'>
                <div class='application'>
                    <div class='left'>
                        <h5 class='title'>{{ application.VacancyName }}</h5>
                        <h5 class='company'>{{ application.CompanyName }}</h5>
                        <h5 class='status' v-if='application.ApplicationStatus == "MATCHED"'>Matched!</h5>
                        <h5 class='status' v-else-if='application.ApplicationStatus == "REJECTED"'>Rejected</h5>
                        <h5 class='status' v-else>Application sent!</h5>
                    </div>
                    <div class='right'>
                        <div class='applied' :title='application.formattedDate'>Updated {{ application.formattedDate }}</div>
                        <button class='button button-grey' @click='deleteApplication' v-if='application.ApplicationStatus == "REJECTED"'>Delete Application</button>
                        <button class='button button-red' @click='cancelApplication' v-else>Cancel Application</button>
                        <button @click='showMatch(application.ApplicationId)' class='button button-green' v-if='application.ApplicationStatus == "MATCHED"'>Match Details</button>
                    </div>
                </div>
            </div>

            <div class='pagination'>
                <div class='pag-block pag-start' @click='page > 1 ? changePage(--page) : page'><i class="fa-solid fa-angle-left"></i></div>
                <div class='pag-block' @click='changePage(i)' v-for='i in numPages' :key='i' :class='i == page ? "pag-active" : ""'>{{ i }}</div>
                <div class='pag-block pag-end' @click='page < numPages ? changePage(++page) : page'><i class="fa-solid fa-angle-right"></i></div>
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

    .application {
        height: 50px;
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 25px;
    } 

    .applied {
        width: 200px;
        text-align: center;
        margin-right: 20px;
    }

    .button {
        font-weight: 500; /* required for some reason */
        border-radius: 12px;
        color: #fff;
        border: 2.2px solid #333;
        width: 150px;
        margin-left: 15px;
        font-size: 13px;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--font);
        padding: 2px 6px;
    }

    .button-green {
        background: var(--green);
    }

    .button-green:hover, .button-green:focus, .button-green:active {
        background: var(--green-focus);
        cursor: pointer;
    } 

    .button-grey {
        background: var(--slate);
    }

    .button-grey:hover, .button-grey:focus, .button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
    } 

    .button-red {
        background: var(--red);
    }

    .button-red:hover, .button-red:focus, .button-red:active {
        background: var(--red-focus);
        cursor: pointer;
    }

    .company {
        font-size: 16px;
        width: 300px;
        text-align: center;
        font-weight: 500;
    }

    .left {
        width: 60%;
        display: flex;
        align-items: center;
        flex-shrink: 1;
    }

    .right {
        display: flex;
        align-items: center;
        flex-grow: 1;
        justify-content: flex-end;
    }

    .status {
        font-size: 16px;
        width: 300px;
        text-align: center;
    }

    .title {
        font-size: 18px !important;
        cursor: default;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        text-align: left;
        margin-right: 30px;
        width: calc(100% - 230px);
        font-weight: 500;
    }

    .updated {
        width: 180px;
        text-align: center;
        margin-right: 5px;
        cursor: default;
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

    .applications {
        width: calc(100% - 10px);;
        padding: 0 5px;
        display: block;
    }

    .applications-section {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
</style>