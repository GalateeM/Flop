import { Constraint } from '@/models/Constraint'
import { defineStore } from 'pinia'
import { computed, ref, type Ref } from 'vue'
class ConstraintStore  {

    constructor(){
        setTimeout(() => {
            const cts = window.eval('constraints')
            Object.keys(cts).forEach((c) => {
                const constraint = cts[c]
                const cstNameClass = constraint.name
                const curConstrainte = Constraint.unserialize(constraint)
                if (!this.constraints.value.has(cstNameClass)) {
                    this.insertNewClass(cstNameClass)
                    this.insertNewConstraint(cstNameClass, curConstrainte.id, curConstrainte)
                } else {
                    this.insertNewConstraint(cstNameClass, curConstrainte.id, curConstrainte)
                }
            })
        }, 5000)
    }

    /**
     * Sorted by classes then by objects
     */
    private map: Ref<Map<string, Map<number, Constraint>>> = ref(new Map<string, Map<number, Constraint>>())

    /**
     * Accessor for
     * {@link map}
     */
    constraints = computed(() => this.map.value)

    /**
     * Mutator for
     * {@link map}
     *
     * Insert a new entry in the second layout
     */
    insertNewConstraint(ClassName: string, id: number, constraint: Constraint) {
        if (this.map.value.has(ClassName)) {
            this.map.value.get(ClassName)?.set(constraint.id, constraint)
        } else throw Error('Class ' + ClassName + ' not found')
    }

    /**
     * Mutator for
     * {@link map}
     *
     * Insert a new entry in the first layout with an empty map for the second layout
     */
    insertNewClass(ClassName: string) {
        if (!this.map.value.has(ClassName)) {
            this.map.value.set(ClassName, new Map<number, Constraint>())
        } else throw Error('Class already in')
    }
}

export const useConstraintStore = defineStore('contraint', () => {
    const store: ConstraintStore = new ConstraintStore()

    const constraints = store.constraints

    function insertNewConstraint(className: string, id: number, constraint: Constraint) {
        store.insertNewConstraint(className, id, constraint)
    }

    function insertNewClass(className: string) {
        store.insertNewClass(className)
    }

    return { constraints, insertNewConstraint, insertNewClass }
})
