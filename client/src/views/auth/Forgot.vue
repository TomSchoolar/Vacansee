<script setup>
    import Joi from 'joi';
    import api, { apiCatchError } from '@/assets/js/api';
    import validateForm from '@/assets/js/formValidator';
    
    import { ref } from 'vue';

	const email = ref('');
    const isSubmitted = ref(false);

    const submit = () => {
        isSubmitted.value = !isSubmitted.value;
    };

	const postForgot = async () => {
        const schema = Joi.object({
            'email': Joi.string().email({ tlds: { allow: false } }).max(254).required()
        });

        const formData = {
            email: email.value,
        }; 

        if(!validateForm(schema, formData)) {
            return;
        }

        const response = await api({
            url: '/v1/forgot/',
            method: 'post',
            withCredentials: true,
			data: formData,
            responseType: 'json'
        }).catch(apiCatchError)

        const data = response?.data ?? false;

        if(!data)
            return;

		submit();

		return data;
    }
</script>

<template>
    <main class='main'>
        <section class='container' v-if='!isSubmitted'>
			<p class='logo'>Vacansee</p>
            <p class='info'>If you have forgotten your password, please enter your account's associated email address and we will send you a link to reset your password.</p>
			<form @submit.prevent='postForgot'>
			    <input v-model='email' type='text' name='email' placeholder='Email' id='email' />
			    <button class='submit'>Submit</button>
			</form>
            <router-link to='/login' class='return-link'>Remembered your password? Login here</router-link>
		</section>
        <section class='container' v-if='isSubmitted'>
        	<p class='logo'>Vacansee</p>
            <p class='info'>If you have forgotten your password, please enter your account's associated email address and we will send you a link to a reset form</p>
			<div class='submitted-info'><p>You have been sent an email if an account with the provided email was found. Please check your email inbox.</p></div>
            <router-link to='/login' class='return-link'>Remembered your password? Login here</router-link>
        </section>
    </main>
</template>

<style scoped>
	.main {
		width: 100vw;
		height: 100vh;
		position: relative;
	}
	
	.container {
		width: 100%;
		max-width: 400px;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		position: absolute;
	}

	.container input {
		border: 1px solid var(--slate);
		border-radius: 5px;
		color: var(--slate-focus);
		font-size: 16px;
		line-height: 24px;
		display: block;
		padding: 5px 10px;
		margin: 10px 0 0 0;
		width: calc(100% - 21px);
	}

    .info {
        text-align: left;
        font-size: 14px;
        text-align: center;
        margin-bottom: 22px;
    }

    .invalid-input {
        border: 3px solid var(--red) !important;
    }


	.logo {
		color: var(--blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 25px 0;
	}

    .return-link {
        display: block;
        margin: 10px;
        color: var(--red);
        text-decoration: none;
        font-size: 12px;
    }

    .return-link:hover {
        color: var(--red-focus);
    }

	.submit {
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
        margin: 25px 0 10px 0;
	}

    .submit:active, .submit:focus, .submit:hover {
        background: var(--red-focus);
        cursor: pointer;
    }

    .submitted-info {
        background-color: var(--red);
        padding: 5px;
        color: white;
    }
</style>