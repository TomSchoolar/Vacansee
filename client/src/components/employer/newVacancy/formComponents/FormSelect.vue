<script setup>
    const props = defineProps(['name', 'label', 'multiple', 'options', 'placeholder', 'multipleValue', 'value'])
</script>

<template>
    <div class='form-group'>
        <label :for='name' class='label'>{{ label }}:</label>
        <select 
            :name='name' 
            class='input'
            :id='name' 
            required
            :multiple='(multiple ? multiple : false)'
            :style='(multiple ? "height: 150px;" : "")'
        >
            <option value='' :selected='!props.value && props.value !== 0 ? true : false' hidden disabled>{{ placeholder }}</option>
            <option v-for='option in options' :key='option.id' :value='option.id' :selected='(props.value || props.value === 0) && ( props.multipleValue && props.value.includes(option.id) || option.id == props.value) ? true : false'>{{ option.text }}</option>
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
        text-align: left;
    }
</style>