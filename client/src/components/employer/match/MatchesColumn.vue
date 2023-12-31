<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import MatchCard from '@/components/employer/match/MatchCard.vue';
    
    import { ref, watch, toRef } from 'vue';

    const props  = defineProps(['selectedVacancy', 'selectedVacancyName']);
    const emits = defineEmits(['show-application', 'update-match-stats'])

    const matches = ref([]);
    const numMatches = ref(0);
    const selectedProfile = ref();
    const searchBarValue = ref("");
    const selectedVacancy = ref(0);
    const sort = ref('LastNameAsc');
    const selected = toRef(props, 'selectedVacancy');

    //download button
    /*
    const download = () => {
        alert("downloaded!");
    }*/

    // api request function
    const getMatches = async (options) => {
        const { sort = 'LastNameAsc', vID = selected.value, searchValue = "" } = options;

        const response = await api({
            method: 'get',
            url: `/v1/e/matches/${ vID }/`,
            responseType: 'json',
            params: {
                vID,
                sort,
                searchValue
            }
        }).catch(apiCatchError);

        if(!response || !response.data)
            return false;

        const { data } = response;

        if(!data)
            return false;

        const {
            matches: newMatches = matches.value,
            numMatches: total = 0,
        } = data;

        numMatches.value = total;
        matches.value = newMatches;

        return true;
    }

    // sort vac
    const sortMatches = async (sortParam) => {
        const result = await getMatches({ sort: sortParam, searchValue: searchBarValue.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }

    const updateMatches = async (newVac) => {
        const result = await getMatches({ sort: sort.value, vID: newVac, searchValue: searchBarValue.value })

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        selectedVacancy.value = newVac;
    }

    const onUnmatch = async () => {
        updateMatches(selectedVacancy.vacancyId);
    }

    const updateCard = (nextProfile) => {
        emits('show-application', nextProfile);
    }

    watch(selectedVacancy, updateMatches);

    watch(selected, (value) => {
        selectedVacancy.value = selected.value;

        searchBarValue.value = "";
    });

    watch(sort, sortMatches);

    const searchBarValueUpdated = async (value) => {
        searchBarValue.value = value;

        const result = await getMatches({ sort: sort.value, searchValue: searchBarValue.value })

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    }

</script>

<template>
    <section class='matches-column'>
        <div class='header'>
            <div class='header-row'>
                <h2 class='header-title'> Matches ({{ numMatches }})</h2>
                
                <!-- download button -->
                <!-- <button type='button' class='button match-download-button' id='download-button' @click='download'>Download All</button> -->
            </div>

            <div class='header-row'>
                <div class='search-group'>
                    <i class="fa-solid fa-magnifying-glass search-icon"></i>
                    <input name='searchbar' v-model='searchbar' @change='searchBarValueUpdated(searchbar)' type='text' placeholder='Search..' class='search' /> 
                </div>

                <div class='select-group'>
                    <div class='select-label'> 
                        <label for='sort-matches'>sort by:</label>
                    </div>

                    <select v-model='sort' aria-label='sort matches' id='sort-matches' class='sort'>
                        <option value='LastNameAsc' selected>Last name (a-z)</option>
                        <option value='LastNameDesc'>Last name (z-a)</option>
                        <option value='FirstNameAsc'>First name (a-z)</option>
                        <option value='FirstNameDesc'>First name (z-a)</option>
                    </select>
                </div>
            </div>
        </div>
        <div class='matches'>
            <h3 class='no-matches' v-if='numMatches == 0'>No matches to display. </h3>
            <div class='match' v-else v-for='match in matches' :key='match'>
                <MatchCard 
                    :stats='match'
                    :vacancyName='selectedVacancyName'
                    :vacancy='selectedVacancy'
                    @showApplication='updateCard' 
                    @unmatch='onUnmatch' 
                />
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

    .matches {
        height: calc(100% - 121px);
        overflow-y: scroll;
    }

    .matches-column {
        min-width: 480px;

        flex-grow: 2;
        border-right: 1px solid var(--jet);
    }

    .no-matches {
        color: var(--blue);
    }

    .select-group {
        position: relative;
        bottom: 8px;
    }
</style>