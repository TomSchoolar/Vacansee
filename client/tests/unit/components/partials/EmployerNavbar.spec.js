import { shallowMount } from '@vue/test-utils';
import EmployerNavbar from '@/components/partials/EmployerNavbar';

describe('EmployerNavbar.vue Test', () => {
    let wrapper;

    beforeEach(() => {
        // render navbar
        wrapper = shallowMount(EmployerNavbar, {
            global: {
                stubs: ['faIcon']
            },
            propsData: {
                page: 'home',
                numNotifs: 3
            },
            attachTo: document.body
        });
    });

    it('renders number of notifications when component is created', () => {
        // check that the number of notifs is correct
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.text()).toBe('3');
    });

    it('highlights the correct navbar link as the active page', () => {
        // check that the home link is highlighted        
        const homeLink = wrapper.find('#navbar-home');
        expect(homeLink.classes()).toContain('navbar-active-link');
    });

    it('shows the notification bubble if there is notif >= 1', () => {
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(true);
    });

    it('hides the notification bubble if there is notif < 1', async () => {
        wrapper = shallowMount(EmployerNavbar, {
            global: {
                stubs: ['faIcon']
            },
            propsData: {
                page: 'home',
                numNotifs: 0
            }
        });
        
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(false);
    })
});