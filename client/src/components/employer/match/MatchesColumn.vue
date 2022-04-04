<script setup>
    import MatchCard from '@/components/employer/match/MatchCard.vue';

    import { getIdFromToken } from '@/assets/js/jwt';
    import { ref, onMounted, watch, toRef } from 'vue';
    import axios from 'axios';

    const emits = defineEmits(["show-application"])
    const selectedProfile = ref();

    const props = defineProps(['selectedVacancy']);

    const selectedVacancy = ref(0);
    const selected = toRef(props, 'selectedVacancy');

    const matches = ref([]);
    const numMatches = ref(0);

    const sort = ref('dateDesc');

    const download = () => {
        alert("downloaded!");
    }

    // api request function
    const getMatches = async (options) => {
        const { sort = 'dateDesc', vID = selected.value  } = options;

        const uID = getIdFromToken(window.localStorage.accessToken);

        const response = await axios({
            method: 'get',
            url: '/e/match/matches/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            params: {
                uID,
                vID,
                sort,
            }
        }).catch((err) => {
            console.log(`oops ${ err }`);
        });

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
        const result = await getMatches({ sort: sortParam });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }

    const updateMatches = async (newVac) => {
        const result = await getMatches({ sort: sort.value, vID: newVac})

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        selectedVacancy.value = newVac;
    }

    const updateCard = (nextProfile) => {
        console.log(`Current Profile: ${ nextProfile.FirstName }`);
        emits("show-application", nextProfile);
    }

    watch(selectedVacancy, updateMatches);

    watch(selected, (value) => {
        selectedVacancy.value = selected.value;
    });

    watch(sort, sortMatches);

</script>

<template>
    <section class='matches-column'>
        <div class='header'>
            <div class='header-row'>
                <h2 class='header-title'> Matches ({{ matches.length }})</h2>

                <button type='button' class='button match-download-button' id='download-button' @click='download'>Download All</button>
            </div>

            <div class='header-row'>
                <div class='search-group'>
                    <i class="fa-solid fa-magnifying-glass search-icon"></i>
                    <input name='searchbar' type='text' placeholder='Search..' class='search' /> 
                </div>

                <div class='select-group'>
                    <div class='select-label'> 
                        <label for='sort-matches'>sort by:</label>
                    </div>

                    <select v-model='sort' aria-label='sort matches' id='sort-matches' class='sort'>
                        <option value='dateDesc' selected>latest first</option>
                        <option value='dateAsc'>oldest first</option>
                        <option value='titleAsc'>title (a-z)</option>
                        <option value='titleDesc'>title (z-a)</option>
                    </select>
                </div>
            </div>
        </div>
        <div class='matches'>
            <h3 class='no-matches' v-if='numMatches == 0'>No matches to display. </h3>
            <div class='match' v-else v-for='match in matches' :key='match'>
                <MatchCard :stats='match' @showApplication='updateCard'/>
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