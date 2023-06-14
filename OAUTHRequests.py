from OAuth import *
import Search


def like_button_event(youtube, video_id):
    request = youtube.videos().rate(
        id=f"{video_id}",
        rating="like"
    )
    request.execute()


def dislike_button_event(youtube, video_id):
    request = youtube.videos().rate(
        id=f"{video_id}",
        rating="dislike"
    )
    request.execute()


def subscribe_button_event(youtube, channel_id):
    request = youtube.subscriptions().insert(
        part="snippet",
        body={
          "snippet": {
            "resourceId": {
              "kind": "youtube#channel",
              "channelId": f"{channel_id}"
            }
          }
        }
    )
    request.execute()

#def execute_api_request(youtube):
    #request = youtube.reports().query(
   #                       ids='channel==MINE',
   #                      startDate='2017-01-01',
    #                      endDate='2017-12-31',
   #                       metrics='estimatedMinutesWatched,views,likes,subscribersGained',
   #                       dimensions='day',
   #                       sort='day')
   # response = request.execute()
  #  return response
