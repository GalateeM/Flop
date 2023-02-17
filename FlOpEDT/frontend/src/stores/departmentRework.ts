import { Department } from '@/models/Department'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class DepartmentStore extends SimpleStoreMap<number, Department> {
    constructor() {
        super()
        setTimeout(() => {
            const envItems = window.eval("database['departments']")
            Object.keys(envItems).forEach((k) => {
                const envItem = envItems[k]
                const id = Number(k)
                const curItem = new Department(id, envItem)
                this.insertNew(curItem)
            })
        }, 5000)
    }
}

export const useDepartmentStore = defineStore('departmentRework', () => {
    /**
     * Sorted by classes then by objects
     */
    const map: SimpleStoreMap<number, Department> = new DepartmentStore()

    const items = map.items
    function insertNew(item: Department) {
        map.insertNew(item)
    }

    return { items, insertNew }
})
