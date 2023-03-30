<template>
    <template v-if="currentPopoverFound">
        <DisplayDocInPopoverAdapter :selectedConstraint="selectedConstraint" :listeningTarget="listeningTarget"
            :showDoc="showDoc" @updateShowDoc="swap"></DisplayDocInPopoverAdapter>
    </template>
    <Suspense>
        <DisplayDocInNewConstraintAdpater :showDoc="showDoc" @updateShowDoc="swap"></DisplayDocInNewConstraintAdpater>
    </Suspense>
</template>

<script setup lang="ts">
import DisplayDocInPopoverAdapter from '@/viewsAdapters/DisplayDocInPopoverAdapter.vue'
import DisplayDocInNewConstraintAdpater from '@/viewsAdapters/DisplayDocInNewConstraintAdpater.vue'
import type { Constraint } from '@/models/Constraint';
import { ref, type Ref } from 'vue';
import { useConstraintStore } from '@/stores/constraint';
interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
    
}
const props = withDefaults(defineProps<Props>(), {})

const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()
const selectedConstraint: Ref<Constraint | null> = ref(null)

const POPOVER_EVENT_NAME = 'contextmenu'
const constraintStore = useConstraintStore()
constraintStore.initialize().then(() => {afterInitializingConstraintStore()})

/**
 * Function called just after the initialisation of the store
 * This function set the selected constraint
 */
function afterInitializingConstraintStore(){
    if (currentPopoverFound.value == true) {
       setCurrentConstraint()
    }
}

/**
 * Swap showDoc value
 */
function swap() {
    increaseSizeOfModal(props.showDoc);
    emit('updateShowDoc', props.showDoc)
}

/**
 * Increase the width of the modal's window when documentation is displayed or not
 * @param showDoc 
 */
 function increaseSizeOfModal(showDoc:boolean) {
    const modal = document.getElementsByClassName('modal-dialog').item(0) as HTMLElement
    if (showDoc) {
        modal.className = 'modal-dialog modal-dialog-centered modal-dialog-scrollable'
    } else {
        modal.className = 'modal-dialog modal-dialog-centered modal-dialog-scrollable modal-xl'
    }
}

/**
 * Change the value of the selected constraint thanks to the string parameter "constraint"
 * @param contraint 
 */
 function matchConstraint(contraint:string){
    const cstIDRegex = new RegExp('^\\D+\\d+$')
    const match = contraint.match(cstIDRegex)
    if (match) {
        if (match[0]) {
            const constraint = constraintStore.items.get(match[0])
            if (constraint) {
                if (constraint) selectedConstraint.value = constraint
            }
        }
    }
}

function selectConstraintFromPopover(){
    listeningTarget.addEventListener(
        POPOVER_EVENT_NAME,
        (e) => {
            setCurrentConstraint()
        },
        false
    )
}

function setCurrentConstraint(){
    const currentPopover = window.eval('currentPopover')
    if (currentPopover) {
        currentPopoverFound.value = true
        const cst = currentPopover._element.getAttribute('data-cst-id') as string
        matchConstraint(cst)
    }
}

const listeningTarget = document.getElementById('constraints-body') as EventTarget
const currentPopoverFound = ref(false)

selectConstraintFromPopover()

</script>