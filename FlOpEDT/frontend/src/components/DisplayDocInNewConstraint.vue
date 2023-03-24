<template>
    <Teleport to=".docDisplayer" :disable="DESACTIVATE_TELEPORTS">
        <div class="documentationContainer">
            <div class="buttonContainer">
                <button id="doc-show-btn" :class="showBtnClassDefiner()" @click="swap">
                    {{ showDoc ? '⬅' : '➡' }}
                </button>
            </div>
            <template v-if="showDoc">
                <div class="scrollbar scrollbar-primary">
                    <template v-if="isLoaded">
                        <template v-if="constraint">
                            <DocumentationControler :constraint="constraint" />
                        </template>
                    </template>
                </div>
            </template>
        </div>
    </Teleport>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue'
import DocumentationControler from '@/components/controler/DocumentationControler.vue'
import { ConstraintClass } from '@/models/ConstraintClass'
import axios from 'axios'
import { Constraint } from '@/models/Constraint'
import { addEventListenerToCancelButton, increaseSizeOfModal, modifyDisplay } from '@/viewsAdapters/displayDocInNewConstraintAdapter'

interface Props {
    /**
     * Reference to know if the documentation is shown
     */
    showDoc: boolean
}
const props = withDefaults(defineProps<Props>(), {})

/**
 * Swap showDoc value
 */
function swap() {
    increaseSizeOfModal(props.showDoc)//Adapter
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

/**
 * Reference to know if the constraint classes map is loaded
 */
 const isLoaded = ref(false)

 
/**
 * Map of all constraint classes
 */
const cstClasses = new Map<string, ConstraintClass>()
//Load all constraint classes et set them in a dedicated map
await axios.get('/fr/api/ttapp/constraint_types/').then(function (response) {
    response.data.forEach((element: any) => {
        const classe = ConstraintClass.unserialize(element)
        cstClasses.set(classe.className, classe)
        isLoaded.value = true
    })
})

/**
 * Constraint being created
 */
 const constraint: Ref<Constraint | null> = ref(null)
/**
 * Select field to choose the constraint class
 */
const constraintEditTypeField = document.getElementById('constraint-edit-type') as HTMLInputElement
//Listen when the user select a new constraint to rerender the documentation displayer
constraintEditTypeField?.addEventListener('change', () => {
    const cstClass = Array.from(cstClasses.values()).find((e) => constraintEditTypeField.value == e.local_name)
    if (cstClass) {
        constraint.value = new Constraint(0, '', cstClass.className, 0, true, '', '', new Map())
    } else {
        constraint.value = null
    }
})


/*
================================ ADAPTATER ================================ 
*/
modifyDisplay()
addEventListenerToCancelButton(constraint)


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
