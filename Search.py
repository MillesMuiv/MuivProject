import argparse
from googleapiclient.discovery import build
import urllib.request
from PIL import Image

thumbnails_file = r'C:\Users\slava\Desktop\DataProject\thumbnails\thumbnail'
DEVELOPER_KEY = 'AIzaSyBXi167dQKUwlOOvzLWnrHVxI7-M4LGCFc'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
max_results = 25


class WebImage:
    def __init__(self, url):
        self.image_url = f'https://i.ytimg.com/vi/{url}/hqdefault.jpg'
        urllib.request.urlretrieve(self.image_url, thumbnails_file)
        self.im = Image.open(thumbnails_file)
        self.im.save(f'{thumbnails_file}.jpg')

    def get(self):
        return self.im

    def close(self):
        self.im.close()


def youtube_search(options, entry):
    search_response = youtube.search().list(
        q=entry,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []
    video_count = 0
    channel_count = 0
    playlist_count = 0
    ids = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s' % search_result['snippet']['title'])
            video_count += 1
            ids.append(search_result['id']['videoId'])
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s' % search_result['snippet']['title'])
            channel_count += 1
            ids.append(search_result['id']['channelId'])
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s' % search_result['snippet']['title'])
            playlist_count += 1
            ids.append(search_result['id']['playlistId'])

    result = videos + channels + playlists

    return result, ids


parser = argparse.ArgumentParser()
# parser.add_argument('--q', help='Search term', default=input())
parser.add_argument('--max-results', help='Max results', default=max_results)
args = parser.parse_args()

if __name__ == '__main__':
    youtube_search(args)
