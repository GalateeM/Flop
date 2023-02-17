import { Module } from '@/models/Module'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class WeekStore extends SimpleStoreMap<number,Module> {
    constructor() {
        super()
        setTimeout(() => {
            const envItems = window.eval("database['modules']")
            Object.keys(envItems).forEach((k) => {
                const envItem = envItems[k]
                const curItem = Module.unserialize(envItem)
                this.insertNew(curItem)
            })
        }, 5000)
    }
}

export const useModuleStore = defineStore('module', () => {
    /**
     * Sorted by classes then by objects
     */
    const map: SimpleStoreMap<number,Module> = new WeekStore()

    const items = map.items
    function insertNew(item:Module){
        map.insertNew(item)
    }

    return { items , insertNew }
})
