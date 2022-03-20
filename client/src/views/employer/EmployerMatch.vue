<script setup>
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerMatches from '@/components/employer/EmployerMatches.vue';
    import ApplyProfileCard from '@/components/partials/ApplyProfileCard.vue';

    import relativeTime from 'dayjs/plugin/relativeTime';
    import dayjs from 'dayjs';
    import { ref, watch } from 'vue';

    dayjs.extend(relativeTime);

    document.title = 'Matches | Vacansee';
   
    const applicantData = {
        firstName: 'Mary',
        pronouns: 'she/her',
        location: 'Birmingham',
        topicSentence: 'A topic sentence',
        skills: ['Excel', 'Typing', 'Communication'],
        experience: [
            {
                title: 'job',
                startDate: '2009',
                endDate: '2013' 
            },
            {
                title: 'a new job',
                startDate: '2013',
                endDate: '2020' 
            },
            {
                title: 'customer service rep',
                startDate: '2020',
                endDate: '2022' 
            }
        ],
        qualifications: ['10 GCSEs (A*-D)', '3 A-Levels (A-C)']
    };

    const vacancies = [
            {
                title: 'Customer Service Rep.',
                closed: false,
            },
            {
                title: 'Accountant',
                closed: true ,},
            {
                title: 'Personal Assistant',
                closed: false,
                numMatches: 6
            },
    ];
    
    const numVacancies = 1;
    const numMatches = 1;

    const matches = [ {
                name: 'Mary Rodriguez',
                pronouns: '(she/her)',
                number: '07747945173',
                email: 'name@email.com',
                timezone: '(UTC +0) London',
                },
                {
                name: 'Brian Johnson',
                pronouns: '(she/her)',
                number: '07747945173',
                email: 'name@email.com',
                timezone: '(UTC +0) London',
                },];
    
    function getMatches(vac){
        alert('show matches for '+ vac.title);
    };

    const downloadbtn = () => {
        alert("downloaded!");
    }

    const vacbtn = () => {
        alert("value");
    }
</script>

<template>
    <EmployerNavbar page='matches' :numNotifs='notifs'></EmployerNavbar>
    <main class='container'>
        <section class='match-title'>
            <h1 class='title'>Strat Security Co. - Matches</h1>
        </section>
        <section class ='match-section'>
            <section class= 'match-left'>
                <div class='match-left-header'> 
                    <div class='left-header-left'>
                        <p> Vacancies ({{vacancies.length}}) </p>
                        <input name='searchbar' type='text' placeholder='Search..' />
                    </div>
                    <div class='left-header-right'>
                        <button type='button' class='button vacdownloadbtn' id='downloadbtn' @click= downloadbtn> Download Full Match Report </button>
                        <div class='select-group'>
                            <div class='select-label'> <label for='sort'>sort by:</label></div>
                            <select v-model='sort' aria-label='sort vacancies' id='sort'>
                                <option value='dateDesc' selected>latest first</option>
                                <option value='dateAsc'>oldest first</option>
                                <option value='titleAsc'>title (a-z)</option>
                                <option value='titleDesc'>title (z-a)</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class='match-left-body'>
                    <h3 class='no-vacancies' v-if='numVacancies == 0'>No vacancies to display</h3>
                    <div class='vacancy' v-for='vac in vacancies' :key='vac.title'>
                        <button type='button' class='vacancybtn' @click=getMatches(vac)> <span style='font-weight: bold;' v-if='vac.closed'>(closed) </span> {{vac.title}} <span style='float:right' v-if='vac.numMatches'> {{vac.numMatches}} matches</span></button>
                    </div>
                </div>
            </section>
            <section class='match-middle'>
                <div class='match-middle-header'>
                    <div class='middle-header-left'>
                        <p> Matches ({{matches.length}})</p>
                        <input name='searchbar' type='text' placeholder='Search..' /> 
                    </div>
                    <div class='middle-header-right'>
                        <button type='button' class='button matchdownloadbtn' id='downloadbtn' @click= downloadbtn> Download All </button>
                        <div class='select-group'>
                            <div class='select-label'> <label for='sort'>sort by:</label></div>
                            <select v-model='sort' aria-label='sort matches' id='sort'>
                                <option value='dateDesc' selected>latest first</option>
                                <option value='dateAsc'>oldest first</option>
                                <option value='titleAsc'>title (a-z)</option>
                                <option value='titleDesc'>title (z-a)</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class='match-middle-body'>
                    <h3 class='no-matches' v-if='numMatches == 0'>No matches to display</h3>
                    <div class='match' v-for='match in matches' v-bind:key='match'>
                        <EmployerMatches :stats='match' />
                    </div>
                </div>
            </section>
            <section class='match-right'>
                <ApplyProfileCard class='card' :application='applicantData' />
            </section>
        </section>
    </main>
</template>

<style scoped>
    input{
        font-size: 12px;
        float: right;
        border-radius: 25px;
        padding-left: 5px;
    }

    .button {
        width: 100%;
        background-color: var(--slate);
        border: 2px solid black;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        transition-duration: 0.4s;
    }

    .button:active {
        background-color: var(--slate-focus);
    }

    .button:hover {
        background-color: var(--slate-focus);
    }

    .card {
        position: relative;
        margin-left : auto; 
        margin-right : auto;
    }
    
    .container {
        padding: 0 40px;
        width: calc(100vw - 80px);
        overflow: hidden;
    }

    .left-header-left {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }

    .left-header-left p {
        margin: 0px;
        font-size: 28px;
        font-weight: 400;
    }

    .left-header-right {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }

    .match {
        border-bottom: 1px solid black;
    }

    .match-left {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        border: 1px solid black;
        overflow: hidden;
    }

    .match-left-body {
        scrollbar-base-color: var(--slate);  
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        flex: 0 1 auto;
    }

    .match-left-header {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        border-bottom: 1px solid black;
        flex: 0 0 auto;
    }

    .match-middle {
        display: flex;
        flex-direction: column;
        flex-grow: 2;
        border-top: 1px solid black;
        border-right: 1px solid black;
        border-bottom: 1px solid black;
        overflow: hidden;
    }

    .match-middle-body {
        scrollbar-base-color: var(--slate);  
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        flex: 0 1 auto;
    }

    .match-middle-header {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        border-bottom: 1px solid black;
        flex: 0 0 auto;
    }

    .match-right {
        display: flex;
        flex-grow: 3;
        flex-direction: row;
        align-items: center;
        align-content: center;
        border-top: 1px solid black;
    }

    .match-section {
        display: flex;
        flex-flow: row;
        justify-content: space-between;
        overflow: hidden;
        height: calc(85vh - 20px);
    }

    .match-title {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .matchdownloadbtn {
        font-size: 18px;
    }

    .middle-header-left {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }

    .middle-header-left p {
        margin: 0px;
        font-size: 28px;
        font-weight: 400;
    }

    .middle-header-right {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 10px;
    }

    .no-matches {
        color: var(--blue);
    }

    .no-vacancies {
        color: var(--blue);
    }

    .select-label {
        font-size: 12px;
    }

    .select-group {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-left: auto;
    }

    .stats{
        border: 2px solid; 
        background-color: white; 
        border-radius: 25px; 
        margin-left:30%; 
        margin-right:30%; 
        margin-top: 40%; 
    }

    .title, div:deep(.title) {
        margin: 0;
        font-size: 32px;
        position: relative;
        left: 5px;
        font-weight: 400;
    }

    .vacancy{
        background-color: white;
        border: 1px solid black;
        display: flex;
        flex-direction: column;
        margin: 3px;
    }

    .vacancybtn {
        font-size: 24px;
        border: none;
        background-color: white;
        transition-duration: 0.4s;
        color: black;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }

    .vacancybtn:hover {
        background-color: #d3d3d3;
    }

    .vacancybtn:active{
        background-color:#D3D3D3;

    }

    .vacdownloadbtn {
        font-size: 18px;
    }

    #sort {
        width: 100%;
    }
</style>