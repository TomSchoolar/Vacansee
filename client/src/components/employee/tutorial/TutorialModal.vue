<script setup>
    const emit = defineEmits(['close-modal'])

</script>


<template>
    <div class='modal-overlay'>
        <div class='modal'>
            <i class="fas fa-times close-icon" @click='emit("close-modal")'></i>
            <slot name='modal-header'>
                This is the default title for the tutorial modal
            </slot>
            <slot name='modal-body'>
                This is the default body for the tutorial modal
            </slot>
            <slot name='modal-footer'></slot>
            <button class='button button-row button-grey' @click='emit("close-modal")'>Close</button>
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
        display: flex;
        justify-content: center;
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
    }
    
    .button-grey {
        background: var(--slate);
    }

    .button-grey:active, .button-grey:focus, .button-grey:hover  {
        background: var(--slate-focus);
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

    :slotted(.desc) {
        margin:0 0 15px 0;
        font-size: 14px;
    }

    .modal {
        background-color: white;
        z-index : 20;
        min-height: 200px;
        max-width: min(425px, 90%);
        padding: 25px 20px 40px 20px;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        bottom: 30px;
    }

    :slotted(.modal-body) {
        width: 85%;
        margin: 10px 0 35px 0;
        font-size: 14px;
        font-weight: 500;
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
        background-color: #00000040;
        min-height: 100vh;
        min-width: 100vw;
    }
</style>