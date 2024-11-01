import os
import sys

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
    suported_video_extensions = ['mp4']
    file_extension = file.split('.')
    try:
        if file_extension[1] in suported_video_extensions:
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
    for item in os.listdir():
        if is_a_folder(item):
            playlists.append(Playlist(item, f"{PATH}/{item}"))

    for playlist in playlists:
        if playlist.name == "blank":
            for item in os.listdir(playlist.path):
                if is_a_video(item):
                    playlist.videos.append(Video(item, f"{playlist.path}/{item}").__dict__)
        else:
            playlist.get_videos(playlist.path)
        print(playlist.__dict__)

run()