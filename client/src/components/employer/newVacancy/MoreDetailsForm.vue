<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormTextArea from '@/components/employer/newVacancy/formComponents/FormTextArea.vue';
    import FormExpandingText from '@/components/employer/newVacancy/formComponents/FormExpandingText.vue';

    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'Description': Joi.string().min(10).max(150).required().label('description'),
            'SkillsRequired-1': Joi.string().min(0).max(50).label('skill 1'),
            'SkillsRequired-2': Joi.string().min(0).max(50).label('skill 2'),
            'SkillsRequired-3': Joi.string().min(0).max(50).label('skill 3'),
        });

        // get input data
        const data = {
            'Description': document.querySelector('textarea[name="Description"]').value,
            'SkillsRequired-1': document.querySelector('input[name="SkillsRequired-1"]').value,
            'SkillsRequired-2': document.querySelector('input[name="SkillsRequired-2"]').value,
            'SkillsRequired-3': document.querySelector('input[name="SkillsRequired-3"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
</script>

<template>
    <FormHeader title='More Details'>
        Enter more job specifics so applicants know what they're applying for.
    </FormHeader>

    <FormTextArea label='job description' name='Description' rows='7' />
    <FormExpandingText label='necessary skills' name='SkillsRequired' :max='3' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>