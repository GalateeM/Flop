<template>
    <TriggeredTeleporter
        to=".popover-body"
        :disable="DESACTIVATE_TELEPORTS"
        :listeningTarget="listeningTarget"
        eventName="contextmenu"
    >
        <hr />
        <div>
            <div class="buttonContainer">
                <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap()">{{ showDoc ? '-' : '+' }}</button>
            </div>
            <template v-if="showDoc">
                <input type="file" @change="handleFileUpload" />
                <template v-if="doc">
                    <div>
                        <MarkdownDisplayer :doc="doc" />
                    </div>
                </template>
            </template>
        </div>
    </TriggeredTeleporter>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'
import TriggeredTeleporter from '@/components/TriggeredTeleporter.vue'
import MarkdownDisplayer from '@/components/MarkdownDisplayer.vue'

import { MarkdownParser } from '@/models/MardownParser'
import type { MarkdownDocumentation } from '@/models/MarkdownDocumentation'

const p = new MarkdownParser()
const doc: Ref<MarkdownDocumentation | null> = ref(null)
const f: Ref<File | null> = ref(null)

// MOCKER
async function handleFileUpload(event: Event) {
    const inputElem = event.target as HTMLInputElement
    if (inputElem.files) {
        f.value = inputElem.files.item(0) as File
        await p.parse(f.value).then((response) => (doc.value = response))
    }
}

const DESACTIVATE_TELEPORTS = ref(false)
const listeningTarget = document.getElementById('constraints-body') as EventTarget
const constraintsBodyFound = listeningTarget != null
if (!constraintsBodyFound) throw new Error('constraints-body element not found')

/**
 * Reference to know if the documentation is shown
 */
const showDoc = ref(false)

/**
 * Swap showDoc value
 */
function swap() {
    showDoc.value = !showDoc.value
}

/**
 * doc-show-btn class definer
 */
const showBtnClassDefiner = () => {
    return showDoc.value ? ' minusButton ' : ' plusButton '
}
</script>

<style scoped>
.buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
}

.plusButton {
    border-radius: 10%;
    border: none;
    background-color: green;
}
.minusButton {
    border-radius: 10%;
    border: none;
    background-color: rgb(180, 47, 47);
}

</style>
