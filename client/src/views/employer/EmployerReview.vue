<script setup>
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';
    import EmployerApplication from '@/components/employer/EmployerApplication.vue';

    import relativeTime from 'dayjs/plugin/relativeTime';
    import dayjs from 'dayjs';
    import { ref, watch } from 'vue';

    dayjs.extend(relativeTime);

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


    const download_button = () => {
        alert('downloading all applications');
    }
</script>



<template>
    <EmployerNavbar page='home' :numNotifs='notifs'></EmployerNavbar>

    <div class='split left'>
    <p> 
        Matches (2)
    </p>
    <hr>
        <input name='searchbar' type='text' float='right'> 
        <button type='button' class='application-button application-button-grey' id= 'download_button' @click= download_button> Download Applications </button>
    
    <div class='scroll'>
        <div class='applicants' v-for='applicant in applicants' :key='applicant.id'>
        <table>
            <tr>
                <th> 
                    <EmployerApplication :stats='applicant' />
                </th>
            </tr>
        </table>
        </div>
    </div>
    </div>

    <div class='split right'>
        <h1> Customer Service Representative </h1>
        <hr>
    </div>
</template>



<style scoped>
    table {
        border: 1px solid;
        height: 100%;
        width: 100%;
    }

    .application-button {
        font-weight: 500; /* required for some reason */
        border-radius: 15px;
        color: #fff;
        border: 2.2px solid #333;
        width: 150px;
        height: 20px;
        margin-left: 15px;
        font-size: 11px;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        float: left;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
    }


    .application-button-grey {
        background: var(--slate);
    }

    .application-button-grey:hover, .application-button-grey:focus, .application-button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
  } 

    .scroll {
        width:100%;
        height: 85%;
        overflow:auto;
        scrollbar-base-color:gold;
        margin: 2px;
        overflow-y:scroll;
    }

    .input{
        float:right;
        align:right;
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

    .right {
        box-sizing: border-box;
        border-left:3px solid;
        left: 30%;
        right: 0;
        padding-top: 20px;
        width: 70%;
    }

    .split {
        color: black;
        height: 100%;
        position: fixed;
        top: 70px;
    
    }
</style>