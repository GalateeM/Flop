<template>
    <ConstraintManagerAdapter :showDoc="showDoc" :currentPopoverFound="currentPopoverFound" :selectedConstraint="selectedConstraint" :listeningTarget="listeningTarget" @updateShowDoc="swap"></ConstraintManagerAdapter>

</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'

import { useConstraintStore } from '@/stores/constraint'
import type { Constraint } from '@/models/Constraint'
import { afterInitializingConstraintStoreFromAdapter, getListeningTarget, getPopoverFound, resetSelectedConstraint, selectConstraintFromPopover, updatePopoversByShowingDoc } from '@/viewsAdapters/ConstraintManagerAdapter'
import DisplayDocInPopoverAdapter from '@/viewsAdapters/DisplayDocInPopoverAdapter.vue'
import DisplayDocInNewConstraintAdpater from '@/viewsAdapters/DisplayDocInNewConstraintAdpater.vue'
import ConstraintManagerAdapter from '@/viewsAdapters/ConstraintManagerAdapter.vue'

const selectedConstraint: Ref<Constraint | null> = ref(null)
const showDoc = ref(false)

const constraintStore = useConstraintStore()
constraintStore.initialize().then(() => {afterInitializingConstraintStore()})

/**
 * Function called just after the initialisation of the store
 * This function set the selected constraint
 */
function afterInitializingConstraintStore(){
    afterInitializingConstraintStoreFromAdapter(matchConstraint) //replace by matchConstraint(nameOfTheConstraint) during the vue implementation of FLOP
}

/**
 * this function change the value of the showDoc
 */
function swap() {
    updatePopoversByShowingDoc(showDoc.value);//Adapter
    showDoc.value = !showDoc.value
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

/*
================================ ADAPTATER ================================ 
*/

selectConstraintFromPopover(matchConstraint)
resetSelectedConstraint(selectedConstraint)

const listeningTarget = getListeningTarget()
const currentPopoverFound = getPopoverFound()

</script>
