<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormTextArea from '@/components/employer/newVacancy/formComponents/FormTextArea.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormExpandingText from '@/components/employer/newVacancy/formComponents/FormExpandingText.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    const props = defineProps(['Description', 'NotableSkills'])
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'TopicSentence': Joi.string().max(200).required().label('profile description'),
            'NotableSkills-1': Joi.string().min(0).max(50).label('skill 1'),
            'NotableSkills-2': Joi.string().min(0).max(50).label('skill 2'),
            'NotableSkills-3': Joi.string().min(0).max(50).label('skill 3')
        });

        // get input data
        const data = {
            'TopicSentence': document.querySelector('textarea[name="TopicSentence"]').value,
            'NotableSkills-1': document.querySelector('input[name="NotableSkills-1"]').value,
            'NotableSkills-2': document.querySelector('input[name="NotableSkills-2"]').value,
            'NotableSkills-3': document.querySelector('input[name="NotableSkills-3"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data, { addErrorToParent: ['NotableSkills-1', 'NotableSkills-2', 'NotableSkills-3' ]}))
            emit('next');
    }
    
</script>

<template>
    <FormHeader title='Soft Skills'>
        First impressions count! Enter a brief sentence to describe yourself and up to three of your most relevant skills
    </FormHeader>

    <FormTextArea label='topic sentence' name='TopicSentence' rows='4' :value='props.Description' />
    <FormExpandingText label='notable skills' name='NotableSkills' :max='3' :value='props.NotableSkills' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />

</template>

<style>

</style>