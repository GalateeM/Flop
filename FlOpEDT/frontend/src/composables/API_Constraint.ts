import { useFetch } from "@/composables/api"
import { Constraint } from "@/models/Constraint"
import { ConstraintClass } from "@/models/ConstraintClass"

export async function loadConstraintClass(){
    return await useFetch('/fr/api/ttapp/constraint_types', ConstraintClass).then(function (response) {
        const res = new Map<string, ConstraintClass>()
        response.forEach((element: any) => {
            const classe = ConstraintClass.unserialize(element)
            res.set(classe.className, classe)
        })
        return res
    })
}

const URL_GET_ALL = "/fr/api/ttapp/constraint"
export async function getAllConstraint(){
    return useFetch(URL_GET_ALL,Constraint)
    .then(items => {
        const res: Array<Constraint> = []
        items.forEach((i:any) => {
            const curItem = Constraint.unserialize(i)
            res.push(curItem)
        })
        return res
    })
}