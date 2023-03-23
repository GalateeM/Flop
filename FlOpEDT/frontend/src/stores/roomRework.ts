import { Room } from '@/models/Room'
import { defineStore } from 'pinia'
import { SimpleStoreMap } from './SimpleStoreMap'

class RoomStore extends SimpleStoreMap<number,Room> {
    gatherData() {
        return new Promise<Array<Room>>((resolve, reject) => {
            setTimeout(() => {
                const res: Array<Room> = []
                const envItems = window.eval("database['rooms']")
                Object.keys(envItems).forEach((k) => {
                    const envItem = envItems[k]
                    const curItem = Room.unserialize(envItem)
                    res.push(curItem)
                })
                resolve(res)
            }, 5000)
        })
    }
}

export const useRoomStore = defineStore('roomRework', () => {
    /**
     * Sorted by classes then by objects
     */
    const store: SimpleStoreMap<number,Room> = new RoomStore()

    const items = store.items
    function insertNew(item:Room){
        store.insertNew(item)
    }
        
    function initialize() {
        return store.initialize()
    }

    return { items , insertNew, initialize }
})
