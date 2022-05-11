<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormExpandingText from '@/components/employer/newVacancy/formComponents/FormExpandingText.vue';


import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    const props = defineProps(['Qualifications'])
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'Qualifications-1': Joi.string().min(0).max(80).label('qualification 1'),
            'Qualifications-2': Joi.string().min(0).max(80).label('qualification 2'),
            'Qualifications-3': Joi.string().min(0).max(80).label('qualification 3'),
        });

        // get input data
        const data = {
            'Qualifications-1': document.querySelector('input[name="Qualifications-1"]').value,
            'Qualifications-2': document.querySelector('input[name="Qualifications-2"]').value,
            'Qualifications-3': document.querySelector('input[name="Qualifications-3"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data, { addErrorToParent: ['Qualifications-1', 'Qualifications-2', 'Qualifications-3' ]}))
            emit('next');
    }
    
</script>

<template>
    <FormHeader title='Qualifications'>
        Enter up to three sets of qualifications below. Include the number and type of the qualification. E.g. "11 GCSEs (A-C).
    </FormHeader>

    <FormExpandingText label='qualifications' name='Qualifications' :max='3' :value='props.Qualifications' :expectValue='true' />
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>