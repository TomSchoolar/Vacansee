<script setup>
    const emit = defineEmits(['close', 'delete'])
    const { display = false } = defineProps(['display']);

</script>

<template>
    <div class='modal-overlay' v-if='display'>
        <div class='modal'>
            <form @submit.prevent='emit("delete")'>
                <i class="fa-solid fa-xmark close" @click='emit("close")'></i>

                <div class="warning-circle">!</div>

                <div class='modal-body'>
                    <h4 class='title'>Are you sure?</h4>
                    <div class='body'>
                        <p class='desc'>Are you sure you want to delete your account?</p>
                        <p class='desc'>This process cannot be undone!</p>
                    </div>
                    <div class='checkbox-container'>
                        <input type='checkbox' id='sure' name='sure' required>
                        <label for='sure' class='label'>I am sure, delete my account</label>
                    </div>
                </div>

                <div class='button-row'>
                    <button type='button' class='button button-grey' @click='emit("close")'>Go Back</button>
                    <button class='button button-red'>Delete Account</button>
                </div>
            </form>
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
        left: 0;
        width: 100%;
    }

    .checkbox-container {
        margin: 20px 0;
    }

    .close {
        color: var(--jet);
        position: absolute;
        top: 16px;
        right: 16px;
        font-size: 18px;
        cursor: pointer;
    }

    .close:active, .close:focus, .close:hover {
        color: var(--red);
    }

    .title {
        font: var(--font);
        font-weight: 600;
        font-size: 30px;
        margin: 0;
    }

    .label {
		font-size: 16px;
		text-align: left;
		margin: 0 0 20px 5px;
	}

    .modal {
        background: white;
        border-radius: 20px;
        width: 300px;
        min-width: 450px;
        position: relative;
        padding: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1vh;
        bottom: 50px;
    }

    .modal-body {
        margin: 25px 0 60px 0;
    }

    .modal-overlay {
        position: absolute;
        top: 0;
        left: 0;
        height: 100vh;
        width: 100vw;
        background: #00000040;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 100;
    }

    .role-container {
        font-size: 25px;
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
        margin: 0 auto;
    }
</style>