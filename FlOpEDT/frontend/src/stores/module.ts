import { Module } from '@/models/Module'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class WeekStore extends SimpleStoreMap<number,Module> {
    gatherData() {
        return new Promise<Array<Module>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<Module> = []
                const envItems = window.eval("database['modules']")
                Object.keys(envItems).forEach((k) => {
                    const envItem = envItems[k]
                    const curItem = Module.unserialize(envItem)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }
}

export const useModuleStore = defineStore('module', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number,Module> = new WeekStore()

    const items = store.items
    function insertNew(item:Module){
        store.insertNew(item)
    }
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
