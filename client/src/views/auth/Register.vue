<script setup>
    //import dayjs from 'dayjs';
    import Joi from 'joi';
    import api, { apiCatchError } from '@/assets/js/api';
    import validateForm from '@/assets/js/formValidator';

    import { ref } from 'vue';
    

	const email = ref('');
    const password = ref('');
    const companyName = ref();
    const phoneNumber = ref();
	const isEmployer = ref(false);


	const register = async () => {
        
        const schemaObj = {
            'email': Joi.string().email({ tlds: { allow: false } }).max(254).required(),
            'password': Joi.string().min(8).required(),
            'isEmployer': Joi.boolean().required()
        }

        const formData = {
            email: email.value,
            password: password.value,
            isEmployer: isEmployer.value
        };
        
        if(isEmployer.value) {
            formData.companyName = companyName.value;
            formData.phoneNumber = phoneNumber.value;

            schemaObj.companyName = Joi.string().alphanum().max(30).required().label('company name');
            schemaObj.phoneNumber = Joi.string().min(8).max(30).required().label('phone number');
        }

        const schema = Joi.object(schemaObj);

        if(!validateForm(schema, formData)) {
            return;
        }

        const response = await api({
            method: 'post',
            url: '/v1/register/',
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
        window.localStorage.setItem('newUser', true)

        if(session.IsEmployer)
            window.location.href = '/e/vacancy'
        else 
            window.location.href = '/profile'
	}
</script>

<template>
	<div class='auth-page'>
		<form @submit.prevent='register' class='auth-page-container'>
			<p class='auth-page-logo'>Vacansee</p>
			
            <input v-model='email' type='text' name='email' placeholder='Email' />
			<input v-model='password' type='password' name='password' placeholder='Password' id='password' />
			
            <div class='employer-details' v-if='isEmployer'>
                <input v-model='companyName' type='text' name='companyName' placeholder='Company Name' />
			    <input v-model='phoneNumber' type='text' name='phoneNumber' placeholder='Phone Number' />
            </div>

            <label class='switch'>
				<input v-model='isEmployer' type='checkbox' name='isEmployer' />
				<span class='slider'></span>
			</label>

            <div class='privacy-row'>
                <input type='checkbox' id='privacy' name='privacy' required />
                <label for='privacy'>By checking, you are agreeing to Vacansee's <router-link to='/privacy' class='privacy-policy'>Privacy Policy</router-link>.</label>
            </div>

			<button class='submit'>Register</button>

            <div class='links'>
			    <router-link to='/login' class='reset-link'>Existing user? Login here</router-link>
            </div>
		</form>
	</div>
</template>

<style scoped>
	input:checked + .slider {
		background-color: var(--blue);
	}

	input:focus + .slider {
		box-shadow: 0 0 1px var(--blue);
	}

	input:checked + .slider:before {
		content: 'Employer';
		-webkit-transform: translateX(121.5px);
		-ms-transform: translateX(121.5px);
		transform: translateX(121.5px);
	}

	label {
		font-size: 12px;
		text-align: left;
        margin: 0;
		margin-left: 5px;
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
		margin: 10px 0 0 0;
		width: calc(100% - 21px);
	}

	.auth-page-logo {
		color: var(--blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 40px 0;
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
        justify-content: center;
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

    .privacy-row {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px auto 5px 0;
    }

    .reset-link {
        color: var(--red);
        font-size: 12px;
        text-decoration: none;
        
    }

    .reset-link:active, .reset-link:focus, .reset-link:hover {
        color: var(--red-focus);
    }

    .submit {
        margin: 15px 0 10px 0;
    }

    .submit:active, .submit:focus, .submit:hover {
        background: var(--red-focus);
        cursor: pointer;
    }

	.switch {
		position: relative;
		display: block;
		width: 250px;
		height: 36px;
		margin: 20px auto 10px auto;
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
		height: 28px;
		width: 120px;
		left: 4px;
		bottom: 4px;
		text-align: center;
		line-height: 30px;
		background-color: #ffffff;
		border-radius: 16px;
		-webkit-transition: .5s;
		transition: .5s;
	}


</style>
