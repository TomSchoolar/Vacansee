<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import $ from 'jquery';

    const emit = defineEmits(['next', 'back']);

    $(document).ready(function(){

        $('#position-1').on("input", function(){
            $('#position-2-input').show();
        });
        $('#position-2').on("input", function(){
            $('#position-3-input').show();
        });
    });


    const validate = () => {
        // define schema
        const schema = Joi.object({
            'position-1': Joi.string().alphanum().max(80).required().label('positions'),
            'position-1-start': Joi.string().alphanum().max(80).required().label('position-1-start'),
            'position-1-end': Joi.string().alphanum().max(80).required().label('position-1-end')
        });

        // get input data
        const data = {
            'position-1': document.querySelector('input[name="position-1"]').value,
            'position-1-start': document.querySelector('input[name="position-1-start"]').value,
            'position-1-end': document.querySelector('input[name="position-1-end"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

    
</script>

<template>
    <h1> Experience </h1> 
    <p> Include up to three of your most relevant or most recent jobs/placements/internships below </p>
    <form>
        <label for='positions'>position title:</label><br />
        <input type='text' id='position-1' name='positions'><br />
        <label for='position-1-start'>start date:</label>
        <label for='position-1-end'>end date:</label><br />
        <input type='date' id='position-1-start' name='position-1-start'> 
        <input type='date' id='position-1-end' name='position-1-end'> <br />

        <div id='position-2-input' style = 'display:none;'>
            <label for='positions'>position title:</label><br />
            <input type='text' id='position-2' name='positions'><br />
            <label for='position-2-start'>start date:</label>
            <label for='position-2-end'>end date:</label><br />
            <input type='date' id='position-2-start' name='position-1-start'> 
            <input type='date' id='position-2-end' name='position-1-end'> <br />
        </div>

        <div id='position-3-input' style = 'display:none;'>
            <label for='positions'>position title:</label><br />
            <input type='text' id='position-3' name='positions'><br />
            <label for='position-3-start'>start date:</label>
            <label for='position-3-end'>end date:</label><br />
            <input type='date' id='position-3-start' name='position-1-start'> 
            <input type='date' id='position-3-end' name='position-1-end'> <br />
        </div>
    </form>
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>