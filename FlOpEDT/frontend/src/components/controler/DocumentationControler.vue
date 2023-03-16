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
import { MarkdownParser } from '@/models/MardownParser'
import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'

import MarkdownDisplayer from '@/components/view/MarkdownDisplayer.vue'
import { type Ref, ref, inject, watch } from 'vue'

import axios from 'axios'

interface Props {
    constraint: Constraint
}
const props = withDefaults(defineProps<Props>(), {})

const lang = inject('lang')


const doc: Ref<MarkdownDocumentation | null> = ref(null)
const p = new MarkdownParser()
const isResolved = ref(false)
const isQuerying = ref(false)
queryDoc()
watch(
    () => props.constraint,
    (nV, oV) => {if(nV != oV) queryDoc()}
)


async function queryDoc() {
    isQuerying.value = true
    await axios
        .get(`/${lang}/api/ttapp/docu/${props.constraint.className}.md`)
        .then(function (response) {
            isResolved.value = true
            p.parse(response.data, props.constraint).then((response) => (doc.value = response))
        })
        .catch(function (error) {
            isResolved.value = false
        })
        .finally(() => (isQuerying.value = false))
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
