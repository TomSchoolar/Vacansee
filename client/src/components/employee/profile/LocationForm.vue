<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    const emit = defineEmits(['next', 'back']);

    const dropdownOptions = [ ];

    for(let i = -11; i < 12; i++) {
        let symbol = "";

        if(i <= 0)
        {
            symbol = "+";
        }

        dropdownOptions.push({
            value: i,
            text: "GMT " + symbol + i,
        });
    }


    const validate = () => {
        // define schema
        const schema = Joi.object({
            'Location': Joi.string().alphanum().max(80).required().label('position title'),
            'TimeZone': Joi.string().required().label('pronouns')
        });

        // get input data
        const data = {
            'Location': document.querySelector('input[name="Location"]').value,
            'TimeZone': document.querySelector('input[name="TimeZone"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

</script>

<template>
    <h1> Location </h1> 
    <p> So we can find jobs near you, enter the closest town/city to your home and how far you are willing to travel to work (range). <br />We're also going to need the TimeZone where you live </p>
    <div id='myform'>
        <label for='Location'>City/Town:</label><br />
        <input type='text' id='Location' name='Location'><br />
        <label for='TimeZone'>TimeZone:</label><br />
        <select id='TimeZone' name='TimeZone'>
            <option v-for='option in dropdownOptions' :key='option.value' :value='option.value'>{{ option.text }}</option>
        </select>
    </div>

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>