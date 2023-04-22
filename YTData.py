from googleapiclient.discovery import build

api_key = 'AIzaSyBXi167dQKUwlOOvzLWnrHVxI7-M4LGCFc'
channel_ids = ['UCtu2BCnJoFGRBOuIh570QWw',
               'UCNdFtR-glRU4MbKGtgEqpeQ',
               'UCcDxHSv_piDmlXptZ_HZNJw',
               'UCDK9qD5DAQML-pzrtA7A4oA']

youtube = build('youtube', 'v3', developerKey=api_key)


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers=response['items'][i]['statistics']['subscriberCount'],
                    Views=response['items'][i]['statistics']['viewCount'],
                    Total_videos=response['items'][i]['statistics']['videoCount'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data


def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()

    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')
    return video_ids


def get_videos_details(youtube, video_ids):
    all_video_details = []
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i + 50]))
        response = request.execute()

        for video in response['items']:
            video_stats = dict(Title=video['snippet']['title'],
                               Published_date=video['snippet']['publishedAt'],
                               Views=video['statistics']['viewCount'],
                               Likes=video['statistics']['likeCount'],
                               Comments=video['statistics']['commentCount'],
                               )

            all_video_stats.append(video_stats)

        for video in response['items']:
            video_details = dict(Channel_Title=video['snippet']['channelTitle'],
                                 Description=video['snippet']['description']
                                 )

            all_video_details.append(video_details)

    return all_video_stats, all_video_details


def get_video_details(youtube, video_id):
    all_video_details = []
    all_video_stats = []

    request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id)
    response = request.execute()

    for video in response['items']:
        video_stats = dict(Title=video['snippet']['title'],
                           Published_date=video['snippet']['publishedAt'],
                           Views=video['statistics']['viewCount'],
                           Likes=video['statistics']['likeCount'],
                           Comments=video['statistics']['commentCount'],
                           )
        all_video_stats.append(video_stats)

    for video in response['items']:
        video_details = dict(Channel_Title=video['snippet']['channelTitle'],
                             Description=video['snippet']['description']
                             )
        all_video_details.append(video_details)

    return all_video_stats, all_video_details

# TODO: turn these into functions that build graphs from a button press
# channel_statistics = get_channel_stats(youtube, channel_ids)
# channel_data = pd.DataFrame(channel_statistics)
# channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
# channel_data['Views'] = pd.to_numeric(channel_data['Views'])
# channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])
#
# playlist_id = channel_data.loc[channel_data['Channel_name'] == 'OfflineTV', 'playlist_id'].iloc[0]
# video_ids = get_video_ids(youtube, playlist_id)
#
# video_details = get_video_details(youtube, video_ids)
# video_data = pd.DataFrame(video_details)

