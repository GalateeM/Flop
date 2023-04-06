<template>
    <Teleport to=".popover-body" :disable="DESACTIVATE_TELEPORTS" :key="key"><!-- KEY = ADAPTER-->
        <DisplayDocInPopover
            :selectedConstraint="selectedConstraint"
            :showDoc="showDoc" 
            @updateShowDoc="swap"
        ></DisplayDocInPopover>
    </Teleport>
</template>


<script setup lang="ts">
import DisplayDocInPopover from '@/components/DisplayDocInPopover.vue'
import type { Constraint } from "@/models/Constraint";
import { ref, type Ref } from "vue";

interface Props{
    listeningTarget: EventTarget
    selectedConstraint: Constraint | null
    showDoc: boolean
    /**
     * Popover max width
     */
    popoverMaxWidth: string
}

const props = withDefaults(defineProps<Props>(), {})
const key = ref(0)
const DESACTIVATE_TELEPORTS = ref(false)
const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()

/**
 * Enlarge the width of the parent popover & center the bottons Duplicate/Modify/Delete
 */
function enlargePopover() {
    const popover = document.getElementsByClassName('popover').item(0) as HTMLElement
    if (popover !== null) {
        popover.style.maxWidth = props.popoverMaxWidth
        window.scroll(popover.getBoundingClientRect().right, 0)
    }
    const groupeOfButton = document.getElementsByClassName('btn-group').item(0) as HTMLElement
    if (groupeOfButton !== null) {
        groupeOfButton.style.alignItems='center';
        groupeOfButton.style.justifyContent='center';
        groupeOfButton.style.display = 'flex'
    }
}
function forceTeleport(key:Ref<number>){
    key.value++;
    enlargePopover()
}
/**
 * Permit to force the teleportation when the target is changing
 * @param key 
 * @param target 
 */
function addEventListenerForForceTeleport(key:Ref<number>,target:EventTarget){
    const eventName = 'contextmenu'
    target.addEventListener(eventName, (e) => forceTeleport(key), false)
}
/**
 * Swap showDoc value
 */
function swap() {
    emit('updateShowDoc', props.showDoc)
}
//Force the component to rerender by updating a ref
addEventListenerForForceTeleport(key,props.listeningTarget);
enlargePopover()
</script>