/* eslint-disable */
import type { Constraint } from "@/models/Constraint";
import { ref, type Ref } from "vue";
import { increaseSizeOfModal } from "./displayDocInNewConstraintAdapter";

const listeningTarget = document.getElementById('constraints-body') as EventTarget
const POPOVER_EVENT_NAME = 'contextmenu'
const constraintsBodyFound = listeningTarget != null
if (!constraintsBodyFound) throw new Error('constraints-body element not found')
const currentPopoverFound = ref(false)

export function updatePopoversByShowingDoc(showing:boolean){
    increaseSizeOfModal(showing);
}

export function resetSelectedConstraint(selectedConstraint:Ref<Constraint | null>){
    document.addEventListener('click', (e) => {
        const currentPopover = window.eval('currentPopover')
        if (!currentPopover) {
            selectedConstraint.value = null
            currentPopoverFound.value = false
        }
    })
}

export function selectConstraintFromPopover(fct:Function){
    listeningTarget.addEventListener(
        POPOVER_EVENT_NAME,
        (e) => {
            setCurrentConstraint(fct)
        },
        false
    )
}

export function getPopoverFound(){
    return currentPopoverFound
}

export function getListeningTarget(){
    return listeningTarget
}

export function afterInitializingConstraintStoreFromAdapter(fct:Function){
    if (currentPopoverFound.value == true) {
       setCurrentConstraint(fct)
    }
}

function setCurrentConstraint(fct:Function){
    const currentPopover = window.eval('currentPopover')
    if (currentPopover) {
        currentPopoverFound.value = true
        const cst = currentPopover._element.getAttribute('data-cst-id') as string
        fct(cst)
    }
}