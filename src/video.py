import os
import json

from googleapiclient.discovery import build
from src.apimixin import APIMixin


class Video(APIMixin):
    """Класс Youtube-видео"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        youtube = self.get_service()
        # youtube = build('youtube', 'v3', developerKey=Video.api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        print(json.dumps(video_response, indent=2, ensure_ascii=False))
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


    def __str__(self):
        """Возвращает название видео"""
        return f'{self.title}'

class PLVideo(Video, APIMixin):
    """Класс Youtube-видео и плейлиста"""

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        """Возвращает название плейлиста"""
        return f'{self.title}'
