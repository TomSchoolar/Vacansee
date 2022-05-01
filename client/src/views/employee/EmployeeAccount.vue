<script setup>
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
	import AccountModal from '@/components/employer/account/AccountModal.vue';
	import ProfileCard from '@/components/employee/account/ProfileCard.vue';

	import { logout } from '@/assets/js/jwt';
    import api, { apiCatchError } from '@/assets/js/api';
    import { ref, onMounted, watch } from 'vue';

	const url = window.location.pathname;

	//const notifs = ref(2);
	const saved = ref(false);
	const accountDetails = ref({});	
	const details = ref({})
	const displayModal = ref(false);
	const profile = ref({});

	document.title = 'Account | Vacansee'

	const showDeletion = () => {
		displayModal.value = true;
	}

	const getAccount = async () => {

		const response = await api({
			url: `/account/`,
			method: 'get',
			responseType: 'json'
		}).catch(apiCatchError);

		if (!response)
			return false;

		const { data } = response;

		if(!data)
			return false;

		const {
			email: apiEmail = ''
		} = data;

		accountDetails.value.Email = apiEmail;

		return true;
	}

	const updateAccount = async (newEmail) => {
		const response = await api({
			url: '/account/update/',
			method: 'put',
			data: {
				setEmail: newEmail
			},
			responseType: 'json'
		}).catch(apiCatchError);

		if (!response) {
			return false;
		}

		const { data = {} } = response;

		saved.value = true;

		return data;
	}

	const deleteAccount = async () => {
		const response = await api({
			url: '/account/delete/',
			method: 'delete',
			responseType: 'json'
		}).catch(apiCatchError);

		if (!response) {
			return false;
		}

		const { data = {} } = response;

		displayModal.value = false;
		logout();
	}

	const getProfile = async () => {
		const response = await api({
			url: '/account/profile',
			method: 'get',
			responseType: 'json'
		}).catch(apiCatchError);

		if (!response) {
			return false;
		}

		const { data } = response;

		const {
			details: newDetails = accountDetails.value,
		} = data;

		profile.value = newDetails;
		return true;
	}

	onMounted(async () => {
		const result = await getAccount({ });
		const response = await getProfile({});

		if(!result || !response) {
			return;
		};
	})

	const flipSaved = () => {
		saved.value = false;
	}

	watch(saved, () => {
		setTimeout(flipSaved, 3000);
	});

</script>

<template>
    <main class='main'>

        <!-- <EmployeeNavbar page='account' :numNotifs='notifs'></EmployeeNavbar> -->
		<EmployeeNavbar page='account' ></EmployeeNavbar>
        <section class='container'>
			<AccountModal :display='displayModal' @close='displayModal = false' @delete='deleteAccount' />
			<div>
				<p class='logo'>Account Profile</p>
				<ProfileCard class='card' :profile='profile' />
				<router-link to='/profile/edit' class='profileBtn' >Edit Profile</router-link>
			</div>
			<p class='logo'>Account Details</p>
			<label for='email'>Current Email Address:</label>
			<input type='text' placeholder='...' v-model='accountDetails.Email' required/>
			<div class='button-container'>
				<button class='delete-account' @click=showDeletion>Delete Account</button>
				<button class='save' @click="updateAccount(accountDetails.Email)">Save</button>
			</div>
			<div class='saved-indicator' v-show='saved'>
				<p>Saved!</p>
			</div>
		</section>
    </main>
</template>

<style scoped>
	label {
		font-size: 18px;
	}

	.main {
		width: 100vw;
		height: 100vh;
	}

	.button-container {
		display: flex;
		gap: 0.2vw;
	}

	.card {
		margin-left : auto; 
        margin-right : auto;
        min-width: 350px;
	}

	.container {
		display: flex;
		flex-direction: column;
		align-content: center;
		width: 20vw;
		margin-right: auto;
		margin-left: auto;
	}

	.container input {
		border: 1px solid var(--slate);
		border-radius: 5px;
		color: var(--slate);
		font-size: 16px;
		line-height: 24px;
		padding: 5px 10px;
		margin: 0 0 10px 0;
	}

	.delete-account{
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
		padding: 5px 0;
		width: 50%;
	}

	.delete-account:active .delete-account:focus .delete-account:hover {
		background: var(--red-focus);
	}

	.logo {
		color: var(--blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 25px 0;
	}

	.profileBtn{
		background: var(--red);
		color: #ffffff;
		border: 0;
		border-radius: 5px;
		display: block;
		cursor: pointer;
		font-family: var(--fonts);
		font-size: 16px;
		font-weight: bold;
		text-decoration: none;
		line-height: 24px;
		padding: 5px 0;
		margin-bottom: 1vw;
	}

	.profileBtn:active .profileBtn:focus .profileBtn:hover {
		background: var(--red-focus);
	}


	.save {
		background: var(--blue);
		color: #ffffff;
		border: 0;
		border-radius: 5px;
		display: block;
		cursor: pointer;
		font-family: var(--fonts);
		font-size: 16px;
		font-weight: bold;
		line-height: 24px;
		padding: 5px 0;
		width: 50%;
	}

	.saved-indicator {
		margin: 10px;
		background: var(--green);
		border-radius: 5px;
		color: #ffffff;
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