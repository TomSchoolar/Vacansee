<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    const props = defineProps(['companyName']);
    const emit = defineEmits(['next']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'FirstName': Joi.string().alphanum().max(80).required().label('FirstName'),
            'LastName': Joi.string().alphanum().max(80).required().label('LastName'),
            'Pronouns': Joi.string().required().label('Pronouns'),
            'PhoneNumber': Joi.string().min(8).max(30).required().label('PhoneNumber'),
        });

        // get input data
        const data = {
            'FirstName': document.querySelector('input[name="FirstName"]').value,
            'LastName': document.querySelector('input[name="LastName"]').value,
            'Pronouns': document.querySelector('input[name="Pronouns"]').value,
            'PhoneNumber': document.querySelector('input[name="PhoneNumber"]').value,
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }


</script>

<template>
    <div id ='personalDetails'> 
            <h1> Personal Details </h1> 
            <p> Let's start off with the simple stuff. Enter your name, pronouns and phone number</p>
            <label for='FirstName'>First name:</label><br />
            <input type='text' id='FirstName' name='FirstName'><br />
            <label for='LastName'>Last name:</label><br />
            <input type='text' id='LastName' name='LastName'> <br />
            <label>Pronouns:</label><br />
            <select id='Pronouns' name='Pronouns'>
                <option value = 'he/him'> He/Him </option>
                <option value = 'she/her'> She/Her </option>
                <option value = 'they/them'> They/Them </option>
            </select><br />
            <label for='PhoneNumber'>Phone number:</label><br />
            <input type='text' id='PhoneNumber' name='PhoneNumber'><br />
    </div>

    <FormButtons :next='true' @next='emit("next")' />
</template>

<style>

</style>