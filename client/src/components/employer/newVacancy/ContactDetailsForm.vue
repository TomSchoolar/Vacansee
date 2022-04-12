<script setup>
    import FormText from '@/components/employer/newVacancy/formComponents/FormText.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';

    const props = defineProps(['phoneNumber', 'email']);
    const emit = defineEmits(['back', 'next']);
</script>

<template>
    <FormHeader title='Contact Details'>
        We need your contact details next. Enter a current phone number and email address.
    </FormHeader>

    <FormText type='text' label='phone number' name='phoneNumber' :value='props.phoneNumber' />
    <FormText type='email' label='email' name='email' :value='props.email' />

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>