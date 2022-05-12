<script setup>
    import Joi from 'joi';
    import validateForm from '@/assets/js/formValidator';
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import FormExpandingDoubleText from '@/components/employer/newVacancy/formComponents/FormExpandingDoubleText.vue';

    const props = defineProps(['Experience'])
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'Experience-1': Joi.string().min(0).max(50).label('experience position'),
            'Experience-1-time': Joi.string().min(0).max(20).label('experience time'),
            
            'Experience-2': Joi.string().min(0).max(50).label('experience position'),
            'Experience-2-time': Joi.string().min(0).max(20).label('experience time'),
            
            'Experience-3': Joi.string().min(0).max(50).label('experience position'),
            'Experience-3-time': Joi.string().min(0).max(20).label('experience time'),
        }).when('.Experience-1', { is: Joi.string().min(1), then: Joi.object({ 'Experience-1-time': Joi.string().min(1).required() }).required() })
        .when('.Experience-2', { is: Joi.string().min(1), then: Joi.object({ 'Experience-2-time': Joi.string().min(1).required() }).required() })
        .when('.Experience-3', { is: Joi.string().min(1), then: Joi.object({ 'Experience-3-time': Joi.string().min(1).required() }).required() })

        // get input data
        const data = {
            'Experience-1': document.querySelector('input[name="Experience-1"]').value,
            'Experience-1-time': document.querySelector('input[name="Experience-1-time"]').value,
            
            'Experience-2': document.querySelector('input[name="Experience-2"]').value,
            'Experience-2-time': document.querySelector('input[name="Experience-2-time"]').value,
            
            'Experience-3': document.querySelector('input[name="Experience-3"]').value,
            'Experience-3-time': document.querySelector('input[name="Experience-3-time"]').value,
        }
        

        // validate and handle any errors
        if(validateForm(schema, data, { addErrorToParent: ['Experience-1', 'Experience-1-time', 'Experience-2', 'Experience-2-time', 'Experience-3', 'Experience-3-time'] }))
            emit('next');
    }

    
</script>

<template>
    <FormHeader title='Experience'>
        Include up to three of your most relevant or most recent jobs/placements/internships below
    </FormHeader>

    <FormExpandingDoubleText 
        label='experience' 
        name='Experience' 
        placeholder='position' 
        secondPlaceholder='time' 
        :max='3' 
    />
    
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate()' />
</template>

<style>

</style>