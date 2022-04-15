<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    

    const emit = defineEmits(['next', 'back']);

    $(document).ready(function(){

        $('#skill-1').on("input", function(){
            console.log('hello');
            $('#skill-2').show();
        });
        $('#skill-2').on("input", function(){
            console.log('hello');
            $('#skill-3').show();
        });
    });

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'topic': Joi.string().alphanum().max(80).required().label('topic'),
            'skill-1': Joi.string().alphanum().max(80).required().label('skills')
        });

        // get input data
        const data = {
            'topic': document.querySelector('input[name="topic"]').value,
            'skill-1': document.querySelector('input[name="skills"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
    
</script>

<template>
    <h1> Soft Skills </h1> 
    <p> First impressions count! Enter a brief sentence to describe yourself and up to three of your most relevant skills </p>
    
        <label for='topic'>topic sentence:</label><br />
        <input type='text' id='topic' name='topic'><br />
    <form id='myform'>
        <label for='skills'>Notable skills:</label><br />
        <input type='text' id='skill-1' name='skills'><br />
        <input type='text' id='skill-2' name='skills' style = 'display:none;'><br />
        <input type='text' id='skill-3' name='skills' style = 'display:none;'><br />
        <div id='skill-2-input'> </div>
        <div id='skill-3-input'> </div>
    </form>
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>