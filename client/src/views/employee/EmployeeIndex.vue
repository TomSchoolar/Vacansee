<script setup>
    import axios from 'axios';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import VacancyCard from '@/components/employee/index/VacancyCard.vue';
    import ApplyVacancyCard from '@/components/employee/index/ApplyVacancyCard.vue';

    import functions from '@/assets/js/jwt';

    import { getAccessToken } from '@/assets/js/jwt';
    import { ref, watch, onMounted } from 'vue';

    // vars init
    const tagsLim = 6;
    const extraTags = '';
    const notifs = ref(2);
    const vacancies = ref([]);

    // dropdown values
        const limit = ref(3);
    const filter = ref('active');
    const sort = ref('dateDesc');

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(0);

    const currentVacancy = ref({});

    const tags = [
        {
            id: 0,
            icon: 'fa-solid fa-book'
        },
        {
            id: 1,
            icon: 'fa-solid fa-code'
        },
        {
            id: 2,
            icon: 'fa-brands fa-python'
        },
        {
            id: 3,
            icon: 'fa-solid fa-school'
        },
        {
            id: 4,
            icon: 'fa-solid fa-briefcase'
        },
        {
            id: 5,
            icon: 'fa-solid fa-database'
        },
    ]

    document.title = 'Home | Vacansee';

    // api request function
    const getVacancies = async (options) => {
        const { count = 3, pageNum = 1, sort = 'dateDesc', filter = 'active' } = options;

        const token = getAccessToken(window.localStorage.accessToken);

        const response = await axios({
            method: 'get',
            url: '/vacancy/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            headers: {
                Authorization: `Bearer: ${ token }`
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
            }
        });

        if(!response || !response.data)
            return false;

        const { data } = response;

        if(!data)
            return false;

        const { 
            vacancies: newVacancies = vacancies.value, 
            numPages: pages = 1, 
            numVacancies: total = 0,
        } = data;


        while((page.value - 1) * limit.value >= total) page.value--;

        numPages.value = pages;
        numVacancies.value = total;
        vacancies.value = newVacancies;
        currentVacancy.value = vacancies.value[0];
        return true;
    }

    // vacancy api request
    onMounted(async () => {
        const result = await getVacancies({ });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });

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
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filterValue });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        filter.value = filterValue;
    });

    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        while((page.value - 1) * limit.value >= numVacancies.value) page.value--;

        if(page.value < 0)
            page.value = 0;

        const result = await getVacancies({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        limit.value = newLimit;
    });

    watch(sort, sortVacancies);

    const apply = () => {
        alert("applied!");
    }

</script>

<template>
    <EmployeeNavbar page='home' :numNotifs='notifs'></EmployeeNavbar>

    <div class='container'>
        <div class='left'>
            <h1 class='title'>Vacancies</h1>
            <div class='search-group'>
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input name='searchbar' class='search' type='text' placeholder='Search..'> 
            </div>

            
            <div class='select-group'>
                <select v-model='filter' aria-label='filter vacancies' id='filter'>
                    <option value='active' selected>show active adverts</option>
                    <option value='all'>show all adverts</option>
                    <option value='closed'>show closed adverts</option>
                </select>
            </div>


            <div class='select-group'>
                <select v-model='limit' aria-label='set page size' id='limit'>
                    <option value=3 selected>3 per page</option>
                    <option value=6>6 per page</option>
                    <option value=9>9 per page</option>
                    <option value=12>12 per page</option>
                </select>
            </div>


            <div class='select-group'>
                <select v-model='sort' aria-label='sort vacancies' id='sort'>
                    <option value='dateDesc' selected>latest first</option>
                    <option value='dateAsc'>oldest first</option>
                    <option value='titleAsc'>title (a-z)</option>
                    <option value='titleDesc'>title (z-a)</option>
                </select>
            </div>


            <div class='filter-tags-row'>
                    <th class='filter-tags-header'> Selected Tags </th>
                    <div class='filter-tag'>
                        <i class='fa-solid fa-book tag'></i> 
                    </div>
            </div>


            <!-- table below in place of vacancy cards -->
            <div class='vacancy-container'>
                <VacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' :tags='tags' />
            </div>
                    

            <button type='button' class='button arrow-btn' @click='page < numPages ? changePage(page + 1) : page'>
            <i class="fa-solid fa-circle-arrow-right"></i>
            </button>
            <button type='button' class='button arrow-btn' @click='page > 1 ? changePage(page - 1) : page'>
                <i class="fa-solid fa-circle-arrow-left"></i>
            </button>
            
        </div>

        <div class='right'>
            <button type='button' class='button apply-btn' @click= apply>Apply Now!</button>
            <ApplyVacancyCard :vacancy='currentVacancy' :tags='tags' @newVacancy='(newVacancy) => { currentVacancy = newVacancy }' />
        </div>
    </div>
    
    
</template>


<style scoped>
    select {
        border: 2px solid;
        float:right;
        font-size:12px;
        margin: 1px;
        padding: 3px;
    }

    th {
        font-weight: normal;
        padding-bottom: 0px;
        padding-top: 0px;
    }

    .arrow-btn {
        background-color: white;
        border:none;
        float: right;
        font-size: 20px;
        padding: 2px;
    }

    .apply-btn {
        background-color: white;
        border-radius: 10px;
        margin-bottom: 40px !important;
    }

    .button {
        border: 2px solid;
        border-radius: 15px;
        color: black;
        cursor: pointer;
        display: inline-block;
        font-size: 35px;
        margin: 2px;
        padding-left: 30px;
        padding-right: 30px;
        padding-top: 10px;
        padding-bottom: 10px;
        text-align: center;
        text-decoration: none;
        transition-duration: 0.4s;
    }

    .button:active {
        background-color:#D3D3D3;
        font-size: 50%;
    }

    .button:hover {
        background-color:#D3D3D3;
    }

    .container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
    }

    .filter-tag {
        font-size: 32px;
    }

    .filter-tags-header {
        width: 70px;
        text-overflow: wrap;
        border-right: 1.5px solid black;
        padding-right: 10px;
        margin-right: 15px;
    }

    .filter-tags-row {
        display: flex;
        align-items: center;
        border: 1px solid black;
        width: calc(100% - 40px);
        position: relative;
        top: 5px;
        margin-bottom: 5px;
        padding: 7px 20px;
        border-radius: 15px;
    }

    .left {
        height: 100%;
        padding: 10px 50px 0 50px;
        width: 70%;       
    }

    .right {
        border-left: 3px solid;
        padding-top: 20px;
        width: 30%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .search {
        border-radius: 8px;
        float: left;
        font-size: 12px;
        margin: 1px;
        padding: 5px 5px 5px 25px;
    }

    .search-icon {
        position: absolute;
        left: 7px;
        top: 6px;
        color: black;
        font-size: 17px;
    }

    .search-group {
        position: relative;
    }

    .select-group {
        flex-direction: column;
    }

    .tags-header {
        border-right: 2px solid; 
        width: 10%; 
        padding-right: 10px; 
        font-size: 18px;
    }

    .title {
        text-align: left;  
        margin-top:0; 
        border-bottom: 1px solid;
    }

    .vacancy-container {
        width: 100%; 
        text-align: center; 
        display: flex; 
        justify-content: space-between; 
        flex-wrap: wrap;
    }
</style>
