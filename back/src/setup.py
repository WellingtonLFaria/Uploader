import http.client as httplib
import httplib2
import os
import subprocess

# NOTE: Aparentemente as bibliotecas implementadas atualmente estão obsoletas
# TODO: Verificar se existem bibliotecas mais recentes para o OAuth2 do Google
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

# TODO: Transformar constantes em variáveis de ambiente
PLAYLIST_PATH_FILE = "playlist.json"
CLIENT_SECRETS_FILE = "client_secrets.json"

httplib2.RETRIES = 1
MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error,
    IOError,
    httplib.NotConnected,
    httplib.IncompleteRead,
    httplib.ImproperConnectionState,
    httplib.CannotSendRequest,
    httplib.CannotSendHeader,
    httplib.ResponseNotReady,
    httplib.BadStatusLine,
)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtubepartner",
]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service():
    try:
        flow = flow_from_clientsecrets(
            CLIENT_SECRETS_FILE,
            scope=YOUTUBE_SCOPES,
            message=MISSING_CLIENT_SECRETS_MESSAGE,
        )
        storage = Storage("oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()),
        )
    except Exception as e:
        raise e


def run():
    get_authenticated_service()
    command = "flask run --debug"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    print(result.stdout)


if __name__ == "__main__":
    run()
