<script setup>
    const props = defineProps(['name', 'label', 'placeholder', 'value', 'disabled'])
</script>

<template>
    <div class='form-group'>
        <label for='' class='label'>{{ props.label }}:</label>
        <input 
            type='text' 
            :name='props.name' 
            class='input'
            :id='props.name' 
            :placeholder='props.placeholder ? props.placeholder : "" ' 
            :value='props.value ? props.value : "" ' 
            :disabled='props.disabled ? true : false'
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

    .label {
        font-weight: bold;
        font-size: 11px;
        margin: 0;
        position: relative;
        left: 1px;
    }
</style>