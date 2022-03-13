<script setup>
    const props = defineProps(['stats']);

    const downloadApplication = () => {
        alert('download application');
    };

    const unmatch = () => {
        alert('unmatch');
    };

    const showApplication = () => {
        alert('showing application');
    };

    
</script>



<meta name='viewport' content='width=device-width, initial-scale=1'>
<template>
    <div class='stat-boxes'>
        <p> {{stats.name}} ({{stats.pronouns}}) <button class='application-button application-button-grey' @click='showApplication' id='show'>Show Application</button> <br /> 
            {{stats.phoneNumber}}  <button class='application-button application-button-grey' @click='downloadApplication'>Download Application</button><br /> 
            {{stats.email}}  <button class='application-button application-button-red' @click='unmatch'>Unmatch</button> <br /> 
            {{stats.timeZone}}  <br />
        </p>
        
    </div>


</template>



<style scoped>


    
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
        float: right;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
    }

    .application-button-grey {
        background: var(--slate);
    }

    .application-button-grey:hover, .application-button-grey:focus, .application-button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
  } 

    .application-button-red {
        background: var(--red);
    }
    

    .stat-boxes {
        text-align:left;
        width: 100%;
        display: fixed;
        margin: 10px;
        font-size: 14px;
    }
    
    .button{
        float: right;
        width: 30%;
        background-color:#D3D3D3;
        border: 2px solid;
        border-radius: 5px;
        color: black;
        cursor: pointer;
        display: inline-block;
        font-size: 12px;
        margin-right: 10px;
        text-decoration: none;
        transition-duration: 0.4s;

    }


    

</style>