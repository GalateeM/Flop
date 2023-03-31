import { useFetch } from "@/composables/api"
import { Department } from "@/models/Department"

const URL_GET_ALL =  "/fr/api/fetch/alldepts"
export async function getAllDepartement(){
    return useFetch(URL_GET_ALL,Department)
    .then(items => {
        const res: Array<Department> = []
        items.forEach((i:any) => {
            const curItem = Department.unserialize(i)
            res.push(curItem)
        })
        return res
    })
}