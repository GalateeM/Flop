import { Week } from '@/models/Week'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class WeekStore extends SimpleStoreMap<number,Week> {
    gatherData() {
        return new Promise<Array<Week>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<Week> = []
                const env = window.eval("database['weeks']")
                Object.keys(env).forEach((key) => {
                    const item = env[key]
                    const curItem = Week.unserialize(item)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }
}

export const useWeekStore = defineStore('week', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number,Week> = new WeekStore()

    const items = store.items
    function insertNew(item:Week){
        store.insertNew(item)
    }
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
