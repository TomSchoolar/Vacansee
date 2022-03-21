<script setup>
    import { ref } from 'vue';

    let { numVacancies = 0, vacancies = [] } = defineProps(['numVacancies', 'vacancies']);

    const sortVacancies = ref('matchesDesc');

    const getMatches = (vacancy) => {
        alert('show matches for '+ vacancy.title);
    };
</script>

<template>
    <section class='column'>
        <div class='header'> 
            <div class='header-row'>
                <h2 class='header-title'> Vacancies ({{vacancies.length}}) </h2>
                
                <button type='button' class='button download-button' @click='download'>Download Report</button>
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

                    <select v-model='sortVacancies' aria-label='sort vacancies' id='vacancy-sort' class='sort'>
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
            
            <div class='vacancy' v-else v-for='vacancy in vacancies' :key='vacancy.title'>
                <span class='vacancy-title'>
                    <span class='vacancy-closed' v-if='vacancy.closed'>(closed) </span> 
                    {{ vacancy.title }} 
                </span>

                <span class='vacancy-matches' v-if='vacancy.numMatches'> {{ vacancy.numMatches }} matches</span>
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
        height: calc(100vh - 155.5px);
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
        height: calc(100% - 110.8px);
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
        color: var(--slate);
        font-style: italic;
    }

</style>