<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';

    const props = defineProps(['Location', 'TimeZone']);
    const emit = defineEmits(['next', 'back']);

    const tz = 0;

    const dropdownOptions = [ ];

    for(let i = -11; i < 12; i++) {
        let symbol = "+";

        if(i < 0)
        {
            symbol = "";
        }

        dropdownOptions.push({
            value: i,
            text: "GMT" + symbol + i,
        });
    }

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'Location': Joi.string().max(30).required().label('location'),
            'TimeZone': Joi.string().required().label('timezone')
        });

        // get input data
        const data = {
            'Location': document.querySelector('input[name="Location"]').value,
            'TimeZone': document.querySelector('select[name="TimeZone"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

</script>

<template>
    <FormHeader title='Location'>
        So we can find jobs near you, enter the closest town/city to your home. We're also going to need the timezone where you live.
    </FormHeader>

    <FormText type='text' label='location' name='Location' :value='props.Location' />
    <FormSelect label='timezone' name='TimeZone' placeholder='select a timezone' :options='dropdownOptions'  :value='tz' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>