<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import Footer from '@/components/partials/Footer.vue';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import NoCardsModal from '@/components/employee/index/NoCardsModal.vue';
    import TagSearchModal from '@/components/employee/index/TagSearchModal.vue';
    import TutorialModal from '@/components/employee/tutorial/TutorialModal.vue';
    import ApplyVacancyCard from '@/components/employee/index/ApplyVacancyCard.vue';

    import { computed, onMounted, ref, watch } from 'vue';

    const showModalNoCards = ref(false);
    const showModal = ref(false);

    // vars init
    const tagsLim = 6;
    const extraTags = '';
    //const notifs = ref(2);
    const emptyCards = ref(0);
    const vacancies = ref([]);
    const cardsPerRow = ref(1);
    
    // tutorial values
    const isNewUser = ref(window.localStorage.getItem('newUserFavourites') == null);

    const searchBarValue = ref("");

    // dropdown values
    const sort = ref('dateDesc');
    const limitMultiplier = ref(1);

    const limit = computed(() => {
        return limitMultiplier.value * cardsPerRow.value;
    });

    const tagsFilter = ref("null");
    const tagsFilterRaw = ref([]);
    const haveTriedTags = ref();

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(1);

    const getTags = async () => {
        const response = await api({
            method: 'get',
            url: '/v1/vacancies/tags/',
            responseType: 'json',
        }).catch(apiCatchError);

        if(!response || !response.data)
            return false;

        const { data } = response;

        if(!data)
            return false;

        tags.value = response.data;

        return true;
    }

    const tags = ref([]);

    document.title = 'Favourites | Vacansee';

        // api request function
    const getFavourites = async (options) => {
        const { count = limit.value, pageNum = 1, sort = 'dateDesc', tagsFilter = 'null', searchValue = "" } = options;


        const response = await api({
            method: 'get',
            url: '/v1/favourites/',
            responseType: 'json',
            params: {
                sort,
                count,
                pageNum,
                tagsFilter,
                searchValue
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
            triedTags: haveTriedTags = triedTags.value
        } = data;


        while((page.value - 1) * limit.value >= total) page.value--;

        numPages.value = pages;
        numVacancies.value = total;
        vacancies.value = newVacancies;

        if(numVacancies.value > 0)
            emptyCards.value = numVacancies.value > 0 ? limit.value - vacancies.value.length : 0;
        else
            emptyCards.value = 0;

        if(haveTriedTags){
            showModalNoCards.value = true;
            tagSearch([]);
        }

        return true;
    }

    // vacancy api request
    onMounted(async () => {
        const resizeFunc = () => {
            cardsPerRow.value = Math.floor(document.querySelector('.vacancy-container').offsetWidth / 449);
        }

        resizeFunc();
        window.addEventListener("resize", resizeFunc);     

        getTags();

        const result = await getFavourites({ });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });

    // get vacancies in new order
    const sortVacancies = async (sortParam) => {
        const result = await getFavourites({ sort: sortParam, count: limit.value, pageNum: page.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });
        
        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }

    // pagination: change page
    const changePage = async (newPage) => {
        const result = await getFavourites({ sort: sort.value, count: limit.value, pageNum: newPage, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

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

        const result = await getFavourites({ sort: sort.value, count: newLimit, pageNum: page.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });


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
            tagsFilter.value = "null";
            tagsFilterRaw.value = [];
        }

        const result = await getFavourites({ sort: sort.value, count: limit.value, pageNum: page.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }
    }

    const searchBarValueUpdated = async (value) => {
        searchBarValue.value = value;

        const result = await getFavourites({ sort: sort.value, count: limit.value, pageNum: page.value, tagsFilter: tagsFilter.value, searchValue: searchBarValue.value });

        if(!result) {
            return;
        }
    }

    watch(sort, sortVacancies);

    const updatePage = async () => {
        await getFavourites({ sort: sort.value, pageNum: page.value })
    }

    const finishTutorial = () => {
        window.localStorage.setItem('newUserFavourites', false);
        isNewUser.value = false;
    }

</script>

<template>
    <!-- <EmployeeNavbar page='favourites' :numNotifs='notifs'></EmployeeNavbar> -->
    <EmployeeNavbar page='favourites' ></EmployeeNavbar>

    <div class='container'>
        <div class='main'>
            <h1 class='title'>Favourites</h1>
            <div class='search-group'>
                <i class="fa-solid fa-magnifying-glass search-icon"></i>
                <input name='searchbar' v-model='searchbar' @change='searchBarValueUpdated(searchbar)' class='search' type='text' placeholder='Search..'/> 
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
                <button type='button' class='button arrow-btn' @click='showModal = true'>
                    <th>Select Tags</th>
                </button>
                <button type='button' class='button arrow-btn' @click='tagSearch("")'>
                    <th>Remove Tags</th>
                </button>

                <div class='selected-tags'>
                    <h1 class='tags-title'>Selected Tags:</h1>
                    <span class='no-tags' v-if='tagsFilter == "null"'>None</span>
                    <i class='tag' v-for='tag in tagsFilterRaw' v-bind:key='tag.id' :class='tags[parseInt(tag-1)]["icon"]' :title='tag.text'></i>
                </div>
            </div>

            <NoCardsModal v-show='showModalNoCards' @close-modal='showModalNoCards = false' />

            <TagSearchModal v-show='showModal' @search='tagSearch' @close-modal='showModal = false' />

            <div class="vacancy-container">
                <h3 class='no-vacancies' v-if='numVacancies == 0'>You haven't got any favourites atm...</h3>
                <ApplyVacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' :favourited='true' :tags='tags' @update='updatePage' />
                <div v-for='i in emptyCards' :key='i' class='card-placeholder'></div>
            </div>

            <div class='pagination' v-if='numPages > 1'>
                <div class='pag-block pag-start' @click='page > 1 ? changePage(page - 1) : page'><i class="fa-solid fa-angle-left"></i></div>
                <div class='pag-block' @click='changePage(i)' v-for='i in numPages' :key='i' :class='i == page ? "pag-active" : ""'>{{ i }}</div>
                <div class='pag-block pag-end' @click='page < numPages ? changePage(page + 1) : page'><i class="fa-solid fa-angle-right"></i></div>            
            </div>
            
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


    <Footer></Footer>

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
        padding: 0 40px;
        width: calc(100vw - 80px);
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
        top: 1.5px;
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
    }
</style>
