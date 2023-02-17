<template>
    <div>
        <VueShowdown
            :markdown="doc.textContent"
            :vue-template="true"
            :vue-template-data="{
                courseTypes,
                department,
                groups,
                modules,
                trainProgs,
                tutors,
                weeks,
            }"
        />
    </div>
</template>

<script setup lang="ts">
import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'
import { VueShowdown } from 'vue-showdown'

import { useCourseTypeStore } from '@/stores/courseType'
import { useDepartmentStore } from '@/stores/departmentRework'
import { useGroupStore } from '@/stores/group'
import { useModuleStore } from '@/stores/module'
import { useTrainProgStore } from '@/stores/trainProg'
import { useTutorStore } from '@/stores/tutor'
import { useWeekStore } from '@/stores/week'

interface Props {
    /**
     * Documentation to render
     */
    doc: MarkdownDocumentation
}
const props = withDefaults(defineProps<Props>(), {})

/**
 * courseType map in the associated store
 */
const courseTypes = useCourseTypeStore().items

/**
 * department map in the associated store
 */
const department = useDepartmentStore().items

/**
 * group map in the associated store
 */
const groups = useGroupStore().items

/**
 * module map in the associated store
 */
const modules = useModuleStore().items

/**
 * train program map in the associated store
 */
const trainProgs = useTrainProgStore().items

/**
 * tutor map in the associated store
 */
const tutors = useTutorStore().items

/**
 * week map in the associated store
 */
const weeks = useWeekStore().items

</script>

<style scoped></style>
