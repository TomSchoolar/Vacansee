<template>
	<div class='auth-page'>
		<div class='auth-page-container'>
			<p class='auth-page-logo'>Tindeed</p>
			<input v-model='email' type='email' placeholder='Email' />
			<input v-model='password' type='password' placeholder='Password' />
			<button @click='login'>Log In</button>
		</div>
	</div>
</template>

<script setup>
    import { ref } from 'vue';

	const email = ref('');
    const password = ref('');

	const login = () => {
		alert(`log in req, email: ${ email.value } password: ${ password.value }`);
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
		max-width: 500px;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		position: absolute;
	}

	.auth-page-container input {
		color: --var(slate);
		font-size: 18px;
		line-height: 24px;
	}

	.auth-page-logo {
		color: --var(blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 25px 0;
	}
</style>
