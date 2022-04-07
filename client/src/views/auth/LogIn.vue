<template>
	<div class='auth-page'>
		<form @submit.prevent='login' class='auth-page-container'>
			<p class='auth-page-logo'>Vacansee</p>
			<input v-model='email' type='email' placeholder='Email' required />
			<input v-model='password' type='password' placeholder='Password' id='password' required />
			<label for='password' class='reset-label'><router-link to='/reset' class='reset-link'>Forgot your password?</router-link></label>
			<br />
			<input type='checkbox' id='privacy' name='privacy' required />
			<label for='privacy'>By checking, you are agreeing to Vacansee's <router-link to='/privacy' class='privacy-policy'>Privacy Policy</router-link>.</label>
			<button class='submit'>Log In</button>
		</form>
	</div>
</template>

<script setup>
    import dayjs from 'dayjs';
    import { ref } from 'vue';
    import api, { apiCatchError } from '@/assets/js/api';

	const email = ref('');
    const password = ref('');

	const login = async () => {
        const { data = {} } = await api({
            method: 'post',
            url: '/login/',
            withCredentials: true,
            data: {
                email: email.value,
                password: password.value
            }
        }).catch((err) => {
            if(err.response && err.response.status == 401) {
                alert('incorrect email or password');
            } else {            
                console.log(`oops ${ err }`);
            }
        });

        const { userData: session, accessToken = false, refreshToken = false } = data;

        if(!session || !accessToken || !refreshToken) {
            alert('uh oh, we encountered an error while logging you in, please try again later')
            console.error('uh oh, error logging in')
            return;
        }

        session.expire = dayjs().add(2, 'hour').toDate();

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

	.reset-label {
		float: right;
		margin: 2px;
	}

	.reset-link {
		color: var(--red);
		text-decoration: none;
	}

	.reset-link:hover {
		color: var(--red-focus);
	}

    .submit:active, .submit:focus, .submit:hover {
        background: var(--red-focus);
        cursor: pointer;
    }
</style>
