/* eslint-disable */ 
<template>
    <template v-if="anchorFound || disable">
        <Teleport :to='to' :disabled="disable" :key="key">
            <slot></slot>
        </Teleport>
    </template>
</template>

<script setup lang="ts">
import { ref, Teleport, computed } from 'vue';

interface Props {
    to: string, //Element ID where append the template in the slot
    /**
     * When `true`, the content will remain in its original
     * location instead of moved into the target container.
     * Can be changed dynamically.
     * Else will try to teleport. If no anchor point is found nothing is displayed
     */
    disable?: Boolean, 
    target: EventTarget, //From which element should we catch the event
    eventName: string //The event name to catch
}
const { to, disable = false, target, eventName } = defineProps<Props>()

//Ref to track if the anchor point is found
const anchorFound = ref(false);
//A mechanism to force reload
const key = ref(0);
//Force the component to rerender by updating a ref
const forceRender = () => key.value++
//Attach the listener a force a teleportation when the event is catched
if (!disable)
    target.addEventListener(eventName, (e) => {
        anchorFound.value = true
        forceRender()
    }, false);

</script>
    
<style scoped>

</style>