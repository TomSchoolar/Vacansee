<script setup>
    import { onMounted, ref } from 'vue';

    const props = defineProps(['name', 'label', 'placeholder', 'max'])
    
    let fields = [];
    let listeners = [];
    const numFields = ref(1);
    
    onMounted(() => {
        fields = document.querySelectorAll(`.input-${ props.name }`);

        for(let i = 0; i < props.max; i++) {
            let listener = fields[i].addEventListener('input', (event) => {
                let input = event.target;
                let value = input.value;
                const id = input.id.split('-');
                let inputNum = parseInt(id[1]);
                let previousInputNum = ( inputNum - 1 >= 1 ? inputNum - 1 : false )
                let nextInputNum = ( inputNum + 1 <= props.max ? inputNum + 1 : false );

                if(value && nextInputNum) {
                    // field has been populated, add another field if not at max
                    let nextInput = document.querySelector(`#${ id[0] }-${ nextInputNum }`);
                    nextInput.classList.remove('input-hidden');
                }

                // TODO: fix when populate all 3 fields, empty first and second
                
                if(!value && nextInputNum) {
                    // field is empty, if next field is also empty, remove it
                    let nextInput = document.querySelector(`#${ id[0] }-${ nextInputNum }`);
                    
                    if(!nextInput.value) {
                        nextInput.classList.add('input-hidden');
                    }
                }

            });

            listeners.push(listener);
        }
    });


</script>

<template>
    <div class='form-group'>
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

    .input:not(:last-of-type) {
        margin-bottom: 12px;
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