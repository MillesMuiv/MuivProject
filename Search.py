import argparse
from googleapiclient.discovery import build

DEVELOPER_KEY = 'AIzaSyBXi167dQKUwlOOvzLWnrHVxI7-M4LGCFc'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
max_results = 25


def youtube_search(options):

    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                         search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                          search_result['id']['playlistId']))

    return videos, channels, playlists


parser = argparse.ArgumentParser()
parser.add_argument('--max-results', help='Max results', default=max_results)
args = parser.parse_args()


if __name__ == '__main__':
    youtube_search(args)
