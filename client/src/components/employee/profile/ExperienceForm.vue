<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import $ from 'jquery';


    const emit = defineEmits(['next', 'back']);

    $(document).ready(function(){

        $('#position1').on("input", function(){
            $('#position2-input').show();
        });
        $('#position2').on("input", function(){
            $('#position3-input').show();
        });
    });


    const validate = () => {
        // define schema
        const schema = Joi.object({
            'position1': Joi.string().alphanum().max(80).required().label('position1'),
            'position1start': Joi.string().alphanum().max(80).required().label('position1start'),
            'position1end': Joi.string().alphanum().max(80).required().label('position1end')
        });

        // get input data
        const data = {
            'position1': document.querySelector('input[name="position1"]').value,
            'position1start': document.querySelector('input[name="position1start"]').value,
            'position1end': document.querySelector('input[name="position1end"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

    
</script>

<template>
    <h1> Experience </h1> 
    <p> Include up to three of your most relevant or most recent jobs/placements/internships below </p>
    <div id='myform'>
        <label for='position1'>position title:</label><br />
        <input type='text' id='position1' name='position1'><br />
        <label for='position1start'>start date:</label>
        <label for='position1end'>end date:</label><br />
        <input type='date' id='position1start' name='position1start'> 
        <input type='date' id='position1end' name='position1end'> <br />

        <div id='position2-input' style = 'display:none;'>
            <label for='position2'>position title:</label><br />
            <input type='text' id='position2' name='position2'><br />
            <label for='position2start'>start date:</label>
            <label for='position2end'>end date:</label><br />
            <input type='date' id='position2start' name='position2start'> 
            <input type='date' id='position2end' name='position2end'> <br />
        </div>

        <div id='position3-input' style = 'display:none;'>
            <label for='position3'>position title:</label><br />
            <input type='text' id='position3' name='position3'><br />
            <label for='position3start'>start date:</label>
            <label for='position3end'>end date:</label><br />
            <input type='date' id='position3start' name='position3start'> 
            <input type='date' id='position3end' name='position3end'> <br />
        </div>
    </div>
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>