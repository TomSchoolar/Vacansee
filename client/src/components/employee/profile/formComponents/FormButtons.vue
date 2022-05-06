<script setup>
    const props = defineProps(['next', 'back', 'publish']);
    const emit = defineEmits(['next', 'back', 'publish']);
</script>

<template>
    <div class='container'>
        <button type='button' class='btn btn-back' @click='emit("back")' v-if='back'>
            Back
        </button>
        <button type='button' class='btn btn-next' @click='emit("next")' v-if='next'>
            Next
        </button>
        <button type='button' class='btn btn-next' @click='emit("publish")' v-if='publish'>
            Submit
        </button>
    </div>
</template>

<style scoped>
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
        background: var(--red);
    }

    .btn-next:active, .btn-next:focus, .btn-next:hover {
        background: var(--red-focus);
    }
    
    .container {
        display: flex;
        flex-direction: row;
        width: 100%;
        max-width: 500px;
        margin: auto;
    }
</style>
