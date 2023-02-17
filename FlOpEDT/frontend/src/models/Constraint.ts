import { ConstrParameter } from '@/models/ConstrParameter'

/**
 * @class
 */
export class Constraint {
    private _id!: number
    private _title!: string
    private _name!: string
    private _weight!: number
    private _is_active!: boolean
    private _comment!: string
    private _modified_at!: string
    private _parameters!: Array<ConstrParameter>

    constructor(
        id: number,
        title: string,
        name: string,
        weight: number,
        is_active: boolean,
        comment: string,
        modified_at: string,
        parameters: Array<ConstrParameter>
    ) {
        this.id = id
        this.title = title
        this.name = name
        this.weight = weight
        this.is_active = is_active
        this.comment = comment
        this.modified_at = modified_at
        this.parameters = parameters
    }

    get id() {
        return this._id
    }
    set id(id) {
        this._id = id
    }

    get title() {
        return this._title
    }
    set title(title) {
        this._title = title
    }

    get name() {
        return this._name
    }
    set name(name) {
        this._name = name
    }

    get weight() {
        return this._weight
    }
    set weight(weight) {
        this._weight = weight
    }

    get is_active() {
        return this._is_active
    }
    set is_active(is_active) {
        this._is_active = is_active
    }

    get comment() {
        return this._comment
    }
    set comment(comment) {
        this._comment = comment
    }

    get modified_at() {
        return this._modified_at
    }
    set modified_at(modified_at) {
        this._modified_at = modified_at
    }

    get parameters() {
        return this._parameters
    }
    set parameters(parameters) {
        this._parameters = parameters
    }

    static serialize(param: ConstrParameter) {
        throw Error('Method not yet implemented')
    }

    static unserialize(obj: any) {
        const listParam: Array<ConstrParameter> = []
        obj.parameters.forEach((param: any) => {
            listParam.push(ConstrParameter.unserialize(param))
        })
        return new Constraint(
            obj.id,
            obj.title,
            obj.name,
            obj.weight,
            obj.is_active,
            obj.comment,
            obj.modified_at,
            listParam
        )
    }
}
