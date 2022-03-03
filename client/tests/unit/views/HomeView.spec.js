import { mount } from '@vue/test-utils';
import HomeView from '@/views/HomeView.vue';

describe('HomeView.vue Test', () => {
    let wrapper;

    beforeEach(() => {
        // render navbar
        wrapper = mount(HomeView, {
            global: {
                stubs: ['faIcon']
            },
            attachTo: document.body
        });
    });

    it('adds and removes one from notifs when add/remove buttons are clicked', async () => {
        let notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(false);

        let addButton = wrapper.findAll('button').at(0);
        await addButton.trigger('click');

        notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.text()).toBe('1');

        let removeButton = wrapper.findAll('button').at(1);
        await removeButton.trigger('click');

        notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(false);
    });
});