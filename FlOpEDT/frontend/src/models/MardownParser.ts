import { MarkdownDocumentation } from "./MarkdownDocumentation";

export class MarkdownParser {
    private _fileReader = new FileReader();

    /**
     * Transform a file as string
     * 
     * @param file file to transform
     * @returns content file as string
     */
    async readFile(file: File) {
        this._fileReader.readAsText(file);
        const fr = this._fileReader
        return new Promise<string>(resolve => {
            this._fileReader.onload = function () {
                resolve(fr.result as string);
            }
        })
    }

    /**
     * Transform a file as MarkdownDocumentation
     * @param file file to transform
     * @returns a MarkdownDocumentation
     */
    async parse(file: File) {
        return new Promise<MarkdownDocumentation>(resolve => {
            this.readFile(file).then(response => {
                const content = response
                resolve(new MarkdownDocumentation(content));
            })
        })
    }
}