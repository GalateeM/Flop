import { Tutor } from '@/models/Tutor'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'
import { useDepartmentStore } from '@/stores/departmentRework'
import type { Department } from '@/models/Department'

class TutorStore extends SimpleStoreMap<number, Tutor> {
    gatherData() {
        return new Promise<Array<Tutor>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<Tutor> = []
                const envId = window.eval("database['tutors_ids']")
                const envData = window.eval("database['tutors']")
                //Open department store
                const store_department = useDepartmentStore()
                Object.keys(envId).forEach((key) => {
                    const name = envId[key].name
                    const departments: Array<Department> = []
                    envData[name].departments.forEach((d: any) => {
                        //Check is the tutor's departments are in the department store
                        const dep = store_department.items.get(d.id)
                        if (dep) departments.push(dep)
                        else throw Error('Department not found in the store')
                    })

                    const curItem = new Tutor(
                        Number(key),
                        name,
                        envData[name].first_name,
                        envData[name].last_name,
                        envData[name].email,
                        departments
                    )

                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }
}

export const useTutorStore = defineStore('tutor', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number, Tutor> = new TutorStore()

    const items = store.items
    function insertNew(item: Tutor) {
        store.insertNew(item)
    }

    function initialize() {
        return store.initialize()
    }

    return { items, insertNew, initialize }
})
