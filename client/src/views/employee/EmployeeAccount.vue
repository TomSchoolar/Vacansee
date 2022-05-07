<script setup>
	import api, { apiCatchError } from '@/assets/js/api';
	import Footer from '@/components/partials/Footer.vue';
    import EmployeeNavbar from '@/components/employee/EmployeeNavbar.vue';
	import ProfileCard from '@/components/employee/account/ProfileCard.vue';
	import AccountModal from '@/components/employer/account/AccountModal.vue';
	import TutorialModal from '@/components/employee/tutorial/TutorialModal.vue';


	import { logout } from '@/assets/js/jwt';
    import { ref, onMounted, watch } from 'vue';

	const url = window.location.pathname;

	//const notifs = ref(2);
	const saved = ref(false);
	const accountDetails = ref({});	
	const details = ref({})
	const displayModal = ref(false);
	const profile = ref({});
	const isNewUser = ref(window.localStorage.getItem('newUserEmployeeAccount') == null);


	document.title = 'Account | Vacansee'

	const showDeletion = () => {
		displayModal.value = true;
	}

	const getAccount = async () => {

		const response = await api({
			url: `/v1/accounts/`,
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
			url: '/v1/accounts/',
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
			url: '/v1/accounts/',
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
			url: '/v1/accounts/profiles',
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

	const resetTutorial = () => {
        window.localStorage.removeItem('newUserEmployeeAccount');
		window.localStorage.removeItem('newUserApplications');
		window.localStorage.removeItem('newUserFavourites');
		window.localStorage.removeItem('newUserEmployeeIndex');
		window.localStorage.removeItem('newUserEmployeeProfile');


        isNewUser.value = true;
    }

	const finishTutorial = () => {
        window.localStorage.setItem('newUserEmployeeAccount', false);
        isNewUser.value = false;
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
    <main>

        <!-- <EmployeeNavbar page='account' :numNotifs='notifs'></EmployeeNavbar> -->
		<EmployeeNavbar page='account' ></EmployeeNavbar>

        <div class='container'>
            <h1 class='title'>My Account</h1>

			<AccountModal :display='displayModal' @close='displayModal = false' @delete='deleteAccount' />
            
            <div class='row'>
                <section class='col'>
                    <h2 class='col-title'>My Profile</h2>
                    <ProfileCard class='card' :profile='profile' />
                    <router-link to='/profile/edit' class='button button-blue' id='profile-button'>Edit Profile</router-link>

                </section>

                <section class='col'>

                    <h2 class='col-title'>Account Details</h2>
                    <label for='email' class='label'>Current Email Address:</label>
                    <input type='text' class='email-input' placeholder='...' v-model='accountDetails.Email' required/>
                    <div class='button-row'>
                        <button class='button button-red' @click=showDeletion>Delete Account</button>
                        <button class='button button-blue' @click="updateAccount(accountDetails.Email)">Save</button>
                    </div>
                    <button class ='button button-red' @click='resetTutorial'>Reset tutorial</button>
                    <div class='saved-indicator' v-show='saved'>Saved!</div>
                </section>
            </div>





        </div>


    </main>

	
	<TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Employee Account</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    On the account page, you can edit your profile by clicking edit profile and complete the forms afterwards.
                </p>
				<p class='desc'>
					You can edit your email by changing it just below the profile section.
				</p>
                <p class='desc'>
                    You can also delete your account should you wish so by clicking the delete button.
                </p>
                <p class='desc'>
                    In addition, the ability to restart tutorials for each page is provided by clicking the reset tutorial button.
                </p>
            </div>
        </template>
    </TutorialModal>

	<Footer></Footer>
</template>

<style scoped>
	label {
		font-size: 18px;
	}

	.button {
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
        margin-top: 15px;
        height: 50px;
        text-decoration: none;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .button-blue {
        background: var(--blue);
    }

    .button-blue:active, .button-blue:focus, .button-blue:hover {
        background: var(--blue-focus);
    }
	
    .button-red {
        background: var(--red);
    }

    .button-red:active, .button-red:focus, .button-red:hover {
        background: var(--red-focus);
    }

    .button-row {
		display: flex;
		gap: 8px;
	}

    .col {
        width: 40%;
        min-width: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .col * {
        width: 80%;
    }

    .col-title {
		color: var(--blue);
		font-weight: bold;
		font-size: 30px;
		line-height: 1;
		margin-bottom: 20px;
	}

	.container {
		display: flex;
		flex-direction: column;
		align-content: center;
		max-width: 70vw;
		margin-right: auto;
		margin-left: auto;
	}

    .email-input {
		border: 1px solid var(--slate);
		border-radius: 5px;
		color: var(--slate);
		font-size: 16px;
		line-height: 24px;
		padding: 5px 10px;
        width: calc(80% - 20px);
        margin: 3px 0 10px;
	}

    .label {
        font-size: 13px;
        font-weight: bold;
        color: var(--jet);
        text-align: left;
        margin-top: 10px;
    }

    .row {
        display: flex;
        justify-content: space-evenly;
        margin: 20px 0;
    }

	.saved-indicator {
		margin-top: 15px;
		background: var(--green);
		border-radius: 5px;
		color: #ffffff;
        text-align: center;
        padding: 5px 0;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
	}

    .title {
        text-align: left;  
        margin-top:0; 
        border-bottom: 1px solid;
        font-size: 35px;
    }

    #profile-button {
        width: calc(370px + 40px);
    }
</style>
