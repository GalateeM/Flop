import type { Constraint } from "@/models/Constraint"
import type { Ref } from "vue"

/**
 * Increase the width of the modal's window when documentation is displayed or not
 * @param showDoc 
 */
export function increaseSizeOfModal(showDoc:boolean) {
    const modal = document.getElementsByClassName('modal-dialog').item(0) as HTMLElement
    if (showDoc) {
        modal.className = 'modal-dialog modal-dialog-centered modal-dialog-scrollable'
    } else {
        modal.className = 'modal-dialog modal-dialog-centered modal-dialog-scrollable modal-xl'
    }
}

/**
 * modify the modal window's DOM to make the teleported component clickable
 * only called Once
 *
 */
export function modifyDisplay() {
    const modal = document.getElementsByClassName('modal-content').item(0) as HTMLElement
    modal.style.flexDirection = 'row'

    const header = document.getElementsByClassName('modal-header').item(0) as HTMLElement
    const body = document.getElementsByClassName('modal-body').item(0) as HTMLElement
    const footer = document.getElementsByClassName('modal-footer').item(0) as HTMLElement
    if (header) {
        modal.removeChild(header)
    }
    if (body) {
        modal.removeChild(body)
    }
    if (footer) {
        modal.removeChild(footer)
    }
    const oldDiv = document.createElement('div')
    oldDiv.appendChild(header)
    oldDiv.appendChild(body)
    oldDiv.appendChild(footer)
    modal.appendChild(oldDiv)

    const docDisplayer = document.createElement('div')
    docDisplayer.className = 'docDisplayer'
    modal.appendChild(docDisplayer)
}

/**
 * Add an EventListener on the Cancel button of the popover
 * Permit to reset the current doc's constraint
 * @param constraint 
 */
export function addEventListenerToCancelButton(constraint:Ref<Constraint | null>){
    /**
     * Cancel button of the popover
     */
    const cancelEditBtn = document.getElementById('cancel-edit-constraint') as HTMLInputElement
    //Set the selectedConstraint to null when user leave the popover
    cancelEditBtn?.addEventListener('click', () => {
        constraint.value = null
    })
}



