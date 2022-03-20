<script setup>
    import ApplyVacancyCard from '@/components/partials/ApplyVacancyCard.vue';
    import VacancyCard from '@/components/partials/VacancyCard.vue';

    import ApplyProfileCard from '@/components/partials/ApplyProfileCard.vue';
    import ProfileCard from '@/components/partials/ProfileCard.vue';
</script>

<template>
    <main class='container'>
        <section class='landing-page'>
            <h1>Landing Page</h1>
        </section>
        <div class='login'>
            <router-link :to='`/login`' class='login-button'>Login</router-link>
        </div>
    </main>
</template>

<style>
    .login {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .login-button {
        width: 200px;
        border: 2px solid black;
        border-radius: 5px;
        font-size: 24px;
        background-color: var(--slate);
        color: white;
        text-decoration: none;
    }
</style>