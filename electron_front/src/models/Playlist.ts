import Video from "./Video"

export default class Playlist {
    public name : string
    public path : string
    public videos : Video[]
    constructor(name : string, path : string, videos : Video[]) {
        this.name = name
        this.path = path
        this.videos = videos
    }
}