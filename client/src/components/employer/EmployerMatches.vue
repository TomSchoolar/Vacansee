<script setup>
    const props = defineProps(['stats']);

    const download = () => {
        alert('download application');
    };

    const unmatch = () => {
        alert('unmatch');
    };

    const show = () => {
        alert('showing application');
    };
</script>

<meta name='viewport' content='width=device-width, initial-scale=1'>
<template>
    <div class='stat-container'>
        <div class='stat-left'>
            <div class='name-pronouns'>
                <p class='name'> {{stats.name}} </p>
                <p class='pronouns'> {{stats.pronouns}} </p>
            </div>
            <p> {{stats.number}} </p>
            <p> {{stats.email}} </p>
            <p> {{stats.timezone}} </p>
        </div>
        <div class='stat-right'>
            <button class='button' @click='show' id='show'>Show Application</button>
            <button class='button' @click='download'>Download Application</button>
            <button class='button unmatch' @click='unmatch'>Unmatch</button>
        </div>
    </div>
</template>

<style scoped>
    .button{
        width: 100%;
        height: 100%;
        background-color: var(--slate);
        border: 2px solid black;
        border-radius: 5px;
        color: white;
        cursor: pointer;
        font-size: 16px;
        margin: 5px;
        text-decoration: none;
        transition-duration: 0.4s;
    }

    .button:active{
        background-color: var(--slate-focus);
        font-size: 70%;
    }

    .button:hover{
        background-color: var(--slate-focus);
    }

    .name {
        font-weight: bold;
        font-size: 20px;
    }

    .name-pronouns {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        gap: 5px;
    }

    .pronouns {
        font-style: italic;
        color: var(--slate);
    }

    .stat-container {
        display: flex;
        flex-direction: row;
    }

    .stat-left {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        flex: 3;
        margin: 10px;
    }

    .stat-left p {
        margin: 3px;
    }

    .stat-right {
        display: flex;
        flex-direction: column;
        flex: 1;
        align-items: center;
        align-content: center;
        justify-content: space-around;
        margin: 10px;
    }

    .unmatch{
        background-color: var(--red);
    }

    .unmatch:hover{
        background-color: var(--red-focus);
    }
</style>