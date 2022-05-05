<script setup>
    import { watch, onMounted } from 'vue';

    const props = defineProps(['stepNum']);

    let oldStep = props.stepNum;

    onMounted(() => {
        let circles = document.querySelectorAll('.circle');
        circles.forEach((circle) => circle.classList.remove('circle-colour'));

        let line = document.querySelector('.line-colour');
        line.style.width = 0;
    })

    watch(props, (props) => {
        let { stepNum: newStep } = props;
        let newWidth = (newStep - 1) * 20 + 10;
        newWidth = Math.min(Math.max(newWidth, 0), 100);
        let line = document.querySelector('.line-colour');
        line.style.width = `${ newWidth }%`;

        let i;

        if(newStep > oldStep)
            i = oldStep;
        else
            i = oldStep - 1;

        let circle = document.querySelectorAll('.circle')[i];
        circle.classList.toggle('circle-colour');

        oldStep = props.stepNum;
    });
</script>

<template>
    <nav class='form-stepper'>
        <div class='line'>
            <div class='line-background'></div>
            <div class='line-colour'></div>
        </div>
        
        <div class='form-page'>
            <div class='circle'>
                <i class='fa-solid fa-check'></i>
            </div>
            <div class='label'>
                Basic Details
            </div>
        </div>
        
        <div class='spacer'></div>
        
        <div class='form-page'>
            <div class='circle'>
                <i class='fa-solid fa-check'></i>
            </div>
            <div class='label'>
                More Details
            </div>
        </div>
        
        <div class='spacer'></div>
        
        <div class='form-page'>
            <div class='circle'>
                <i class='fa-solid fa-check'></i>
            </div>
            <div class='label'>
                Contact Details
            </div>
        </div>
        
        <div class='spacer'></div>
        
        <div class='form-page'>
            <div class='circle'>
                <i class='fa-solid fa-check'></i>
            </div>
            <div class='label'>
                Logistics
            </div>
        </div>
        
        <div class='spacer'></div>
        
        <div class='form-page'>
            <div class='circle'>
                <i class='fa-solid fa-check'></i>
            </div>
            <div class='label'>
                Tags
            </div>
        </div>
        
        <div class='spacer'></div>
        
        <div class='form-page'>
            <div class='circle'>
                <i class='fa-solid fa-check'></i>
            </div>
            <div class='label'>
                Review
            </div>
        </div>
    </nav>
</template>

<style>
    .form-pane {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>

<style scoped>
    .circle {
        background: var(--accent-grey);
        border-radius: 50%;
        height: 25px;
        width: 25px;
        transition: 0.1s linear 0.05s;
        color: var(--accent-grey);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .circle i {
        position: relative;
        top: 1px;
        right: 0.5px;
    }

    .circle-colour {
        background: var(--green);
        color: white;
    }

    .label {
        bottom: -15px;
        font-size: 12px;
        color: var(--jet);
        white-space: nowrap;
        margin-top: 2px;
    }

    .line {
        width: calc(100% - 94px);
        position: absolute;
        top: 12.5px;
    }

    .line-background {
        width: 100%;
        z-index: -2;
        position: relative;
        border-top: 2px solid var(--accent-grey);
    }

    .line-colour {
        width: 0%;
        z-index: -1;
        position: absolute;
        bottom: 0.5px;
        border-top: 2px solid var(--green);
        transition: 0.15s ease-in-out;
    }

    .form-page {
        display: flex;
        align-items: center;
        flex-direction: column;
        width: 94px;
    }

    .form-stepper {
        display: flex;
        width: 40%;
        min-width: 600px;
        margin: 20px auto;
        justify-content: center;
        align-items: center;
        position: relative;
    }

    .spacer {
        flex-grow: 1;
        height: 0;
    }
</style>
