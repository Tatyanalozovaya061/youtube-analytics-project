import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('API_KEY')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        youtube = build('youtube', 'v3', developerKey=PlayList.api_key)
        playlist = youtube.playlists().list(id=playlist_id, part='contentDetails,snippet', maxResults=50, ).execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

        videolist = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                 maxResults=50, ).execute()
        videos_id = []

        for video in videolist['items']:
            videos_id.append(video['contentDetails']['videoId'])
        self.__total_duration = datetime.timedelta()

        max_like_count = 0

        for video_id in videos_id:
            video_response = youtube.videos().list(id=video_id, part='snippet,statistics,contentDetails,topicDetails',
                                                   maxResults=50, ).execute()
            duration = video_response['items'][0]['contentDetails']['duration']
            self.__total_duration += isodate.parse_duration(duration)
            like_count = int(video_response['items'][0]['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                self.__best_video_url = f"https://youtu.be/{video_id}"

    @property
    def total_duration(self):
        return self.__total_duration

    def show_best_video(self):
        return self.__best_video_url
