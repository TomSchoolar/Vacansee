<template>
    <section id='footer'>
        <span class='footer-centre-wrapper'>
            <div class='footer-link-block'>
                <router-link to='/privacy' class='footer-link'>Privacy Policy</router-link>
            </div>
        </span>
    </section>
</template>



<style scoped>
    .footer-active-link {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    .footer-centre-wrapper {
        display: flex;
        margin: 0 auto;
    }

    .footer-link {
        color: #ffffff;
        text-decoration: none;
    }

    .footer-link:focus, .footer-link:hover, .footer-link:active {
        color: #d5d5d5;
    }

    .footer-link-block {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #footer {
        width: 60vw;
        height: 70px;
        padding: 0 20vw;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #ffffff;
        background: var(--jet);
        position: absolute;
        top: calc(max(calc(100vh - 70px), 100%));
    }
</style>
