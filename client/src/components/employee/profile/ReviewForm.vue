<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import ProfileCard from '@/components/employer/match/ProfileCard.vue';
    import ContactCard from '@/components/employee/profile/ContactCard.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    import { ref, computed } from 'vue';

    const props = defineProps(['formData']);
    const emit = defineEmits(['back', 'next', 'publish']);

    let session = window.localStorage.getItem('session') ?? '{}'
    const { Email: em = false } = JSON.parse(session);
    const email = ref(em);

    const formDataProp = computed(() => {
        const object = {};

        if(!props.formData) {
            return;
        }

        props.formData.forEach((value, key) =>  {
            object[key] = value;
        });

        parseExpandingList(object, 'NotableSkills', 1);
        parseExpandingList(object, 'Experience', 2);
        parseExpandingList(object, 'Qualifications', 1);

        return object;
    });

    const parseExpandingList = (inputObj, field, inputsPerItem) => {
        let array = [];
        Object.keys(inputObj).forEach((key) => {
            if((key.split('-')[0] == field)) {
                array.push(inputObj[key]);
                delete inputObj[key];
            }
        });

        if(inputsPerItem > 1) {
            // more than one input per item, create 2d array
            array = array.map((el, i, arr) => {
                if(i % inputsPerItem == 0 && el) {
                    let subArr = [];
                    for(let j = 0; j < inputsPerItem; j++) {
                        subArr.push(arr[i + j]);
                    }
                    return subArr.join('&&');
                }
            });
        }

        inputObj[field] = array.filter((el) => el ? true : false);
    }

    const publish = async () => {
        
        const data = { ...formDataProp.value };

        //format skills data

        data.Qualifications = JSON.stringify(data.Qualifications)
        data.NotableSkills = JSON.stringify(data.NotableSkills)
        data.Experience = JSON.stringify(data.Experience);

        const response = await api({
            url: '/v1/profiles/',
            method: 'post',
            data,
            contentType: 'json'
        }).catch(apiCatchError);

        if(response?.data?.status != 200) {
            return;
        }

        emit('next')
        
        let session = localStorage.getItem('session');
        session = JSON.parse(session);
        session.HasProfileSetup = true;
        session = JSON.stringify(session);
        localStorage.setItem('session', session);

        await new Promise(r => setTimeout(r, 1000));

        window.location.href = '/vacancy';
    }


</script>

<template>
    <FormHeader title='Review'>
        Here's how your profile looks to employers. Check the details and publish when you're ready.
    </FormHeader>

    <div class="review-container">
        <ProfileCard :profile='formDataProp' />
        <ContactCard :FirstName='formDataProp?.FirstName' :LastName='formDataProp?.LastName' :Pronouns='formDataProp?.Pronouns' :PhoneNumber='formDataProp?.PhoneNumber' :Email=email :TimeZone='formDataProp?.TimeZone' />
    </div>

    <FormButtons :back='true' :publish='true' @back='emit("back")' @publish='publish()' />
</template>

<style scoped>
    *:deep(.card) {
        width: 42.5%;
    }    
    
    .review-container {
        width: 43vw;
        min-width: 700px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 20px 0;
    }
</style>
