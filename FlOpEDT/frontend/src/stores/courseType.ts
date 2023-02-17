import { CourseType } from '@/models/CourseType'
import { Department } from '@/models/Department'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { SimpleStoreMap } from './SimpleStoreMap'


class CourseTypeStore extends SimpleStoreMap<number,CourseType> {
    constructor() {
        super()
        setTimeout(() => {
            const envItems = window.eval("database['course_types']")
            Object.keys(envItems).forEach((k) => {
                const envItem = envItems[k]
                const id = Number(k)
                const curItem = new CourseType(id, envItem)
                this.insertNew(curItem)
            })
        }, 5000)
    }
}

export const useCourseTypeStore = defineStore('courseType', () => {
    /**
     * Sorted by classes then by objects
     */
    const map: SimpleStoreMap<number,CourseType> = new CourseTypeStore()

    const items = map.items
    function insertNew(item:CourseType){
        map.insertNew(item)
    }

    return { items , insertNew }
})
