<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    const emit = defineEmits(['next', 'back']);

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'qualification': Joi.string().alphanum().max(80).required().label('qualification')
        });

        // get input data
        const data = {
            'qualification': document.querySelector('input[name="qualification"]').value
        }

        // validate and handle any errors
        if(validateForm(schema, data))
            emit('next');
    }
    
</script>

<template>
    <h1> Qualifications </h1> 
    <p> Enter up to three sets of qualifications below E.g. GCSEs, A-Levels, Degree. <br /> Include the number of that type of qualification you got and the minimum and maximum grades you achieved.</p>
    <form>
        <label for='qualification'>qualification type:</label><br />
        <select id='qualification' name='qualification'>
            <option value = 'temp' hidden selected> Choose option </option>
            <option value = 'gcses'> GCSEs </option>
            <option value = 'alevels'> A Levels </option>
            <option value = 'degree'> Degree </option>
            <option value = 'other'> Other: </option>
        </select> <br />
        <div id='gcse-alevel-form' style='display:none;'>
            <label for='lowgrade'>lowest grade:</label> <label for='highgrade'>highest grade:</label> <label for='number'>number:</label><br />
            <input type='text' id='lowgrade' name='lowgrade' size='7'> <input type='text' id='highgrade' name='highgrade' size='7'> <input type='number' id='number' name='number' min = '1' max = '10' style = 'width = 6px;'><br />
        </div>
        <div id='degree-form' style='display:none;'>
            <label for='subject'>subject:</label><br />
            <input type='text' id='subject' name='subject'><br />
            <label for='type'>type:</label> <label for='classification'>classification:</label> <br />
            <input type='text' id='type' name='type' size='4'> <input type='text' id='classification' name='classification' size='10'> <br />
        </div>
    </form>
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>