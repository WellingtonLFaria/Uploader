import os
import sys
from json import dumps

PATH = sys.argv[1]

def is_a_folder(path: str):
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

class Playlist:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path
        self.videos = []

    def add_videos(self) -> None:
        for item in os.listdir(self.path):
            if is_a_video(item):
                self.videos.append(item)
    
    def get_videos(self, path):
        for item in os.listdir(path):
            if is_a_folder(f"{path}/{item}"):
                self.get_videos(f"{path}/{item}")
            else:
                if is_a_video(item):
                    self.videos.append(Video(item, f"{path}/{item}").__dict__)

class Video:
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path


def run():
    playlists = [Playlist("blank", PATH)]
    for item in os.listdir(PATH):
        if is_a_folder(f"{PATH}/{item}"):
            playlists.append(Playlist(item, f"{PATH}/{item}"))

    for playlist in playlists:
        if playlist.name == "blank":
            for item in os.listdir(playlist.path):
                if is_a_video(item):
                    playlist.videos.append(Video(item, f"{playlist.path}/{item}").__dict__)
        else:
            playlist.get_videos(playlist.path)
        print(playlist.__dict__)
    
    with open("playlist.json", "w") as file:
        file.write('{"playlists":[')
        tamanho = len(playlists)
        for playlist in playlists:
            if playlists.index(playlist) == tamanho - 1:
                file.write(f"{dumps(playlist.__dict__)}")
            else:
                file.write(f"{dumps(playlist.__dict__)},")
        file.write("]}")
run()