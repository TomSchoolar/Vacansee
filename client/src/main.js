import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// import fontawesome icons
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBell } from '@fortawesome/free-solid-svg-icons';

library.add(faBell);

createApp(App)
    .use(router)
    .component('faIcon', FontAwesomeIcon)
    .mount('#app')
