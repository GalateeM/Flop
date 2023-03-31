import { useFetch } from "@/composables/api"
import { Group } from "@/models/Group"

const URL_GET_ALL =  "/fr/api/fetch/idgroup"
export async function getAllGroup(){
    return useFetch(URL_GET_ALL,Group)
    .then(items => {
        const res: Array<Group> = []
        items.forEach((i:any) => {
            const curItem = Group.unserialize(i)
            res.push(curItem)
        })
        return res
    })
}