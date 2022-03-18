<script setup>
    const props = defineProps(['stats']);

    const download = () => {
        alert('download application');
    };

    const unmatch = () => {
        alert('unmatch');
    };

    const show = () => {
        alert('showing application');
    };

    
</script>



<meta name='viewport' content='width=device-width, initial-scale=1'>
<template>
    <div class='stat-boxes'>
        <p> {{stats.name}} {{stats.pronouns}} <button class='button' @click='show' id='show'>Show Application</button> <br /> 
            {{stats.number}}  <button class='button' @click='download'>Download Application</button><br /> 
            {{stats.email}}  <button class='button unmatch' @click='unmatch'>Unmatch</button> <br /> 
            {{stats.timezone}}  <br />
        </p>
        
    </div>


</template>



<style scoped>

    

    .stat-boxes {
        text-align:left;
        width: 100%;
        display: fixed;
        margin: 10px;
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

    .unmatch{
        float:right;
        background-color: red;
    }
    .button:active{
        background-color:#D3D3D3;
        font-size: 70%;
    }

    .button:hover{
        background-color:#D3D3D3;

    }


    

</style>