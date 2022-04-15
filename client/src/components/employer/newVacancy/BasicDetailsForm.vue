<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';    

    const props = defineProps(['companyName']);
    const emit = defineEmits(['next']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'CompanyName': Joi.string(),
            'VacancyName': Joi.string().max(80).required().label('position title'),
            'Salary': Joi.string().required().max(80).label('salary')
        });

        // get input data
        const data = {
            'CompanyName': document.querySelector('input[name="CompanyName"]').value,
            'VacancyName': document.querySelector('input[name="VacancyName"]').value,
            'Salary': document.querySelector('input[name="Salary"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
</script>

<template>
    <FormHeader title='Basic Details'>
        Let's start off with the simple stuff. Enter the position title and wage/salary.
    </FormHeader>

    <FormText type='text' label='company name' name='CompanyName' :value='props.companyName' :readonly='true' />
    <FormText type='text' label='position title' name='VacancyName' />
    <FormText type='text' label='salary/wage' name='Salary' placeholder='e.g. NMW or £30,000 pa or $8/hr' />

    <FormButtons :next='true' @next='validate()' />
</template>

<style>

</style>