<template>
    <div id='navbar'>
        <span class='navbar-left-wrapper'>
            <a href='/e/vacancy' id='navbar-title'>TINDEED</a>
            
            <div class='navbar-link-block'>
                <a href='/e/vacancy' class='navbar-link' id='navbar-home'>Home</a>
                <span class='navbar-divider'></span>
                <a href='/e/vacancy/new' class='navbar-link' id='navbar-newVacancy'>New Vacancy</a>
                <span class='navbar-divider'></span>
                <a href='/e/match' class='navbar-link' id='navbar-matches'>Matches</a>
            </div>
        </span>

        <div class='navbar-link-block'>
            <a href='#' class='navbar-link' id='navbar-notif-container'>
                <faIcon @click='notification' id='navbar-notif' icon='bell'></faIcon>
                <span id='navbar-notif-alert' v-if='notifs'>{{ numNotifs }}</span>
            </a>
            <span class='navbar-divider'></span>
            <a href='#' @click='logout' class='navbar-link'>Log out</a>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted, toRef, watch } from 'vue';
    
    const props = defineProps(['page', 'numNotifs']);

    let notifs = toRef(props, 'numNotifs');
    
    onMounted(() => {
        const pageLink = document.getElementById(`navbar-${ props.page }`);

        if(pageLink != null) {
            pageLink.classList.add('navbar-active-link');
        }
    });

    const notification = () => {
        alert("notification!");
    }

    const logout = () => {
        alert("logged out!");
    }
</script>

<style>
    body {
        margin: 0;
    }

    .navbar-active-link {
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
        font-weight: 500;
    }

    .navbar-link:focus, .navbar-link:hover, .navbar-link:active {
        color: #bbbbbb;
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
        background: #08415c;
    }

    #navbar-notif-alert {
        background-color: #cc2936;
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