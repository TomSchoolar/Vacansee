<script setup>
    const props = defineProps(['title']);
</script>

<template>
    <div class='container'>
        <h2 class='header'>{{ title }}</h2>

        <p class='description'>
            <slot>Add a description to the form</slot>
        </p>
    </div>

</template>

<style scoped>
    .container {
        width: 100%;
    }

    .description {
        font-size: 12px;
        margin: 15px 0 25px 0;

    }

    .header {
        margin: 0;
    }
</style>

