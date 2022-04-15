<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'phonenum': Joi.string().min(8).max(30).required().label('phonenum'),
            'email': Joi.string().email({ tlds: { allow: false } }).max(254).required().label('email'),
        });

        // get input data
        const data = {
            'phonenum': document.querySelector('input[name="phonenum"]').value,
            'email': document.querySelector('input[name="email"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

</script>

<template>
    <h1> Contact Details </h1> 
    <p> We need your contact details next. Enter a current phone number and email address </p>
    <form>
        <label for='phonenum'>Phone number:</label><br />
        <input type='text' id='phonenum' name='phonenum'><br />
        <label for='email'>Email address:</label><br />
        <input type='text' id='email' name='email'>
    </form>

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>