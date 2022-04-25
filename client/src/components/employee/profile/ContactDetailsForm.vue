<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'PhoneNumber': Joi.string().min(8).max(30).required().label('PhoneNumber'),
        });

        // get input data
        const data = {
            'PhoneNumber': document.querySelector('input[name="PhoneNumber"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

</script>

<template>
    <h1> Contact Details </h1> 
    <p> We need your contact details next. Enter a current phone number and Email address </p>
    <div id='myform'>
        <label for='PhoneNumber'>Phone number:</label><br />
        <input type='text' id='PhoneNumber' name='PhoneNumber'><br />
    </div>

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>