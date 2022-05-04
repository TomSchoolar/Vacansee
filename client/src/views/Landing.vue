<script setup>
    import axios from 'axios';
    import VacancyCard from '@/components/auth/VacancyCard.vue';
    
    import { onMounted, ref } from 'vue';

    const vacancies = ref([]);

    onMounted(async () => {
        const response = await axios({
            baseURL: process.env.VUE_APP_API_ENDPOINT,
            url: '/vacancy/',
            method: 'get',
            responseType: 'json',
            timeout: 3000,
            params: {
                count: 10,
                noAuth: true
            }
        }).catch((err) => {
            console.error(err);
        });

        if(!response?.data?.vacancies)
            return;

        if(response.data.message)
            console.log(response.data.message);

        vacancies.value = response.data.vacancies;
    });


</script>

<template>
    <main class='container'>
        <section class='top'>
            <div class='top-col-left'>
                <div class='top-intro-container'>
                    <h1 class='top-title'>VACANSEE</h1>
                    <p class='top-tagline'> Making finding soul-sucking jobs a little less naff </p>
                    <router-link :to='`/login`' class='button button-red'>Start Now</router-link>
                </div>
            </div>

            <div class = 'top-col-right'>
                <img src='@/assets/career-center-carousel-p-500.v4.png' class='top-img' alt='smiling man in suit punching the air' />
            </div>
        </section>

        <section class='mid'>
            <div class='mid-text'>
                <h3 class='title'> Feast your eyes, employment gannets </h3>
                <p class='desc'>
                    Thousands of organisations that we just made up publish advertisements for new vacancies every hour, so there is something for everyone held by the scruff of the neck by the Student Loans Company. 
                </p>
            </div>
            <div class='mid-cards'>
                <div class='mid-slider' v-if='vacancies.length != 0'>
                    <div class='mid-slide-track'>
                        <VacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' id= 'cards'/>
                        <VacancyCard v-for='vacancy in vacancies' :key='vacancy.VacancyId' :vacancy='vacancy' id= 'cards'/>
                    </div>
                </div>
            </div>
        </section>

        <section class='bottom'>
            <div class='bottom-container'>
                <h3 class='title'>In a rush?</h3>
                <p class='desc'> We provide applicants and employers with tools that allow them to get what they're doing done. Fast. </p>
                <router-link :to='`/login`' class='button button-white'>Start Now</router-link>
            </div>
        </section>

    </main>
</template>

<style scoped>
    body {
        overflow-x: hidden;
    }

    .bottom{
        padding: 20px;
        height: 40vh;
        background-color: #08415c;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .bottom-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .bottom-login {
        width: 10vw;
        height: 3vh;
        border: 0;
        border-radius: 5px;
        background-color: white;
        color: var(--blue);
        text-decoration: none;
        line-height: 3vh;
    }

    .bottom-login:active .bottom-login:focus .bottom-login:hover {
        color: var(--blue-focus);
    }

    .bottom-title {
        font-size: calc(18px + 0.8vw);
        margin: 0;
        margin-bottom: calc(15px + 1.0%);
    }

    .button {
        height: 3vh;
        border: 0;
        border-radius: 5px;
        color: white;
        text-decoration: none;
        line-height: 3vh;
        font-size: calc(12px + 0.3vw);
        padding: calc(6px + 0.2vh) calc(12px + 0.4vw);
        margin: calc(5px + 2%) 0;
    }

    .button-red {
        background-color: var(--red);
    }

    .button-red:active, .button-red:hover, .button-red:focus {
        background-color: var(--red-focus);
    }

    .button-white {
        color: var(--blue);
        background-color: white;
    }

    .button-white:active, .button-white:hover, .button-white:focus {
        background-color: #ddd;
    }

    .desc {
        color: #bbb;
        font-size: calc(13px + 0.25vw)
    }

    .mid {
        width: 100vw;
        padding: calc(25px + 1.0%) 0;
        background-color: #333;
        color: white;
        min-height: 50vh;
    }

    .mid-cards {
        display: flex;
        justify-content: space-evenly;
        margin-bottom: 20px;
        position: relative;
    }

    .mid-slider {
        background: var(--jet);
        min-height: 100px;
        margin: auto;
        overflow:hidden;
        position: relative;
        width: 100vw;
	}

    .mid-slider::before, .mid-slider::after {
        background: linear-gradient(to right,  rgba(51,51,51,1) 0%, rgba(51,51,51,0) 100%);
        content: "";
        height: 100%;
        position: absolute;
        width: 100px;
        z-index: 2;
    }
	
	.mid-slider::after {
		right: 0;
		top: 0;
		transform: rotateZ(180deg);
	}

	.mid-slider::before {
		left: 0;
		top: 0;
	}

	.mid-slide-track {
		animation: scroll 60s linear infinite;
		display: flex;
		width: calc(370px * 20);
	}

    .mid-text {
        width: 50%;
        margin: 0 auto;
        text-align: left;
    }

    .title {
        font-size: calc(18px + 0.8vw);
        margin: 0;
        margin-bottom: calc(15px + 1.0%);
    }

    .top {
        color: black;
        position: relative;
        min-height: 320px;
        height: 60vh;
    }

    .top::after {
        content: "";
        display: table;
        clear: both;
    }

    .top-col-left {
        background-color: white;
        float: left;
        width: 42.5%;
        height: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }

    .top-col-right {
        float: right;
        width: 50vw;
        height: 100%;
        background-color: white;
        position: relative;
        animation: 1.0s ease-in-out 0s 1 slideInFromRight;
    }

    .top-col-right::before {
        content: '';
        position: absolute;
        top: 0; 
        right: 0;
        width: 150%; 
        height: 100%;
        background-color: var(--red);
        animation: 0.75s ease-out 0s 1 angleSlideInFromRight;

        -webkit-transform: skewX(-15deg) translateX(33%);
        -ms-transform: skewX(-15deg) translateX(33%);
        transform: skewX(-15deg) translateX(33%);
    }

    .top-img {
        position: absolute;
        max-height: 100%;
        max-width: 100%;
        bottom: 0;
        left: 0;
    }

    .top-intro-container {
        width: 40%;
        min-width: 160px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        text-align: left;
        margin: 30px 0;
    }

    .top-tagline {
        color: var(--jet);
        font-size: calc(16px + 0.7vw);
        font-weight: 500;
        margin: calc(5px + 2%) 0;
    }

    .top-title {
        font-size: calc(25px + 1.5vw);
        color: var(--blue);
        margin: calc(5px + 2%) 0;
    }

    @keyframes slideInFromRight {
        0% {
            transform: translateX(200%);
        }

        100% {
            transform: translateX(0%);
        }
    }

    @keyframes angleSlideInFromRight {
        0% {
            transform: skewX(-15deg) translateX(133%);
        }

        100% {
            transform: skewX(-15deg) translateX(33%);
        }
    }

    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(calc(-370px * 10 - 10px))}
    }
</style>