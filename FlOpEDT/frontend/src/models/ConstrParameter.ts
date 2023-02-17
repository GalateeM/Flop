/**
 * @class
 */
export class ConstrParameter {
    private _name!: string
    private _type!: string //Should be an enum
    private _required!: boolean
    private _multiple!: boolean
    private _id_list!: Array<number>

    constructor(name: string, type: string, required: boolean, multiple: boolean, id_list: Array<number>) {
        this.name = name
        this.type = type
        this.required = required
        this.multiple = multiple
        this.id_list = id_list
    }

    get name() {
        return this._name
    }
    set name(name: string) {
        this._name = name
    }

    get type() {
        return this._type
    }
    set type(type: string) {
        this._type = type
    }

    get required() {
        return this._required
    }
    set required(required: boolean) {
        this._required = required
    }

    get multiple() {
        return this._multiple
    }
    set multiple(multiple: boolean) {
        this._multiple = multiple
    }

    get id_list() {
        return this._id_list
    }
    set id_list(id_list: Array<number>) {
        this._id_list = id_list
    }

    static serialize(param: ConstrParameter) {
        throw Error('Method not yet implemented')
    }

    static unserialize(obj: any) {
        return new ConstrParameter(obj.name, obj.type, obj.required, obj.multiple, obj.id_list)
    }
}
