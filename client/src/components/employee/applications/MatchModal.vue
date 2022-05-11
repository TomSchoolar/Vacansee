<script setup>
    const emit = defineEmits(['close'])
    const { display = false, stats = false } = defineProps(['display', 'stats']);

</script>

<template>
    <div class='cover' v-if='display'>
        <div class='modal'>
            <i class="fa-solid fa-xmark close" @click='emit("close")'></i>

            <h4 class='company'>{{ stats.CompanyName }}</h4>
            <div class='role-container'><span class='role'>{{ stats.VacancyName }}</span> <span class='match'>MATCH!</span></div>

            <p class='description'>{{ stats.Description }}</p>
        
            <div class='contact'>
                <i class="fa-solid fa-phone"></i>
                {{ stats.Email }}
            </div>

            <div class='contact'>
                <i class="fa-solid fa-envelope-open"></i>
                {{ stats.PhoneNumber }}
            </div>

            <div class='contact'>
                <i class="fa-solid fa-clock"></i>
                {{ stats.TimeZone }}
            </div>
        </div>
    </div>
</template>

<style scoped>
    .close {
        color: var(--jet);
        position: absolute;
        top: 16px;
        right: 16px;
        font-size: 18px;
        cursor: pointer;
    }

    .close:active, .close:focus, .close:hover {
        color: var(--red)
    }

    .company {
        font: var(--font);
        font-weight: 600;
        font-size: 30px;
        margin: 0;
    }

    .contact {
        font-size: 17px;
    }

    .contact i {
        font-size: 22px;
        margin: 10px 10px 10px 0;
    }

    .cover {
        position: absolute;
        top: 0;
        left: 0;
        height: 100vh;
        width: 100vw;
        background: #00000080;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 100;
        min-height: 100vh;
        min-width: 100vw;
    }

    .description {
        text-align: left;
        margin: 10px 0;
    }

    .role {
        margin-right: 10px;
    }

    .role-container {
        font-size: 25px;
        text-align: left;
    }

    .match {
        color: var(--green);
        font-weight: bold;
    }

    .modal {
        background: white;
        border-radius: 8px;
        width: 30vw;
        min-width: 450px;
        position: relative;
        padding: 25px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }


</style>