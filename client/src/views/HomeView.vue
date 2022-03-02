<template>
    <EmployerNavbar page='home' :numNotifs='notifs'></EmployerNavbar>

    <button @click='addNotif'>Add notification</button>
    <button @click='removeNotif'>Remove Notification</button>

	<div class="home">
		<img alt="Vue logo" src="../assets/logo.png" />
		<HelloWorld msg="Welcome to Your Vue.js App" />
	</div>
</template>

<script setup>
// @ is an alias to /src
    import HelloWorld from '@/components/HelloWorld.vue';
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';

    import { ref } from 'vue';

    let notifs = ref(0);

    const addNotif = () => {
        notifs.value++;
    }

    const removeNotif = () => {
        if(notifs.value > 0)
            notifs.value--;
    }
    
</script>
