<script setup>
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormDropdown from '@/components/employer/newVacancy/formComponents/FormDropdown.vue';
    import FormExpandingDoubleText from '@/components/employer/newVacancy/formComponents/FormExpandingDoubleText.vue';

    const emit = defineEmits(['next', 'back']);
</script>

<template>
    <FormHeader title='Logistics'>
        So we can find good applications that are cohesive with your team, enter how much experience is required for the position and the timezone in which candidates should be based.
    </FormHeader>

    <FormExpandingDoubleText label='relevant experience required' name='experience' placeholder='position' secondPlaceholder='time' :max='3' />
    <FormDropdown label='timezone' name='timezone' />


    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>