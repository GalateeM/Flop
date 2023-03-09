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
                <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap">
                    {{ showDoc ? '⬆' : '⬇' }}
                </button>
            </div>
            <template v-if="showDoc">
                <div class="scrollbar scrollbar-primary">
                    <Suspense>
                        <DocumentationControler :constraint="selectedConstraint" />
                        <template #fallback>
                            <p>Chargement</p>
                        </template>
                    </Suspense>
                </div>
            </template>
        </div>
    </TriggeredTeleporter>
</template>

<script setup lang="ts">
import TriggeredTeleporter from '@/components/controler/TriggeredTeleporter.vue'
import DocumentationControler from '@/components/controler/DocumentationControler.vue'

import type { Constraint } from '@/models/Constraint'
import { ref } from 'vue'

const DESACTIVATE_TELEPORTS = ref(false)

interface Props {
    listeningTarget: EventTarget
    selectedConstraint: Constraint
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
}
const props = withDefaults(defineProps<Props>(), {})

const emit = defineEmits<{
    (e:'updateShowDoc',value:boolean):void
}>()

/**
 * Enlarge the width of the parent popover & center the bottons Duplicate/Modify/Delete
 */
function enlargePopover() {
    const popover = document.getElementsByClassName('popover').item(0) as HTMLElement
    if (popover !== null) {
        popover.style['max-width'] = '80vw'
        window.scroll(popover.getBoundingClientRect().right,0)
        
    }
    const groupeOfButton = document.getElementsByClassName('btn-group').item(0) as HTMLElement
    if (groupeOfButton !== null) {
        groupeOfButton.style['align-items'] = 'center'
        groupeOfButton.style['justify-content'] = 'center'
        groupeOfButton.style['display'] = 'flex'
    }
}

/**
 * Swap showDoc value
 */
function swap() {
    emit('updateShowDoc',props.showDoc)
}

/**
 * doc-show-btn class definer
 * permit to setup the display parameters
 */
const showBtnClassDefiner = () => {
    enlargePopover()
    return props.showDoc ? ' minusButton ' : ' plusButton '
}
</script>

<style scoped>
.buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: larger;
}

.plusButton {
    width: 100%;
    height: 30px;
    border-radius: 20px;
    border: none;
    background-color: green;
}

.plusButton:hover {
    background-color: darkgreen;
}

.minusButton {
    width: 100%;
    height: 30px;
    border-radius: 20px;
    border: none;
    background-color: firebrick;
}

.minusButton:hover {
    background-color: darkred;
}

.scrollbar {
    max-height: 70vh;
    overflow-y: scroll;
}

.scrollbar-primary::-webkit-scrollbar {
    width: 12px;
}

.scrollbar-primary::-webkit-scrollbar-thumb {
    border-radius: 4px;
    background-color: dodgerblue;
}
.scrollbar-primary::-webkit-scrollbar-thumb:hover {
    border-radius: 4px;
    background-color: royalblue;
}

.scrollbar-primary {
    scrollbar-color: #aaaaaa #f5f5f5;
}
</style>
