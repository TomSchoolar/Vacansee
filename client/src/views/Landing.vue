<script setup>
    import ApplyVacancyCard from '@/components/partials/ApplyVacancyCard.vue';
    import VacancyCard from '@/components/partials/VacancyCard.vue';

    import ApplyProfileCard from '@/components/partials/ApplyProfileCard.vue';
    import ProfileCard from '@/components/partials/ProfileCard.vue';

    let vacancyData = {
        vID: 1,
        companyName: 'Sarah\'s Flower Co.',
        jobTitle: 'Customer Service Representative',
        favourited: true,
        location: 'London',
        description: 'What an awesome description of a company job is happeneing right here in this very paragraph - Wild!',
        skills: ['Good customer approach', 'Friendly attitude', 'Patience'],
        experience: ['1 Year, Customer Service', '2 Years, Management', '1 Year, Retail'],
        tags: [
            {
                id: 1,
                icon: 'fa-solid fa-book',
                title: 'book'
            },
            {
                id: 2,
                icon: 'fa-solid fa-clock',
                title: 'clock'
            },
            {
                id: 3,
                icon: 'fa-solid fa-handshake',
                title: 'handshake'
            },
            {
                id: 4,
                icon: 'fa-solid fa-users',
                title: 'users'
            },
            {
                id: 5,
                icon: 'fa-brands fa-stack-overflow',
                title: 'stack overflow'
            },
            {
                id: 6,
                icon: 'fa-brands fa-stack-overflow',
                title: 'google'
            },
            {
                id: 7,
                icon: 'fa-brands fa-stack-overflow',
                title: 'twitter'
            }
        ]
    };


    let applicantData = {
        firstName: 'George',
        pronouns: 'he/him',
        location: 'London',
        topicSentence: 'Good luck convincing people to hire you with one sentence.',
        skills: ['75 wpm typing speed', 'Microsoft Excel', 'Patience'],
        experience: [
            {
                title: 'fast food restaurant',
                startDate: '2016',
                endDate: '2019' 
            },
            {
                title: 'customer service call centre',
                startDate: '2019',
                endDate: '2021' 
            },
            {
                title: 'level 1 support tech',
                startDate: '2021',
                endDate: '2022' 
            }
        ],
        qualifications: ['9 GCSEs (A*-D)', '3 A-Levels (A-B)']
    }
</script>

<template>
    landing page..?
    <div class='cards'>
        <ApplyVacancyCard :vacancy='vacancyData' />
        <VacancyCard :vacancy='vacancyData' />
    </div>

    <div class='cards'>
        <ApplyProfileCard :application='applicantData' />
        <ProfileCard :application='applicantData' />
    </div>

</template>

<style>
    .cards {
        display: flex;
        justify-content: space-evenly;
        margin-bottom: 20px;
    }
</style>