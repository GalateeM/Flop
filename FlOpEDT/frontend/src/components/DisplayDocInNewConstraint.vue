<template>
    <div class="documentationContainer">
        <div class="buttonContainer">
            <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap">
                {{ showDoc ? '⬅' : '➡' }}
            </button>
        </div>
        <template v-if="showDoc">
            <div class="scrollbar scrollbar-primary">
                <template v-if="constraint">
                    <DocumentationControler :constraint="constraint" />
                </template>
            </div>
        </template>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DocumentationControler from '@/components/controler/DocumentationControler.vue'
import type { Constraint } from '@/models/Constraint'

interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
    constraint: Constraint | null
}
const props = withDefaults(defineProps<Props>(), {})

/**
 * Swap showDoc value
 */
function swap() {
    emit('updateShowDoc', props.showDoc)
}

const emit = defineEmits<{
    (e: 'updateShowDoc', value: boolean): void
}>()

const DESACTIVATE_TELEPORTS = ref(false)

/**
 * doc-show-btn class definer
 * permit to setup the display parameters
 */
const showBtnClassDefiner = () => {
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
    height: 100%;
    border: none;
    background-color: green;
}

.plusButton:hover {
    background-color: darkgreen;
}

.minusButton {
    width: 100%;
    height: 100%;
    border: none;
    background-color: firebrick;
}

.minusButton:hover {
    background-color: darkred;
}

.documentationContainer {
    height: 100%;
    display: flex;
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
