<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';

    const props = defineProps(['tags', 'options']);
    const emit = defineEmits(['next', 'back']);

</script>

<template>
    <FormHeader title='Tags'>
        In order to help well-suited applicants find this vacancy more easily, select as many tags below as are relevant to the position.
    </FormHeader>

    <FormSelect label='tags' name='tagsInput' :multiple='true' :options='options' :multipleValue='true' :value='tags' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>