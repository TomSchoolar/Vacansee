<template>
    <EmployerNavbar page='home' :numNotifs='notifs'></EmployerNavbar>

    <button @click='notifs++'>Add notification</button>
    <button @click='notifs < 1 ? 0 : notifs--'>Remove Notification</button>

	<div class="home">
		<img alt="Vue logo" src="../../assets/logo.png" />
		<HelloWorld msg="Welcome to Your Vue.js App" />
	</div>
</template>

<script setup>
// @ is an alias to /src
    import HelloWorld from '@/components/HelloWorld.vue';
    import EmployerNavbar from '@/components/partials/EmployerNavbar.vue';

    import { ref } from 'vue';

    let notifs = ref(0);    
</script>
