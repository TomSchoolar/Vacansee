<template>
	<div class='auth-page'>
		<form @submit.prevent='login' class='auth-page-container'>
			<p class='auth-page-logo'>Tindeed</p>
			<input v-model='email' type='email' placeholder='Email' required />
			<input v-model='password' type='password' placeholder='Password' required />
			<button class='submit'>Log In</button>
		</form>
	</div>
</template>

<script setup>
    import axios from 'axios';
    import { ref } from 'vue';

	const email = ref('');
    const password = ref('');

	const login = async () => {
        const response = await axios({
            method: 'post',
            url: '/login/',
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            data: {
                email: email.value,
                password: password.value
            }
        }).catch((err) => {
            console.log(`oops ${ err }`);
        });

        console.log(response.data);

	}
</script>

<style>
	.auth-page {
		width: 100vw;
		height: 100vh;
		position: relative;
	}
	
	.auth-page-container {
		width: 100%;
		max-width: 400px;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		position: absolute;
	}

	.auth-page-container input {
		border: 1px solid var(--slate);
		border-radius: 5px;
		color: var(--slate);
		font-size: 16px;
		line-height: 24px;
		display: block;
		padding: 5px 10px;
		margin: 0 0 10px 0;
		width: calc(100% - 21px);
	}

	.auth-page-logo {
		color: var(--blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 25px 0;
	}

	.auth-page-container button {
		background: var(--red);
		border: 0;
		border-radius: 5px;
		color: #ffffff;
		display: block;
		font-family: var(--fonts);
		font-size: 16px;
		font-weight: bold;
		line-height: 24px;
		padding: 5px 0;
		width: 100%;
	}

    .submit:active, .submit:focus, .submit:hover {
        background: var(--red-focus);
        cursor: pointer;
    }
</style>
