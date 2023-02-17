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
            //RegExp to find all interpolations (mustache) in the markdown
            const regex = new RegExp('(?<match>{{(?<content>.*)}})', 'g')
            const it = content.matchAll(regex)

            //List of interpolations to be replaced
            const replacements: [string, string][] = []
            let resultat = it.next()
            while (!resultat.done) {
                if (resultat.value.groups?.match) {
                    //clean the content of the interpolation
                    const content = resultat.value.groups?.content.trim()
                    if (content) {
                        //Retrieve the constant parameter associated to the interpolation
                        const cstParam = assocCst.parameters.find((p) => p.name == content)
                        if (cstParam) {
                            //Set the replacement to calls to the store associated to the interpolation
                            const newString = cstParam.id_list
                                .map((id) => cstParam.name + '.get(' + id + ')', '')
                                .join("+ ' ' +")
                            replacements.push([resultat.value.groups.match, newString])
                        }
                        resultat = it.next()
                    }
                }
            }

            //Replace old interpolations by their respective replacement
            replacements.forEach((e) => (content = content.replaceAll(e[0], '{{' + e[1] + '}}')))
            console.log(content)
            resolve(new MarkdownDocumentation(content))
        })
        // })
    }
}
