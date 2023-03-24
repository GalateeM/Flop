import type { Ref } from "vue";

/**
 * Enlarge the width of the parent popover & center the bottons Duplicate/Modify/Delete
 */
export function enlargePopover() {
    const popover = document.getElementsByClassName('popover').item(0) as HTMLElement
    if (popover !== null) {
        popover.style.maxWidth = '80vw'
        window.scroll(popover.getBoundingClientRect().right, 0)
    }
    const groupeOfButton = document.getElementsByClassName('btn-group').item(0) as HTMLElement
    if (groupeOfButton !== null) {
        groupeOfButton.style.alignItems='center';
        groupeOfButton.style.justifyContent='center';
        groupeOfButton.style.display = 'flex'
    }
}

export function forceTeleport(key:Ref<number>){
    key.value++;
}

export function addEventListenerForForceTeleport(key:Ref<number>,target:EventTarget){
    const eventName = 'contextmenu'
    target.addEventListener(eventName, (e) => forceTeleport(key), false)
}