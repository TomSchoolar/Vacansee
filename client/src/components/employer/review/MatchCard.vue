<script setup>
    const { stats } = defineProps(['stats']);
    const { application = {}, profile = {} } = stats;

    const downloadApplication = () => {
        alert('download application');
    };

    const unmatch = () => {
        alert('unmatch');
    };

    const showApplication = () => {
        alert('showing application');
    };

    
</script>


<template>
    <article class='application'>
        <div class='application-left'>
            <div class='title'>
                <span class='name'>
                    {{ profile.FirstName }} {{ profile.LastName }}
                </span> 
                <span class='pronouns' v-if='profile.Pronouns'>
                    ({{ profile.Pronouns }}) 
                </span>
            </div>
            <div class='contact'>
                <i class="fa-solid fa-phone"></i>
                {{ profile.PhoneNumber }}  
            </div>
            <div class='contact'>
                <i class="fa-solid fa-envelope-open"></i>
                {{ profile.Email }}  
            </div>
            <div class='contact'>
                <i class="fa-solid fa-clock"></i>
                GMT {{ profile.TimeZone }}
            </div>
        </div>

        <div class='application-right'>
            <button class='application-button application-button-grey' @click='showApplication' id='show'>Show Application</button>
            <button class='application-button application-button-grey' @click='downloadApplication'>Download Application</button>
            <button class='application-button application-button-red' @click='unmatch'>Unmatch</button>
        </div>
    </article>
    <hr class='slim-hr' />
</template>


<style scoped>
    .application {
        display: flex;
        justify-content: space-between;
        padding: 8px 12px;
        height: 100px;
    }

    .application-button {
        font-weight: 500; /* required for some reason */
        border-radius: 7px;
        color: #fff;
        border: 2.2px solid #333;
        min-width: 150px;
        font-size: 12px;
        text-decoration: none;
        padding: 2px 4px;
        font-family: Poppins, Avenir, Helvetica, Arial, sans-serif;
    }

    .application-button-grey {
        background: var(--slate);
    }

    .application-button-grey:hover, .application-button-grey:focus, .application-button-grey:active {
        background: var(--slate-focus);
        cursor: pointer;
    } 

    .application-button-red {
        background: var(--red);
    }

    .application-button-red:hover, .application-button-red:focus, .application-button-red:active {
        background: var(--red-focus);
        cursor: pointer;
    } 

    .application-left {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: flex-start;
    }

    .application-right {
        display: flex;
        flex-direction: column;
        height: calc(100% - 4px);
        justify-content: space-between;
        padding: 2px 0;
    }

    .contact {
        font-size: 14px;
    }

    .contact i {
        margin-right: 5px;
    }

    .name {
        font-size: 18px;
    }

    .slim-hr {
        margin: 1px 0;
    }
</style>