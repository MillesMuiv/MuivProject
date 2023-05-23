from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
import sys


CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v2"


def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=SCOPES)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def execute_api_request(youtube):
    request = youtube.reports().query(
                          ids='channel==MINE',
                          startDate='2017-01-01',
                          endDate='2017-12-31',
                          metrics='estimatedMinutesWatched,views,likes,subscribersGained',
                          dimensions='day',
                          sort='day')
    response = request.execute()
    return response


if __name__ == "__main__":
    youtube = get_authenticated_service()
    print(execute_api_request(youtube))
