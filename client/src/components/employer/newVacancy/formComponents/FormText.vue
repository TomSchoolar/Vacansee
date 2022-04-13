<script setup>
    const props = defineProps(['name', 'label', 'placeholder', 'type', 'value', 'readonly', 'disabled'])
</script>

<template>
    <div class='form-group'>
        <label :for='props.name' class='label'>{{ props.label }}:</label>
        <input 
            :type='props.type' 
            :name='props.name' 
            class='input'
            :id='props.name' 
            :placeholder='props.placeholder ? props.placeholder : "" ' 
            :value='props.value ? props.value : "" ' 
            :readonly='props.readonly ? true : false'
            :disabled='props.disabled ? true : false'
            
        >
    </div>
</template>

<style scoped>
    input[readonly] {
        /* chrome default disabled styles */
        cursor: default;
        background-color: rgba(239, 239, 239, 0.3);/*, rgba(59, 59, 59, 0.3)); */
        color: rgb(84, 84, 84);/*, rgb(170, 170, 170));*/
        border-color: rgba(118, 118, 118, 0.3);
        border-width: 1.5px;
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
    }

    .label {
        font-weight: bold;
        font-size: 11px;
        margin: 0;
        position: relative;
        left: 1px;
    }
</style>