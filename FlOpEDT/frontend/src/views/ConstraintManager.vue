<template>
    <template v-if="constraintsBodyFound">
        <TriggeredTeleporter
            to=".popover-body"
            :disable="DESACTIVATE_TELEPORTS"
            :listeningTarget="listeningTarget"
            eventName="contextmenu"
        >
            <div></div>
        </TriggeredTeleporter>
    </template>
</template> 

<script setup lang="ts">
import { ref } from 'vue'
import TriggeredTeleporter from '@/components/TriggeredTeleporter.vue'

const DESACTIVATE_TELEPORTS = ref(false)
const listeningTarget = document.getElementById('constraints-body') as EventTarget
const constraintsBodyFound = listeningTarget != null
if (!constraintsBodyFound) throw new Error('constraints-body element not found')
</script>

<style scoped></style>
