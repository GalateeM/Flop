export class MarkdownDocumentation {
    private _id : string;
    private _textContent : string;
    private _paramCallCount : Map<string,number>

    constructor(id:string, textContent:string, paramCallCount:Map<string,number>){
        this._id = id
        this._textContent = textContent
        this._paramCallCount = paramCallCount
    }

    get id(){
        return this._id
    }

    get textContent(){
        return this._textContent
    }

    get paramCallCount(){
        return this._paramCallCount
    }


}