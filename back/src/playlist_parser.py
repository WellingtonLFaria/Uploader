import os
import sys
from json import dumps

PATH = sys.argv[1]

class Playlist:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.videos = []

    def add_videos(self) -> None:
        for item in os.listdir(self.path):
            if is_a_video(item):
                self.videos.append(item)
    
    def get_videos(self, path: str):
        for item in os.listdir(path):
            if is_a_folder(f"{path}/{item}"):
                self.get_videos(f"{path}/{item}")
            else:
                if is_a_video(item):
                    self.videos.append(Video(item.split(".")[0].capitalize(), f"{path}/{item}").__dict__)

class Video:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.uploaded = False

def is_a_folder(path: str) -> bool:
    try:
        if path.split("/")[-1][0] == ".":
            return False
        os.listdir(path)
        return True
    except:
        return False

def is_a_video(file: str) -> bool:
    supported_video_extensions = ['mp4','mkv','mov']
    file_extension = file.split('.')
    try:
        if file_extension[1] in supported_video_extensions:
            return True
        return False
    except:
        return False

def run():
    playlists = create_playlists()
    playlists = get_playlists_videos(playlists)
    save_playlists(playlists)

def create_playlists() -> list[Playlist]:
    playlists = [Playlist("blank", PATH)]
    for item in os.listdir(PATH):
        if is_a_folder(f"{PATH}/{item}"):
            playlists.append(Playlist(item, f"{PATH}/{item}"))
    return playlists

def get_playlists_videos(playlists: list[Playlist]) -> list[Playlist]:
    for playlist in playlists:
        if playlist.name == "blank":
            for item in os.listdir(playlist.path):
                if is_a_video(item):
                    playlist.videos.append(Video(item.split(".")[0], f"{playlist.path}/{item}").__dict__)
        else:
            playlist.get_videos(playlist.path)
    return playlists

def save_playlists(playlists: list[Playlist]) -> None:
    with open("playlist.json", "w", encoding="utf-8") as file:
        file.write('{"playlists":[')
        length = len(playlists)
        for playlist in playlists:
            if playlists.index(playlist) == length - 1:
                file.write(f"{dumps(playlist.__dict__)}")
            else:
                file.write(f"{dumps(playlist.__dict__)},")
        file.write("]}")


if __name__ == "__main__":
    run()