<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import VacancyCard from '@/components/employee/profile/VacancyCard.vue';
    import ContactCard from '@/components/employee/profile/ProfileCard.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    import { computed } from 'vue';

    const props = defineProps(['formData']);
    const emit = defineEmits(['back', 'next', 'publish']);


    const formDataProp = computed(() => {
        const object = {};

        if(!props.formData) {
            console.log('um');
        }

        console.log('values: ');
        console.log(object);
        props.formData.forEach((value, key) =>  {
            object[key] = value;
            console.log('x');
        });

        console.log(object);
        return object;
    });


    const publish = async () => {
        
        const data = { ...formDataProp.value };

        //format skills data
        data.NotableSkills = [data.skill1, data.skill2, data.skill3];
        delete data['skill1'];
        delete data['skill2'];
        delete data['skill3'];
        console.log(data.NotableSkills);

        //format experience data
        if (data.position1 != ''){
            var pos1 = data.position1 + ' (' + data.position1start + '-' + data.position1end + ')';
            if (data.position2 != ''){
                var pos2 = data.position2 + ' (' + data.position2start + '-' + data.position2end + ')';
                if (data.position3 != ''){
                var pos3 = data.position3 + ' (' + data.position3start + '-' + data.position3end + ')';
                data.Experience = [pos1,pos2,pos3];
            }
            else{
                data.Experience = [pos1,pos2];
            }
            }
            else{
                data.Experience = [pos1];
            }
        }
        
        delete data['position1'];
        delete data['position1start'];
        delete data['position1end'];
        delete data['position2'];
        delete data['position2start'];
        delete data['position2end'];
        delete data['position3'];
        delete data['position3start'];
        delete data['position3end'];
        console.log(data.Experience);

        //format qualification data
        data.Qualifications = [data.qualification1, data.qualification2, data.qualification3]
        delete data['qualification1'];
        delete data['lowgrade1'];
        delete data['highgrade1'];
        delete data['number1'];
        delete data['subject1'];
        delete data['type1'];
        delete data['classification1'];
        delete data['qualification2'];
        delete data['lowgrade2'];
        delete data['highgrade2'];
        delete data['number2'];
        delete data['subject2'];
        delete data['type2'];
        delete data['classification2'];
        delete data['qualification3'];
        delete data['lowgrade3'];
        delete data['highgrade3'];
        delete data['number3'];
        delete data['subject3'];
        delete data['type3'];
        delete data['classification3'];    
        console.log(data.Qualifications);

        const response = await api({
            url: '/profile/',
            method: 'post',
            data,
            contentType: 'json'
        }).catch(apiCatchError);

        if(response?.data?.status != 200) {
            return;
        }

        emit('next')

        await new Promise(r => setTimeout(r, 1000));

        window.location.href = '/profile/';
    }


</script>

<template>
    <FormHeader title='Review'>
        Here's how your vacancy looks to applicants. Check the details and publish when you're ready.
    </FormHeader>

    <div class="review-container">
        <VacancyCard :vacancy='formDataProp' />
        <ContactCard :FirstName='formDataProp?.FirstName' :LastName='formDataProp?.LastName' :Pronouns='formDataProp?.Pronouns' :PhoneNumber='formDataProp?.PhoneNumber' :Email='formDataProp?.Email' :TimeZone='formDataProp?.timezone' />
    </div>

    <FormButtons :back='true' :publish='true' @back='emit("back")' @publish='publish()' />
</template>

<style>
    .review-container {
        width: 43vw;
        min-width: 700px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 20px 0;
    }

    .card {
        width: 42.5% !important;
    }
</style>
