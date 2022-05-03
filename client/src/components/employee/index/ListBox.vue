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

        <div class='container'>
            <button class='btn btn-back' @click='emit("close-modal")'>Go Back</button>
            <button class='btn btn-next' @click='emit("search", selectedValues)'>Search</button>
        </div>
    </div>


</template>

<style scoped>
    .container {
        display: flex;
        flex-direction: row;
        width: 100%;
        max-width: 500px;
        margin: auto;
    }

    .btn {
        width: 85px;
        padding: 5.5px 0;
        color: white;
        border: none;
        font-family: var(--font-family);
        font-weight: 500;
        font-size: 16px;
        margin: 10px auto 0 auto;
        cursor: pointer;
    }

    .btn-back {
        background: var(--slate);
    }

    .btn-back:active, .btn-back:focus, .btn-back:hover {
        background: var(--slate-focus);
    }

    .btn-next {
        background: var(--blue);
    }

    .btn-next:active, .btn-next:focus, .btn-next:hover {
        background: var(--blue-focus);
    }

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