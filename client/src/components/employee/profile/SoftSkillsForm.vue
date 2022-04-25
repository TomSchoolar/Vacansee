<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import $ from 'jquery';

    const emit = defineEmits(['next', 'back']);

    $(document).ready(function(){

        $('#skill1').on("input", function(){
            $('#skill2').show();
        });
        $('#skill2').on("input", function(){
            $('#skill3').show();
        });
    });

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'TopicSentence': Joi.string().alphanum().max(80).required().label('TopicSentence'),
            'skill1': Joi.string().alphanum().max(80).required().label('skill1'),
            'skill2': Joi.string().alphanum().max(80).required().label('skill2'),
            'skill3': Joi.string().alphanum().max(80).required().label('skill3')
        });

        // get input data
        const data = {
            'TopicSentence': document.querySelector('input[name="TopicSentence"]').value,
            'skill1': document.querySelector('input[name="skill1"]').value,
            'skill2': document.querySelector('input[name="skill2"]').value,
            'skill3': document.querySelector('input[name="skill3"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
    
</script>

<template>
    <h1> Soft Skills </h1> 
    <p> First impressions count! Enter a brief sentence to describe yourself and up to three of your most relevant skills </p>
    
        <label for='TopicSentence'>Topic sentence:</label><br />
        <input type='text' id='TopicSentence' name='TopicSentence'><br />

        <label for='skill1'>Notable skills:</label><br />
        <input type='text' id='skill1' name='skill1'><br />
        <input type='text' id='skill2' name='skill2' style = 'display:none;'><br />
        <input type='text' id='skill3' name='skill3' style = 'display:none;'><br />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>