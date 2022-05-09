<script setup>
	import Footer from '@/components/partials/Footer.vue';
    import EmployerNavbar from '@/components/employer/EmployerNavbar.vue';
	import AccountModal from '@/components/employer/account/AccountModal.vue';
	import TutorialModal from '../../components/employer/tutorial/TutorialModal.vue';


	import { logout } from '@/assets/js/jwt';
    import api, { apiCatchError } from '@/assets/js/api';
    import { ref, onMounted, watch } from 'vue';


	const url = window.location.pathname;

	//const notifs = ref(2);
	const saved = ref(false);
	const details = ref({});
	const displayModal = ref(false);
	const isNewUser = ref(window.localStorage.getItem('newUserEmployerAccount') == null);


	document.title = 'Account | Vacansee'

	const showDeletion = () => {
		displayModal.value = true;
	}

	const getAccount = async () => {

		const response = await api({
			url: `/v1/e/accounts/`,
			method: 'get',
			responseType: 'json'
		}).catch(apiCatchError);

		if (!response)
			return false;

		const { data } = response;

		if(!data)
			return false;

		const {
			details: apiDetails = {},
			email: apiEmail = ''
		} = data;

		details.value = apiDetails;
		details.value.Email = apiEmail;

		return true;
	}

	const updateAccount = async (newCompanyName, newPhoneNumber, newEmail) => {
		const response = await api({
			url: '/v1/e/accounts/',
			method: 'put',
			data: {
				setCompanyName: newCompanyName,
				setPhoneNumber: newPhoneNumber,
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
			url: '/v1/e/accounts/',
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

	const resetTutorial = () => {
        window.localStorage.removeItem('newUserEmployerAccount');
		window.localStorage.removeItem('newUserEditVacancy');
		window.localStorage.removeItem('newUserEmployerIndex');
		window.localStorage.removeItem('newUserEmployerMatch');
		window.localStorage.removeItem('newUserCreateVacancy');
		window.localStorage.removeItem('newUserReview');

        isNewUser.value = true;
    }

	const finishTutorial = () => {
        window.localStorage.setItem('newUserEmployerAccount', false);
        isNewUser.value = false;
    }

	onMounted(async () => {
		const result = await getAccount({ });

		if(!result) {
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
        <!-- <EmployerNavbar page='account' :numNotifs='notifs'></EmployerNavbar> -->
		<EmployerNavbar page='account' ></EmployerNavbar>

        <section class='container'>
			<AccountModal :display='displayModal' @close='displayModal = false' @delete='deleteAccount' />
			
            <h1 class='title'>My Account</h1>

            <div class='col'>
                <p class='col-title'>Account Details</p>

                <label for='title' class='label'>Company Name:</label>
                <input type='text' class='input' placeholder='...' v-model='details.CompanyName' id='title' required/>
                
                <label for='phone' class='label'>Default Phone Number:</label>
                <input type='text' class='input' placeholder='...' v-model='details.PhoneNumber' id='phone' required/>
                
                <label for='email' class='label'>Current Email Address:</label>
                <input type='email' class='input' placeholder='...' v-model='details.Email' id='email' required/>
                
                <div class='button-container'>
                    <button class='button button-red' @click='showDeletion'>Delete Account</button>
                    <button class='button button-blue' @click='updateAccount(details.CompanyName, details.PhoneNumber, details.Email)'>Save</button>
                </div>
                
                <button class ='button button-blue' @click='resetTutorial'> Reset tutorial</button>
            
                <div class='saved-indicator' v-show='saved'>
                    <p>Saved!</p>
                </div>
            </div>
		</section>

		<Footer></Footer>
    </main>

	<TutorialModal v-if='isNewUser' @close-modal='finishTutorial' >
        <template #modal-header>
            <h3>Employer account</h3>
        </template>
        <template #modal-body> 
            <div class='modal-body'>
                <p class='desc'>
                    On the account page, you can change your company's name and contact information by filling in the form and clicking
                    the save button.
                </p>
                <p class='desc'>
                    You can also delete your account should you wish so by clicking the delete button.
                </p>
                <p class='desc'>
                    In addition, the ability to restart tutorials for each page is also provided by clicking the reset tutorial button.
                </p>
            </div>
        </template>
    </TutorialModal>
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
    }

    .button-blue {
        background: var(--blue);
    }

    .button-blue:active, .button-blue:focus, .button-blue:hover {
        background: var(--blue-focus);
    }

	.button-container {
		display: flex;
		gap: 0.2vw;
	}

    .button-red {
        background: var(--red);
    }

    .button-red:active, .button-red:focus, .button-red:hover {
        background: var(--red-focus);
    }

    .col {
        width: 40%;
        min-width: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 0 auto;
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

	.input {
		border: 1px solid var(--slate);
		border-radius: 5px;
		color: var(--jet);
		font-size: 16px;
		line-height: 24px;
		padding: 5px 10px;
		margin: 0 0 10px 0;
        width: calc(80% - 20px);
	}

    .label {
        font-size: 13px;
        font-weight: bold;
        color: var(--jet);
        text-align: left;
        margin-top: 10px;
    }

	.logo {
		color: var(--blue);
		font-weight: bold;
		font-size: 36px;
		line-height: 1;
		text-transform: uppercase;
		margin: 0 0 25px 0;
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
</style>
