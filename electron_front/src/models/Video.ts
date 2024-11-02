export default class Video {
    public name: string
    public path: string
    public uploaded?: boolean
    constructor(name : string, path : string, uploaded? : boolean) {
        this.name = name
        this.path = path
        this.uploaded = uploaded
    }
}