<template>
    <div>
        <VueShowdown :markdown="doc.textContent" :vue-template="true" />
    </div>
</template>

<script setup lang="ts">
import { MarkdownDocumentation } from '@/models/MarkdownDocumentation'
const props = defineProps({
    /**
     * Documentation to display
     */
    doc: { type: MarkdownDocumentation, required: true },
})
</script>

<style scoped></style>
