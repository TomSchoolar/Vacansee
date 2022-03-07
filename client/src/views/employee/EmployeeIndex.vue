<template>
    <EmployeeNavbar page='home' :numNotifs='notifs'></EmployeeNavbar>

    <button @click='notifs++'>Add notification</button>
    <button @click='notifs < 1 ? 0 : notifs--'>Remove Notification</button>
</template>

<script setup>
    import EmployeeNavbar from '@/components/partials/EmployeeNavbar.vue';

    import { ref } from 'vue';

    let notifs = ref(0);    
</script>