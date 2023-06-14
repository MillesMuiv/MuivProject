from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
import sys


CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
OAUTH_API_SERVICE_NAME = "youtubeAnalytics"
OAUTH_API_VERSION = "v2"
LOGGED_IN = 0
DEVELOPER_KEY = "AIzaSyBXi167dQKUwlOOvzLWnrHVxI7-M4LGCFc"
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
    LOGGED_IN = 1
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials), LOGGED_IN





if __name__ == "__main__":
    youtube_oauth = get_authenticated_service()
