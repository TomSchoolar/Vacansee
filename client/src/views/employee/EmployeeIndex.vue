<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import VacancyCard from '@/components/employee/index/VacancyCard.vue';
    import ApplyVacancyCard from '@/components/employee/index/ApplyVacancyCard.vue';

    import { computed, onMounted, ref, watch } from 'vue';

    // vars init
    const tagsLim = 6;
    const extraTags = '';
    const notifs = ref(2);
    const vacancies = ref([]);

    // dropdown values
    const emptyCards = ref(0);
    const cardsPerRow = ref(1);
    const filter = ref('active');
    const sort = ref('dateDesc');
    const limitMultiplier = ref(1);

    const limit = computed(() => {
        return limitMultiplier.value * cardsPerRow.value;
    });

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(1);

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
        const { count = limit.value, pageNum = 1, sort = 'dateDesc', filter = 'active' } = options;
        
        const response = await api({
            method: 'get',
            url: '/vacancy/',
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


        const { 
            vacancies: newVacancies = vacancies.value, 
            numPages: pages = 1, 
            numVacancies: total = 0,
        } = response.data;

        while((page.value - 1) * limit.value >= total && page.value > 1) page.value--;

        numVacancies.value = total;
        vacancies.value = newVacancies;
        currentVacancy.value = vacancies.value[0] ?? {};

        emptyCards.value = limit.value - vacancies.value.length;

        return true;
    }
    
    // vacancy api request
    onMounted(async () => {
        console.log(document.querySelector('.vacancy-container').offsetWidth)
        const resizeFunc = () => {
            cardsPerRow.value = Math.floor((document.querySelector('.vacancy-container').offsetWidth - 25) / 449);
        }

        setTimeout(() => {
            resizeFunc();
            window.addEventListener("resize", resizeFunc);
        }, 5);
    });

    // get vacancies in new order
    const sortVacancies = async (sortParam) => {
        const result = await getVacancies({ sort: sortParam, count: limit.value, pageNum: page.value, filter: filter.value });
        
        if(!result) {
            return;
        }

    }

    // pagination: change page
    const changePage = async (newPage) => {
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: newPage, filter: filter.value });

        if(!result) {
            return;
        }

        page.value = newPage;   
    }

    // dropdown watchers
    watch(filter, async (filterValue) => {
        // change which vacancies are display based on isOpen
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filterValue });

        if(!result) {
            return;
        }

    });

    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        while((page.value - 1) * limit.value >= numVacancies.value && page.value > 1) page.value--;

        const result = await getVacancies({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value });

        if(!result) {
            return;
        }
    });

    watch(sort, sortVacancies);

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
                <select v-model='limitMultiplier' aria-label='set page size' id='limit'>
                    <option value='1'>{{ cardsPerRow }} per page</option>
                    <option value='2'>{{ cardsPerRow * 2 }} per page</option>
                    <option value='3'>{{ cardsPerRow * 3 }} per page</option>
                    <option value='4'>{{ cardsPerRow * 4 }} per page</option>
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

            <div class='vacancy-container'>
                <h3 class='no-vacancies' v-if='numVacancies == 0'>There are no vacancies currently accepting applications</h3>
                <VacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' :tags='tags' />
                <div v-for='i in emptyCards' :key='i' class='card-placeholder'></div>
            </div>

                  

            <button type='button' class='button arrow-btn' @click='page < numPages ? changePage(page + 1) : page'>
            <i class="fa-solid fa-circle-arrow-right"></i>
            </button>
            <button type='button' class='button arrow-btn' @click='page > 1 ? changePage(page - 1) : page'>
                <i class="fa-solid fa-circle-arrow-left"></i>
            </button>
            
        </div>

        <div class='right'>
            <ApplyVacancyCard :vacancy='currentVacancy' :tags='tags' :favourited='false' />
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

    .card-placeholder {
        width: 449px;
        height: 1px;
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
        border-radius: 7px;
        margin: 10px 0 25px 0;
    }

    .left {
        height: 100%;
        padding: 10px 50px 0 50px;
        width: 70%;       
    }

    .no-vacancies {
        color: var(--jet);
        font-weight: 500;
        position: relative;
        top: 25px;
        font-size: 18px;
        font-style: italic;
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
        bottom: 2px;
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
        display: flex; 
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;
        padding-left: 25px;
    }

    .vacancy-container:deep(.card) {
        margin: 12px 25px 12px 0;
    }
</style>
