<script setup>
    import MatchCard from '@/components/employer/review/MatchCard.vue';

    import { ref } from 'vue';

    let { matches = [], numMatches = 0 } = defineProps(['matches', 'numMatches'])

    const sortMatches = ref('dateDesc');

    const download = () => {
        alert("downloaded!");
    }
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

                    <select v-model='sortMatches' aria-label='sort matches' id='sort-matches' class='sort'>
                        <option value='dateDesc' selected>latest first</option>
                        <option value='dateAsc'>oldest first</option>
                        <option value='titleAsc'>title (a-z)</option>
                        <option value='titleDesc'>title (z-a)</option>
                    </select>
                </div>
            </div>
        </div>
        <div class='matches'>
            <h3 class='no-matches' v-if='numMatches == 0'>No matches to display</h3>
            <div class='match' v-else v-for='match in matches' :key='match'>
                <MatchCard :stats='match' />
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
        height: calc(100% - 110.8px);
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