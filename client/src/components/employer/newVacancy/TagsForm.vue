<script setup>
    import Joi from 'joi';
    import api, { apiCatchError } from '@/assets/js/api';
    import validateForm from '@/assets/js/formValidator';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';

    const props = defineProps(['tags', 'options']);
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'tagsInput': Joi.array().min(1).max(10).label('tags'),
        });

        // get input data
        const data = {
            'tagsInput': Array.from(document.querySelectorAll('select[name="tagsInput"] option:checked')),
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
</script>

<template>
    <FormHeader title='Tags'>
        In order to help well-suited applicants find this vacancy more easily, select as many tags below as are relevant to the position.
    </FormHeader>

    <FormSelect label='tags' name='tagsInput' :multiple='true' :options='options' :multipleValue='true' :value='tags' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='validate' />
</template>

<style>

</style>