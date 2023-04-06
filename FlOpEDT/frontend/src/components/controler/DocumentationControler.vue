<template>
    <div class="container">
        <template v-if="isQuerying">
            <p>Loading the documentation</p>
        </template>
        <template v-else>
            <template v-if="isResolved">
                <div>
                    <template v-if="doc">
                        <Suspense>
                            <MarkdownDisplayer :doc="doc" :constraint="constraint" />
                            <template #fallback> Loading data</template>
                        </Suspense>
                    </template>
                </div>
            </template>
            <template v-else>
                <div class="docNotFoundContainer">
                    <b class="text">Cannot found documentation</b>
                </div>
            </template>
        </template>
    </div>
</template>

<script setup lang="ts">
import type { Constraint } from '@/models/Constraint'
import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'
import { queryDoc } from '@/composables/API_documentation'
import MarkdownDisplayer from '@/components/controler/MarkdownDisplayer.vue'
import { type Ref, ref, inject, watch } from 'vue'

interface Props {
    constraint: Constraint
}
const props = withDefaults(defineProps<Props>(), {})

const lang = inject('lang') as string


const doc: Ref<MarkdownDocumentation | null> = ref(null)
const isResolved = ref(false)
const isQuerying = ref(false)
queryDocu()
watch(
    () => props.constraint,
    (nV, oV) => { if (nV != oV) queryDocu() }
)


async function queryDocu() {
    isQuerying.value = true
    isResolved.value = false
    await queryDoc(props.constraint.className, lang)
        .then(res => {
            isResolved.value = true
            doc.value = res as MarkdownDocumentation
        })
        .catch(error => console.log(error))
        .finally(() => isQuerying.value = false)
}

</script>

<style scoped>
.container {
    display: table;
    width: 100%;
}

.docNotFoundContainer {
    display: table-cell;
    vertical-align: middle;
    text-align: center;
    height: 10vh;
}

.text {
    color: firebrick;
    font-size: large;
}
</style>
