<script setup>
    import api, { apiCatchError } from '@/assets/js/api';

    import { onMounted, ref, watch } from 'vue';
    
    const emits = defineEmits(['selectVacancy']);

    //let { numVacancies = 0, vacancies = [] } = defineProps(['numVacancies', 'vacancies']);

    //const sortVacancies = ref('matchesDesc');

    const getMatches = (vacancy) => {
        alert('show matches for '+ vacancy.title);
    };

    const vacancies = ref([]);
    const sort = ref('matchesDesc');

    const numVacancies = ref(0);

    // api request function
    const getVacancies = async (options) => {
        const { sort = 'matchesDesc' } = options;

        const response = await api({
            method: 'get',
            url: '/v1/e/matches/',
            responseType: 'json',
            params: {
                sort
            }
        }).catch(apiCatchError);

        if(!response || !response.data)
            return false;

        const { data } = response;

        if(!data)
            return false;

        const {
            vacancies: newVacancies = vacancies.value,
            numVacancies: total = 0,
        } = data;

        numVacancies.value = total;
        vacancies.value = newVacancies;

        return true;
    }

    onMounted(async () => {
        const result = await getVacancies({ });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });

    // sort vac
    const sortVacancies = async (sortParam) => {
        const result = await getVacancies({ sort: sortParam });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }

    watch(sort, sortVacancies);

    /*const selectVacancy = (vacancy) => {
        $emit('select-vacancy', vacancy);
    }*/


</script>

<template>
    <section class='column'>
        <div class='header'> 
            <div class='header-row'>
                <h2 class='header-title'> Vacancies ({{vacancies.length}}) </h2>
                
                <!-- download button -->
                <!-- <button type='button' class='button download-button' @click='download'>Download Report</button> -->
            </div>

            <div class='header-row'>
                <div class='search-group'>
                    <i class="fa-solid fa-magnifying-glass search-icon"></i>
                    <input name='searchbar' type='text' placeholder='Search..' class='search' /> 
                </div>
                
                <div class='select-group'>
                    <div class='select-label'> 
                        <label for='vacancy-sort'>sort by:</label>
                    </div>

                    <select v-model='sort' aria-label='sort vacancies' id='vacancy-sort' class='sort'>
                        <option value='matchesDesc' selected>number of matches</option>
                        <option value='dateDesc' >latest first</option>
                        <option value='dateAsc'>oldest first</option>
                        <option value='titleAsc'>title (a-z)</option>
                        <option value='titleDesc'>title (z-a)</option>
                    </select>
                </div>
            </div>
        </div>

        <div class='vacancies'>
            <h3 class='no-vacancies' v-if='numVacancies == 0'>No vacancies to display</h3>
            
            <div class='vacancy' v-else v-for='vacancy in vacancies' :key='vacancy.VacancyName' @click='$emit("selectVacancy", vacancy)'>
                <span class='vacancy-title' :title='( !vacancy.IsOpen ? "(closed) " : "" ) + vacancy.VacancyName'>
                    <span class='vacancy-closed' v-if='!vacancy.IsOpen'>(closed) </span> 
                    {{ vacancy.VacancyName }} 
                </span>

                <span class='vacancy-matches' v-if='vacancy.MatchesCount != undefined'> {{ vacancy.MatchesCount }} matches</span>
            </div>
        </div>
    </section>
</template>

<style scoped>
    .button {
        background-color: var(--slate);
        border: 2px solid black;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        font-family: var(--font);
        font-size: 13px;
        min-width: 140px;
    }

    .column {
        min-width: 480px;
        flex-grow: 1;
        border-right: 1px solid var(--jet);
        height: calc(100vh - 157px);
    }

    .download-button {
        position: relative;
        bottom: 3px;
    }

    .header {
        display: flex;
        flex-direction: column;
        padding: 10px 20px 5px 20px;
        border-bottom: 1px solid var(--jet);
    }

    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-top: 8px;
    }

    .header-title {
        font-weight: 500;
        font-size: 26px;
        margin: 0;
        position: relative;
    }

    .no-vacancies {
        color: var(--blue);
    }

    .select-group {
        position: relative;
        bottom: 8px;
    }

    .vacancies {
        height: calc(100% - 121px);
        overflow-y: scroll;
    }

    .vacancy {
        background-color: white;
        border-bottom: 1px solid var(--jet);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        font-size: 18px;
    }

    .vacancy:active, .vacancy:focus, .vacancy:hover  {
        background-color: #eee;
        cursor: pointer;
    }

    .vacancy-closed {
        font-weight: 600;
    }

    .vacancy-matches {
        font-size: 14px;
        width: 90px;
        color: var(--slate);
        font-style: italic;
    }


    .vacancy-title {
        text-overflow: ellipsis !important; 
        max-width: calc(100% - 90px);
        overflow: hidden;
        white-space: nowrap;
    }
</style>