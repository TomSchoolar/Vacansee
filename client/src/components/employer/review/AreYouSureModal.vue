<script setup>
    const { profile = {} } = defineProps(['profile']);
    const emit = defineEmits(['unmatch', 'close-modal'])

    const unmatched = () => {
        emit('close-modal');
        emit('unmatch');
    };
</script>

<template>
  <div class='modal-overlay'>
    <div class='modal'>
      <img class='warning' src='../../../assets/AreYouSureImage.png' alt='' />
      <p class='description'>You are about to unmatch with</p>
      <p class='name'>{{profile.FirstName}} {{profile.LastName}}</p>
      <p class='description'>Are you sure you want to do this?</p>
      <button class='application-button application-button-grey' @click="emit('close-modal')">Go Back</button>
      <button class='application-button application-button-red' @click="unmatched">Unmatch</button>
    </div>
  </div>
</template>

<style scoped>

.warning {
  width: 150px;
}

.description p {
    height: 50px;
    padding-top: 5px;
    padding-bottom: 5px;
}

.name { 
    font-weight: bold;
    font-size: 18px;
    margin: 0px;
    padding: 0px 0px 0px 0px;
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
    margin-left: 10px;
    margin-right: 10px;
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


.modal-overlay {
  position: absolute;
  z-index: 10;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  background-color: #000000da;
}

.modal {
  text-align: center;
  background-color: white;
  height: 380px;
  width: 400px;
  margin-top: 5%;
  padding: 20px 0;
  border-radius: 20px;
}

button {
  background-color: #ac003e;
  width: 150px;
  height: 40px;
  color: white;
  font-size: 14px;
  border-radius: 16px;
  margin-top: 50px;
}
</style>