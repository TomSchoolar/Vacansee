<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormExpandingDoubleText from '@/components/employer/newVacancy/formComponents/FormExpandingDoubleText.vue';

    const emit = defineEmits(['next', 'back']);

    const dropdownOptions = [ ];

    for(let i = -11; i < 12; i++) {
        let symbol = "";

        if(i <= 0)
        {
            symbol = "+";
        }

        dropdownOptions.push({
            value: i,
            text: "GMT " + symbol + i,
        });
    }

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'ExperienceRequired-1': Joi.string().min(0).max(50).label('experience position'),
            'ExperienceRequired-1-time': Joi.string().min(0).max(20).label('experience time'),
            
            'ExperienceRequired-2': Joi.string().min(0).max(50).label('experience position'),
            'ExperienceRequired-2-time': Joi.string().min(0).max(20).label('experience time'),
            
            'ExperienceRequired-3': Joi.string().min(0).max(50).label('experience position'),
            'ExperienceRequired-3-time': Joi.string().min(0).max(20).label('experience time'),

            'Location': Joi.string().max(30).required().label('location'),
            'TimeZone': Joi.string().required().label('timezone')
        }).when('.ExperienceRequired-1', { is: Joi.string().min(1), then: Joi.object({ 'ExperienceRequired-1-time': Joi.string().min(1).required() }).required() })
        .when('.ExperienceRequired-2', { is: Joi.string().min(1), then: Joi.object({ 'ExperienceRequired-2-time': Joi.string().min(1).required() }).required() })
        .when('.ExperienceRequired-3', { is: Joi.string().min(1), then: Joi.object({ 'ExperienceRequired-3-time': Joi.string().min(1).required() }).required() })

        // get input data
        const data = {
            'ExperienceRequired-1': document.querySelector('input[name="ExperienceRequired-1"]').value,
            'ExperienceRequired-1-time': document.querySelector('input[name="ExperienceRequired-1-time"]').value,
            
            'ExperienceRequired-2': document.querySelector('input[name="ExperienceRequired-2"]').value,
            'ExperienceRequired-2-time': document.querySelector('input[name="ExperienceRequired-2-time"]').value,
            
            'ExperienceRequired-3': document.querySelector('input[name="ExperienceRequired-3"]').value,
            'ExperienceRequired-3-time': document.querySelector('input[name="ExperienceRequired-3-time"]').value,

            'Location': document.querySelector('input[name="Location"]').value,
            'TimeZone': document.querySelector('select[name="TimeZone"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data, { addErrorToParent: ['ExperienceRequired-1', 'ExperienceRequired-1-time', 'ExperienceRequired-2', 'ExperienceRequired-2-time', 'ExperienceRequired-3', 'ExperienceRequired-3-time']}))
            emit('next');
    }
</script>

<template>
    <FormHeader title='Logistics'>
        So we can find good applications that are cohesive with your team, enter how much experience is required for the position and the timezone in which candidates should be based.
    </FormHeader>

    <FormExpandingDoubleText label='relevant experience required' name='ExperienceRequired' placeholder='position' secondPlaceholder='time' :max='3' />
    <FormText label='nearest city' name='Location' type='text' />
    <FormSelect label='timezone' name='TimeZone' placeholder='select a timezone' :options='dropdownOptions' />


    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>