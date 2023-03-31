import { useFetch } from "@/composables/api"
import { Tutor } from "@/models/Tutor"

const URL_GET_ALL = "/fr/api/fetch/idtutor"
export async function getAllTutor(){
    return useFetch(URL_GET_ALL,Tutor)
    .then(items => {
        const res: Array<Tutor> = []
        items.forEach((i:any) => {
            const curItem = Tutor.unserialize(i)
            res.push(curItem)
        })
        return res
    })
}
