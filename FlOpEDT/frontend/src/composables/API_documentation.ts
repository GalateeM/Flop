import { MarkdownDocumentation } from "@/models/MarkdownDocumentation"
import axios from "axios"

/**
 * 
 * @param documentationName 
 * @param lang 
 * @returns a Promise containing the MarkdownDocumentation 
 */
export async function queryDoc(documentationName:string,lang:string) {
    return new Promise((resolve,reject) => axios
        .get(`/${lang}/api/ttapp/docu/${documentationName}.md`)
        .then( (response) => {
            const interpolationsCount = new Map<string,number>()
            Object.keys(response.data.inter).forEach(p => {
                interpolationsCount.set(p,response.data.inter[p])
            })
            const doc = new MarkdownDocumentation(response.data.text,interpolationsCount)
            resolve(doc)     
        })
        .catch( (error) => {
            reject(error)
        })
    )
}
