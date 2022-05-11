<script setup>
    import { toRef } from 'vue';
    import { logout } from '@/assets/js/jwt';
    
    const props = defineProps(['page']);
    
    //notification alerts
    /*const props = defineProps(['page', 'numNotifs']);

    let notifs = toRef(props, 'numNotifs');

    const notification = () => {
        alert("notification!");
    }*/
</script>



<template>
    <div id='navbar'>
        <span class='navbar-left-wrapper'>
            <router-link to='/e/vacancy' id='navbar-title'>VACANSEE</router-link>
            
            <div class='navbar-link-block'>
                <router-link to='/e/vacancy' class='navbar-link' :class='{"navbar-active-link": (page == "home")}'>Home</router-link>
                <span class='navbar-divider'></span>
                <router-link to='/e/vacancy/new' class='navbar-link' :class='{"navbar-active-link": (page == "newVacancy")}'>New Vacancy</router-link>
                <span class='navbar-divider'></span>
                <router-link to='/e/match' class='navbar-link' :class='{"navbar-active-link": (page == "matches")}'>Matches</router-link>
            </div>
        </span>

        <div class='navbar-link-block'>

            <!-- Notification bar -->
            <!-- <a href='#' class='navbar-link' id='navbar-notif-container'>
                <i @click='notification' id='navbar-notif' class='fas fa-bell'></i>
                <span id='navbar-notif-alert' v-if='notifs'>{{ numNotifs }}</span>
            <span class='navbar-divider'></span>
            </a> -->
            
            <router-link to='/e/account' class='navbar-link' :class='{"navbar-active-link": (page == "account")}'>My Account</router-link>
            <span class='navbar-divider'></span>
            <a href='#' @click='logout' class='navbar-link'>Log out</a>
        </div>
    </div>
</template>



<style scoped>
    .navbar-active-link {
        font-weight: bold !important;
        color: #bbbbbb !important;
    }

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

    .navbar-link {
        color: #ffffff;
        text-decoration: none;
    }

    .navbar-link:focus, .navbar-link:hover, .navbar-link:active {
        color: #cccccc;
    }

    .navbar-link-block {
        display: flex;
        justify-content: center;
        align-items: center;
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
        background: var(--blue);
    }

    #navbar-notif-alert {
        background-color: var(--red);
        border-radius: 30%;
        height: 14px;
        min-width: 14px;
        padding: 1px;
        font-size: 11px;
        display: inline-flex;
        justify-content: center;
        align-content: center;
        position: absolute;
        bottom: -4px;
        right: -4px;
    }

    #navbar-notif-container {
        position: relative;
    }

    #navbar-notif {
        font-size: 23px;
        position: relative;
        top: 3px;
        margin: 0 5px;
    }

    #navbar-title {
        font-weight: bold;
        font-size: 22px;
        margin-right: 40px;
        color: #ffffff;
        text-decoration: none;
    }

    #navbar-user {
        font-size: 23px;
        position: relative;
        top: 3px;
        margin: 0 5px;
    }
</style>