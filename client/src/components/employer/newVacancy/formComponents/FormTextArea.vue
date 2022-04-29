<script setup>
    import { ref } from 'vue';

    const props = defineProps(['name', 'label', 'placeholder', 'value', 'rows'])
</script>

<template>
    <div class='form-group'>
        
        <label :for='name' class='label'>{{ label }}:</label>
        <textarea 
            :name='name' 
            class='textarea'
            :id='name' 
            :placeholder='placeholder ? placeholder : "" ' 
            :rows='rows ? rows : 5'
        >{{ value }}</textarea>
    </div>
</template>

<style scoped>
    .form-group {
        display: flex;
        flex-direction: column;
        width: calc(100% - 8px);
        margin: 0 4px 25px 4px;
    }

    .label {
        font-weight: bold;
        font-size: 11px;
        margin: 0;
        position: relative;
        left: 1px;
    }

    .textarea {
        padding: 4px 2px;
        font-size: 16px;
    }
</style>