<script setup>
    const props = defineProps(['name', 'label', 'multiple', 'options', 'placeholder', 'multipleValue', 'value']);

    import { ref } from 'vue';

    const tagSelection = ref([]);
    let selectedValues = ref([]);


    const updateSelected = (values) => {
        selectedValues = values;
    }
</script>

<template>
    <div class='form-group'>
        <label :for='name' class='label'>{{ label }}:</label>
        <select 
            :name='name' 
            class='input'
            v-model='tagSelection'
            @change='updateSelected(tagSelection)'
            :id='name' 
            required
            :multiple='(multiple ? multiple : false)'
            :style='(multiple ? "height: 150px;" : "")'
        >
            <option value='' :selected='!value ? true : false' hidden disabled>{{ placeholder }}</option>
            <option v-for='option in options' :key='parseInt(option.id)' :value='parseInt(option.id)' :selected='value && ( multipleValue && value.includes(option.id) || option.id == value) ? true : false'>{{ (option.text) }}</option>
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
        font-size: 12px;
        margin: 0 0 4px 0;
        position: relative;
        left: 1px;
        width: 90%;
        text-align: left;
    }
</style>