import { useFetch } from "@/composables/api"
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