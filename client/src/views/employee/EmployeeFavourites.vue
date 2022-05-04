<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import ApplyVacancyCard from '@/components/employee/index/ApplyVacancyCard.vue';
    import TutorialModal from '@/components/employee/tutorial/TutorialModal.vue';

    
    import { computed, onMounted, ref, watch } from 'vue';


    // vars init
    const tagsLim = 6;
    const extraTags = '';
    const notifs = ref(2);
    const emptyCards = ref(0);
    const vacancies = ref([]);
    const cardsPerRow = ref(1);
    
    // tutorial values
    const isNewUser = ref(window.localStorage.getItem('newUserFavourites') == null);

    // dropdown values
    const sort = ref('dateDesc');
    const limitMultiplier = ref(1);

    const limit = computed(() => {
        return limitMultiplier.value * cardsPerRow.value;
    });

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(1);

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

    document.title = 'Favourites | Vacansee';

        // api request function
    const getFavourites = async (options) => {
        const { count = limit.value, pageNum = 1, sort = 'dateDesc' } = options;


        const response = await api({
            method: 'get',
            url: '/favourites/',
            responseType: 'json',
            params: {
                sort,
                count,
                pageNum
            }
        }).catch(apiCatchError);

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

        emptyCards.value = numVacancies > 0 ? limit.value - vacancies.value.length : 0;

        return true;
    }

    // vacancy api request
    onMounted(async () => {
        const resizeFunc = () => {
            cardsPerRow.value = Math.floor(document.querySelector('.vacancy-container').offsetWidth / 449);
        }

        resizeFunc();
        window.addEventListener("resize", resizeFunc);     

        const result = await getFavourites({ });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });

    // get vacancies in new order
    const sortVacancies = async (sortParam) => {
        const result = await getFavourites({ sort: sortParam, count: limit.value, pageNum: page.value });
        
        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }

    // pagination: change page
    const changePage = async (newPage) => {
        const result = await getFavourites({ sort: sort.value, count: limit.value, pageNum: newPage });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        page.value = newPage;   
    }

    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        while((page.value - 1) * limit.value >= numVacancies.value && page.value > 1) page.value--;

        if(page.value < 0)
            page.value = 0;

        const result = await getFavourites({ sort: sort.value, count: newLimit, pageNum: page.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });

    watch(sort, sortVacancies);

    const updatePage = () => {
        window.location.reload();
    }

    const finishTutorial = () => {
        window.localStorage.setItem('newUserFavourites', false);
        isNewUser.value = false;
    }

</script>

<template>
    <EmployeeNavbar page='favourites' :numNotifs='notifs'></EmployeeNavbar>

    <div class='container'>
        <div class='main'>
            <h1 class='title'>Favourites</h1>
            <div class='search-group'>
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input name='searchbar' class='search' type='text' placeholder='Search..'/> 
            </div>

            <div class="select-row">
                <div class='select-group'>
                    <select v-model='limitMultiplier' aria-label='set page size' id='limit'>
                        <option :value='1' selected>{{ cardsPerRow }} per page</option>
                        <option :value='2'>{{ cardsPerRow * 2 }} per page</option>
                        <option :value='3'>{{ cardsPerRow * 3 }} per page</option>
                        <option :value='4'>{{ cardsPerRow * 4 }} per page</option>
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
            </div>

            <div class='filter-tags-row'>
                    <th class='filter-tags-header'> Selected Tags </th>
                    <div class='filter-tag'>
                        <i class='fa-solid fa-book tag'></i> 
                    </div>
            </div>
            <div class="vacancy-container">
                <h3 class='no-vacancies' v-if='numVacancies == 0'>You haven't got any favourites atm...</h3>
                <ApplyVacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' :favourited='true' :tags='tags' />
                <div v-for='i in emptyCards' :key='i' class='card-placeholder'></div>
            </div>

            <button type='button' class='button arrow-btn' @click='page < numPages ? changePage(page + 1) : page'>
            <i class="fa-solid fa-circle-arrow-right"></i>
            </button>
            <button type='button' class='button arrow-btn' @click='page > 1 ? changePage(page - 1) : page'>
                <i class="fa-solid fa-circle-arrow-left"></i>
            </button>
            
        </div>
    </div>

    <TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Employee Favourites</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    You can review vacancies which are added to your favourites here, and sort them using filters on the top right.
                </p>
				<p class='desc'>
					You can also reject, unfavourite, and accept vacancies by clicking the corresponding buttons on each card.
                </p>
            </div>
        </template>
    </TutorialModal>

</template>


<style scoped>
    *:deep(.card) {
        margin-right: 25px;
    }

    select {
        border: 2px solid;
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
        padding: 0 40px;
        width: calc(100vw - 80px);
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
        margin: 10px 0 25px 0;
        padding: 7px 20px;
        border-radius: 7px;
    }

    .no-vacancies {
        color: var(--jet);
        font-weight: 500;
        position: relative;
        top: 25px;
        font-size: 18px;
        font-style: italic;
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
        margin-left: 2px;
    }

    .select-row {
        display: flex;
        flex-grow: 1;
        justify-content: flex-end;
        padding-right: 2px;
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
    }
</style>
