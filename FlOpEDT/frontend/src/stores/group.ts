import type { FlopAPI } from '@/assets/js/api'
import { requireInjection, apiKey } from '@/assets/js/keys'
import { Group } from '@/models/Group'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { SimpleStoreMap } from './SimpleStoreMap'

class GroupStore extends SimpleStoreMap<number,Group> {
    gatherData() {
        return new Promise<Array<Group>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<Group> = []
                const envItems = window.eval("database['groups']")
                Object.keys(envItems).forEach((k) => {
                    const envItem = envItems[k]
                    const curItem = Group.unserialize(envItem)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }
}

export const useGroupStore = defineStore('group', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number,Group> = new GroupStore()

    const items = store.items

    function insertNew(item:Group){
        store.insertNew(item)
    }
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
