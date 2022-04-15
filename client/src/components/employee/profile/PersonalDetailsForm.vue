<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    const props = defineProps(['companyName']);
    const emit = defineEmits(['next']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'fname': Joi.string().alphanum().max(80).required().label('fname'),
            'lname': Joi.string().alphanum().max(80).required().label('lname'),
            'pronouns': Joi.string().required().label('pronouns')
        });

        // get input data
        const data = {
            'fname': document.querySelector('input[name="fname"]').value,
            'lname': document.querySelector('input[name="lname"]').value,
            'pronouns': document.querySelector('input[name="pronouns"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }


</script>

<template>
    <div id ='personalDetails'> 
            <h1> Personal Details </h1> 
            <p> Let's start off with the simple stuff. Enter your first and last name and your pronouns </p>
            <form>
                <label for='fname'>First name:</label><br />
                <input type='text' id='fname' name='fname'><br />
                <label for='lname'>Last name:</label><br />
                <input type='text' id='lname' name='lname'> <br />
                <label>Pronouns:</label><br />
                <select id='pronouns' name='pronouns'>
                    <option value = 'he/him'> He/Him </option>
                    <option value = 'she/her'> She/Her </option>
                    <option value = 'they/them'> They/Them </option>
                </select>
            </form>
    </div>

    <FormButtons :next='true' @next='emit("next")' />
</template>

<style>

</style>