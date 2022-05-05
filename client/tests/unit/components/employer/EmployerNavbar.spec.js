import { shallowMount, RouterLinkStub } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import EmployerNavbar from '@/components/employer/EmployerNavbar';
import routes from '@/router/routes';

const router = createRouter({
    routes,
    history: createWebHistory()
});

const mountSettings = {
    propsData: {
        page: 'home',
        //numNotifs: 3
    },
    global: {
        plugins: [router],
        stubs: {
            stubs: ['faIcon'],
            RouterLink: RouterLinkStub
        }
    }
};

describe('EmployerNavbar.vue', () => {
    let wrapper;

    beforeEach(() => {
        // render navbar
        wrapper = shallowMount(EmployerNavbar, mountSettings);
    });

    it('highlights the correct navbar link as the active page', () => {
        // check that the home link is highlighted        
        const homeLink = wrapper.findAll('.navbar-link').at(0);
        expect(homeLink.classes()).toContain('navbar-active-link');
    });

    /*
    it('renders number of notifications when component is created', () => {
        // check that the number of notifs is correct
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.text()).toBe('3');
    });

    

    it('shows the notification bubble if there is notif >= 1', () => {
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(true);
    });

    it('hides the notification bubble if there is notif < 1', async () => {
        mountSettings.propsData.numNotifs = 0;
        wrapper = shallowMount(EmployerNavbar, mountSettings);

        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(false);
    })*/
});