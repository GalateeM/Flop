export class MarkdownDocumentation {
    private _textContent : string;

    constructor(textContent:string){
        this._textContent = textContent;
    }

    get textContent(){
        return this._textContent
    }
}