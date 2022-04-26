<script setup>
    import Joi from 'joi';
    import { ref } from 'vue';
    import validateForm from '@/assets/js/formValidator';
    import api, { apiCatchError } from '@/assets/js/api';

	const email = ref('');
    const password = ref('');

	const login = async () => {
        const schema = Joi.object({
            'email': Joi.string().email({ tlds: { allow: false } }).max(254).required(),
            'password': Joi.string().required()
        });

        const formData = {
            email: email.value,
            password: password.value
        };
              

        if(!validateForm(schema, formData)) {
            return;
        }
        
        const response = await api({
            method: 'post',
            url: '/login/',
            withCredentials: true,
            data: formData
        }).catch(apiCatchError);

        const { userData: session, accessToken = false, refreshToken = false } = response?.data ?? {};

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

<template>
	<div class='auth-page'>
		<div class='auth-page-container'>
			<p class='auth-page-logo'>Vacansee</p>
			<input v-model='email' type='text' name='email' placeholder='Email' />
			<input v-model='password' type='password' name='password' placeholder='Password' id='password' />

			<button type='button' class='submit' @click='login()'>Log In</button>

            <div class='links'>
			    <router-link to='/register' class='reset-link'>New user? Register here</router-link>
			    <router-link to='/forgot' class='reset-link'>Forgot your password?</router-link>
            </div>
		</div>
	</div>
</template>

<style scoped>
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

	.auth-page-container input {
		border: 1px solid var(--slate);
		border-radius: 5px;
		color: var(--slate);
		font-size: 16px;
		line-height: 24px;
		display: block;
		padding: 5px 10px;
		margin: 10px 0 0 0;
		width: calc(100% - 21px);
	}

	.auth-page-logo {
		color: var(--blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 30px 0;
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

    .invalid-input {
        border: 3px solid var(--red) !important;
    }

    .links {
        display: flex;
        justify-content: space-between;
        margin: 2px 0 10px 0;
        padding: 0 5px;
    }

	.privacy-policy {
		color: var(--red);
		text-decoration: none;
		display: inline;
	}

	.privacy-policy:hover {
		color: var(--red-focus);
	}

	.reset-link {
		color: var(--red);
		text-decoration: none;
        font-size: 12px;
	}

	.reset-link:hover {
		color: var(--red-focus);
	}

    .submit {
        margin: 25px 0 10px 0;
    }

    .submit:active, .submit:focus, .submit:hover {
        background: var(--red-focus);
        cursor: pointer;
    }
</style>
