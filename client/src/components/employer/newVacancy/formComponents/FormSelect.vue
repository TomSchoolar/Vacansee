<script setup>
    const props = defineProps(['name', 'label', 'multiple', 'options', 'placeholder'])
</script>

<template>
    <div class='form-group'>
        <label :for='props.name' class='label'>{{ props.label }}:</label>
        <select 
            :name='props.name' 
            class='input'
            :id='props.name' 
            required
            :multiple='(props.multiple ? props.multiple : false)'
            :style='(props.multiple ? "height: 150px;" : "")'
        >
            <option value='' selected hidden disabled>{{ props.placeholder }}</option>
            <option v-for='option in options' :key='option.value' :value='option.value'>{{ option.text }}</option>
        </select>
    </div>
</template>

<style scoped>
    select:required:invalid {
        color: var(--slate);
    }

    option {
        color: black;
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