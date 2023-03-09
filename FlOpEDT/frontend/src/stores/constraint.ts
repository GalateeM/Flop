import { Constraint } from '@/models/Constraint'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'


class CourseTypeStore extends SimpleStoreMap<string,Constraint> {
    
    gatherData() {
        return new Promise<Array<Constraint>>((resolve, reject) => {
        setTimeout(() => {
            const res: Array<Constraint> = []
            const envItems = window.eval("constraints")
            Object.keys(envItems).forEach((k) => {
                const envItem = envItems[k]
                const curItem = Constraint.unserialize(envItem)
                res.push(curItem)
            })
            resolve(res)
        }, 5000)
        })
    }
}

export const useConstraintStore = defineStore('contraint', () => {
    const store: SimpleStoreMap<string,Constraint> = new CourseTypeStore()

    const items = store.items

    function insertNew(item:Constraint){
        store.insertNew(item)
    }
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
