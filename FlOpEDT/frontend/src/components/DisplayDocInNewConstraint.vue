<template>
    <Teleport to=".docDisplayer" :disable="DESACTIVATE_TELEPORTS">
        <div class="documentationContainer">
            <div class="buttonContainer">
                <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap">
                    {{ showDoc ? '⬅' : '➡' }}
                </button>
            </div>
            <template v-if="showDoc">
                <div class="scrollbar scrollbar-primary">
                    <template v-if="isLoaded">
                        <template v-if="constraint">
                            <DocumentationControler :constraint="constraint" />
                        </template>
                    </template>
                </div>
            </template>
        </div>
    </Teleport>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'
import DocumentationControler from '@/components/controler/DocumentationControler.vue'
import type { ConstraintClass } from '@/models/ConstraintClass'
import {loadConstraintClass} from "@/composables/API_constraint"
import { Constraint } from '@/models/Constraint'

interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
}
const props = withDefaults(defineProps<Props>(), {})

/**
 * Swap showDoc value
 */
function swap() {
    increaseSizeOfModal()
    emit('updateShowDoc', props.showDoc)
}

const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()

const DESACTIVATE_TELEPORTS = ref(false)

/**
 * doc-show-btn class definer
 * permit to setup the display parameters
 */
const showBtnClassDefiner = () => {
    return props.showDoc ? ' minusButton ' : ' plusButton '
}

/*
================================ ADAPTATER ================================ 

/**
 * Increase the width of the modal's window when documentation is displayed or not
 */
function increaseSizeOfModal() {
    const modal = document.getElementsByClassName('modal-dialog').item(0) as HTMLElement
    if (props.showDoc) {
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
    modal.style['flex-direction'] = 'row'

    const header = document.getElementsByClassName('modal-header').item(0) as HTMLElement
    const body = document.getElementsByClassName('modal-body').item(0) as HTMLElement
    const footer = document.getElementsByClassName('modal-footer').item(0) as HTMLElement
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
    oldDiv.appendChild(header)
    oldDiv.appendChild(body)
    oldDiv.appendChild(footer)
    modal.appendChild(oldDiv)

    const docDisplayer = document.createElement('div')
    docDisplayer.className = 'docDisplayer'
    modal.appendChild(docDisplayer)
}

/**
 * variable which allows the modification of the modal window's DOM only once
 */
const domModified = ref(false)

if (!domModified.value) {
    modifyDisplay()
    domModified.value = true
}

/**
 * Reference to know if the constraint classes map is loaded
 */
const isLoaded = ref(false)
/**
 * Map of all constraint classes
 */
let cstClasses = new Map<string, ConstraintClass>()
//Load all constraint classes et set them in a dedicated map
await loadConstraintClass().then(function (response) {
        cstClasses = response
        isLoaded.value = true
})

const key = ref(0)
const rerenderDocControler = () => key.value++
/**
 * Constraint being created
 */
const constraint: Ref<Constraint | null> = ref(null)
/**
 * Select field to choose the constraint class
 */
const constraintEditTypeField = document.getElementById('constraint-edit-type') as HTMLInputElement
//Listen when the user select a new constraint to rerender the documentation displayer
constraintEditTypeField?.addEventListener('change', () => {
    const cstClass = Array.from(cstClasses.values()).find((e) => constraintEditTypeField.value == e.local_name)
    if (cstClass) {
        constraint.value = new Constraint(0, '', cstClass.className, 0, true, '', '', new Map())
        rerenderDocControler()
    } else {
        constraint.value = null
    }
})

/**
 * Cancel button of the popover
 */
const cancelEditBtn = document.getElementById('cancel-edit-constraint') as HTMLInputElement
//Set the selectedConstraint to null when user leave the popover
cancelEditBtn?.addEventListener('click', () => {
    constraint.value = null
})
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
    height: 100%;
    border: none;
    background-color: green;
}

.plusButton:hover {
    background-color: darkgreen;
}

.minusButton {
    width: 100%;
    height: 100%;
    border: none;
    background-color: firebrick;
}

.minusButton:hover {
    background-color: darkred;
}

.documentationContainer {
    height: 100%;
    display: flex;
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
