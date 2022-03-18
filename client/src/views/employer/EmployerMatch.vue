<script setup>
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerMatches from '@/components/employer/EmployerMatches.vue';

    import relativeTime from 'dayjs/plugin/relativeTime';
    import dayjs from 'dayjs';
    import { ref, watch } from 'vue';

    dayjs.extend(relativeTime);

    
    const downloadbtn = () => {
        alert("downloaded!");
    }

    const vacbtn = () => {
        alert("value");
    }
    const vacancies = [
            {title: 'Customer Service Rep.',
            closed: false,
            },
            {title: 'Accountant',
            closed: true ,},
            {title: 'Personal Assistant',
            closed: false,},
    ];
    
    var matches = [ {
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
                },
                {
                name: 'Mary Rodriguez',
                pronouns: '(she/her)',
                number: '07747945173',
                email: 'name@email.com',
                timezone: '(UTC +0) London',
                },];
    
    function getMatches(vac){
        alert('show matches for '+ vac.title);
    };
        
</script>



<template>
    <EmployerNavbar page='home' :numNotifs='notifs'></EmployerNavbar>
    
    <div class= 'split left'>
        <p style='text-align:left; padding-left: 10px;'> 
        Vacancies ({{vacancies.length}})
        <input name='searchbar' type='text' placeholder='Search..'> 
        <button type='button' class='button downloadbtn' id= 'downloadbtn' @click= downloadbtn> Download Full Match Report </button>
        <select v-model='sort' aria-label='sort matches' id='sort'>
                <option selected hidden>sort by</option>
                <option value='dateDesc'>latest first</option>
                <option value='dateAsc'>oldest first</option>
                <option value='titleAsc'>title (a-z)</option>
                <option value='titleDesc'>title (z-a)</option>
            </select>
    </p>
    <div class='scroll'>
        <div class='vacancies' v-for='vac in vacancies' :key='vac.title'>
        <table>
            <tr>
                <th> <b style = 'float:left; margin: 6px;' v-if='vac.closed'>(closed)</b> <button type='button' class='button vacancies' id= 'vacbtn' @click= getMatches(vac)> {{vac.title}} </button> </th>
            </tr>
        </table>
        </div>
    </div>
    </div>

    <div class='split middle'>
    <p id='mid' style='text-align:left; padding-left: 10px;'> 
        Matches ({{matches.length}})
    </p>
    <p style='text-align:left; padding-left: 10px;'> 
        <input name='searchbar' type='text' placeholder='Search..'> 
        <button type='button' class='button downloadbtn' id= 'downloadbtn' @click= downloadbtn> Download All </button>
        <select v-model='sort' aria-label='sort matches' id='sort'>
                <option selected hidden>sort by</option>
                <option value='dateDesc'>latest first</option>
                <option value='dateAsc'>oldest first</option>
                <option value='titleAsc'>title (a-z)</option>
                <option value='titleDesc'>title (z-a)</option>
            </select>
    </p>
    <div  class='scroll'>
        
        <div class='matches' v-for='match in matches'>
        <table>
            <div id='displayMatches'>
            <tr >
                <th> <EmployerMatches :stats='match' /> </th>
            </tr>
            </div>
        </table>
        </div>
    </div>
        
    </div>

    <div class='split right'>
        <h1 style= 'border-bottom: 2px solid; margin:20px;'> Vacancy title </h1>

        <p> Profile Card </p>

    </div>


</template>



<style scoped>

    select{
        border: 2px solid;
        float:right;
        font-size:12px;
        margin: 1px;
        padding: 3px;
    }

    table {
        border: 2px solid;
        height: 100%;
        width: 100%;
        overflow-y: auto;
    }

    .stats{
        border: 2px solid; 
        background-color: white; 
        border-radius: 25px; 
        margin-left:30%; 
        margin-right:30%; 
        margin-top: 40%; 
    }
    .scroll {
        width:100%;
        height: 85%;
        overflow:auto;
        scrollbar-base-color:gold;
        margin: 2px;
        overflow-y:scroll;
    }
    input{
        font-size: 12px;
        float: right;
        margin-top:2px;
        border-radius: 25px;
        padding: 2px;
        padding-left: 5px;
        margin-right: 5px;
    }

    .button{
        float: right;
        background-color:#D3D3D3;
        border: 2px solid;
        border-radius: 15px;
        color: black;
        cursor: pointer;
        display: inline-block;
        font-size: 12px;
        margin: 2px;
        text-align: center;
        text-decoration: none;
        transition-duration: 0.4s;

    }

    .vacancies{
        float: center;
        font-size: 18px;
        background-color: white;
        border: none;
        margin: 10px;
        text-align: center;

    }

    .button:active{
        background-color:#D3D3D3;
        font-size: 70%;
    }

    .button:hover{
        background-color:#D3D3D3;

    }

    .left {
        box-sizing: border-box;
        height: 100%;
        padding-top: 10px;
        width: 30%;          
    }

    .middle {
        box-sizing: border-box;
        height: 100%;
        padding-top: 10px;
        width: 30%;
        left: 30%;
        right: 40%;
    }

    .right {
        box-sizing: border-box;
        background-color: #f0f8fa;
        border-left:3px solid;
        left: 60%;
        right: 0;
        padding-top: 20px;
        width: 40%;
    }

    .split {
        color: black;
        height: 100%;
        position: fixed;
        top: 70px;
    
    }

    .select-group {
        align: right;
        flex-direction: column;
    }

</style>