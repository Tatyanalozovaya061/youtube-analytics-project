import datetime
import isodate

from src.apimixin import APIMixin


class PlayList(APIMixin):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        youtube = self.get_service()
        playlist = youtube.playlists().list(id=playlist_id, part='contentDetails,snippet', maxResults=50, ).execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    def __str__(self):
        """Возвращает название плейлиста"""
        return f'{self.title}'

    @property
    def total_duration(self):
        youtube = self.get_service()
        videolist = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                 maxResults=50, ).execute()

        videos_id = []
        for video in videolist['items']:
            videos_id.append(video['contentDetails']['videoId'])
        total_duration = datetime.timedelta()

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(videos_id)
                                               ).execute()

        duration = video_response['items'][0]['contentDetails']['duration']
        total_duration += isodate.parse_duration(duration)
        return total_duration

    def show_best_video(self):
        youtube = self.get_service()
        videolist = youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                 maxResults=50, ).execute()

        max_like_count = 0
        for video_id in videolist['items']:
            like_count = int(videolist['items'][0]['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                best_video_url = f"https://youtu.be/{video_id}"
            return best_video_url
