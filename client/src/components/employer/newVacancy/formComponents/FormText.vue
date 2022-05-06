<script setup>
    const props = defineProps(['name', 'label', 'placeholder', 'type', 'value', 'readonly', 'disabled'])
</script>

<template>
    <div class='form-group'>
        <label :for='name' class='label'>{{ label }}:</label>
        <input 
            :type='type' 
            :name='name' 
            class='input'
            :id='name' 
            :placeholder='placeholder ? placeholder : "" ' 
            :value='value ? value : "" ' 
            :readonly='readonly ? true : false'
            :disabled='disabled ? true : false'
            
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
        text-align: left;
    }
</style>