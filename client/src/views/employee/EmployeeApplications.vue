<script setup>
    import dayjs from 'dayjs';
    import api, { apiCatchError } from '@/assets/js/api';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import MatchModal from '@/components/employee/applications/MatchModal.vue';
    import EmployeeStatBar from '@/components/employee/applications/EmployeeStatBar.vue';
    import AreYouSureModal from '../../components/employer/match/AreYouSureModal.vue';
    import TutorialModal from '@/components/employee/tutorial/TutorialModal.vue';


    import { ref, watch, onMounted } from 'vue';
    

   // vars init
    const stats = ref({
        total: '...',
        new: '...',
        matches: '...',
    });


    const showModal = ref(false);
    const currentModalApplication = ref();
    const isNewUser = ref(window.localStorage.getItem('newUserApplications') == null);


    const page = ref(1);
    const limit = ref(5);
    const notifs = ref(2);
    const numPages = ref(1);
    const filter = ref('all');
    const modalStats = ref({});
    const applications = ref([]);
    const numApps = ref(1);
    const sort = ref('dateDesc');
    const displayModal = ref(false);

    document.title = 'Applications | Vacansee'

    // api request function
    const getApplications = async (options) => {
        const { count = 5, pageNum = 1, sort = 'dateDesc', filter = 'all' } = options;

        const response = await api({
            method: 'get',
            url: '/applications/',
            responseType: 'json',
            params: {
                sort,
                count,
                filter,
                pageNum
            }
        }).catch(apiCatchError);

        if(!response?.data)
            return false;

        const { applications: newApps = [], numPages: ps = 1, pageNum: pn = 1, numApps: na = 0 } = response.data;

        if(!newApps)
            return false;

        page.value = pn;
        numPages.value = ps;
        applications.value = newApps;
        numApps.value = na;

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
        const response = await api({
            method: 'get',
            url: '/applications/stats/',
            responseType: 'json'
        }).catch(apiCatchError);

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
        const response = await api({
            url: `/applications/${ matchId }/`,
            method: 'get',
            responseType: 'json'
        }).catch(apiCatchError);

        const { data: newStats = false } = response;

        if(!stats)
            return;

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
        const result = await getApplications({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        limit.value = newLimit;
    });

    watch(sort, sortApps);

    
    // application button actions

    const deleteApplication = async (applicationId) => {

        const response = await api({
            url: `/applications/delete/${ applicationId }`,
            method: 'delete',
            responseType: 'json'
        }).catch(apiCatchError);

        const { data = false } = response;

        if(data)
            emit('newVacancy', data);

        const count = limit.value;
        const pageNum = page.value;
        
        const response2 = await api({
            method: 'get',
            url: '/applications/',
            responseType: 'json',
            params: {
                sort: sort.value,
                count,
                filter: filter.value,
                pageNum
            }
        }).catch(apiCatchError);

        if(!response2 || !response2.data)
            return false;

        const { applications: newApps = [], numPages: ps = 1 } = response2.data;

        if(!newApps)
            return false;

        numPages.value = ps;
        applications.value = newApps;

        applications.value.forEach((application) => {
            application.formattedDate = dayjs(application.LastUpdated).format("DD/MM/YYYY")
        });
    }

    const finishTutorial = () => {
        window.localStorage.setItem('newUserApplications', false);
        isNewUser.value = false;
    }
</script>



<template>
    <EmployeeNavbar page='applications' :numNotifs='notifs'></EmployeeNavbar>

    <main class='container'>
        <EmployeeStatBar :stats='stats' />

        <section class='applications-section'>
            <div class='title-bar'>
                <div class='title-bar-left'>
                    <h1 class='title'>Applications</h1>
                    <p class='showing' v-if='numApps'>Showing {{ (page - 1) * limit + 1 }} to {{ Math.min(page * limit, numApps) }} of {{ numApps }} </p>              
                </div>
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

            <hr />

            <MatchModal :display='displayModal' :stats='modalStats' @close='displayModal = false' />
            
            <h3 class='no-applications' v-if='numApps == 0'>No applications yet...</h3>

            <div class='applications' v-for='application in applications' :key='application.id'>
                <div class='application'>
                    <div class='left'>
                        <h5 class='application-title'>{{ application.VacancyName }}</h5>
                        <h5 class='company'>{{ application.CompanyName }}</h5>
                        <h5 class='status' v-if='application.ApplicationStatus == "MATCHED"'>Matched!</h5>
                        <h5 class='status' v-else-if='application.ApplicationStatus == "REJECTED"'>Rejected</h5>
                        <h5 class='status' v-else>Application sent!</h5>
                    </div>
                    <div class='right'>
                        <div class='applied' :title='application.formattedDate'>Updated {{ application.formattedDate }}</div>
                        <div class='button-container'>
                            <button @click='showMatch(application.ApplicationId)' class='button button-green' v-if='application.ApplicationStatus == "MATCHED"'>Match Details</button>
                            <button class='button button-red' @click='showModal = true; currentModalApplication = application' v-if='application.ApplicationStatus != "REJECTED"'>Delete Application</button>
                            <button class='button button-disabled' title='You cannot delete rejected applications' v-else>Delete Application</button>
                        </div>
                    </div>
                </div>
                <AreYouSureModal v-if='showModal' :name='currentModalApplication.CompanyName' :vacancyName='currentModalApplication.VacancyName' :employer='false' @close-modal='showModal = false' @unmatch='deleteApplication(currentModalApplication.ApplicationId)' />
            </div>

            <div class='pagination' v-if='numPages > 1'>
                <div class='pag-block pag-start' @click='page > 1 ? changePage(--page) : page'><i class="fa-solid fa-angle-left"></i></div>
                <div class='pag-block' @click='changePage(i)' v-for='i in numPages' :key='i' :class='i == page ? "pag-active" : ""'>{{ i }}</div>
                <div class='pag-block pag-end' @click='page < numPages ? changePage(++page) : page'><i class="fa-solid fa-angle-right"></i></div>
            </div>
        </section>
    </main>

    <TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Employee Applications</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    On this page you can view all of the applications made on every vacancy you have applied for. 
                </p>
                <p class='desc'>
                    If you have any applications, you can sort them using filters on the top right,
                    and delete applications by clicking delete application on the relevant entry.
                </p>
            </div>

        </template>
    </TutorialModal>
    
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
        border-radius: 7px;
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

    .button-container {
        display: flex;
        width: 330px;
        justify-content: flex-end;
    }

    .button-disabled {
        border-color: #999999;
        background-color: #cccccc;
        color: #666666;
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

    .no-applications {
        color: var(--jet);
        font-weight: 500;
        position: relative;
        top: 25px;
        font-size: 18px;
        font-style: italic;
        margin: 0 auto;
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

    .showing {
        margin-left: 30px;
        font-size: 14px;
        color: var(--slate);
        font-style: italic;
        position: relative;
        top: 4px;
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

    .title-bar-left {
        display: flex;
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

    .application-title {
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