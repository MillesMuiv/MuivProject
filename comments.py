from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyBXi167dQKUwlOOvzLWnrHVxI7-M4LGCFc'
channel_ids = ['UCtu2BCnJoFGRBOuIh570QWw',
               'UCNdFtR-glRU4MbKGtgEqpeQ',
               'UCcDxHSv_piDmlXptZ_HZNJw',
               'UCDK9qD5DAQML-pzrtA7A4oA']
video_ids = ['pDfNPoEXEJo',
             'qGV5dK6oP5Q',
             'dpb3ZcMnhZc',
             '3AfSY22NTwI',
             'Av95OByV-rM',
             'VEPz_eT0cLk']

youtube = build('youtube', 'v3', developerKey=api_key)


def get_video_comments(youtube, video_ids):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId="eQji1bEXwc0")
    response = request.execute()
    for i in range(len(response['items'])):
        comments.append(response['items'][i]['snippet']['topLevelComment']
                                            ['snippet']['textDisplay'])
    return comments

