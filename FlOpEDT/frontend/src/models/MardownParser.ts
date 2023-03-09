import type { Constraint } from '@/models/Constraint'
import { MarkdownDocumentation } from './MarkdownDocumentation'

export class MarkdownParser {
    private _fileReader = new FileReader()

    /**
     * Transform a file as string
     *
     * @param file file to transform
     * @returns content file as string
     */
    async readFile(file: File) {
        this._fileReader.readAsText(file)
        const fr = this._fileReader
        return new Promise<string>((resolve) => {
            this._fileReader.onload = function () {
                resolve(fr.result as string)
            }
        })
    }

    /**
     * Transform a file as MarkdownDocumentation
     * @param file file to transform
     * @returns a MarkdownDocumentation
     */
    async parse(file: string, assocCst: Constraint) {
        return new Promise<MarkdownDocumentation>((resolve) => {
            let content = file
            const paramCallCount = new Map<string, number>()
            //RegExp to find all interpolations (mustache) in the markdown
            const regex = new RegExp('(?<match>{{(?<content>.*)}})', 'g')
            const it = content.matchAll(regex)

            let resultat = it.next()
            while (!resultat.done) {
                if (resultat.value.groups?.match) {
                    //clean the content of the interpolation
                    const interpContent = resultat.value.groups?.content.trim()
                    if (interpContent) {
                        //Retrieve the constant parameter associated to the interpolation
                        // const cstParam = assocCst.parameters.get(interpContent)
                        const cstParam = {name : interpContent}
                        // if (cstParam) {
                            let v = 1
                            if (paramCallCount.has(cstParam.name)) {
                                v = paramCallCount.get(cstParam.name) as number
                                paramCallCount.set(cstParam.name, ++v)
                            } else paramCallCount.set(cstParam.name, v)

                            //Replace the interpolation call by an anchor point
                            const newString = '<div id="' + cstParam.name + 'Displayer'+v+'"></div>'
                            content = content.replace(resultat.value.groups.match,newString)

                        resultat = it.next()
                    }
                }
            }
            const id = assocCst.className + assocCst.id
            resolve(new MarkdownDocumentation(id,content,paramCallCount))
        })
    }
}
