<script setup>
    const props = defineProps(['name', 'label', 'multiple', 'options', 'placeholder', 'multipleValue', 'value']);
    const emit = defineEmits(['search', 'close-modal']);

    import { ref } from 'vue';

    const tagSelection = ref([]);
    let selectedValues = ref([]);


    const updateSelected = (values) => {
        selectedValues.value = values;
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

        <div class='button-row'>
            <button class='button button-grey' @click='emit("close-modal")'>Go Back</button>
            <button class='button button-blue' @click='emit("search", selectedValues)'>Search</button>
        </div>
    </div>


</template>

<style scoped>
    option {
        color: black;
    }

    select:required:invalid {
        color: var(--slate);
    }

    .button {
        color: white;
        width: 150px;
        font-weight: 500; /* required for some reason */
        border: none;
        color: #fff;
        font-size: 14px;
        text-decoration: none;
        padding: 14px 4px;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
        flex-grow: 1;
        cursor: pointer;
    }

    .button:first-of-type {
        border-bottom-left-radius: 20px;
    }

    .button:last-of-type {
        border-bottom-right-radius: 20px;
    }

    .button-grey {
        background: var(--slate);
    }

    .button-grey:active, .button-grey:focus, .button-grey:hover  {
        background: var(--slate-focus);
    } 

    .button-blue {
        background: var(--blue);
    }

    .button-blue:active, .button-blue:focus, .button-blue:hover {
        background: var(--blue-focus);
    } 

    .button-row {
        position: absolute;
        display: flex;
        bottom: 0;
        left: 0;
        width: 100%;
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