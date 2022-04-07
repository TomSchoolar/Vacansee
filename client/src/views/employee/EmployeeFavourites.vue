<script setup>
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    import ApplyVacancyCard from '@/components/employee/index/ApplyVacancyCard.vue';
    
    import { ref } from 'vue';


    // vars init
    const tagsLim = 6;
    const extraTags = '';
    const notifs = ref(2);
    const favourites = ref([
        {
            "VacancyName":"Junior Developer","Salary":"Competitive","Description":"Looking for a young developer with knowledge in Python","SkillsRequired":["Python","Team-Working","Django"],"ExperienceRequired":["Agile team experience"],"TimeZone":0,"Tags":["0","1","4"],"IsOpen":true,"PhoneNumber":"07745469444","Email":"example@facebook.com","Created":"2022-03-01","Location":"Birmingham",'Favourited':true,"UserId":4,"CompanyName":"Facebook"
        },
        {
            "VacancyName":"Junior Developer","Salary":"Competitive","Description":"Looking for a young developer with knowledge in Python","SkillsRequired":["Python","Team-Working","Django"],"ExperienceRequired":["Agile team experience"],"TimeZone":0,"Tags":["0","1","4"],"IsOpen":true,"PhoneNumber":"07745469444","Email":"example@facebook.com","Created":"2022-03-01","Location":"Birmingham",'Favourited':true,"UserId":4,"CompanyName":"Facebook"
        },
        {
            "VacancyName":"Junior Developer","Salary":"Competitive","Description":"Looking for a young developer with knowledge in Python","SkillsRequired":["Python","Team-Working","Django"],"ExperienceRequired":["Agile team experience"],"TimeZone":0,"Tags":["0","1","4"],"IsOpen":true,"PhoneNumber":"07745469444","Email":"example@facebook.com","Created":"2022-03-01","Location":"Birmingham",'Favourited':true,"UserId":4,"CompanyName":"Facebook"
        },
        {
            "VacancyName":"Junior Developer","Salary":"Competitive","Description":"Looking for a young developer with knowledge in Python","SkillsRequired":["Python","Team-Working","Django"],"ExperienceRequired":["Agile team experience"],"TimeZone":0,"Tags":["0","1","4"],"IsOpen":true,"PhoneNumber":"07745469444","Email":"example@facebook.com","Created":"2022-03-01","Location":"Birmingham",'Favourited':true,"UserId":4,"CompanyName":"Facebook"
        }
    ]);

    // dropdown values
    const limit = ref(3);
    const sort = ref('dateDesc');

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numFavourites = ref(0);

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

            <div class='select-group'>
                <select v-model='limit' aria-label='set page size' id='limit'>
                    <option value=3 selected>3 per page</option>
                    <option value=6>6 per page</option>
                    <option value=9>9 per page</option>
                    <option value=12>12 per page</option>
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
                    <th class='filter-tags-header'> Selected Tags </th>
                    <div class='filter-tag'>
                        <i class='fa-solid fa-book tag'></i> 
                    </div>
            </div>

            <div class='vacancy-container'>
                <ApplyVacancyCard v-for='vacancy in favourites' :key='vacancy.VacancyId' :vacancy=vacancy :tags='tags' />
            </div> 

            <button type='button' class='button arrow-btn' @click='page < numPages ? changePage(page + 1) : page'>
            <i class="fa-solid fa-circle-arrow-right"></i>
            </button>
            <button type='button' class='button arrow-btn' @click='page > 1 ? changePage(page - 1) : page'>
                <i class="fa-solid fa-circle-arrow-left"></i>
            </button>
            
        </div>
    </div>
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
        position: relative;
        top: 5px;
        margin-bottom: 5px;
        padding: 7px 20px;
        border-radius: 15px;
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
    }

    .select-group {
        flex-direction: column;
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
        text-align: center; 
        display: flex; 
        justify-content: space-evenly; 
        flex-wrap: wrap;
    }
</style>
