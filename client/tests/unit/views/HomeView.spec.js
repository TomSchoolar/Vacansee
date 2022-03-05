import { mount } from '@vue/test-utils';
import EmployerIndex from '@/views/employer/EmployerIndex.vue';

describe('EmployerIndexView.vue Test', () => {
    let wrapper;

    beforeEach(() => {
        // render navbar
        wrapper = mount(EmployerIndex, {
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