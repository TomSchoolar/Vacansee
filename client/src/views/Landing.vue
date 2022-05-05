<script setup>
    import VacancyCard from '@/components/auth/VacancyCard.vue';
    import Footer from '@/components/partials/CompactFooter.vue';

    let vacancies = [
        {
        jobTitle: 'Newsdancer',
        position: 'The News',
        description: 'We are looking for a lot of words and more words here because we need more words to fill up space with words.',

        },

        {
        jobTitle: 'Reporter',
        position: 'The News',
        description: 'We are looking for...',

        },

        {
        jobTitle: 'Reporter',
        position: 'The News',
        description: 'We are looking for...',
        },

                {
        jobTitle: 'Reporter',
        position: 'The News',
        description: 'We are looking for...',
        },


         {
        jobTitle: 'Newsdancer',
        position: 'The News',
        description: 'We are looking for a lot of words and more words here because we need more words to fill up space with words.',

        },

        {
        jobTitle: 'Reporter',
        position: 'The News',
        description: 'We are looking for...',

        },

        {
        jobTitle: 'Reporter',
        position: 'The News',
        description: 'We are looking for...',
        },

        {
        jobTitle: 'Reporter',
        position: 'The News',
        description: 'We are looking for...',
        },

    ];
    

</script>

<template>
    <main class='container'>
        <section class='top'>
            <div class='left column'>
                <h1 class = 'tagline'>Vacansee</h1>
                <p class = 'tagline'> Making finding soul-sucking jobs a little less naff </p>
                <div class='login-top'>
                    <router-link :to='`/login`' class='login-button-top'>Start Now</router-link>
                </div>
            </div>

            <div class = 'right column'>
                <img src='@/assets/career-center-carousel-p-500.png' alt='man' height=310 />
            </div>
        </section>

        <section class='mid'>
            <h3> Feast your eyes, employment gannets </h3>
            <p style= 'padding:10px 50px 10px 50px;'> Thousands of organisations that we just made up publish advertisements for new vacancies every hour,<br /> so there is something for everyone held by the scruff of the neck by the Student Loans Company </p>
            <div class='cards'>
                <VacancyCard v-for='vacancy in vacancies' :vacancy='vacancy' id= 'cards'/>
            </div>
        </section>

        <section class='bottom'>
            <h3> Feeling a little boujie? </h3>
            <p style= 'padding:0px 50px 10px 50px;'> We provide employers with tools that allow them to post vacancies and to review and contact applicants. </p>
            <div class='login'>
                <router-link :to='`/login`' class='login-button'>Start Now</router-link>
            </div>
        </section>

    </main>

    <Footer></Footer>
</template>

<style scoped>
    @keyframes example {
        0%   {left:0px;}
        25%  {left:-50px;}
        50%  { left:-100px;}
        75%  { left:-150px;}
        100% { left:-200px;}
    }

    .bottom{
        padding: 20px;
        height: 20vh;
        background-color: #08415c;
        color: white;

    }

    .cards {
        display: flex;
        justify-content: space-evenly;
        margin-bottom: 20px;
        position: relative;
        animation-name: example;
        animation-duration: 4s;
        animation-iteration-count: infinite;
        animation-delay: 2s;
    }

    .login {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .login-button {
        width: 10vw;
        height: 3vh;
        border: 0;
        border-radius: 5px;
        background-color: white;
        color: var(--blue);
        text-decoration: none;
        line-height: 3vh;
    }

    .login-button:active .login-button:focus .login-button:hover {
        color: var(--blue-focus);
    }

    .login-button-top {
        width: 10vw;
        height: 3vh;
        border: 0;
        border-radius: 5px;
        background-color: var(--red);
        color: white;
        text-decoration: none;
        line-height: 3vh;
    }

    .login-button-top:active .login-button-top:hover .login-button-top:focus {
        background-color: var(--red-focus);
    }

    .login-top {
        display: flex;
        flex-direction: column;
        align-items: left;
        padding: 0px 120px 0px 120px;
        text-align: center;
    }

    .left{
        background-color: white;
        float:left;
        width:40%;
        height: 300px;
        padding: 10px;

    }


    .mid{
        padding: 50px;
        background-color: #333;
        color: white;
        height: 40vh;
    }

    .right{
        background-color: #cc2936;
        float:right;
        width:50%;
        height: 300px;
        padding:10px;
    }

    

    .tagline{
        font-size: 24px;
        padding: 0px 120px 0px 120px;
        text-align: left;
    }

    .top{
        color: black;
    }


    .top:after {
        content: "";
        display: table;
        clear: both;
    }

</style>
