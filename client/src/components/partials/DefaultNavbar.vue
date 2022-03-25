<template>
    <section id='navbar'>
        <span class='navbar-left-wrapper'>
            <router-link to='/login' id='navbar-title'>VACANSEE</router-link>
        </span>
    </section>
</template>



<style scoped>
    .navbar-divider {
        height: 22px;
        width: 0;
        border-left: 2px solid #ffffff;
        border-radius: 2px;
        margin: 0 10px;
        position: relative;
        top: 1px;
    }

    .navbar-left-wrapper {
        display: flex;
    }

    #navbar {
        width: 60vw;
        height: 70px;
        margin-bottom: 30px;
        padding: 0 20vw;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #ffffff;
        background: var(--red);
    }

    #navbar-title {
        font-weight: bold;
        font-size: 22px;
        margin-right: 40px;
        color: #ffffff;
        text-decoration: none;
    }
</style>