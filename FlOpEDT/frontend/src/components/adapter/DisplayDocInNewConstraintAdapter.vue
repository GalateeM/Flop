<template>
    <Teleport to=".modal-content">
        <div class="documentationContainer">
            <DocDisplayerControler :constraint="constraint" :showDoc="showDoc" @updateShowDoc="swap" hideLabel="⬅"
                showLabel="➡" />
        </div>
    </Teleport>
</template>

<script setup lang="ts">
import DocDisplayerControler from '@/components/controler/DocDisplayerControler.vue';
import { loadConstraintClass } from '@/composables/API_Constraint';
import { Constraint } from '@/models/Constraint';
import type { ConstraintClass } from '@/models/ConstraintClass';
import { ref, watch, type Ref } from 'vue'
/** =========================================================================================
 *  In charge to : 
 *      - Alter the existing page by redifining CSS 
 *      - Adding new content by teleporting it to the right place
 *      - Load the constraint classes
 *      - Prepare the constraint under building
 */

/**
 * Properties declaration interface of the component
 */
interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
}
const props = withDefaults(defineProps<Props>(), {})

/**
 * Events emits by the component
 */
const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()

const MODAL_CLASSES = `modal-dialog modal-dialog-centered modal-dialog-scrollable`
const MODAL_XL_CLASSES = `${MODAL_CLASSES} modal-xl`

/**
 * Dummy constraint needed to use the markdown displayer
 */
const constraint: Ref<Constraint | null> = ref(null)

/**
 * Map of all constraint classes
 * Could be used to initialize the parameters map of the new constraint
 */
let cstClasses = new Map<string, ConstraintClass>()

/**
* Select field to choose the constraint class
*/
const constraintEditTypeField = document.getElementById('constraint-edit-type') as HTMLInputElement

/**
 * The modal containing the form to create a constraint
 */
const modalElement = document.getElementById('constraint-edit-popup') as HTMLElement

/**
 * Swap showDoc value
 */
function swap() {
    emit('updateShowDoc', props.showDoc)
}

/**
 * Change the width of the modal's window when documentation is displayed or not
 * @param showDoc 
 */
function setModalSize(showDoc: boolean) {
    const modal = document.getElementsByClassName('modal-dialog').item(0) as HTMLElement
    if (showDoc)
        modal.className = MODAL_XL_CLASSES
    else
        modal.className = MODAL_CLASSES
}

/**
 * modify the modal window's DOM to make the teleported component clickable
 * only called Once
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
 * find the constraint based on the selected constraint in the field.
 * Set to null if no match is found
 */
function setConstraint() {
    const cstClass = Array.from(cstClasses.values()).find((e) => constraintEditTypeField.value == e.local_name)
    if (cstClass) {
        const paramMap = new Map<string, null>()
        cstClass.parameters.forEach(p => paramMap.set(p.name, null))
        constraint.value = new Constraint(0, '', cstClass.className, 0, true, '', '', paramMap)
    } else {
        constraint.value = null
    }
}

/**
 * Reload the constraint when the user select a constraint
 */
constraintEditTypeField?.addEventListener('change', () => {
    setConstraint()
})

await loadConstraintClass().then(function (response) {
    cstClasses = response
})
modifyDisplay()

/**
 * Change the modal size on change of the showDoc props
 */
watch(
    () => props.showDoc,
    () => { setModalSize(props.showDoc) }
)

/**
 * Observer on the modal that reset the constraint when the modal is hidden
 * and change the constraint when it is opened
 */
new MutationObserver((mutationList: any[], observer: any) =>
    mutationList.forEach((mutation: { type: string; attributeName: string; }) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
            if (!modalElement.classList.contains('show'))
                constraint.value = null
            else
                setConstraint()
        }
    })).observe(modalElement, {
        attributes: true
    })
</script>


<style scoped>
* :deep() .buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: larger;
}

* :deep() .plusButton {
    width: 100%;
    height: 100%;
    border: none;
    background-color: green;
}

* :deep() .plusButton:hover {
    background-color: darkgreen;
}

* :deep() .minusButton {
    width: 100%;
    height: 100%;
    border: none;
    background-color: firebrick;
}

* :deep() .minusButton:hover {
    background-color: darkred;
}

.documentationContainer {
    display: flex;
    flex: 1;
}

* :deep() .scrollbar {
    max-height: 70vh;
    overflow-y: scroll;
    flex: 1;
}

* :deep() .scrollbar-primary::-webkit-scrollbar {
    width: 12px;
}

* :deep() .scrollbar-primary::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background-color: dodgerblue;
}

* :deep() .scrollbar-primary::-webkit-scrollbar-thumb:hover {
    border-radius: 4px;
    background-color: royalblue;
}

* :deep() .scrollbar-primary {
    scrollbar-color: #aaaaaa #f5f5f5;
}
</style>
