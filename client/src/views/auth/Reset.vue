<script setup>
    import DefaultNavbar from '@/components/partials/DefaultNavbar.vue';

    import api, { apiCatchError } from '@/assets/js/api';
    import { ref, onMounted } from 'vue';

    const url = window.location.pathname;
    const token = url.substring(url.lastIndexOf('/') + 1);

	const password = ref('');
    const passwordVerify = ref('');
    const alert = ref('');
    const isSubmitted = ref(false);

    const submit = () => {
        isSubmitted.value = !isSubmitted.value;
    };

    const getReset = async () => {
        const response = await api({
            url: `/reset/${ token }/`,
            method: 'get',
            responseType: 'json'
        }).catch(apiCatchError => {
            if (apiCatchError.status == 500)
                alert('Unauthorised token.');
        })

        if (!response)
            return false;

        const { data = {} } = response;

        return data
    }

    const postReset = async () => {
        const response = await api({
            url: '/reset/',
            method: 'post',
            data: {
                password: password,
                token: token
            },
            responseType: 'json'
        }).catch(apiCatchError => {
            alert.value = apiCatchError.message;   
        })

        if (!response)
            return false;

        const { data = {} } = response;

        window.location.href = '/login/'
        
    }

    const checkAndResetPassword = () => {
        alert.value = '';

        if (password.value != passwordVerify.value) {
            alert.value = 'Passwords must match.';
            return;
        }

        postReset();
    }

    onMounted(async () => {
        const result = await getReset({ });

        if(!result) {
            return;
        }
    });

</script>

<template>
    <main class='main'>
        <DefaultNavbar/>
        <section class='container' v-if='!isSubmitted'>
            <p class='logo'>Reset Password</p>
            <div id="alert" v-if="alert">{{ alert }}</div>
            <form @submit.prevent="checkAndResetPassword">
            <label>
                New password:
                <input type="password" v-model="password" required />
            </label>
            <label>
                Re-type new password:
                <input type="password" v-model="passwordVerify" required />
            </label>
            <button type="submit" class='submit'>Reset password</button>
            </form>
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