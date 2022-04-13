<script setup>
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';
    import FormTextArea from '@/components/employer/newVacancy/formComponents/FormTextArea.vue';
    import FormExpandingText from '@/components/employer/newVacancy/formComponents/FormExpandingText.vue';

    const emit = defineEmits(['next', 'back']);
</script>

<template>
    <FormHeader title='More Details'>
        Enter more job specifics so applicants know what they're applying for.
    </FormHeader>

    <FormTextArea label='job description' name='Description' rows='7' />
    <FormExpandingText label='necessary skills' name='SkillsRequired' :max='3' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>