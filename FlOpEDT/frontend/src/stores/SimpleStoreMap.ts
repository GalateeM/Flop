import { computed, ref, type Ref } from 'vue'

interface I_Identifiable<ID_TYPE> {
    id: ID_TYPE
}

/**
 * A store object consisting in a map where items are sorted by id
 * @class
 */
export abstract class SimpleStoreMap<ID_TYPE, ITEM_TYPE extends I_Identifiable<ID_TYPE>>  {
    /**
     * Items sorted by id
     */
    protected map: Ref<Map<ID_TYPE, ITEM_TYPE>> =  ref(new Map<ID_TYPE, ITEM_TYPE>())

    /**
     * Accessor for
     * {@link map}
     */
    items = computed(() => this.map.value)

    /**
     * Mutator for
     * {@link map}
     *
     * Insert a new entry in the second layout
     */
    insertNew(item: ITEM_TYPE) {
        if (!this.map.value.has(item.id)) {
            this.map.value.set(item.id, item)
        } else throw Error('ID ' + item.id + ' alredy in the map')
    }

}