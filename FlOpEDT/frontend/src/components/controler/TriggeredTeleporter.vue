<template>
    <Teleport :to="to" :disabled="disable" :key="key">
        <slot></slot>
    </Teleport>
</template>

<script setup lang="ts">
import { ref, Teleport } from 'vue'

interface Props {
    /**
     * Element ID where append the template in the slot
     */
    to: string
    /**
     * When `true`, the content will remain in its original
     * location instead of moving into the target container.
     */
    disable?: boolean
    /**
     * From which element should we catch the event
     */
    listeningTarget: EventTarget
    /**
     * The event name to catch
     */
    eventName: string
}
const props = withDefaults(defineProps<Props>(), {
    disable: false,
})
//A mechanism to force reload
const key = ref(0)
//Force the component to rerender by updating a ref
const forceRender = () => key.value++
//Rerender (so reteleport) when the event is catched
if (!props.disable) props.listeningTarget.addEventListener(props.eventName, (e) => forceRender(), false)
</script>

<style scoped></style>
