<script setup>
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormSelect from '@/components/employer/newVacancy/formComponents/FormSelect.vue';
    import FormExpandingDoubleText from '@/components/employer/newVacancy/formComponents/FormExpandingDoubleText.vue';

    const emit = defineEmits(['next', 'back']);

    const dropdownOptions = [
        {
            value: 'all',
            text: 'all'
        },
        {
            value: 'of',
            text: 'of'
        },
        {
            value: 'the',
            text: 'the'
        },
        {
            value: 'timezones',
            text: 'timezones'
        },
    ];
</script>

<template>
    <FormHeader title='Logistics'>
        So we can find good applications that are cohesive with your team, enter how much experience is required for the position and the timezone in which candidates should be based.
    </FormHeader>

    <FormExpandingDoubleText label='relevant experience required' name='experience' placeholder='position' secondPlaceholder='time' :max='3' />
    <FormSelect label='timezone' name='timezone' placeholder='select a timezone' :options='dropdownOptions' />


    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>