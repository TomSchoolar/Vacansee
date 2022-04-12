<script setup>
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';

    const props = defineProps(['companyName']);
    const emit = defineEmits(['next']);
</script>

<template>
    <FormHeader title='Basic Details'>
        Let's start off with the simple stuff. Enter the position title and wage/salary.
    </FormHeader>

    <FormText type='text' label='company name' name='companyName' :value='props.companyName' :disabled='true' />
    <FormText type='text' label='position title' name='vacancyName' />
    <FormText type='text' label='salary/wage' name='salary' placeholder='e.g. NMW or £30,000 pa or $8/hr' />

    <FormButtons :next='true' @next='emit("next")' />
</template>

<style>

</style>