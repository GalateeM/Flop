<template>
    <input type="file" @change="handleFileUpload" />
    <template v-if="doc">
        <div>
            <MarkdownDisplayer :doc="doc"/>
        </div>
    </template>
</template>

<script setup lang="ts">
import type { Constraint } from '@/models/Constraint'
import { MarkdownParser } from '@/models/MardownParser'
import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'

import MarkdownDisplayer from '@/components/MarkdownDisplayer.vue'
import { type Ref, ref } from 'vue'

interface Props {
    constraint: Constraint
}
const props = withDefaults(defineProps<Props>(), {})



const doc: Ref<MarkdownDocumentation | null> = ref(null)
const p = new MarkdownParser()

// MOCKER
const f: Ref<File | null> = ref(null)
async function handleFileUpload(event: Event) {
    const inputElem = event.target as HTMLInputElement
    if (inputElem.files) {
        f.value = inputElem.files.item(0) as File
        await p.parse(f.value,props.constraint).then((response) => (doc.value = response))
    }
}
</script>

<style scoped></style>
