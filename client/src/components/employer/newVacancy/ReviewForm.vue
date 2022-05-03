<script setup>
    import api, { apiCatchError } from '@/assets/js/api';
    import VacancyCard from '@/components/employee/index/VacancyCard.vue';
    import ContactCard from '@/components/employer/newVacancy/ContactCard.vue';
    import FormHeader from '@/components/employer/newVacancy/formComponents/FormHeader.vue';
    import FormButtons from '@/components/employer/newVacancy/formComponents/FormButtons.vue';

    import { computed } from 'vue';

    const props = defineProps(['formData', 'edit']);
    const emit = defineEmits(['back', 'next', 'publish']);

    const tags = [
        {
            id: 0,
            icon: 'fa-solid fa-book'
        },
        {
            id: 1,
            icon: 'fa-solid fa-code'
        },
        {
            id: 2,
            icon: 'fa-brands fa-python'
        },
        {
            id: 3,
            icon: 'fa-solid fa-school'
        },
        {
            id: 4,
            icon: 'fa-solid fa-briefcase'
        },
        {
            id: 5,
            icon: 'fa-solid fa-database'
        },
    ]

    const formDataProp = computed(() => {
        const object = {};
        object.Tags = [];

        if(!props.formData) {
            return;
        }

        props.formData.forEach((value, key) =>  {
            if(key == 'tagsInput')
                object.Tags.push(value);
            else
                object[key] = value;
        });

        parseExpandingList(object, 'SkillsRequired', 1);
        parseExpandingList(object, 'ExperienceRequired', 2);

        return object;
    });

    const parseExpandingList = (inputObj, field, inputsPerItem) => {
        let array = [];
        Object.keys(inputObj).forEach((key) => {
            if(key.split('-')[0] == field) {
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
        delete data['CompanyName'];
        
        data.Tags = data.Tags.map((tag) => parseInt(tag) );
        data.TimeZone = parseInt(data.TimeZone)

        data.Tags = JSON.stringify(data.Tags);
        data.SkillsRequired = JSON.stringify(data.SkillsRequired);
        data.ExperienceRequired = JSON.stringify(data.ExperienceRequired);

        let id;
        if(props.edit) {
            id = window.location.pathname.split('/').pop();
        }
        
        const response = await api({
            url: (props.edit ? `/v1/e/vacancies/edit/${ id }/` : '/v1/e/vacancies/'),
            method: (props.edit ? 'put' : 'post'),
            data,
            contentType: 'json'
        }).catch(apiCatchError);

        if(response?.data?.status != 200) {
            return;
        }

        emit('next')

        await new Promise(r => setTimeout(r, 1000));

        window.location.href = '/e/vacancy/';
    }

</script>

<template>
    <FormHeader title='Review'>
        Here's how your vacancy looks to applicants. Check the details and publish when you're ready.
    </FormHeader>

    <div class="review-container">
        <VacancyCard :vacancy='formDataProp' :tags='tags' />
        <ContactCard :PhoneNumber='formDataProp?.PhoneNumber' :Email='formDataProp?.Email' :TimeZone='formDataProp?.TimeZone' />
    </div>

    <FormButtons :back='true' :publish='true' @back='emit("back")' @publish='publish()' />
</template>

<style scoped>
    .review-container {
        width: 43vw;
        min-width: 700px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 20px 0;
    }

    div:deep(.card) {
        width: 42.5%;
    }
</style>