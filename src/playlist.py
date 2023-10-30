import datetime
import isodate

from src.apimixin import APIMixin


class PlayList(APIMixin):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist = self.get_service().playlists().list(id=playlist_id, part='contentDetails,snippet', maxResults=50, ).execute()
        self.title = playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __str__(self):
        """Возвращает название плейлиста"""
        return f'{self.title}'

    @property
    def total_duration(self):
        """Возвращает общую длительность плейлиста"""
        video_response = self.get_playlists_videos()
        duration = datetime.timedelta()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """Выводит ссылку на видео с самым большим количеством лайков"""
        video_response = self.get_playlists_videos()

        max_like_count = 0
        video_id = ''
        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > max_like_count:
                max_like_count = like_count
                video_id = video['id']
        return f"https://youtu.be/{video_id}"

    def get_playlists_videos(self):
        """Возвращает ответ API на запрос всех видео плейлиста"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id, part='contentDetails',
                                                             maxResults=50, ).execute()
        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                       id=','.join(video_ids)
                                                       ).execute()
        return video_response
