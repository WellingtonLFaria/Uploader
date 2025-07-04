from pydantic import BaseModel


class Video(BaseModel):
    name: str
    path: str
    uploaded: bool = False


class Playlist(BaseModel):
    name: str
    path: str
    videos: list[Video] = []
