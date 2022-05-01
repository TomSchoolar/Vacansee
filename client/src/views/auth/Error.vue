<script setup>
    import DefaultNavbar from '@/components/partials/DefaultNavbar.vue';
</script>

<template>
    <DefaultNavbar></DefaultNavbar>

    <main class='container'>
        <section class='error'>
            <span class='fourOhFour'>404</span>
            <span class='notFound'>Page not found</span>
            <router-link to='/login' id='homeLink'><i class="fa-solid fa-circle-arrow-left"></i>Home?</router-link>
        </section>
    </main>
</template>

<style>
    span {
        display: block;
    }

    .container {
        width: 100vw;
        height: calc(100vh - 100px);
        margin: 0 auto;
        position: relative;
    }

    .error {
        text-align: center;
        position: absolute;
        width: 300px;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .fourOhFour {
        color: var(--red);
        font-size: 156px;
        line-height: 1;
        font-weight: 600;
        padding: 0 0 10px 0;
    }

    .notFound {
        font-size: 24px;
        line-height: 1;
        font-weight: 500;
        padding: 0 0 100px 0;
    }

    #homeLink {
        color: var(--red);
        font-size: 18px;
        line-height: 1;
        text-decoration: none;
    }

    #homeLink i {
        padding: 0 7px 0 0;
    }
</style>
