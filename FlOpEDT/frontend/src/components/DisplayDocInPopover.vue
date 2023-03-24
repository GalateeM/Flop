<template>
    <Teleport to=".popover-body" :disable="DESACTIVATE_TELEPORTS" :key="key"><!-- KEY = ADAPTER-->
        <hr />
        <div>
            <div class="buttonContainer">
                <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap">
                    {{ showDoc ? '⬆' : '⬇' }}
                </button>
            </div>
            <template v-if="selectedConstraint">
                <template v-if="showDoc">
                    <div class="scrollbar scrollbar-primary">
                        <DocumentationControler :constraint="selectedConstraint" />
                    </div>
                </template>
            </template>
        </div>
    </Teleport>
</template>

<script setup lang="ts">
import DocumentationControler from '@/components/controler/DocumentationControler.vue'

import type { Constraint } from '@/models/Constraint'
import { addEventListenerForForceTeleport } from '@/viewsAdapters/displayDocInPopoverAdapter';
import { ref } from 'vue'

const DESACTIVATE_TELEPORTS = ref(false)

interface Props {
    listeningTarget: EventTarget
    selectedConstraint: Constraint | null
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
}
const props = withDefaults(defineProps<Props>(), {})

const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()

/**
 * Swap showDoc value
 */
function swap() {
    emit('updateShowDoc', props.showDoc)
}

/**
 * doc-show-btn class definer
 * permit to setup the display parameters
 */
const showBtnClassDefiner = () => {
    return props.showDoc ? ' minusButton ' : ' plusButton '
}


/*
================================ ADAPTATER ================================ 
*/
const key = ref(0)
//Force the component to rerender by updating a ref
addEventListenerForForceTeleport(key,props.listeningTarget);


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
