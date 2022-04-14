<script setup>
    import { onMounted, ref } from 'vue';

    const props = defineProps(['name', 'label', 'placeholder', 'max'])

    let fields = [];
    let activeFields = [];
    const numFields = ref(1);
    
    onMounted(() => {
        // get fields and add event listeners
        const fieldPane = document.getElementById(`expanding-${ props.name }`);
        fields = document.querySelectorAll(`.input-${ props.name }`);
        activeFields.push(fields[0]);

        fieldPane.addEventListener('keyup', () => {
            for(let i = 0; i < activeFields.length; i++) {
                let field = activeFields[i];
                listenerAction(field);
            }
        });
            
        const listenerAction = (input) => {
            let value = input.value;
            const id = input.id.split('-');
            let inputNum = parseInt(id[1]);
            let nextInputNum = ( inputNum + 1 <= props.max ? inputNum + 1 : false );
            let nextInput = document.querySelector(`#${ id[0] }-${ nextInputNum }`);

            if(value && nextInputNum && nextInput.classList.contains('input-hidden')) {
                // field has been populated, add another field if not at max
                nextInput.classList.remove('input-hidden');
                activeFields.push(nextInput);
            }

            // TODO: fix when populate all 3 fields, empty first and second
            
            if(!value && inputNum < activeFields.length && !nextInput?.value) {
                // if current and next fields are empty, a field needs to be removed
                if(activeFields.length > inputNum + 1) {
                    // if there is a field after the next one, its value needs shuffling down
                    shuffleInputValues(inputNum)
                } else {
                    // if the next field is last, it can just be removed
                    activeFields.pop().classList.add('input-hidden')
                }
            }
        };
    });

    const shuffleInputValues = (startIndex) => {
        for(let i = --startIndex; i + 2 < activeFields.length; i++) {
            // move fields values up two places
            activeFields[i].value = activeFields[i+2].value;
            activeFields[i+2].value = '';
        }
        
        // remove last input from form and active fields array
        activeFields.pop().classList.add('input-hidden');
    }


</script>

<template>
    <div class='form-group' :id='`expanding-${ props.name }`'>
        <label :for='`${ props.name }-1`' class='label'>{{ props.label }}:</label>
        <input 
            v-for='i in props.max'
            :key='i' 
            type='text' 
            :name='`${ props.name }-${ i }`' 
            :class='"input " + `input-${ props.name }` + " " + ( i <= numFields ? "" : "input-hidden" )'
            :id='`${ props.name }-${ i }`' 
            :placeholder='props.placeholder ? props.placeholder : "" ' 
        >
    </div>
</template>

<style scoped>
    .form-group {
        display: flex;
        flex-direction: column;
        width: calc(100% - 8px);
        margin: 0 4px 25px 4px;
    }

    .input {
        padding: 4px 2px;
        font-size: 16px;
    }

    .input:not(:first-of-type) {
        margin-top: 12px;
    }

    .input-hidden {
        display: none;
    }

    .label {
        font-weight: bold;
        font-size: 11px;
        margin: 0;
        position: relative;
        left: 1px;
    }
</style>