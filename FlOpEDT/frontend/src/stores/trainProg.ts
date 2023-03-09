import { TrainProg } from '@/models/TrainProg'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class TrainProgStore extends SimpleStoreMap<number, TrainProg> {
    gatherData() {
        return new Promise<Array<TrainProg>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<TrainProg> = []
                const env = window.eval("database['train_progs']")
                Object.keys(env).forEach((key) => {
                    const item = env[key]
                    const curItem = TrainProg.unserialize(item)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
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
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
