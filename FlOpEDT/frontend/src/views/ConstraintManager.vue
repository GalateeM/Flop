<template>
    <template v-if="currentPopoverFound">
        <DisplayDocInPopover
            :selectedConstraint="selectedConstraint"
            :listeningTarget="listeningTarget"
            :showDoc="showDoc" 
            @updateShowDoc="swap"
        ></DisplayDocInPopover>
    </template>
    <Suspense>
        <DisplayDocInNewConstraint :showDoc="showDoc" @updateShowDoc="swap"></DisplayDocInNewConstraint>
    </Suspense>

</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'

import DisplayDocInPopover from '@/components/DisplayDocInPopover.vue'
import DisplayDocInNewConstraint from '@/components/DisplayDocInNewConstraint.vue'
import { useConstraintStore } from '@/stores/constraint'
import type { Constraint } from '@/models/Constraint'

const showDoc = ref(false)

const constraintStore = useConstraintStore()
constraintStore.initialize().then(() => {
    if (currentPopoverFound.value == true) {
        const currentPopover = window.eval('currentPopover')
        if (currentPopover) {
            currentPopoverFound.value = true
            const cst = currentPopover._element.getAttribute('data-cst-id') as string
            const cstIDRegex = new RegExp('^\\D+\\d+$')
            const match = cst.match(cstIDRegex)
            if (match) {
                if (match[0]) {
                    const constraint = constraintStore.items.get(match[0])
                    if (constraint) {
                        if (constraint) {
                            selectedConstraint.value = constraint
                        }
                    }
                }
            }
        }
    }
})

const selectedConstraint: Ref<Constraint | null> = ref(null)

/*
================================ ADAPTATER ================================ 
*/
const listeningTarget = document.getElementById('constraints-body') as EventTarget
const POPOVER_EVENT_NAME = 'contextmenu'
const constraintsBodyFound = listeningTarget != null
if (!constraintsBodyFound) throw new Error('constraints-body element not found')
const currentPopoverFound = ref(false)

listeningTarget.addEventListener(
    POPOVER_EVENT_NAME,
    (e) => {
        const currentPopover = window.eval('currentPopover')
        if (currentPopover) {
            currentPopoverFound.value = true
            const cst = currentPopover._element.getAttribute('data-cst-id') as string
            const cstIDRegex = new RegExp('^\\D+\\d+$')
            const match = cst.match(cstIDRegex)
            if (match) {
                if (match[0]) {
                    const constraint = constraintStore.items.get(match[0])
                    if (constraint) {
                        if (constraint) selectedConstraint.value = constraint
                    }
                }
            }
        }
    },
    false
)

function swap() {
    showDoc.value = !showDoc.value
}

document.addEventListener('click', (e) => {
    const currentPopover = window.eval('currentPopover')

    if (!currentPopover) {
        selectedConstraint.value = null
        currentPopoverFound.value = false
    }
})

</script>
