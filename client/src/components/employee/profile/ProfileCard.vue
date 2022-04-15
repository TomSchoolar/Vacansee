<script setup>
    const props = defineProps(['Name', 'PhoneNumber', 'Email', 'TimeZone']);
</script>

<template>
    <div class="contact-card">
        <h5 class="name">{{ Name}}</h5>
        <div class='contact'>
            <i class="fa-solid fa-phone"></i>
            {{ PhoneNumber }}  
        </div>
        <div class='contact'>
            <i class="fa-solid fa-envelope-open"></i>
            {{ Email }}  
        </div>
        <div class='contact'>
            <i class="fa-solid fa-clock"></i>
            {{ TimeZone }}
        </div>
    </div>
</template>

<style scoped>
    .name {
        font-size: 20px;
        margin: 0 0 15px 0;
    }

    .contact {
        font-size: 16px;
        margin-bottom: 2.5px;
    }

    .contact i {
        margin-right: 5px;
    }
    
    .contact-card {
        border: 2px solid var(--jet);
        min-height: 110px;
        min-width: 260px;
        border-radius: 5px;
        width: calc(40% - 40px);
        position: relative;
        bottom: 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        padding: 15px 20px;
    }
</style>
