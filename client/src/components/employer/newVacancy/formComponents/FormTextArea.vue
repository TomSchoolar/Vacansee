<script setup>
    const props = defineProps(['name', 'label', 'placeholder', 'value', 'rows'])
</script>

<template>
    <div class='form-group'>
        <label :for='props.name' class='label'>{{ props.label }}:</label>
        <textarea 
            :name='props.name' 
            class='textarea'
            :id='props.name' 
            :placeholder='props.placeholder ? props.placeholder : "" ' 
            :rows='props.rows ? props.rows : 5'
            v-model='props.value' 
        ></textarea>
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