<template>
	<div class='auth-page'>
		<form @submit.prevent='register' class='auth-page-container'>
			<p class='auth-page-logo'>Vacansee</p>
			<input v-model='email' type='email' placeholder='Email' required />
			<input v-model='password' type='password' placeholder='Password' id='password' required />
			<label class='switch'>
				<input v-model='isEmployer' type='checkbox' />
				<span class='slider'></span>
			</label>
			<input type='checkbox' id='privacy' name='privacy' required />
			<label for='privacy'>By checking, you are agreeing to Vacansee's <router-link to='/privacy' class='privacy-policy'>Privacy Policy</router-link>.</label>
			<button class='submit'>Register</button>
		</form>
	</div>
</template>

<script setup>
    //import dayjs from 'dayjs';
    import { ref } from 'vue';
    import api, { apiCatchError } from '@/assets/js/api';

	const email = ref('');
    const password = ref('');
	const isEmployer = false;

	const register = async () => {
        const { data = {} } = await api({
            method: 'post',
            url: '/register/',
            withCredentials: true,
            data: {
                email: email.value,
                password: password.value,
				isEmployer: isEmployer.checked
            }
        }).catch(apiCatchError);

        const { userData: session, accessToken = false, refreshToken = false } = data;

        if(!session || !accessToken || !refreshToken) {
            alert('uh oh, we encountered an error while logging you in, please try again later')
            console.error('uh oh, error logging in')
            return;
        }

        window.localStorage.setItem('session', JSON.stringify(session))
        window.localStorage.setItem('accessToken', accessToken)
        window.localStorage.setItem('refreshToken', refreshToken)

        if(session.IsEmployer)
            window.location.href = '/e/vacancy'
        else
            window.location.href = '/vacancy'
	}
</script>

<style>
	label {
		font-size: 12px;
		text-align: left;
		margin: 0 0 10px 5px;
	}

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

	.auth-page-container input:not(#privacy) {
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

	.privacy-policy {
		color: var(--red);
		text-decoration: none;
		display: inline;
	}

	.privacy-policy:hover {
		color: var(--red-focus);
	}

    .submit:active, .submit:focus, .submit:hover {
        background: var(--red-focus);
        cursor: pointer;
    }

	.switch {
		position: relative;
		display: block;
		width: 200px;
		height: 40px;
		margin: 0 auto;
	}

	.switch input {
		opacity: 0;
		width: 0;
		height: 0;
	}

	.slider {
		position: absolute;
		cursor: pointer;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: var(--red);
		border-radius: 40px;
		-webkit-transition: .5s;
		transition: .5s;
	}

	.slider:before {
		position: absolute;
		content: 'Employee';
		height: 32px;
		width: 92px;
		left: 4px;
		bottom: 4px;
		text-align: center;
		line-height: 30px;
		background-color: #ffffff;
		border-radius: 16px;
		-webkit-transition: .5s;
		transition: .5s;
	}

	input:checked + .slider {
		background-color: var(--blue);
	}

	input:focus + .slider {
		box-shadow: 0 0 1px var(--blue);
	}

	input:checked + .slider:before {
		content: 'Employer';
		-webkit-transform: translateX(100px);
		-ms-transform: translateX(100px);
		transform: translateX(100px);
	}
</style>
