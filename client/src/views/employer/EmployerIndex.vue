<script setup>
    import dayjs from 'dayjs';
    import api, { apiCatchError } from '@/assets/js/api';
    import relativeTime from 'dayjs/plugin/relativeTime';
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import EmployerStatBar from '@/components/employer/EmployerStatBar.vue';
    import CloseApplicationModal from '../../components/employer/index/CloseApplicationsModal.vue';
    import DeleteVacancyModal from '../../components/employer/index/DeleteVacancyModal.vue';
    import Footer from '@/components/partials/Footer.vue';

    const showModal = ref(false);
    const showDeleteModal = ref(false);
    const currentModalVacancy = ref('');

    import { ref, watch, onMounted } from 'vue';
    
    dayjs.extend(relativeTime);
    
    // vars init
    const stats = ref({
        activeAdverts: '...',
        totalApplications: '...',
        newApplications: '...',
        acceptedApplications: '...',
        rejectedApplications: '...'
    });

    const notifs = ref(2);
    const vacancies = ref(null);
    const displayModal = ref(false);
    const modalType = ref(0);
    const selectedVacancy = ref(0);

    // dropdown values
    const limit = ref(5);
    const filter = ref('all');
    const sort = ref('newApps');

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(0);

    document.title = 'Home | Vacansee';

    // api request function
    const getVacancies = async (options) => {
        const { count = 5, pageNum = 1, sort = 'newApps', filter = 'all' } = options;

        const response = await api({
            method: 'get',
            url: '/e/vacancy/',
            responseType: 'json',
            params: {
                sort,
                count,
                filter,
                pageNum
            }
        }).catch(apiCatchError);

        if(!response)
            return false;

        const { data } = response;

        data?.vacancies.forEach((vacancy) => {
            vacancy.listedAgo = dayjs(vacancy.Created).fromNow();
        });

        if(!data)
            return false;

        const { 
            numPages: pages = 1, 
            numVacancies: total = 0,
            vacancies: newVacancies = vacancies.value, 
        } = data;


        while((page.value - 1) * limit.value >= total) page.value--;

        numPages.value = pages;
        numVacancies.value = total;
        vacancies.value = newVacancies;

        return true;
    }


    // vacancy api request
    onMounted(async () => {
        const result = await getVacancies({ });

        if(!result) {
            return;
        }
    });


    // stats api request, separate request to speed up page load
    onMounted(async () => {
        // get stats
        // TODO: fix this spaghetti code and get show application working on matches again
        const response = await api({
            method: 'get',
            url: '/e/vacancy/stats/',
            responseType: 'json'
        }).catch(apiCatchError);

        if(!response?.data) {
            return;
        }

        stats.value = response.data?.stats;
    })


    // get vacancies in new order
    const sortVacancies = async (sortParam) => {
        const result = await getVacancies({ sort: sortParam, count: limit.value, pageNum: page.value, filter: filter.value });
        
        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }


    // pagination: change page
    const changePage = async (newPage) => {
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: newPage, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        page.value = newPage;   
    }


    // dropdown watchers

    watch(filter, async (filterValue) => {
        // change which vacancies are display based on isOpen
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: 1, filter: filterValue });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        page.value = 1;
        filter.value = filterValue;
    });


    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        while((page.value - 1) * limit.value >= numVacancies.value) page.value--;

        if(page.value < 0)
        {
            page.value = 0;
        }

        newPage = 1;

        currentFirstVacancy = page.value * limit;
        newPage = currentFirstVacancy / newLimit;

        page.value = newPage;

        const result = await getVacancies({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        limit.value = newLimit;
    });

    watch(sort, sortVacancies);


    // vacancy button actions

    const closeVacancy = async () => {
        const response = await api({
            method: 'put',
            url: `/e/vacancy/close/${ selectedVacancy.value }/`,
            responseType: 'json'
        }).catch(apiCatchError);

        if (!response)
            return false;

        const { data = {} } = response;

		displayModal.value = false;
        window.location.reload();
    }


    const deleteVacancy = async () => {
        const response = await api({
            method: 'delete',
            url: `/e/vacancy/delete/${ selectedVacancy.value }/`,
            responseType: 'json'
        }).catch(apiCatchError);

        if (!response)
            return false;

        const { data = {} } = response;

		displayModal.value = false;
        window.location.reload();
    }

    const updateModalVacancy = async (vacanacyName) => {
        currentModalVacancy = vacanacyName;
        showModal = true;
    } 
</script>



<template>
    <EmployerNavbar page='home' :numNotifs='notifs'></EmployerNavbar>

    <main class='container'>
        <EmployerStatBar :stats='stats' />
        <section class='vacancies-section'>
            <div class='title-bar'>
                <div class='title-bar-left'>
                    <h1 class='title'>Listed Vacancies</h1>
                    <p class='showing' v-if='numVacancies'>Showing {{ (page - 1) * limit + 1 }} to {{ Math.min(page * limit, numVacancies) }} of {{ numVacancies }} </p>
                </div>
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
                            <option value=5 selected>5 per page</option>
                            <option value=10>10 per page</option>
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

            <div class='vacancies'>
                <h3 class='no-vacancies' v-if='numVacancies == 0'>No vacancies to display</h3>
                <div class='vacancy' v-for='vacancy in vacancies' :key='vacancy.id'>
                    <div class='vacancy-left'>
                        <h5 class='vacancy-title' :title='vacancy.title'>
                            <span v-if='!vacancy.IsOpen' class='vacancy-closed'>(closed)</span>
                            {{ vacancy.VacancyName }}
                        </h5>
                        <h5 class='vacancy-new' v-if='vacancy.NewApplications'>{{ vacancy.NewApplications }} New Applications!</h5>
                        <p class='vacancy-new' v-else>No New Applications</p>
                    </div>
                    <div class='vacancy-right'>
                        <div class='vacancy-decisions'>{{ vacancy.AcceptedApplications }} Accepted / {{ vacancy.RejectedApplications }} Rejected</div>
                        <div class='vacancy-listed' :title='vacancy.formattedDate'>Listed {{ vacancy.listedAgo }}</div>

                        <div class='vacancy-button-container'>
                            <router-link :to='`/e/vacancy/edit/${ vacancy.VacancyId }`' class='vacancy-button vacancy-button-blue' v-if='vacancy.IsOpen'>Edit</router-link>
                            <router-link :to='`/e/review/${ vacancy.VacancyId }`' class='vacancy-button vacancy-button-blue'>Review</router-link>
                            <button class='vacancy-button vacancy-button-red' @click='showModal = true; currentModalVacancy = vacancy.VacancyName; selectedVacancy = vacancy.VacancyId' v-if='vacancy.IsOpen'>Close</button>
                            <button class='vacancy-button vacancy-button-red' @click='showDeleteModal = true; currentModalVacancy = vacancy.VacancyName; selectedVacancy = vacancy.VacancyId' v-else>Delete</button>
                        </div>
                        <DeleteVacancyModal v-if='showDeleteModal' :vacancyName='currentModalVacancy' @close-modal='showDeleteModal = false' @deleteVacancy='deleteVacancy' />
                        <CloseApplicationModal v-if='showModal' :vacancyName='currentModalVacancy' @close-modal='showModal = false' @closeApplications='closeVacancy' />
                    </div>
                </div>
            </div>

            <div class='pagination' v-if='numPages > 1'>
                <div class='pag-block pag-start' @click='page > 1 ? changePage(page - 1) : page'><i class="fa-solid fa-angle-left"></i></div>
                <div class='pag-block' @click='changePage(i)' v-for='i in numPages' :key='i' :class='i == page ? "pag-active" : ""'>{{ i }}</div>
                <div class='pag-block pag-end' @click='page < numPages ? changePage(page + 1) : page'><i class="fa-solid fa-angle-right"></i></div>            </div>
        </section>
    </main>

    <button @click='notifs++'>Add notification</button>
    <button @click='notifs < 1 ? 0 : notifs--'>Remove Notification</button>

    <Footer></Footer>

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

    .no-vacancies {
        color: var(--blue);
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
        margin-left: 10px;
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

    .vacancy-button-container {
        display: flex;
        flex-direction: row;
        width: 290px;
        justify-content: space-between;
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

    .vacancy-closed {
        font-weight: bold;
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
