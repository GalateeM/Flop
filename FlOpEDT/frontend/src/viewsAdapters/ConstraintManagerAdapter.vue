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
interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
    currentPopoverFound:boolean
    selectedConstraint:Constraint | null
    listeningTarget:EventTarget
}
const props = withDefaults(defineProps<Props>(), {})

const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()
/**
 * Swap showDoc value
 */
 function swap() {
    emit('updateShowDoc', props.showDoc)
}

</script>