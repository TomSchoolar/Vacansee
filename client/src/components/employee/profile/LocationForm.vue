<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'city': Joi.string().alphanum().max(80).required().label('position title'),
            'range': Joi.string(),
            'timezone': Joi.string().required().label('pronouns')
        });

        // get input data
        const data = {
            'city': document.querySelector('input[name="city"]').value,
            'range': document.querySelector('input[name="range"]').value,
            'timezone': document.querySelector('input[name="timezone"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }

</script>

<template>
    <h1> Location </h1> 
    <p> So we can find jobs near you, enter the closest town/city to your home and how far you are willing to travel to work (range). <br />We're also going to need the timezone where you live </p>
    <form>
        <label for='city'>City/Town:</label><br />
        <input type='text' id='city' name='city'><br />
        <label for='range'>Range:</label><br />
        <input type='range' min='0' max='100' value='50' step='20' list='tickmarks' id='range' name='range'>
        <datalist id='tickmarks'>
            <option>0</option>
            <option>20</option>
            <option>40</option>
            <option>60</option>
            <option>80</option>
            <option>100</option>
        </datalist> <br />
        <div id = 'output'>  </div>
        <label for='timezone'>Timezone:</label><br />
        <select id='timezone' name='timezone'>
            <option> Timezone 1 </option>
            <option> Timezone 2 </option>
            <option> Timezone 3 </option>
        </select>
    </form>

    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>