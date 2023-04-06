<template>
        <Teleport to=".modal-content" :disable="DESACTIVATE_TELEPORTS">
            <DisplayDocInNewConstraint :showDoc="showDoc" :constraint="constraint" @updateShowDoc="swap"></DisplayDocInNewConstraint>
        </Teleport>
</template>

<script setup lang="ts">
import DisplayDocInNewConstraint from '@/components/view/DisplayDocInNewConstraint.vue'
import { loadConstraintClass } from '@/composables/API_Constraint';
import { Constraint } from '@/models/Constraint';
import type { ConstraintClass } from '@/models/ConstraintClass';
import { ref, type Ref } from 'vue'
interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
}
const DESACTIVATE_TELEPORTS = ref(false)
const constraint: Ref<Constraint | null> = ref(null)
const props = withDefaults(defineProps<Props>(), {})
const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()
/**
 * Map of all constraint classes
 */
 let cstClasses = new Map<string, ConstraintClass>()
 /**
 * Select field to choose the constraint class
 */
 const constraintEditTypeField = document.getElementById('constraint-edit-type') as HTMLInputElement

/**
 * Swap showDoc value
 */
 function swap() {
    increaseSizeOfModal(props.showDoc)//Adapter
    emit('updateShowDoc', props.showDoc)
}

await loadConstraintClass().then(function (response) {
        cstClasses = response
})

//Listen when the user select a new constraint to rerender the documentation displayer
constraintEditTypeField?.addEventListener('change', () => {
    const cstClass = Array.from(cstClasses.values()).find((e) => constraintEditTypeField.value == e.local_name)
    if (cstClass) {
        constraint.value = new Constraint(0, '', cstClass.className, 0, true, '', '', new Map())
    } else {
        constraint.value = null
    }
})

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
 * modify the modal window's DOM to make the teleported component clickable
 * only called Once
 *
 */
function modifyDisplay() {
    const modal = document.getElementsByClassName('modal-content').item(0) as HTMLElement
    modal.style.flexDirection = 'row'
    const header = document.getElementsByClassName('modal-header').item(0) as HTMLElement
    const body = document.getElementsByClassName('modal-body').item(0) as HTMLElement
    const footer = document.getElementsByClassName('modal-footer').item(0) as HTMLElement
    footer.style.flex = "1"
    if (header) {
        modal.removeChild(header)
    }
    if (body) {
        modal.removeChild(body)
    }
    if (footer) {
        modal.removeChild(footer)
    }
    const oldDiv = document.createElement('div')
    oldDiv.style.flexDirection = "column"
    oldDiv.style.display = "flex"
    oldDiv.appendChild(header)
    oldDiv.appendChild(body)
    oldDiv.appendChild(footer)
    modal.appendChild(oldDiv)
}

/**
 * Add an EventListener on the Cancel button of the popover
 * Permit to reset the current doc's constraint
 * @param constraint 
 */
function addEventListenerToCancelButton(constraint:Ref<Constraint | null>){
    /**
     * Cancel button of the popover
     */
    const cancelEditBtn = document.getElementById('cancel-edit-constraint') as HTMLInputElement
    //Set the selectedConstraint to null when user leave the popover
    cancelEditBtn?.addEventListener('click', () => {
        constraint.value = null
    })
}

/*
================================ ADAPTATER ================================ 
*/
modifyDisplay()
addEventListenerToCancelButton(constraint)

</script>
