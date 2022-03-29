<template>
    <main class='main'>
        <section class='container' v-if='!isSubmitted'>
			<p class='logo'>Vacansee</p>
            <p class='info'>If you have forgotten your password, please enter your account's associated email address and we will send you a link to a reset form</p>
			<input v-model='email' type='email' placeholder='Email' id='email' required />
			<button class='submit' @click='submit'>Submit</button>
            <router-link to='/login' class='return-link'>Return to log in page</router-link>
		</section>
        <section class='container' v-if='isSubmitted'>
        	<p class='logo'>Vacansee</p>
            <p class='info'>If you have forgotten your password, please enter your account's associated email address and we will send you a link to a reset form</p>
			<div class='submitted-info'><p>You have been sent a password reset form. Please check your email inbox.</p></div>
            <router-link to='/login' class='return-link'>Return to log in page</router-link>
        </section>
    </main>
</template>

<script setup>
    import { ref } from 'vue';

	const email = ref('');
    const isSubmitted = ref(false);

    const submit = () => {
        isSubmitted.value = !isSubmitted.value;
    };
</script>

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
		color: var(--slate);
		font-size: 16px;
		line-height: 24px;
		display: block;
		padding: 5px 10px;
		margin: 0 0 10px 0;
		width: calc(100% - 21px);
	}

    .info {
        text-align: left;
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