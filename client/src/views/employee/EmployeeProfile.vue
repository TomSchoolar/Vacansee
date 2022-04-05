<script setup>

    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
    function personalDetails(){
        document.getElementById('personalDetails').style.display = '';
        document.getElementById('contactDetails').style.display = 'none';
        document.getElementById('location').style.display = 'none';
        document.getElementById('softskills').style.display = 'none';
    }

    function contactDetails(){
        document.getElementById('contactDetails').style.display = '';
        document.getElementById('personalDetails').style.display = 'none';
        document.getElementById('location').style.display = 'none';
        document.getElementById('softskills').style.display = 'none';
    }

    function location(){
        document.getElementById('location').style.display = '';
        document.getElementById('personalDetails').style.display = 'none';
        document.getElementById('contactDetails').style.display = 'none';
        document.getElementById('softskills').style.display = 'none';
        var range = document.getElementById('range');
        var output = document.getElementById('output');

        range.onchange = function() {
            output.innerHTML = '<p>' + this.value + ' miles </p>';
        }
    }

    function softskills(){
        document.getElementById('softskills').style.display = '';
        document.getElementById('personalDetails').style.display = 'none';
        document.getElementById('contactDetails').style.display = 'none';
        document.getElementById('location').style.display = 'none';
        var skill1 = document.getElementById('skill-1');
        var skill2input = document.getElementById('skill-2-input');
        var skill3input = document.getElementById('skill-3-input');
        skill1.onchange = function() {
            skill2input.innerHTML = "<input type='text' id='skill-2' name='skills'><br />";
            var skill2 = document.getElementById('skill-2');
            skill2.onchange = function() {
                skill3input.innerHTML = "<input type='text' id='skill-3' name='skills'><br />";
            }
        }
        
    }

    

</script>

<template>
    <EmployeeNavbar page='home' :numNotifs='notifs'></EmployeeNavbar>
    <div class= 'container'>
        <h1 class ='title'> User Profile SetUp </h1>
        <div class= 'bar'>
            <button @click = 'personalDetails' id= 'personalDetails-button'> Personal Details </button>
            <button @click = 'contactDetails' id= 'contactDetails-button'> Contact Details </button>
            <button @click= 'location' id='location-button'> Location </button>
            <button @click= 'softskills' id='softskills-button'> Soft Skills </button>
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
            <button @click = 'location'> Next </button>
        </div>
        <div id='location' style='display:none;'>
            <h1> Location </h1> 
            <p> So we can find jobs near you, enter the closest town/city to your home <br /> and how far you are willing to travel to work (range). <br /> We're also going to need the timezone where you live </p>
            <form>
                <label for='city'>City/Town:</label><br />
                <input type='text' id='city' name='city'><br />
                <label for='range'>Range:</label><br />
                <input type='range' min='0' max='100' value='50' step='20' list='tickmarks' id='range' name='range'>
                <datalist id='tickmarks'>
                    <option>0</option>
                    <option>20</option>
                    <option>40</option>
                    <option>60</option>
                    <option>80</option>
                    <option>100</option>
                </datalist> <br />
                <div id = 'output'>  </div>
                <label for='timezone'>Timezone:</label><br />
                <select id='timezone' name='timezone'>
                    <option> Timezone 1 </option>
                    <option> Timezone 2 </option>
                    <option> Timezone 3 </option>
                </select>
            </form>
            <button @click = 'contactDetails'> Back </button>
            <button @click = 'softskills'> Next </button>
        </div>

        <div id='softskills' style='display:none;'>
            <h1> Soft Skills </h1> 
            <p> First impressions count! <br /> Enter a brief sentence to describe yourself and up to three of your most relevant skills </p>
            <form>
                <label for='topic'>topic sentence:</label><br />
                <input type='text' id='topic' name='topic'><br />
                <label for='skills'>Notable skills:</label><br />
                <input type='text' id='skill-1' name='skills'><br />
                <div id='skill-2-input'> </div>
                <div id='skill-3-input'> </div>
            </form>
            <button @click = 'location'> Back </button>
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

    .output{
        font-size: 8;
    }
    
</style>
