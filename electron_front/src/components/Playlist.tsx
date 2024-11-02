import Playlist from "../models/Playlist";
import Video from "../models/Video";

export default function PlaylistComponent(props : {playlist: Playlist}) {
    return (
        <div className="w-full border-2 rounded p-1 my-1">
            <p className="text-lg">{props.playlist.name}</p>
            <p>{props.playlist.path}</p>
            <hr className="border-2 rounded"></hr>
            {props.playlist.videos.map((video: Video) => {
            return (
                <div className="grid grid-flow-col gap-2 p-2" key={video.name}>
                <div className="w-14 h-14  bg-neutral-400">
                </div>
                <div>
                    <p>{video.name}</p>
                    <p>{video.path}</p>
                </div>
                </div>
            )
            })}
        </div>
    );
}