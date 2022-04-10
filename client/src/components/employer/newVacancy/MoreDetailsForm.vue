<script setup>
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';

    const emit = defineEmits(['next', 'back']);
</script>

<template>
    <FormHeader title='More Details'>
        Enter more job specifics so applicants know what they're applying for.
    </FormHeader>

    <FormText label='company name' name='companyName' :disabled='true' />
    <FormText label='position title' name='vacancyName' />
    <FormText label='salary/wage' name='salary' placeholder='e.g. NMW or £30,000 pa or $8/hr' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>