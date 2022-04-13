<script setup>
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';

    const emit = defineEmits(['next', 'back']);
    const options = [
        {
            value: '0;fa-solid fa-book',
            text: 'book'
        },
        {
            value: '1;fa-solid fa-code',
            text: 'code'
        },
        {
            value: '2;fa-brands fa-python',
            text: 'python'
        },
        {
            value: '3;fa-solid fa-school',
            text: 'school'
        },
        {
            value: '4;fa-solid fa-briefcase',
            text: 'briefcase'
        },
        {
            value: '5;fa-solid fa-database',
            text: 'database'
        },
    ]
</script>

<template>
    <FormHeader title='Tags'>
        In order to help well-suited applicants find this vacancy more easily, select as many tags below as are relevant to the position.
    </FormHeader>

    <FormSelect label='tags' name='tags' :multiple='true' :options='options' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>