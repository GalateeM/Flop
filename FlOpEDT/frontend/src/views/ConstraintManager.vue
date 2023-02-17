<template>
    <template v-if="selectedConstraint">
        <DisplayDocInPopover :selectedConstraint="selectedConstraint" :listeningTarget="listeningTarget"></DisplayDocInPopover>
    </template>
    <DisplayDocInNewConstraint></DisplayDocInNewConstraint>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'

import DisplayDocInPopover from  '@/components/DisplayDocInPopover.vue'
import DisplayDocInNewConstraint from  '@/components/DisplayDocInNewConstraint.vue'
import { useConstraintStore } from '@/stores/constraint'
import type { Constraint } from '@/models/Constraint'

const constraintStore = useConstraintStore()

const selectedConstraint: Ref<Constraint | null> = ref(null)

/*
================================ ADAPTATER ================================ 
*/
const listeningTarget = document.getElementById('constraints-body') as EventTarget
const POPOVER_EVENT_NAME = 'contextmenu'
const constraintsBodyFound = listeningTarget != null
if (!constraintsBodyFound) throw new Error('constraints-body element not found')

listeningTarget.addEventListener(
    POPOVER_EVENT_NAME,
    (e) => {
        const currentPopover = window.eval('currentPopover')
        if (currentPopover) {
            const cst = currentPopover._element.getAttribute('data-cst-id') as string
            const cstIDRegex = new RegExp('^(?<class>\\D+)(?<id>\\d+)$')
            const matches = cst.match(cstIDRegex)
            if (matches)
                if (matches.groups) {
                    const cClass = constraintStore.constraints.get(matches.groups.class)
                    if (cClass) {
                        const constraint = cClass.get(Number(matches.groups.id))
                        if (constraint) selectedConstraint.value = constraint
                    }
                }
        }
    },
    false
)

document.addEventListener('click', (e) => {
    const currentPopover = window.eval('currentPopover')
    if (!currentPopover) selectedConstraint.value = null
})
</script>