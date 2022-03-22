
<script setup>
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    
    import relativeTime from 'dayjs/plugin/relativeTime';
    import dayjs from 'dayjs';
    import { ref, watch } from 'vue';

    const tags = [
        {
            id: 0,
            icon: 'book'
        },
    ]

    dayjs.extend(relativeTime);
    let notifs = ref(2);
    let filter = ref('all');
    let limit = ref(10);
    let sort = ref('newApps');

    watch(filter, (filterValue) => {
        alert(`showing ${ filterValue } adverts`);
    });

    watch(limit, (newLimit) => {
        alert(`showing ${ newLimit } articles per page`);
    });

    watch(sort, (sortParam) => {
        alert(`sorted by ${ sortParam }`);
    });

    const applybtn = () => {
        alert("applied!");
    }
    
    const next = () => {
        alert("next page");
    }

    const prev = () => {
        alert("previous page");
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
                <option value='all' selected>show all adverts</option>
                <option value='active'>show active adverts</option>
                <option value='closed'>show closed adverts</option>
            </select>
        </div>


        <div class='select-group'>
            <select v-model='limit' aria-label='set page size' id='limit'>
                <option value=5>5 per page</option>
                <option value=10 selected>10 per page</option>
                <option value=20>20 per page</option>
                <option value=50>50 per page</option>
            </select>
        </div>


        <div class='select-group'>
            <select v-model='sort' aria-label='sort vacancies' id='sort'>
                <option value='newApps' selected>new applications</option>
                <option value='dateDesc'>latest first</option>
                <option value='dateAsc'>oldest first</option>
                <option value='titleAsc'>title (a-z)</option>
                <option value='titleDesc'>title (z-a)</option>
            </select>
        </div>


        <div class='tags' t-for='tag in tags' :key='tags.id'>
            <table style='padding: 5px; width: 100%; border: 2px solid;text-align: left; border-radius: 15px; margin-top: 50px;'>
                <tr> 
                    <th style='border-right: 2px solid; width: 10%; padding-right: 10px; font-size: 18px;'> Selected Tags </th>
                    <th> <i class='fa-solid fa-book tag'></i> </th>
                    <th>  </th>
                </tr>

            </table>
            <br />

            <!-- table below in place of vacancy cards -->
            <table style = 'padding: 5px; height: 55%; width: 100%; border: 1px solid; text-align: center; border-radius: 15px;'>
                <tr> 
                    <th> Card 1 </th>
                    <th> Card 2 </th>
                    <th> Card 3 </th>
                    <th> Card 4 </th>
                    <th> Card 5 </th>
                </tr>
                <tr> 
                    <th> Card 1 </th>
                    <th> Card 2 </th>
                    <th> Card 3 </th>
                    <th> Card 4 </th>
                    <th> Card 5 </th>
                </tr>

            </table>
        </div>

        <button type='button' class='button arrowbtn' id= 'next' @click=next>
        <i class="fa-solid fa-circle-arrow-right"></i>
        </button>
        <button type='button' class='button arrowbtn' id= 'prev' @click=prev>
            <i class="fa-solid fa-circle-arrow-left"></i>
        </button>
        
    </div>

<div class='split right'>
    <button type='button' class='button applybtn' id= 'applybtn' @click= applybtn>Apply Now!</button>
    <p>Employee info partial.</p>
</div>
    
</template>


<style scoped>

    input{
        border:2px solid;
        border-radius:25px;
        float:left;
        font-size:12px;
        margin: 1px;
        padding:5px;
    }

    select{
        border: 2px solid;
        float:right;
        font-size:12px;
        margin: 1px;
        padding: 3px;
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

    .button:active{
        background-color:#D3D3D3;
        font-size: 50%;
    }

    .button:hover{
        background-color:#D3D3D3;

    }

    .arrowbtn{
        background-color: white;
        border:none;
        float: right;
        font-size: 20px;
        padding: 2px;
    }
    .applybtn{
        background-color: white;
        border-radius: 10px;
    }

    

    .left {
        box-sizing: border-box;
        height: 100%;
        padding-left: 50px;
        padding-right: 50px;
        padding-top: 10px;
        width: 70%;          
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
        align: right;
        flex-direction: column;
    }


    .tag{
        font-size: 250%;
        margin: 10px;
    }

</style>

