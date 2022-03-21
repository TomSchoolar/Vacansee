<script setup>
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
    import ApplyProfileCard from '@/components/employer/review/ApplyProfileCard';
    import MatchCard from '@/components/employer/review/MatchCard.vue';

    const applicants = [
        {
            id: 0,
            name: 'Mary Rodriguez',
            phoneNumber: '07747945173',
            email: 'mary.r92@gmail.com',
            timeZone: '(UTC+0) London, Dublin, Lisbon',
            pronouns: 'she/her'
        },

        {
            id: 1,
            name: 'Michael Brent',
            phoneNumber: '07747945173',
            email: 'michael.b92@gmail.com',
            timeZone: '(UTC+0) London, Dublin, Lisbon',
            pronouns: 'he/him'
        }
    ]

    let applicantData = {
        firstName: 'George',
        pronouns: 'he/him',
        location: 'London',
        topicSentence: 'Good luck convincing people to hire you with one sentence.',
        skills: ['75 wpm typing speed', 'Microsoft Excel', 'Patience'],
        experience: [
            {
                title: 'fast food restaurant',
                startDate: '2016',
                endDate: '2019' 
            },
            {
                title: 'customer service call centre',
                startDate: '2019',
                endDate: '2021' 
            },
            {
                title: 'level 1 support tech',
                startDate: '2021',
                endDate: '2022' 
            }
        ],
        qualifications: ['9 GCSEs (A*-D)', '3 A-Levels (A-B)']
    }


    const download_button = () => {
        alert('downloading all applications');
    }
</script>



<template>
    <EmployerNavbar :numNotifs='notifs'></EmployerNavbar>

    <div class='container'>
        <div class='col col-left'>
            <div class='col-header'> 
                <h3 class='col-title'>Matches ({{ applicants.length }})</h3>
                <div class='header-right'>
                    <button type='button' class='application-button application-button-grey' id= 'download_button' @click= download_button>Download Applications</button>
                    <div class='search-group'>
                        <i class="fas fa-search search-icon"></i>
                        <input class='search' placeholder='search' type='text'> 
                    </div>
                </div>
            </div>

            <hr class='slim-hr'/>

            <div class='applications'>
                <MatchCard v-for='applicant in applicants' :key='applicant.id' :stats='applicant' />
            </div>
        </div>

        <div class='col col-right'>
            <div class='col-header'> 
                <h3 class='col-title'>Strat Security Co. - Customer Service Representative</h3>
            </div>

            <hr class='slim-hr' />

            <main class='card-container'>
                <ApplyProfileCard class='card' :application='applicantData' />
            </main>
        </div>
    </div>

</template>



<style scoped>
    table {
        border: 1px solid;
        height: 100%;
        width: 100%;
    }

    .applications {
        overflow-y: scroll;
        height: calc(100% - 47px);
        overflow-x: hidden;
    }

    .application-button {
        font-weight: 500; /* required for some reason */
        border-radius: 7px;
        color: #fff;
        border: 2.2px solid #333;
        min-width: 150px;
        font-size: 12px;
        text-decoration: none;
        padding: 2px 4px;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
    }

    .application-button-grey {
        background: var(--slate);
    }

    .application-button-grey:hover, .application-button-grey:focus, .application-button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
    }

    .card {
        position: relative;
        top: -30px;
    }

    .card-container {
        height: calc(100% - 48px);
        width: 100%;
        background: var(--background-blue);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .container {
        display: flex;
    }

    .col {
        height: calc(100vh - 100px);
        margin-top: -30px;
        padding-top: 30px;
    }

    .col-header {
        display: flex;
        padding: 0 20px 7px 20px;
        justify-content: space-between;
        align-items: center;
        margin-top: -10px;
    }

    .col-left {
        flex-grow: 0.3;
        min-width: 550px;
        border-right: 1px solid #9a9a9a;
    }

    .col-right {
        flex-grow: 3;
    }

    .col-title {
        margin: 0;
        font-weight: 500;
        font-size: 21px;
    }

    .header-right {
        display: flex;
    }

    .search {
        border-radius: 7px;
        padding: 2px 4px 2px 22px;
        margin-left: 8px;
        width: 120px;
    }

    .search-icon {
        position: absolute;
        left: 12px;
        top: 6px;
    }

    .search-group {
        position: relative;
    }

    .slim-hr {
        margin-bottom: 0;
    }
</style>