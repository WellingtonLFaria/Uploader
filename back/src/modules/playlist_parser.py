import os
from json import dumps

from src.schemas import Playlist, Video


class PlaylistParser:
    def __init__(self, directory_path: str) -> None:
        self._directory_path = directory_path

    def execute(self) -> None:
        playlists = self._initialize_playlists(self._directory_path)
        playlists = self._initialize_playlists_videos(playlists)

    def _initialize_playlists(self, root_path: str) -> list[Playlist]:
        playlists = [Playlist(name="blank", path=root_path)]
        for file in os.listdir(root_path):
            if self._is_a_folder(f"{root_path}/{file}"):
                playlists.append(Playlist(name=file, path=f"{root_path}/{file}"))
        return playlists

    def _initialize_playlists_videos(self, playlists: list[Playlist]) -> list[Playlist]:
        for playlist in playlists:
            playlist_new_videos = self._get_playlist_videos(playlist)
            playlist.videos.extend(playlist_new_videos)
        return playlists

    # TODO: Verificar os vídeos dentro de pastas dentro da playlist futuramente
    # NOTE: Não realizar essa operação de verificar vídeos internos para a pasta raíz
    def _get_playlist_videos(self, playlist: Playlist) -> list[Video]:
        videos: list[Video] = []
        for file in os.listdir(playlist.path):
            if self._is_a_video(file):
                videos.append(
                    Video(name=file.split(".")[0], path=f"{playlist.path}/{file}")
                )
        return videos

    def _is_a_folder(self, path: str) -> bool:
        try:
            if path.split("/")[-1][0] == ".":
                return False
            os.listdir(path)
            return True
        except Exception as _:
            return False

    def _is_a_video(self, path: str) -> bool:
        supported_video_extensions = ["mp4", "mkv", "mov"]
        file_extension = path.split(".")
        try:
            if file_extension[1] in supported_video_extensions:
                return True
            return False
        except Exception as _:
            return False

    # TODO: Fazer o caminho do arquivo de playlists ser parte das variáveis de ambiente
    def save_playlists(self, playlists: list[Playlist]) -> None:
        with open("playlist.json", "w", encoding="utf-8") as file:
            content = {"playlists": [playlist.model_dump() for playlist in playlists]}
            file.write(dumps(content))
