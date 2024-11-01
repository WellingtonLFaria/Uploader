import http.client as httplib
import httplib2
import os
import sys
import time

import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

PLAYLIST_PATH_FILE = "playlist.json" 
CLIENT_SECRETS_FILE = "client_secrets.json"

httplib2.RETRIES = 1
MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
  httplib.IncompleteRead, httplib.ImproperConnectionState,
  httplib.CannotSendRequest, httplib.CannotSendHeader,
  httplib.ResponseNotReady, httplib.BadStatusLine)
  
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]


YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl", 
          "https://www.googleapis.com/auth/youtubepartner"]
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
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_SCOPES,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("oauth2.json")
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def create_playlist(youtube, title, description, privacy_status):
    body = {
        'snippet': {
            'title': title,
            'description': description
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=body
    ).execute()

    return playlists_insert_response['id']

def add_video_to_playlist(youtube, video_id, playlist_id):
    body = {
        'snippet': {
            'playlistId': playlist_id,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': video_id
            }
        }
    }

    youtube.playlistItems().insert(
        part='snippet',
        body=body
    ).execute()

def initialize_upload(youtube, video, playlist_id):
    body = {
        'snippet': {
            'title': video["name"],
            'description': f"Video: {video['name']}",
            'tags': None,
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video["path"], chunksize=-1, resumable=True)
    )

    response = resumable_upload(insert_request)
    print(response)
    if playlist_id != None:
        add_video_to_playlist(youtube, response['id'], playlist_id)

def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print ("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except(HttpError, e):
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except (RETRIABLE_EXCEPTIONS, e):
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)
  return response

def main():
    with open("playlist.json", "r") as file:
        playlist = json.loads(file.read())
        youtube = get_authenticated_service()
        for item in playlist["playlists"]:
            playlist = item["name"]
            playlist_id = None
            if playlist != "blank":
                playlist_id = create_playlist(youtube, playlist, f"Playlist: {playlist}", "public")
            for video in item["videos"]:
                initialize_upload(youtube, video, playlist_id)
    print("All videos uploaded")

def test():
    with open("playlist.json", "r") as file:
        playlist = json.loads(file.read())
        
        for item in playlist["playlists"]:
            playlist = item["name"]
            print(playlist)
            if playlist != "blank":
                print("blank")
            for video in item["videos"]:
                print(video["name"], video["path"])
    print("All videos uploaded")


if __name__ == '__main__':
   main()