import type { FlopAPI } from '@/assets/js/api'
import { requireInjection, apiKey } from '@/assets/js/keys'
import { Group } from '@/models/Group'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { SimpleStoreMap } from './SimpleStoreMap'

class GroupStore extends SimpleStoreMap<number,Group> {
    constructor() {
        super()
        //Fetch the API to fill the store
        // const api = ref<FlopAPI>(requireInjection(apiKey))
        // api.value.fetch.departments().then((value) => {
        //     value.forEach((d) => this.insertNew(Group.unserialize(d)))
        //     console.log(this.items.value)
        // })

        setTimeout(() => {
            const envItems = window.eval("database['groups']")
            Object.keys(envItems).forEach((k) => {
                const envItem = envItems[k]
                const curItem = Group.unserialize(envItem)
                this.insertNew(curItem)
            })
        }, 5000)
    }
}

export const useGroupStore = defineStore('group', () => {
    /**
     * Sorted by classes then by objects
     */
    const map: SimpleStoreMap<number,Group> = new GroupStore()

    const items = map.items
    function insertNew(item:Group){
        map.insertNew(item)
    }

    return { items , insertNew }
})
