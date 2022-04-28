<script setup>
    const props = defineProps(['name', 'label', 'multiple', 'options', 'placeholder', 'multipleValue', 'value'])
    const emit = defineEmits(['search', 'close-modal'])

    import { ref } from 'vue';

    let selectedValues = ref([]);
    const tagSelection = ref();

    const search = () => {
        emit('search', selectedValues);
    }

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
            <option value='' :selected='!props.value ? true : false' hidden disabled>{{ placeholder }}</option>
            <option v-for='option in options' :key='option.value' :value='option.value' :selected='props.value && ( props.multipleValue && props.value.includes(option.value) || option.value == props.value) ? true : false'>{{ option.text }}</option>
        </select>
    </div>

    <div class="button-row">
        <button class='button button-grey' @click='emit("close-modal")'>Go Back</button>
        <button class='button button-red' @click='search'>Search</button>
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