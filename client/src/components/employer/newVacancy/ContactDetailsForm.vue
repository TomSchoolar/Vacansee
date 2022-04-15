<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';

    const props = defineProps(['phoneNumber', 'email']);
    const emit = defineEmits(['back', 'next']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'PhoneNumber': Joi.string().min(8).max(30).required().label('phone number'),
            'Email': Joi.string().email({ tlds: { allow: false } }).max(254).required().label('email'),
        });

        // get input data
        const data = {
            'PhoneNumber': document.querySelector('input[name="PhoneNumber"]').value,
            'Email': document.querySelector('input[name="Email"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
</script>

<template>
    <FormHeader title='Contact Details'>
        We need your contact details next. Enter a current phone number and email address.
    </FormHeader>

    <FormText type='text' label='phone number' name='PhoneNumber' :value='phoneNumber ? phoneNumber : ""' />
    <FormText type='email' label='email' name='Email' :value='email ? email : ""' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>