import { Week } from '@/models/Week'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class WeekStore extends SimpleStoreMap<number,Week> {
    constructor() {
        super()
        setTimeout(() => {
            const env = window.eval("database['weeks']")
            Object.keys(env).forEach((key) => {
                const item = env[key]
                const CurrentItem = Week.unserialize(item)
                this.insertNew(CurrentItem)
            })
        }, 5000)
    }
}

export const useWeekStore = defineStore('week', () => {
    /**
     * Sorted by classes then by objects
     */
    const map: SimpleStoreMap<number,Week> = new WeekStore()

    const items = map.items
    function insertNew(item:Week){
        map.insertNew(item)
    }

    return { items , insertNew }
})
