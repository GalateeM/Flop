import { CourseType } from '@/models/CourseType'
import { Department } from '@/models/Department'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { SimpleStoreMap } from './SimpleStoreMap'


class CourseTypeStore extends SimpleStoreMap<number,CourseType> {
    gatherData() {
        return new Promise<Array<CourseType>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<CourseType> = []
                const envItems = window.eval("database['course_types']")
                Object.keys(envItems).forEach((k) => {
                    const envItem = envItems[k]
                    const id = Number(k)
                    const curItem = new CourseType(id, envItem)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }
}

export const useCourseTypeStore = defineStore('courseType', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number,CourseType> = new CourseTypeStore()

    const items = store.items

    function insertNew(item:CourseType){
        store.insertNew(item)
    }
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
