<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import ListBox from '@/components/employee/index/ListBox.vue';
    import { ref, onMounted } from 'vue';

    const emit = defineEmits(['search', 'close-modal']);

    const search = (values) => {
        emit('close-modal');
        emit('search', values);
    };

    const getTags = async () => {
        const response = await api({
            method: 'get',
            url: '/vacancy/tags',
            responseType: 'json',
        }).catch(apiCatchError);

        options.value = response.data;

        return true;
    }

    // vacancy api request
    onMounted(async () => {
        await getTags();
    });

    const options = ref([]);

</script>

<template>
    <div class='modal-overlay'>
        <div class='modal'>
            <i class='desc-bold'>Tag Search</i>
            <i class="fas fa-times close-icon" @click='emit("close-modal")'></i>

            <div class="modal-body">
                <ListBox label='tags' name='tagsInput' :multiple='true' :multipleValue='true' :options='options' @search='search' @close-modal='emit("close-modal")' />
            </div>
        </div>
    </div>
</template>


<style scoped>
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

    .button-red {
        background: var(--red);
    }

    .button-red:active, .button-red:focus, .button-red:hover {
        background: var(--red-focus);
    } 

    .button-row {
        position: absolute;
        display: flex;
        bottom: 0;
        width: 100%;
    }

    .close-icon {
        position: absolute;
        top: 20px;
        right: 25px;
        font-size: 18px;
        color: var(--jet);
        cursor: pointer;
    }

    .close-icon:active, .close-icon:focus, .close-icon:hover {
        color: var(--red);
    }

    .desc {
        margin: 10px 0;
        font-size: 14px;
    }

    .desc-bold {
        font-weight: bold;
    }

    .modal {
        background-color: white;
        min-height: 200px;
        max-width: min(425px, 90%);
        min-width: min(250px, 40%);
        padding: 20px 20px 40px 20px;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        bottom: 30px;
    }

    .modal-body {
        width: 100%;
        margin: 25px 0px;
    }

    .modal-overlay {
        position: absolute;
        z-index: 10;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #000000c9;
    }

    .warning-circle {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: var(--red);
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 60px;
        font-weight: bold;
        color: white;
    }


</style>