<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import ProfileCard from '@/components/employee/profile/ProfileCard.vue';
    import ContactCard from '@/components/employee/profile/ContactCard.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employee/profile/formComponents/FormButtons.vue';

    import { computed } from 'vue';

    const props = defineProps(['formData']);
    const emit = defineEmits(['back', 'next', 'publish']);

    const email = 'email@email.com';



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

        function formatGCSEsALevels(q, low, high, num) {
            var qual = num + ' ' + q + ' (' + high + ' - ' + low + ')' ;
            return qual;   
        }

        function formatDegree(subject, type, classification) {
            var qual = type + ' ' + subject + ' (' + classification +')' ;
            return qual;   
        }

        if (data.qualification1 != 'null'){
            if (data.qualification1 == 'gcses' || data.qualification1 == 'alevels' ){
                var q1 = formatGCSEsALevels(data.qualification1, data.lowgrade1, data.highgrade1, data.number1);
            }
            else if ( data.qualification1 == 'degree'){
                var q1 = formatDegree(data.subject1, data.type1, data.classification1);
            }
            else {
                var q1 = 'other';
            }

            if (data.qualification2 != 'null'){
                if (data.qualification2 == 'gcses' || data.qualification2 == 'alevels' ){
                    var q2 = formatGCSEsALevels(data.qualification2, data.lowgrade2, data.highgrade2, data.number2);
                }
                else if ( data.qualification2 == 'degree'){
                    var q2 = formatDegree(data.subject2, data.type2, data.classification2);
                }
                else {
                    var q2 = 'other';
                }
                if (data.qualification3 != 'null'){
                if (data.qualification3 == 'gcses' || data.qualification3 == 'alevels' ){
                    var q3 = formatGCSEsALevels(data.qualification3, data.lowgrade3, data.highgrade3, data.number3);
                }
                else if ( data.qualification3 == 'degree'){
                    var q3 = formatDegree(data.subject3, data.type3, data.classification3);
                }
                else {
                    var q3 = 'other';
                }
                data.Qualifications = [q1,q2,q3];
            }
            else{
                data.Qualifications = [q1,q2];
            }
            }
            else{
                data.Qualifications = [q1];
            }
        }

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
        console.log('quals');    
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
        
        <ProfileCard :profile='formDataProp' />
        <ContactCard :FirstName='formDataProp?.FirstName' :LastName='formDataProp?.LastName' :Pronouns='formDataProp?.Pronouns' :PhoneNumber='formDataProp?.PhoneNumber' :Email=email :TimeZone='formDataProp?.TimeZone' />
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
