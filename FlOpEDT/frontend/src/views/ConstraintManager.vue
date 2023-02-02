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
                <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap()">{{ showDoc ? '⬆' : '⬇' }}</button>
            </div>
            <template v-if="showDoc">
                <input type="file" @change="handleFileUpload" />
                <template v-if="doc">
                    <div class="scrollbar scrollbar-primary">
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


/**
 * Enlarge the width of the parent popover & center the bottons Duplicate/Modify/Delete
 */
function enlargePopover(){
    const popover = document.getElementsByClassName("popover").item(0)
    if(popover!==null){
        popover.style["max-width"]="30vw"
    }
    const groupeOfButton = document.getElementsByClassName("btn-group").item(0)
    if(groupeOfButton!==null){
        groupeOfButton.style["align-items"]="center";
        groupeOfButton.style["justify-content"]="center";
        groupeOfButton.style["display"]="flex";
    }
    
}

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
 * permit to setup the display parameters
 */
const showBtnClassDefiner = () => {
    enlargePopover()
    return showDoc.value ? ' minusButton ' : ' plusButton '
}
</script>

<style scoped>
.buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size:larger;
}

.plusButton {
    width: 100%;
    height: 30px;
    border-radius: 20px;
    border: none;
    background-color: green
}

.plusButton:hover{
    background-color: darkgreen;
}

.minusButton {
    width: 100%;
    height: 30px;
    border-radius: 20px;
    border: none;
    background-color:firebrick;
}

.minusButton:hover{
    background-color:darkred;
}

.scrollbar {
  max-height: 40vh;
  overflow-y: scroll;
}

.scrollbar-primary::-webkit-scrollbar {
  width: 12px;
}

.scrollbar-primary::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background-color:dodgerblue;
}
.scrollbar-primary::-webkit-scrollbar-thumb:hover {
  border-radius: 4px;
  background-color:royalblue;
}

.scrollbar-primary {
  scrollbar-color: #AAAAAA #F5F5F5;
}

</style>
