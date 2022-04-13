<script setup>
    import { onMounted, ref } from 'vue';

    const props = defineProps(['name', 'label', 'placeholder', 'secondPlaceholder', 'max'])

    let fields = [];
    let activeFields = [];
    const numFields = ref(1);
    
    onMounted(() => {
        // get fields and add event listeners
        const fieldPane = document.getElementById(`expanding-${ props.name }`);
        fields = document.querySelectorAll(`.input-${ props.name }`);
        activeFields.push(fields[0]);




        const listener = fieldPane.addEventListener('keyup', () => {
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

            if(value && nextInputNum && nextInput.parentElement.classList.contains('input-hidden')) {
                // field has been populated, add another field if not at max
                nextInput.parentElement.classList.remove('input-hidden');
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
                    let el = activeFields.pop();
                    el.parentElement.classList.add('input-hidden');
                    el.nextElementSibling.value = '';
                }
            }
        };
    });

    const shuffleInputValues = (startIndex) => {
        for(let i = --startIndex; i + 2 < activeFields.length; i++) {
            // move fields values up two places
            activeFields[i].value = activeFields[i+2].value;
            activeFields[i].nextElementSibling.value = activeFields[i+2].nextElementSibling.value;
            activeFields[i+2].value = '';
            activeFields[i+2].nextElementSibling.value = '';
        }
        
        // remove last input from form and active fields array
        activeFields.pop().parentElement.classList.add('input-hidden');
    }


</script>

<template>
    <div class='form-group' :id='`expanding-${ props.name }`'>
        <label :for='`${ props.name }-1`' class='label'>{{ props.label }}:</label>
        <div :class='"double-input-container" + " " + ( i <= numFields ? "" : "input-hidden" )' v-for='i in props.max' :key='i'>
            <input 
                type='text' 
                :name='`${ props.name }-${ i }`' 
                :class='"input " + `input-${ props.name }`'
                :id='`${ props.name }-${ i }`' 
                :placeholder='props.placeholder ? props.placeholder : "" ' 
            >
            <input 
                type="text"
                :name='`${ props.name }-${ i }-time`'
                :class='"input input-time " + `input-${ props.name }-time`'
                :id='`${ props.name }-${ i }`' 
                :placeholder='props.secondPlaceholder ? props.secondPlaceholder : "" ' 
            >
        </div>
    </div>

</template>

<style scoped>
    .double-input-container {
        display: flex;
        width: 100%;
        justify-content: space-between;
    }

    .double-input-container:not(:last-of-type) {
        margin-bottom: 12px;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        width: calc(100% - 8px);
        margin: 0 4px 25px 4px;
    }

    .input {
        padding: 4px 2px;
        font-size: 16px;
        width: 65px;
        flex-grow: 1;
    }

    .input-hidden {
        display: none;
    }

    .input-time {
        margin-left: 10px;
        width: 30%;
        flex-grow: 0;
    }

    .label {
        font-weight: bold;
        font-size: 11px;
        margin: 0;
        position: relative;
        left: 1px;
    }
</style>