<template>
    <div>
        <VueShowdown :markdown="doc.textContent" />
    </div>
    <template v-if="teleportable">
        <template v-if="constraint">
            <template v-for="CstParType in ConstrParameter.types()" :key="CstParType">
                <template v-if="constraint.parameters.get(CstParType)">
                    <template v-for="i in getNumberOfCallAsArray(CstParType)" :key="i">
                        <Teleport :to="'#' + CstParType + 'Displayer' + i">
                            <ConstraintParameterDisplayer
                                :idList="(constraint.parameters.get(CstParType)?.id_list as unknown[])"
                                :values="storesItems.get(CstParType)"
                            />
                        </Teleport>
                    </template>
                </template>
            </template>
        </template>
    </template>
</template>

<script setup lang="ts">
/**
 * Display a contraint documentation and teleport parameters displayer where the documentation
 * ask it
 */

import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'
import { VueShowdown } from 'vue-showdown'

import { onMounted, ref } from 'vue'

import { useCourseTypeStore } from '@/stores/courseType'
import { useDepartmentStore } from '@/stores/departmentRework'
import { useGroupStore } from '@/stores/group'
import { useModuleStore } from '@/stores/module'
import { useTrainProgStore } from '@/stores/trainProg'
import { useTutorStore } from '@/stores/tutor'
import { useWeekStore } from '@/stores/week'
import type { Constraint } from '@/models/Constraint'

import ConstraintParameterDisplayer from './ConstraintParameterDisplayer.vue'
import { ConstrParameter } from '@/models/ConstrParameter'

interface Props {
    /**
     * Documentation to render
     */
    doc: MarkdownDocumentation
    /**
     * Associated constraint
     * Used to fill call for interpolation in the documentation
     */
    constraint: Constraint
}
const props = withDefaults(defineProps<Props>(), {})

const courseTypeStore = useCourseTypeStore()
const departmentStore = useDepartmentStore()
const groupStore = useGroupStore()
const moduleStore = useModuleStore()
const trainProgStore = useTrainProgStore()
const tutorStore = useTutorStore()
const weekStore = useWeekStore()

/**
 * initialize all constraint parameters stores with Promises
 */
async function initializeStores() {
    const promises = [
        courseTypeStore.initialize(),
        departmentStore.initialize(),
        groupStore.initialize(),
        moduleStore.initialize(),
        trainProgStore.initialize(),
        tutorStore.initialize(),
        weekStore.initialize(),
    ]
    await Promise.all(promises)
}

await initializeStores()
const teleportable = ref(false)
onMounted(() => {
    teleportable.value = true //Allow the teleportation of parameters displayer
})

/**
 * Return an integer array from 1 to the number of call of interpolation in the doc property
 * If the parameter is not called, returns an empty array
 *
 * @param param The constraint parameter to check
 */
function getNumberOfCallAsArray(param: string) {
    const nbCall = props.doc.paramCallCount.get(param) as number
    if (nbCall) return Array.from({ length: nbCall }, (v, k) => k + 1)
    else return []
}

/**
 * Map of the items in the stores, accessible by the parameter name
 */
const storesItems = new Map<string, any>([
    ['course_types', courseTypeStore.items],
    ['department', departmentStore.items],
    ['groups', groupStore.items],
    ['modules', moduleStore.items],
    ['train_progs', trainProgStore.items],
    ['tutors', tutorStore.items],
    ['weeks', weekStore.items],
])
</script>

<style scoped></style>
