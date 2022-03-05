<template>
    <section id='navbar'>
        <span class='navbar-left-wrapper'>
            <router-link to='/vacancy' id='navbar-title'>TINDEED</router-link>
            
            <div class='navbar-link-block'>
                <router-link to='/vacancy' class='navbar-link' :class='{"navbar-active-link": (page == "home")}'>Home</router-link>
                <span class='navbar-divider'></span>
                <router-link to='/favourites' class='navbar-link' :class='{"navbar-active-link": (page == "favourites")}'>Favourites</router-link>
                <span class='navbar-divider'></span>
                <router-link to='/applications' class='navbar-link' :class='{"navbar-active-link": (page == "applications")}'>Applications</router-link>
            </div>
        </span>

        <div class='navbar-link-block'>
            <a href='#' class='navbar-link' id='navbar-notif-container'>
                <i @click='notification' id='navbar-notif' class='fas fa-bell'></i>
                <span id='navbar-notif-alert' v-if='notifs'>{{ numNotifs }}</span>
            </a>
            <span class='navbar-divider'></span>
            <a href='#' @click='logout' class='navbar-link'>Log out</a>
        </div>
    </section>
</template>

<script setup>
    import { ref, onMounted, toRef, watch } from 'vue';
    
    const props = defineProps(['page', 'numNotifs']);

    let notifs = toRef(props, 'numNotifs');

    const notification = () => {
        alert("notification!");
    }

    const logout = () => {
        alert("logged out!");
    }
</script>

<style scoped>
    .navbar-active-link {
        font-weight: bold !important;
    }

    .navbar-active-link {
        color: #ffffff !important;
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
        font-weight: 500;
    }

    .navbar-link:focus, .navbar-link:hover, .navbar-link:active {
        color: #d5d5d5;
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
        background: #cc2936;
    }

    #navbar-notif-alert {
        background-color: #08415c;
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
</style>