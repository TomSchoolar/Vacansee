<script setup>
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';
    import $ from 'jquery';

    const emit = defineEmits(['next', 'back']);

    $(document).ready(function(){

        $('#qualification1').change(function(){
            console.log('hello');
            if ($(this).val() == 'gcses' || $(this).val() == 'alevels' ) {
                console.log('hello');
                $('#gcse-alevel-form').show();
                $('#degree-form').hide();
            }
            else if ($(this).val() == 'degree') {
                $('#degree-form').show();
                $('#gcse-alevel-form').hide();
            }
            
        });

        $('#qualification2').change(function(){
                console.log('hello');
                if ($(this).val() == 'gcses' || $(this).val() == 'alevels' ) {
                    console.log('hello');
                    $('#gcse-alevel-form2').show();
                    $('#degree-form2').hide();
                }
                else if ($(this).val() == 'degree') {
                    $('#degree-form2').show();
                    $('#gcse-alevel-form2').hide();
                }
                
            });

        
        $('#qualification3').change(function(){
            console.log('hello');
            if ($(this).val() == 'gcses' || $(this).val() == 'alevels' ) {
                console.log('hello');
                $('#gcse-alevel-form3').show();
                $('#degree-form3').hide();
            }
            else if ($(this).val() == 'degree') {
                $('#degree-form3').show();
                $('#gcse-alevel-form3').hide();
            }
            
        });

    });

    const validate = () => {
        // define schema
        const schema = Joi.object({
            'qualification1': Joi.string().alphanum().max(80).required().label('qualification1'),
            'lowgrade1': Joi.string().alphanum().max(3).required().label('lowgrade1'),
            'highgrade1': Joi.string().alphanum().max(3).required().label('highgrade1'),
            'number1': Joi.string().number().required().label('number1'),
            'subject1': Joi.string().alphanum().max(80).required().label('subject1'),
            'type1': Joi.string().alphanum().max(10).required().label('type1'),
            'classification1': Joi.string().alphanum().max(10).required().label('classification1'),

            'qualification2': Joi.string().alphanum().max(80).required().label('qualification2'),
            'lowgrade2': Joi.string().alphanum().max(3).required().label('lowgrade2'),
            'highgrade2': Joi.string().alphanum().max(3).required().label('highgrade2'),
            'number2': Joi.string().number().required().label('number2'),
            'subject2': Joi.string().alphanum().max(80).required().label('subject2'),
            'type2': Joi.string().alphanum().max(10).required().label('type2'),
            'classification2': Joi.string().alphanum().max(10).required().label('classification2'),

            'qualification3': Joi.string().alphanum().max(80).required().label('qualification3'),
            'lowgrade3': Joi.string().alphanum().max(3).required().label('lowgrade3'),
            'highgrade3': Joi.string().alphanum().max(3).required().label('highgrade3'),
            'number3': Joi.string().number().required().label('number3'),
            'subject3': Joi.string().alphanum().max(80).required().label('subject3'),
            'type3': Joi.string().alphanum().max(10).required().label('type3'),
            'classification3': Joi.string().alphanum().max(10).required().label('classification3'),

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
    <div id='myform'>
        <div class='qual-1'>
            <label for='qualification1'>qualification type:</label><br />
            <select id='qualification1' name='qualification1'>
                <option value = 'temp' hidden selected> Choose option </option>
                <option value = 'gcses'> GCSEs </option>
                <option value = 'alevels'> A Levels </option>
                <option value = 'degree'> Degree </option>
                <option value = 'other'> Other: </option>
            </select> <br />
            <div id='gcse-alevel-form' style='display:none;'>
                <label for='lowgrade1'>lowest grade:</label> <label for='highgrade1'>highest grade:</label> <label for='number1'>number:</label><br />
                <input type='text' id='lowgrade1' name='lowgrade1' size='7'> <input type='text' id='highgrade1' name='highgrade1' size='7'> <input type='number' id='number1' name='number1' min = '1' max = '10' style = 'width = 6px;'><br />
            </div>
            <div id='degree-form' style='display:none;'>
                <label for='subject1'>subject:</label><br />
                <input type='text' id='subject1' name='subject1'><br />
                <label for='type1'>type:</label> <label for='classification1'>classification:</label> <br />
                <input type='text' id='type1' name='type1' size='4'> <input type='text' id='classification1' name='classification1' size='10'> <br />
            </div>
        </div>

        <div class='qual-2'>
            <label for='qualification2'>qualification type:</label><br />
            <select id='qualification2' name='qualification2'>
                <option value = 'null' hidden selected> Choose option </option>
                <option value = 'gcses'> GCSEs </option>
                <option value = 'alevels'> A Levels </option>
                <option value = 'degree'> Degree </option>
                <option value = 'other'> Other: </option>
            </select> <br />
            <div id='gcse-alevel-form2' style='display:none;'>
                <label for='lowgrade2'>lowest grade:</label> <label for='highgrade2'>highest grade:</label> <label for='number2'>number:</label><br />
                <input type='text' id='lowgrade2' name='lowgrade2' size='7'> <input type='text' id='highgrade2' name='highgrade2' size='7'> <input type='number' id='number2' name='number2' min = '1' max = '10' style = 'width = 6px;'><br />
            </div>
            <div id='degree-form2' style='display:none;'>
                <label for='subject2'>subject:</label><br />
                <input type='text' id='subject2' name='subject2'><br />
                <label for='type2'>type:</label> <label for='classification2'>classification:</label> <br />
                <input type='text' id='type2' name='type2' size='4'> <input type='text' id='classification2' name='classification2' size='10'> <br />
            </div>
        </div>

        <div class='qual-3'>
            <label for='qualification3'>qualification type:</label><br />
            <select id='qualification3' name='qualification3'>
                <option value = 'null' hidden selected> Choose option </option>
                <option value = 'gcses'> GCSEs </option>
                <option value = 'alevels'> A Levels </option>
                <option value = 'degree'> Degree </option>
                <option value = 'other'> Other: </option>
            </select> <br />
            <div id='gcse-alevel-form3' style='display:none;'>
                <label for='lowgrade3'>lowest grade:</label> <label for='highgrade3'>highest grade:</label> <label for='number3'>number:</label><br />
                <input type='text' id='lowgrade3' name='lowgrade3' size='7'> <input type='text' id='highgrade3' name='highgrade3' size='7'> <input type='number' id='number3' name='number3' min = '1' max = '10' style = 'width = 6px;'><br />
            </div>
            <div id='degree-form3' style='display:none;'>
                <label for='subject3'>subject:</label><br />
                <input type='text' id='subject3' name='subject3'><br />
                <label for='type3'>type:</label> <label for='classification3'>classification:</label> <br />
                <input type='text' id='type3' name='type3' size='4'> <input type='text' id='classification3' name='classification3' size='10'> <br />
            </div>
        </div>
    </div>
    <FormButtons :back='true' :next='true' @back='emit("back")' @next='emit("next")' />
</template>

<style>

</style>