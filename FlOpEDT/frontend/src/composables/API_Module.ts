import { useFetch } from "@/composables/api"
import { Module } from "@/models/Module"

const URL_GET_ALL = "/fr/api/fetch/idmodule"
export async function getAllModule(){
    return useFetch(URL_GET_ALL,Module)
    .then(items => {
        const res: Array<Module> = []
        items.forEach((i:any) => {
            const curItem = Module.unserialize(i)
            res.push(curItem)
        })
        return res
    })
}