import type { Constraint } from '@/models/Constraint'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'
import { getAllConstraint } from '@/composables/API_Constraint';

class CourseTypeStore extends SimpleStoreMap<string,Constraint> {
    gatherData() {
        return getAllConstraint();
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
