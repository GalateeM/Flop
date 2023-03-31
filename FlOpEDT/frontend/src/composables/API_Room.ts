import { useFetch } from "@/composables/api"
import { Room } from "@/models/Room"

const URL_GET_ALL = "/fr/api/rooms/room"
export async function getAllRoom(){
    return useFetch(URL_GET_ALL,Room)
    .then(items => {
        const res: Array<Room> = []
        items.forEach((i:any) => {
            const curItem = Room.unserialize(i)
            res.push(curItem)
        })
        return res
    })
}

