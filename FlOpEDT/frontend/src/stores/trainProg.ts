import { TrainProg } from '@/models/TrainProg'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class TrainProgStore extends SimpleStoreMap<number, TrainProg> {
    constructor() {
        super()
        setTimeout(() => {
            const env = window.eval("database['train_progs']")
            Object.keys(env).forEach((key) => {
                const item = env[key]
                const CurrentItem = TrainProg.unserialize(item)
                this.insertNew(CurrentItem)
            })
        }, 5000)
    }
}

export const useTrainProgStore = defineStore('trainProg', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number, TrainProg> = new TrainProgStore()

    const items = store.items
    function insertNew(item: TrainProg) {
        store.insertNew(item)
    }

    return { items, insertNew }
})
