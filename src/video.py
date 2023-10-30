import os
import json

from src.apimixin import APIMixin


class Video(APIMixin):
    """Класс Youtube-видео"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, video_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        # print(json.dumps(video_response, indent=2, ensure_ascii=False))
        try:
            self.title = video_response['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={video_id}'
            self.view_count = video_response['items'][0]['statistics']['viewCount']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None


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
