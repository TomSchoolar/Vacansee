<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import FormExpandingText from '@/components/employer/newVacancy/formComponents/FormExpandingText.vue';

    const props = defineProps(['Experience'])
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'Experience-1': Joi.string().min(0).max(200).label('experience'),

            'Experience-2': Joi.string().min(0).max(200).label('experience'),

            'Experience-3': Joi.string().min(0).max(200).label('experience')
        })

        // get input data
        const data = {
            'Experience-1': document.querySelector('input[name="Experience-1"]').value,
            'Experience-2': document.querySelector('input[name="Experience-2"]').value,
            'Experience-3': document.querySelector('input[name="Experience-3"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data, { addErrorToParent: ['Experience-1', 'Experience-2', 'Experience-3']}))
            emit('next');
    }

    
</script>

<template>
    <FormHeader title='Experience'>
        Include up to three of your most relevant or most recent jobs/placements/internships below
    </FormHeader>

    <FormExpandingText label='experience' name='Experience' :max='3' :value='props.Experience' />
    
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>