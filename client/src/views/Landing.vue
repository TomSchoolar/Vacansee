<script setup>
    import ApplyProfileCard from '@/components/partials/ApplyProfileCard.vue';

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
    <ApplyProfileCard :application='applicantData' />
</template>

<style></style>