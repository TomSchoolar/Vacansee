<script setup>

    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    function personalDetails(){
        document.getElementById('personalDetails').style.display = '';
        document.getElementById('contactDetails').style.display = 'none';
    }

    function contactDetails(){
        document.getElementById('contactDetails').style.display = '';
        document.getElementById('personalDetails').style.display = 'none';
    }
</script>

<template>
    <EmployeeNavbar page='home' :numNotifs='notifs'></EmployeeNavbar>
    <div class= 'container'>
        <h1 class ='title'> User Profile SetUp </h1>
        <div class= 'bar'>
            <button @click = 'personalDetails' id= 'personalDetails-button'> Personal Details </button>
            <button @click = 'contactDetails' id= 'contactDetails-button'> Contact Details </button>
            <button id='location-button'> Location </button>
            <button> Soft Skills </button>
            <button> Experience </button>
            <button> Qualifications </button>
            <button> Review </button>
        </div>

        <div id ='personalDetails' style='display:none;'> 
            <h1> Personal Details </h1> 
            <p> Let's start off with the simple stuff. <br /> Enter your first and last name and your pronouns </p>
            <form>
                <label for='fname'>First name:</label><br />
                <input type='text' id='fname' name='fname'><br />
                <label for='lname'>Last name:</label><br />
                <input type='text' id='lname' name='lname'> <br />
                <label>Pronouns:</label><br />
                <select id='pronouns' name='pronouns'>
                    <option value = 'he/him'> He/Him </option>
                    <option value = 'she/her'> She/Her </option>
                    <option value = 'they/them'> They/Them </option>
                </select>
            </form>
            <button @click = 'contactDetails'> Next </button>
        </div>
        <div id='contactDetails' style='display:none;'>
            <h1> Contact Details </h1> 
            <p> We need your contact details next. <br /> Enter a current phone number and email address </p>
            <form>
                <label for='phonenum'>Phone number:</label><br />
                <input type='text' id='phonenum' name='phonenum'><br />
                <label for='email'>Email address:</label><br />
                <input type='text' id='email' name='email'>
            </form>
            <button @click = 'personalDetails'> Back </button>
            <button> Next </button>
        </div>

    </div>
</template>


<style scoped>
    button{
        border: none;
        padding: 20px;
        text-align: center;
        display: inline-block;
        margin: 4px 2px;
        border-radius: 50%;

    }

    .container {
        margin-bottom: 30px;
        padding: 10px;
    }

    .bar{
        display: flex;
        justify-content: center;
    }

    .title {
        align: left;
        text-align: left;  
        margin-top:0; 
        border-bottom: 1px solid;
    }
    
</style>
