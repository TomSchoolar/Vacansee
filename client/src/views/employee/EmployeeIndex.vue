<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import Footer from '@/components/partials/CompactFooter.vue';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import VacancyCard from '@/components/employee/index/VacancyCard.vue';
    import NoCardsModal from '@/components/employee/index/NoCardsModal.vue';
    import TagSearchModal from '@/components/employee/index/TagSearchModal.vue';
    import TutorialModal from '@/components/employee/tutorial/TutorialModal.vue';
    import ApplyVacancyCard from '@/components/employee/index/ApplyVacancyCard.vue';


    import { computed, onMounted, ref, watch } from 'vue';


    // vars init
    const tagsLim = 6;
    const extraTags = '';
    //const notifs = ref(2);
    let initialReq = true;
    const vacancies = ref([]);
    const cardAction = ref('');
    const showModal = ref(false);
    const showModalNoCards = ref(false);

    //tutorial values
	const isNewUser = ref(window.localStorage.getItem('newUserEmployeeIndex') === 'true');

    // dropdown values
    const emptyCards = ref(0);
    const cardsPerRow = ref(1);
    const filter = ref('active');
    const sort = ref('dateDesc');
    const tagsFilterRaw = ref([]);
    const limitMultiplier = ref(1);
    const tagsFilter = ref("null");

    const searchBarValue = ref('');

    const limit = computed(() => {
        return limitMultiplier.value * cardsPerRow.value;
    });

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(1);

    // tags
    const options = ref([]);
    const currentVacancy = ref({});


    document.title = 'Home | Vacansee';


    const getTags = async () => {
        const response = await api({
            method: 'get',
            url: '/v1/vacancies/tags/',
            responseType: 'json',
        }).catch(apiCatchError);

        if(!response?.data)
            return false;

        options.value = response.data;

        return true;
    }


    // api request function
    const getVacancies = async (options) => {
        const { count = limit.value, pageNum = 1, sort = 'dateDesc', filter = 'active', newCard = false, tagsFilter: tagsFilterParam = 'null', searchValue = "" } = options;
        
        const response = await api({
            method: 'get',
            url: '/v1/vacancies/',
            responseType: 'json',
            params: {
                sort,
                count,
                filter,
                pageNum,
                searchValue,
                tagsFilter: tagsFilterParam
            }
        }).catch(apiCatchError);

        if(!response?.data)
            return false;

        let { 
            vacancies: newVacancies = vacancies.value, 
            numPages: pages = 1, 
            numVacancies: total = 0,
            triedTags: haveTriedTags = triedTags.value
        } = response.data;
        
        if(newVacancies) {
            newVacancies = newVacancies.map((vacancy) => {
                let obj = { ...vacancy, tags: vacancy.Tags };
                delete obj['Tags']
                return obj;
            });
        } else {
            newVacancies = vacancies.value;
        }


        while((page.value - 1) * limit.value >= total && page.value > 1) page.value--;

        numPages.value = pages;
        numVacancies.value = total;
        vacancies.value = newVacancies;

        if(currentVacancy?.value && Object.keys(currentVacancy.value).length === 0 || newCard) {
            // if initial fetch, then update current vacancy
            currentVacancy.value = vacancies.value[0] ?? {};
        }

        if(numVacancies.value > 0)
            emptyCards.value = limit.value - vacancies.value.length;
        else
            emptyCards.value = 0;
        
        if(haveTriedTags){
            tagsFilter.value = 'null';
            tagsFilterRaw.value = [];
            showModalNoCards.value = true;
        }

        return true;
    }


    const updateData = async (newData) => {
        cardAction.value = null;
        await getVacancies({ pageNum: page.value, sort: sort.value, filter: filter.value, newCard: true });
    }

    
    // vacancy api request
    onMounted(async () => {
        const resizeFunc = () => {
            cardsPerRow.value = Math.max(Math.floor((document.querySelector('.vacancy-container').offsetWidth - 25) / 449), 1);
        }

        setTimeout(async () => {
            resizeFunc();
            window.addEventListener("resize", resizeFunc);
            getTags();
            getVacancies({ });
        }, 50);

        
        window.addEventListener('keyup', (event) => {
            if(event.key == 'ArrowLeft') {
                cardAction.value = 'reject';
            } else if(event.key == 'ArrowRight') {
                cardAction.value = 'apply';
            } else if(event.key == 'ArrowUp') {
                cardAction.value = 'favourite';
            }
        });
    });


    // get vacancies in new order
    const sortVacancies = async (sortParam) => {
        const result = await getVacancies({ sort: sortParam, count: limit.value, pageNum: page.value, filter: filter.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });
        
        if(!result) {
            return;
        }

    }

    // pagination: change page
    const changePage = async (newPage) => {
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: newPage, filter: filter.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }

        page.value = newPage;   
    }


    const tagSearch = async (value) => {

        tagsFilterRaw.value = value;

        let i = 0;

        tagsFilter.value = "";

        for(i = 0; i < value.length; i++){
            tagsFilter.value = tagsFilter.value + (value[i].toString());
            if(i != value.length-1){
                tagsFilter.value = tagsFilter.value + ",";
            }
        }

        if(value.length == 0) {
            tagsFilter.value = 'null';
            tagsFilterRaw.value = [];
        }

        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filter.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }
    }


    // dropdown watchers
    watch(filter, async (filterValue) => {
        // change which vacancies are display based on isOpen
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filterValue, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }

    });

    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        if(initialReq) {
            initialReq = false;
            return;
        }

        while((page.value - 1) * limit.value >= numVacancies.value && page.value > 1) page.value--;

        const result = await getVacancies({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }
    });

    const searchBarValueUpdated = async (value) => {
        searchBarValue.value = value;

        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filter.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }
    }

    watch(sort, sortVacancies);

    const finishTutorial = () => {
        window.localStorage.removeItem('newUserEmployeeIndex');
        isNewUser.value = false;
    }
</script>

<template>
    <!-- <EmployeeNavbar page='home' :numNotifs='notifs'></EmployeeNavbar> -->
    <EmployeeNavbar page='home' ></EmployeeNavbar>

    <div class='container'>
        <div class='left'>
            <h1 class='title'>Vacancies</h1>
            <div class='search-group'>
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input name='searchbar' v-model='searchBarValue' @change='searchBarValueUpdated(searchBarValue)' class='search' type='text' placeholder='Search..'> 
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
                <button type='button' class='button arrow-btn' @click='showModal = true'>
                    <th>Select Tags</th>
                </button>
                <button type='button' class='button arrow-btn' @click='tagSearch([])'>
                    <th>Remove Tags</th>
                </button>

                <div class='selected-tags'>
                    <h1 class='tags-title'>Selected Tags:</h1>
                    <span class='no-tags' v-if='tagsFilter == "null"'>None</span>
                    <i class='tag' v-for='tag in tagsFilterRaw' v-bind:key='tag.id' :class='options[tag-1]["icon"]' :title='tag.text'></i>
                </div>
                    
            </div>

            <NoCardsModal v-show='showModalNoCards' @close-modal='showModalNoCards = false' />
            <TagSearchModal v-show='showModal' @search='tagSearch' @close-modal='showModal = false' />

            <div class='vacancy-container'>
                <h3 class='no-vacancies' v-if='numVacancies == 0'>There are no vacancies currently accepting applications</h3>
                {{ vacancies.length > 0 ? vacancies[0].Tags : '' }}
                <VacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' :tags='options' />
                <div v-for='i in emptyCards' :key='i' class='card-placeholder'></div>
            </div>

                  
            <div class='pagination' v-if='numPages > 1'>
                <div class='pag-block pag-start' @click='page > 1 ? changePage(page - 1) : page'><i class="fa-solid fa-angle-left"></i></div>
                <div class='pag-block' @click='changePage(i)' v-for='i in numPages' :key='i' :class='i == page ? "pag-active" : ""'>{{ i }}</div>
                <div class='pag-block pag-end' @click='page < numPages ? changePage(page + 1) : page'><i class="fa-solid fa-angle-right"></i></div>            
            </div>
            
        </div>

        <div class='divider'></div>

        <div class='right'>
            <ApplyVacancyCard :vacancy='currentVacancy' :tags='options' :favourited='false' :cardAction='cardAction' @update='updateData' />
        </div>
    </div>
    

    <TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Employee index</h3>
        </template>
        <template #modal-body>
            <div class='modal-body'>
                <p class='desc'>
                    The home page displays a list of adverts posted by companies in the first column on the left of the page, just below the navigation bar.
                    Adverts can be sorted using the filters on the top right.

                </p>>
                <p class='desc'>
                    The action card, on the right side of the page, is where you can interact with vacancies.
                </p>
                <p class='desc'>
                    You can ignore a vacancy by clicking the red cross on the vacancy card,
                </p>
                <p class='desc'>
                    add it to your favourite by clicking the star button next to ignore,
                </p>
                <p class='desc'>
                    or send an application for it by clicking the green tick next to unfavourite.
                </p>
            </div> 

        </template>
    </TutorialModal>
    
    
    <Footer></Footer>
    
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
        font-size: 10px;
        padding: 2px;
    }

    .apply-btn {
        background-color: white;
        border-radius: 10px;
        margin-bottom: 40px !important;
    }

    .button {
        border: 2px solid;
        border-radius: 7px;
        color: black;
        cursor: pointer;
        display: inline-block;
        font-size: 13px;
        margin: 2px 4px;
        padding: 7px 15px;
        text-align: center;
        text-decoration: none;
    }

    .button:active, .button:focus, .button:hover {
        background-color:#eee;
    }

    .card-placeholder {
        width: 449px;
        height: 1px;
    }

    .container {
        display: flex;
        justify-content: center;
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
        border-right: 3px solid black;
        min-height: calc(100vh - 210px);
        margin-bottom: 30px;
    }

    .no-vacancies {
        color: var(--jet);
        font-weight: 500;
        position: relative;
        top: 25px;
        font-size: 18px;
        font-style: italic;
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
    
    .no-tags {
        position: relative;
        top: 0.5px;
    }

    .right {
        padding-top: 20px;
        width: 30vw;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .right div {
        position: relative;
        top: 100px;
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

    .selected-tags {
        display: flex;
        align-items: center;
        margin-left: 12px;
        height: 45px;
    }

    .selected-tags .tag {
        font-size: 22px;
        margin: 0 7px;
    }

    .tags-header {
        border-right: 2px solid; 
        width: 10%; 
        padding-right: 10px; 
        font-size: 18px;
    }

    .tags-title {
        margin: 0 10px 0 0;
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
