import { Department } from '@/models/Department'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class DepartmentStore extends SimpleStoreMap<number, Department> {
    gatherData() {
        return new Promise<Array<Department>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<Department> = []
                const envItems = window.eval("database['departments']")
                Object.keys(envItems).forEach((k) => {
                    const envItem = envItems[k]
                    const id = Number(k)
                    const curItem = new Department(id, envItem)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }    
}

export const useDepartmentStore = defineStore('departmentRework', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number, Department> = new DepartmentStore()

    const items = store.items
    function insertNew(item: Department) {
        store.insertNew(item)
    }

    function initialize() {
        return store.initialize()
    }

    return { items, insertNew, initialize }
})
