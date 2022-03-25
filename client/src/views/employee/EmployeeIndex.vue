<script setup>
    import { ref, watch, onMounted } from 'vue';
    import { jwtGetId } from '@/assets/js/jwt';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    
    import axios from 'axios';


    // vars init
    const notifs = ref(2);
    const vacancies = ref(null);
    const tagsLim = 6;
    const extraTags = '';

    // dropdown values
    const filter = ref('active');
    const limit = ref(3);
    const sort = ref('dateDesc');

    // pagination
    const page = ref(1);
    const numPages = ref(1);
    const numVacancies = ref(0);

    const tags = [
        {
            id: 0,
            icon: 'book'
        },
    ]

    document.title = 'Home | Vacansee';

    // api request function
    const getVacancies = async (options) => {
        const { count = 3, pageNum = 1, sort = 'dateDesc', filter = 'active' } = options;

        const uID = jwtGetId(window.localStorage.jwt);

        const response = await axios({
            method: 'get',
            url: '/vacancy/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            responseType: 'json',
            params: {
                uID,
                sort,
                count,
                filter,
                pageNum
            }
        }).catch((err) => {
            console.log(`oops: ${ err }`);
        });

        if(!response || !response.data)
            return false;

        const { data } = response;

        if(!data)
            return false;

        const { 
            vacancies: newVacancies = vacancies.value, 
            numPages: pages = 1, 
            numVacancies: total = 0,
        } = data;


        while((page.value - 1) * limit.value >= total) page.value--;

        numPages.value = pages;
        numVacancies.value = total;
        vacancies.value = newVacancies;

        console.log(vacancies.value);

        return true;
    }

    // vacancy api request
    onMounted(async () => {
        const result = await getVacancies({ });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }
    });

    // get vacancies in new order
    const sortVacancies = async (sortParam) => {
        const result = await getVacancies({ sort: sortParam, count: limit.value, pageNum: page.value, filter: filter.value });
        
        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        sort.value = sortParam;
    }

    // pagination: change page
    const changePage = async (newPage) => {
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: newPage, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        page.value = newPage;   
    }

    // dropdown watchers
    watch(filter, async (filterValue) => {
        // change which vacancies are display based on isOpen
        const result = await getVacancies({ sort: sort.value, count: limit.value, pageNum: page.value, filter: filterValue });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        filter.value = filterValue;
    });

    watch(limit, async (newLimit) => {
        // change number of vacancies per page
        while((page.value - 1) * limit.value >= numVacancies.value) page.value--;

        if(page.value < 0)
            page.value = 0;

        const result = await getVacancies({ sort: sort.value, count: newLimit, pageNum: page.value, filter: filter.value });

        if(!result) {
            alert('uh oh! something went wrong :(');
            return;
        }

        limit.value = newLimit;
    });

    watch(sort, sortVacancies);

    const apply = () => {
        alert("applied!");
    }

    

</script>

<template>
    <EmployeeNavbar page='home' :numNotifs='notifs'></EmployeeNavbar>

    <div class='split left'>
        <h1 style='text-align: left;  margin-top:0; border-bottom: 1px solid;'> Vacancies </h1>
        <p style='padding: 5px; solid;'></p>
        <input name='searchbar' type='text' placeholder='Search..'> 
        
        <div class='select-group'>
            <select v-model='filter' aria-label='filter vacancies' id='filter'>
                <option value='active' selected>show active adverts</option>
                <option value='all'>show all adverts</option>
                <option value='closed'>show closed adverts</option>
            </select>
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


        <div class='tags' v-for='tag in tags' :key='tag.id'>
            <table style='padding: 5px; width: 100%; border: 2px solid;text-align: left; border-radius: 15px; margin-top: 50px;'>
                <tr> 
                    <th style='border-right: 2px solid; width: 10%; padding-right: 10px; font-size: 18px;'> Selected Tags </th>
                    <th> <i class='fa-solid fa-book tag'></i> </th>
                    <th>  </th>
                </tr>

            </table>
            <br />

            <!-- table below in place of vacancy cards -->
            <div style = 'padding: 5px; height: 55%; width: 100%; border: 1px solid; text-align: center; border-radius: 15px; display: flex; justify-content: space-between; flex-wrap: wrap'>
                <div v-for='vacancy in vacancies' :key='vacancy.VacancyId' class='card'>
                    <div class='card-main-container'>
                        <div class='company-info'>
                            <div class='company-name'>{{ vacancy.CompanyName }}<!-- <i id='favourite' class='fas fa-star' title='favourited' v-if="favourited"></i>--></div>
                            <p class='job-title'>{{ vacancy.VacancyName }}</p>
                            <p class='location' v-if='vacancy.Location'>Based in {{ vacancy.Location }}</p>
                        </div>
                        <div class='description'>
                            <p>{{ vacancy.Description }}</p>
                        </div>
                        <span v-if='vacancy.SkillsRequired' class='card-section'>Necessary Skills:</span>
                        <div class='skills'>
                            <table>
                                <tr v-for='skill in vacancy.SkillsRequired' v-bind:key='skill'>
                                    <th>- {{ skill }}</th>
                                </tr>
                            </table>
                        </div>
                        <span v-if='vacancy.ExperienceRequired' class='card-section'>Experience:</span>
                        <div class='experience'>
                            <table>
                                <tr v-for='xp in vacancy.ExperienceRequired' v-bind:key='xp'>
                                    <th>- {{ xp }}</th>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <div class="card-tag-container">
                        <span v-if='vacancy.Tags' class='card-section'>Requirements:</span>
                        <table style='margin: 5px 0 10px 0'>
                            <tr>
                                <th class='card-tags' v-for='tag in vacancy.Tags.slice(0,tagsLim)' v-bind:key='tag'>
                                    <i v-if='tag == 1' class='fa-solid fa-database'></i>
                                    <i v-else-if='tag == 2' class='fa-solid fa-code'></i>
                                    <i v-else-if='tag == 3' class='fa-brands fa-python'></i>
                                    <i v-else-if='tag == 4' class='fa-solid fa-school'></i>
                                    <i v-else class='fa-solid fa-briefcase'></i>
                                </th>
                                <!--
                                <th v-if='tags.length > 6' class='card-tags tags-overflow' :title='extraTags'>
                                    <div class='tags-num' ref='extra-tags'>+{{ tags.length - (tagsLim - 1) }}</div>
                                    <i class='fa-solid fa-tags'></i>
                                </th>
                                -->
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <button type='button' class='button arrow-btn' @click='page < numPages ? changePage(page + 1) : page'>
        <i class="fa-solid fa-circle-arrow-right"></i>
        </button>
        <button type='button' class='button arrow-btn' @click='page > 1 ? changePage(page - 1) : page'>
            <i class="fa-solid fa-circle-arrow-left"></i>
        </button>
        
    </div>

<div class='split right'>
    <button type='button' class='button apply-btn' @click= apply>Apply Now!</button>
    <p>Employee info partial.</p>
</div>
    
</template>


<style scoped>
    input {
        border:2px solid;
        border-radius:25px;
        float:left;
        font-size:12px;
        margin: 1px;
        padding:5px;
    }

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

    .card {
        font-size: 16px;
        font-weight: normal;
        height: 500px;
        width: calc((100% / 3) - 56px);
        border: 2px solid #555;
        border-radius: 15px;
        margin: 12px 6px;
        align-items: center;
        text-align: left;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 0 20px;
    }

    .card > * {
        width: 100%;
    }

    .card-section {
        font-weight: 600;
    }

    .company-info p {
        margin: 0px;
        padding: 5px 0px 0px 0px;
    }

    .company-name { 
        font-weight: bold;
        font-size: 24px;
        margin: 0px;
        padding: 10px 0px 0px 0px;
    }

    .description p {
        font-size: 16px;
        margin: 10px 0;
    }
    .job-title {
        font-size: 18px;
        font-style: italic;
    }

    .location {
        font-style: italic;
    }

    .skills {
        font-weight: normal;
    }

    .card-tags {
        font-size: 20px;
        padding: 0 20px 0 0;
    }

    .card-tags i {
        font-size: 32px;
    }

    .tags-num {
        position: absolute;
        background: var(--red);
        color: white;
        font-size: 12px;
        border-radius: 30%;
        bottom: 5px;
        right: 5px;
        padding: 2px 3px;

    }

    .tags-overflow {
        position: relative;
    }

    #favourite {
        float: right;
        padding: 15px;
        font-size: 45px;
        color: var(--red);
    }

    .left {
        box-sizing: border-box;
        height: 100%;
        padding-left: 50px;
        padding-right: 50px;
        padding-top: 10px;
        width: 70%;    
        position: absolute !important;      
    }

    .right {
        border-left:3px solid;
        left:70%;
        right: 0;
        padding-top: 100px;
        width: 30%;
    }

    .split {
        color: black;
        height: 100%;
        position: fixed;
        top: 10;
    
    }

    .select-group {
        flex-direction: column;
    }

    .tag {
        font-size: 250%;
        margin: 10px;
    }
</style>
