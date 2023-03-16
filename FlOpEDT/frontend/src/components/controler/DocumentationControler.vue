<template>
    <div class="container">
    <template v-if="isResolved">
        <div>
            <template v-if="doc">
                <MarkdownDisplayer :doc="doc" :constraint="constraint"/>
            </template>
        </div>
    </template>
    <template v-else>
        <div class="docNotFoundContainer">
            <b class="text">Cannot found documentation</b>
        </div>
    </template>
    </div>
</template>

<script setup lang="ts">
import type { Constraint } from '@/models/Constraint'
import { MarkdownParser } from '@/models/MardownParser'
import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'

import MarkdownDisplayer from '@/components/view/MarkdownDisplayer.vue'
import { type Ref, ref, onMounted, inject } from 'vue'
import axios from 'axios'

interface Props {
    constraint: Constraint
}
const props = withDefaults(defineProps<Props>(), {})

const doc: Ref<MarkdownDocumentation | null> = ref(null)
const p = new MarkdownParser()
const isResolved = ref(false)

const isMounted = ref(false)
onMounted(() => {
    isMounted.value = true
})

const lang = inject('lang')
await axios
    .get(`/${lang}/api/ttapp/docu/${props.constraint.className}.md`)
    .then(function (response) {
        isResolved.value = true
        p.parse(response.data, props.constraint).then((response) => (doc.value = response))
    })
    .catch(function (error) {
        isResolved.value = false
    })
</script>

<style scoped>

.container{
    display: table;
    width: 100%;
}
.docNotFoundContainer{
    display: table-cell;
    vertical-align: middle;
    text-align: center;
    height: 10vh;
}

.text{
    color:firebrick;
    font-size:large;    
}

</style>
