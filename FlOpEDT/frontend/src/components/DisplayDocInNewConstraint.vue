<template>
    <TriggeredTeleporter
            to=".modal-content"
            :disable="DESACTIVATE_TELEPORTS"
            :listeningTarget="listeningTarget"
            eventName="contextmenu">
        <p>Soon here the documentation's place</p>
    </TriggeredTeleporter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TriggeredTeleporter from '@/components/controler/TriggeredTeleporter.vue'



const DESACTIVATE_TELEPORTS = ref(false)

/*
================================ ADAPTATER ================================ 
*/
const listeningTarget = document.getElementById('nav-new-constraint') as EventTarget

</script>

<style scoped>
.buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: larger;
}

.plusButton {
    width: 100%;
    height: 30px;
    border-radius: 20px;
    border: none;
    background-color: green;
}

.plusButton:hover {
    background-color: darkgreen;
}

.minusButton {
    width: 100%;
    height: 30px;
    border-radius: 20px;
    border: none;
    background-color: firebrick;
}

.minusButton:hover {
    background-color: darkred;
}

.scrollbar {
    max-height: 70vh;
    overflow-y: scroll;
}

.scrollbar-primary::-webkit-scrollbar {
    width: 12px;
}

.scrollbar-primary::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background-color: dodgerblue;
}
.scrollbar-primary::-webkit-scrollbar-thumb:hover {
    border-radius: 4px;
    background-color: royalblue;
}

.scrollbar-primary {
    scrollbar-color: #aaaaaa #f5f5f5;
}
</style>
