import argparse
from googleapiclient.discovery import build
import urllib.request
from PIL import Image

video_thumbnail = r'thumbnails\video_thumbnail'
channel_thumbnail = r'thumbnails\channel_thumbnail'
DEVELOPER_KEY = 'AIzaSyBXi167dQKUwlOOvzLWnrHVxI7-M4LGCFc'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
max_results = 25


def thumbnail(url):
    if url[:5] == 'https':
        urllib.request.urlretrieve(url, channel_thumbnail)
        chanim = Image.open(channel_thumbnail)
        chanim.save(f'{channel_thumbnail}.jpg')
        print(url)
        return chanim
    else:
        image_url = f'https://i.ytimg.com/vi/{url}/hqdefault.jpg'
        urllib.request.urlretrieve(image_url, video_thumbnail)
        im = Image.open(video_thumbnail)
        im.save(f'{video_thumbnail}.jpg')
        return im


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
