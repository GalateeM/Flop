/* eslint-disable */ 
<template>
    <TriggeredTeleporter to='.popover-body' :disable="DESACTIVATE_TELEPORTS" :target="teleportTarget"
        eventName="contextmenu">
        <div></div>
    </TriggeredTeleporter>
</template>

<script setup lang="ts">
import { ref, Teleport } from 'vue';
import TriggeredTeleporter from '@/components/TriggeredTeleporter.vue';

const DESACTIVATE_TELEPORTS = ref(false);
let teleportTarget = document.getElementById('constraints-body')
</script>
    
<style scoped>

</style>