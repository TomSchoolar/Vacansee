<script setup>
    const emit = defineEmits(['close'])
    const { display = false } = defineProps(['display']);

</script>

<template>
    <div class='cover' v-if='display'>
        <div class='modal'>
            <form @submit='$emit("delete")'>
            <i class="fa-solid fa-xmark close" @click='emit("close")'></i>

            <h4 class='title'>Are you sure?</h4>
            <div class='role-container'><span>This process cannot be undone!</span></div>
            <input type='checkbox' id='sure' name='sure' required>
            <label for='sure'>I am sure</label>
            <button class='delete'>CONFIRM</button>
            </form>
        </div>
    </div>
</template>

<style scoped>
	label {
		font-size: 18px;
		text-align: left;
		margin: 0 0 20px 5px;
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

    .cover {
        position: absolute;
        top: 0;
        left: 0;
        height: 100vh;
        width: 100vw;
        background: rgba(51, 51, 51, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 100;
    }

    .delete {
		background: var(--red);
		color: #ffffff;
		border: 0;
		border-radius: 5px;
		display: block;
        cursor: pointer;
		font-family: var(--fonts);
		font-size: 16px;
		font-weight: bold;
		line-height: 24px;
		padding: 10px 0;
        width: 100%
	}

    .delete:active .delete:focus .delete:hover {
        background: var(--red-focus);
    }

    .role-container {
        font-size: 25px;
    }

    .modal {
        background: white;
        border-radius: 8px;
        width: 30vw;
        min-width: 450px;
        position: relative;
        padding: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1vh;
    }
</style>